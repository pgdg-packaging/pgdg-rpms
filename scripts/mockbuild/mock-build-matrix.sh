#!/usr/bin/env bash
#
# mock-build-matrix.sh [-p "18 16"] [-d "fedora-43 rocky-9"] <package-name>
#
# Build the SRPM for a PGDG package and mock-build it across the full
# distro matrix (Fedora 43/44, Rocky 9/10, openSUSE Leap 16), to catch
# distro/GCC-specific build failures locally instead of on the buildfarm.
#
# Mock builds within a matrix run in parallel (each distro uses its own
# mock config/chroot under /var/lib/mock/<config>/, so they don't collide).
# Set MOCK_PARALLEL_JOBS to cap how many run concurrently (default: all).
#
# -u/--unique-ext lets a caller (e.g. mock-build-all.sh, running several
# packages against the SAME distro/PG version concurrently) keep those runs
# from colliding on the identical /var/lib/mock/<config>/ chroot -- it's
# passed straight through to mock's own --uniqueext.
#
# PostgreSQL major versions to test against come from PG_VERSIONS below
# (override with -p/--pg-versions), e.g. add 19 once it's out:
#   ./mock-build-matrix.sh -p "18 16 19" orafce
#
# global.sh (assumed to sit alongside this script once deployed) is
# consulted only to tell whether a requested version is currently the
# beta/alpha (pgBetaVersion/pgAlphaVersion) -- if so "make srpmNNtesting"
# is used instead of "make srpmNN". We deliberately don't source the whole
# file (it gates on running as the postgres user and requires
# ~/bin/global-local.sh, which are buildserver-only prerequisites this
# script doesn't need) -- only its PostgreSQL-version array declarations
# are pulled in.
#
# Run from anywhere inside a pgrpms checkout.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GLOBAL_SH="$SCRIPT_DIR/global.sh"

pgBetaVersion=""
pgAlphaVersion=""
if [ -f "$GLOBAL_SH" ]; then
    eval "$(grep -E '^declare -a pg(StableBuilds|TestBuilds|BetaVersion|AlphaVersion)=' "$GLOBAL_SH")"
fi

# Default PG major versions to test against; override with -p/--pg-versions.
PG_VERSIONS=(18 16)
DISTROS=(fedora-43 fedora-44 rocky-9 rocky-10 opensuse-leap-16)
UNIQUE_EXT=""

usage() {
    cat <<EOF >&2
Usage: $0 [-p "18 16"] [-d "fedora-43 rocky-9"] [-u ext] <package-name>

  -p, --pg-versions "18 16"   PostgreSQL major versions to build/test (space-separated).
                              Default: ${PG_VERSIONS[*]}
  -d, --distros "rocky-9"     Override the distro matrix (space-separated distro tokens).
                              Default: ${DISTROS[*]}
  -u, --unique-ext ext        Passed through to mock's --uniqueext, so a caller running
                              several packages concurrently against the same distro/PG
                              version doesn't collide on the same chroot.
EOF
    exit 1
}

while [ $# -gt 0 ]; do
    case "$1" in
        -p|--pg-versions)
            read -r -a PG_VERSIONS <<< "$2"
            shift 2
            ;;
        -d|--distros)
            read -r -a DISTROS <<< "$2"
            shift 2
            ;;
        -u|--unique-ext)
            UNIQUE_EXT="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        --)
            shift
            break
            ;;
        -*)
            echo "Unknown option: $1" >&2
            usage
            ;;
        *)
            break
            ;;
    esac
done

PKG="${1:-}"
if [ -z "$PKG" ]; then
    usage
fi

# Find the pgrpms checkout: use the current directory if it's inside one,
# otherwise fall back to ~/git/pgrpms, the checkout path every buildserver
# script in this repo assumes (see packagebuild.sh) -- needed because this
# script is typically deployed to ~/bin and invoked from elsewhere.
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [ -z "$REPO_ROOT" ] && [ -d "$HOME/git/pgrpms/.git" ]; then
    REPO_ROOT="$HOME/git/pgrpms"
fi
if [ -z "$REPO_ROOT" ]; then
    echo "Not inside a git repository, and no checkout found at ~/git/pgrpms." >&2
    exit 1
fi

MAIN_ROOT="$REPO_ROOT/rpm/redhat/main"
if [ ! -d "$MAIN_ROOT" ]; then
    echo "Could not find rpm/redhat/main under $REPO_ROOT" >&2
    exit 1
