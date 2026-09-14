#!/usr/bin/env bash
#
# mock-build-matrix.sh <package-name>
#
# Build the SRPM for a PGDG package and mock-build it across the full
# distro matrix (Fedora 43/44, Rocky 9/10, openSUSE Leap 16), to catch
# distro/GCC-specific build failures locally instead of on the buildfarm.
#
# Mock builds within a matrix run in parallel (each distro uses its own
# mock config/chroot under /var/lib/mock/<config>/, so they don't collide).
# Set MOCK_PARALLEL_JOBS to cap how many run concurrently (default: all).
#
# Run from anywhere inside a pgrpms checkout.

set -euo pipefail

PKG="${1:-}"
if [ -z "$PKG" ]; then
    echo "Usage: $0 <package-name>" >&2
    exit 1
fi

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [ -z "$REPO_ROOT" ]; then
    echo "Not inside a git repository." >&2
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

DISTROS=(fedora-43 fedora-44 rocky-9 rocky-10 opensuse-leap-16)
MAX_PARALLEL="${MOCK_PARALLEL_JOBS:-${#DISTROS[@]}}"

declare -A RESULTS_PG18
declare -A RESULTS_PG16
HAS_PG16=0

# Only remove a leftover *.src.rpm; never touch anything else in the dir.
clean_srpm() {
    rm -f ./*.src.rpm
}

run_matrix() {
    local pgver="$1"
    local -n results_ref="$2"
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
        echo "=== launching mock -r $cfg $srpm (parallel) ==="
        (
            if sudo mock -r "$cfg" "$srpm" > "$tmpdir/$distro.log" 2>&1; then
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
        results_ref["$distro"]="$(cat "$tmpdir/$distro.result" 2>/dev/null || echo n/a)"
    done

    rm -rf "$tmpdir"
}

if [ "$PKG_KIND" = "common" ]; then
    clean_srpm
    make commonsrpm
    run_matrix 18 RESULTS_PG18
else
    clean_srpm
    make srpm18
    run_matrix 18 RESULTS_PG18

    clean_srpm
    if make srpm16; then
        HAS_PG16=1
        run_matrix 16 RESULTS_PG16
    else
        echo "PG16 build not supported for $PKG — skipping PG16 leg."
    fi
fi

echo
echo "=== Results ==="
if [ "$PKG_KIND" = "common" ]; then
    printf "%-20s %s\n" "Distro" "PG18"
    for distro in "${DISTROS[@]}"; do
        printf "%-20s %s\n" "$distro" "${RESULTS_PG18[$distro]:-n/a}"
    done
else
    printf "%-20s %-6s %s\n" "Distro" "PG18" "PG16"
    for distro in "${DISTROS[@]}"; do
        pg16_result="n/a"
        if [ "$HAS_PG16" -eq 1 ]; then
            pg16_result="${RESULTS_PG16[$distro]:-n/a}"
        fi
        printf "%-20s %-6s %s\n" "$distro" "${RESULTS_PG18[$distro]:-n/a}" "$pg16_result"
    done
fi

echo
echo "On FAIL, check /var/lib/mock/<config>/result/{root,build}.log for the actual error."
