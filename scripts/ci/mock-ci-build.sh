#!/usr/bin/env bash
#
# mock-ci-build.sh <package> <distro> <pg-version> <result-dir>
#
# Build the SRPM of a PGDG package from its OS directory (as the builders
# do, so a missing patch symlink there fails here too) and mock-build it
# with the pgdg-<distro>-pg<NN>-x86_64 config.
#
# Runs as root in a privileged Fedora container on GitHub Actions; see
# .github/workflows/mock-build.yml. Needs mock, rpmdevtools,
# pgdg-mock-configs and pgdg-srpm-macros installed.
#
# Per https://github.com/pgdg-packaging/pgdg-rpms/issues/442

set -euo pipefail

if [ $# -ne 4 ]; then
    echo "Usage: $0 <package> <distro> <pg-version> <result-dir>" >&2
    exit 1
fi

PKG="$1"
DISTRO="$2"
PGVER="$3"
RESULT_DIR="$(realpath -m "$4")"

REPO_ROOT="$(git rev-parse --show-toplevel)"
MAIN_ROOT="$REPO_ROOT/rpm/redhat/main"

declare -A DISTRO_MARKER=(
    [fedora-43]="F-43"
    [fedora-44]="F-44"
    [fedora-45]="F-45"
    [rocky-8]="EL-8"
    [rocky-9]="EL-9"
    [rocky-10]="EL-10"
    [opensuse-leap-16]="SLES-16"
    [amazonlinux-2023]="AL-2023"
)

PKG_ROOT=""
for kind in common non-common non-free extras; do
    if [ -d "$MAIN_ROOT/$kind/$PKG/main" ]; then
        PKG_ROOT="$MAIN_ROOT/$kind/$PKG"
        break
    fi
done
if [ -z "$PKG_ROOT" ]; then
    echo "Could not find '$PKG/main' under rpm/redhat/main." >&2
    exit 1
fi

OS_DIR="$PKG_ROOT/${DISTRO_MARKER[$DISTRO]}"
SPECFILE="$(sed -n 's/^SPECFILE="\(.*\)"/\1/p' "$OS_DIR/Makefile")"

mkdir -p "$RESULT_DIR/srpm"
cd "$OS_DIR"

# What "make srpmNN" / "make commonsrpm" do, minus the git pull in prep.
spectool -g -S --define "_sourcedir $PWD" "$SPECFILE"
rpmbuild --define "_sourcedir $PWD" --define "_specdir $PWD" \
    --define "_builddir $PWD" --define "_srcrpmdir $RESULT_DIR/srpm" \
    --define "_buildrootdir $RESULT_DIR/BUILDROOT" \
    --define "pgmajorversion $PGVER" --define "pginstdir /usr/pgsql-$PGVER" \
    --define "pgpackageversion $PGVER" \
    --nodeps -bs "$SPECFILE"

MOCK_ARGS=(-r "pgdg-${DISTRO}-pg${PGVER}-x86_64" --resultdir "$RESULT_DIR"
           --isolation=simple)

# Fedora 45 packages are only in the testing repos for now.
if [ "$DISTRO" = "fedora-45" ]; then
    MOCK_ARGS+=(--enablerepo=pgdg-common-testing
                --enablerepo="pgdg${PGVER}-updates-testing")
fi

SRPM="$(ls "$RESULT_DIR"/srpm/*.src.rpm)"
if mock "${MOCK_ARGS[@]}" --rebuild "$SRPM"; then
    exit 0
fi

# Specs that run %{__ospython} at parse time fail before mock installs the
# BuildRequires, as the interpreter is not in the chroot yet. Install it
# first, then rebuild in that chroot.
OSPYTHON="$(sed -n 's|^sh: line [0-9]*: \(/usr/bin/python3[.0-9]*\): No such file or directory$|\1|p' \
    "$RESULT_DIR/build.log" | head -1)"
if [ -z "$OSPYTHON" ]; then
    exit 1
fi
echo "=== $OSPYTHON is needed at spec parse time; retrying with it installed ==="
mock "${MOCK_ARGS[@]}" --init
mock "${MOCK_ARGS[@]}" --install "$OSPYTHON"
mock "${MOCK_ARGS[@]}" --no-clean --rebuild "$SRPM"