fi

PKG_DIR=""
PKG_KIND=""
for kind in common non-common non-free extras; do
    if [ -d "$MAIN_ROOT/$kind/$PKG/main" ]; then
        PKG_DIR="$MAIN_ROOT/$kind/$PKG/main"
        PKG_KIND="$kind"
        break
    fi
done

if [ -z "$PKG_DIR" ]; then
    echo "Could not find '$PKG/main' under common/, non-common/, non-free/, or extras/." >&2
    exit 1
fi

echo "Package: $PKG ($PKG_KIND)"
echo "Directory: $PKG_DIR"
cd "$PKG_DIR"

MAX_PARALLEL="${MOCK_PARALLEL_JOBS:-${#DISTROS[@]}}"

# make target for a given PG major version: srpmNNtesting when NN is the
# current beta/alpha version per global.sh, srpmNN otherwise.
srpm_target() {
    local pgver="$1"
    if [ -n "$pgBetaVersion" ] && [ "$pgver" = "$pgBetaVersion" ]; then
        echo "srpm${pgver}testing"
    elif [ -n "$pgAlphaVersion" ] && [ "$pgver" = "$pgAlphaVersion" ]; then
        echo "srpm${pgver}testing"
    else
        echo "srpm${pgver}"
    fi
}

declare -A RESULTS
BUILT_VERSIONS=()

# Only remove a leftover *.src.rpm; never touch anything else in the dir.
clean_srpm() {
    rm -f ./*.src.rpm
}

run_matrix() {
    local pgver="$1"
    local srpm
    srpm="$(ls -t ./*.src.rpm 2>/dev/null | head -1)"
    if [ -z "$srpm" ]; then
        echo "No SRPM found for PG$pgver build." >&2
        return 1
    fi

    local tmpdir
    tmpdir="$(mktemp -d)"

    local running=0
    for distro in "${DISTROS[@]}"; do
        local cfg="pgdg-${distro}-pg${pgver}-x86_64"
        local mock_args=(-r "$cfg")
        [ -n "$UNIQUE_EXT" ] && mock_args+=(--uniqueext="$UNIQUE_EXT")
        echo "=== launching mock ${mock_args[*]} $srpm (parallel) ==="
        (
            if sudo mock "${mock_args[@]}" "$srpm" > "$tmpdir/$distro.log" 2>&1; then
                echo PASS > "$tmpdir/$distro.result"
            else
                echo FAIL > "$tmpdir/$distro.result"
            fi
        ) &

        running=$((running + 1))
        if [ "$running" -ge "$MAX_PARALLEL" ]; then
            wait -n
            running=$((running - 1))
        fi
    done

    wait

    for distro in "${DISTROS[@]}"; do
        RESULTS["${pgver}:${distro}"]="$(cat "$tmpdir/$distro.result" 2>/dev/null || echo n/a)"
    done

    rm -rf "$tmpdir"
}

if [ "$PKG_KIND" = "common" ]; then
    # Common packages aren't PG-version-specific -- build once and just need
    # *a* valid chroot, so use the first configured PG version for that.
    clean_srpm
    make commonsrpm
    common_pgver="${PG_VERSIONS[0]}"
    run_matrix "$common_pgver"
    BUILT_VERSIONS=("$common_pgver")
else
    for pgver in "${PG_VERSIONS[@]}"; do
        target="$(srpm_target "$pgver")"
        clean_srpm
        if make "$target"; then
            run_matrix "$pgver"
            BUILT_VERSIONS+=("$pgver")
        else
            echo "PG$pgver ($target) build not supported/failed for $PKG — skipping mock matrix for this version."
        fi
    done
fi

echo
echo "=== Results ==="
{
    printf "%-20s" "Distro"
    for pgver in "${BUILT_VERSIONS[@]}"; do
        printf " PG%-6s" "$pgver"
    done
    printf "\n"

    for distro in "${DISTROS[@]}"; do
        printf "%-20s" "$distro"
        for pgver in "${BUILT_VERSIONS[@]}"; do
            printf " %-8s" "${RESULTS[${pgver}:${distro}]:-n/a}"
        done
        printf "\n"
    done
}

echo
echo "On FAIL, check /var/lib/mock/<config>/result/{root,build}.log for the actual error."
