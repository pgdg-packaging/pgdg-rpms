#!/usr/bin/env bash
#
# mock-ci-build.sh <package> <distro> <pg-version> <result-dir>
# mock-ci-build.sh --init <distro>
#
# Build the SRPM of a PGDG package from its OS directory (as the builders
# do, so a missing patch symlink there fails here too) and mock-build it
# with the pgdg-<distro>-pg<NN>-x86_64 config, with runselftest enabled so
# that %check runs. The SRPM is built in the target chroot, so that the
# spec's distro conditionals pick the sources and patches the builders use.
#
# Runs as root in a privileged Fedora container on GitHub Actions; see
# .github/workflows/mock-build.yml. Needs mock and pgdg-mock-configs
# installed.
#
# With --init, only set up the distro's chroot, so that mock saves its root
# cache; see .github/workflows/ci-branch-cleanup.yml.
#
# Per https://github.com/pgdg-packaging/pgdg-rpms/issues/442

set -euo pipefail

INIT_ONLY=""
if [ $# -eq 2 ] && [ "$1" = "--init" ]; then
    # The pgdg-<distro>-pg<NN> configs all share one chroot.
    INIT_ONLY=1
    DISTRO="$2"
    PGVER=18
    RESULT_DIR="$(mktemp -d)"
elif [ $# -eq 4 ]; then
    PKG="$1"
    DISTRO="$2"
    PGVER="$3"
    RESULT_DIR="$(realpath -m "$4")"
else
    echo "Usage: $0 <package> <distro> <pg-version> <result-dir>" >&2
    echo "       $0 --init <distro>" >&2
    exit 1
fi

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

if [ -z "$INIT_ONLY" ]; then
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

    OS_NAME="${DISTRO_MARKER[$DISTRO]}"
    SPECFILE="$(sed -n 's/^SPECFILE="\(.*\)"/\1/p' "$PKG_ROOT/$OS_NAME/Makefile")"
fi

mkdir -p "$RESULT_DIR"

MOCK_ARGS=(-r "pgdg-${DISTRO}-pg${PGVER}-x86_64" --resultdir "$RESULT_DIR"
           --isolation=simple --define "runselftest 1")

# Mock builds as the user who runs it, and the test suites refuse to run
# as root, so run mock as an unprivileged member of the mock group.
if ! id mockci >/dev/null 2>&1; then
    useradd -m -G mock mockci
fi
chown -R mockci: "$RESULT_DIR"
MOCK=(runuser -u mockci -- mock)

# A slow mirror can stretch a 5 minute build to an hour. Make dnf give up
# on a mirror that sends less than 256 KiB/s for 30 seconds and move on to
# the next one. Mock discards a root cache that is older than its config
# files, so keep the file's packaged mtime.
if ! grep -q 'minrate' /etc/mock/site-defaults.cfg; then
    MTIME="$(stat -c %Y /etc/mock/site-defaults.cfg)"
    cat >> /etc/mock/site-defaults.cfg <<'EOF'
config_opts['dnf4_common_opts'] += ['--setopt=minrate=262144', '--setopt=timeout=30']
config_opts['dnf5_common_opts'] += ['--setopt=minrate=262144', '--setopt=timeout=30']
EOF
    touch -d "@$MTIME" /etc/mock/site-defaults.cfg
fi

# Fedora 45 packages are only in the testing repos for now.
if [ "$DISTRO" = "fedora-45" ]; then
    MOCK_ARGS+=(--enablerepo=pgdg-common-testing
                --enablerepo="pgdg${PGVER}-updates-testing")
fi

# EPEL 10 is split per minor release, and the template's [epel] follows the
# newest one, which can carry newer packages than the builders see. Use the
# EPEL minor the EL 10 builders are on instead.
EL10_EPEL_MINOR="${EL10_EPEL_MINOR:-10.2}"
if [ "$DISTRO" = "rocky-10" ]; then
    MOCK_ARGS+=(--disablerepo=epel
                --addrepo="https://dl.fedoraproject.org/pub/epel/${EL10_EPEL_MINOR}/Everything/x86_64/")
fi

if [ -n "$INIT_ONLY" ]; then
    "${MOCK[@]}" "${MOCK_ARGS[@]}" --init
    exit 0
fi

# What "make srpmNN" / "make commonsrpm" do, minus the git pull in prep,
# in the target chroot. The rebuild below starts from a clean chroot again.
CHROOT_SRC=/builddir/pgdg-src
DEFINES="--define \"pgmajorversion $PGVER\" --define \"pginstdir /usr/pgsql-$PGVER\""
DEFINES+=" --define \"pgpackageversion $PGVER\" --define \"runselftest 1\""
SRPM_CMD="cd $CHROOT_SRC/$OS_NAME &&
    spectool -g -S --define \"_sourcedir \$PWD\" $DEFINES $SPECFILE &&
    rpmbuild --define \"_sourcedir \$PWD\" --define \"_specdir \$PWD\" \\
        --define \"_builddir \$PWD\" --define \"_srcrpmdir /builddir/pgdg-srpm\" \\
        $DEFINES --nodeps -bs $SPECFILE"

"${MOCK[@]}" "${MOCK_ARGS[@]}" --init
"${MOCK[@]}" "${MOCK_ARGS[@]}" --install rpmdevtools
# SUSE's rpmdevtools names it rpmdev-spectool; the SLES builders have the
# same symlink.
"${MOCK[@]}" "${MOCK_ARGS[@]}" --chroot \
    "command -v spectool || ln -s rpmdev-spectool /usr/bin/spectool"
"${MOCK[@]}" "${MOCK_ARGS[@]}" --copyin "$PKG_ROOT" "$CHROOT_SRC"
if ! "${MOCK[@]}" "${MOCK_ARGS[@]}" --enable-network --chroot "$SRPM_CMD" 2>&1 \
        | tee "$RESULT_DIR/srpm.log"; then
    # Same %{__ospython} parse time problem as for the rebuild, see below.
    OSPYTHON="$(sed -n 's|^sh: \(line [0-9]*: \)\?\(/usr/bin/python3[.0-9]*\): No such file or directory$|\2|p' \
        "$RESULT_DIR/srpm.log" | head -1)"
    if [ -z "$OSPYTHON" ]; then
        exit 1
    fi
    "${MOCK[@]}" "${MOCK_ARGS[@]}" --install "$OSPYTHON"
    "${MOCK[@]}" "${MOCK_ARGS[@]}" --enable-network --chroot "$SRPM_CMD"
fi
"${MOCK[@]}" "${MOCK_ARGS[@]}" --copyout /builddir/pgdg-srpm "$RESULT_DIR/srpm"

SRPM="$(ls "$RESULT_DIR"/srpm/*.src.rpm)"
if "${MOCK[@]}" "${MOCK_ARGS[@]}" --rebuild "$SRPM"; then
    exit 0
fi

# Specs that run %{__ospython} at parse time fail before mock installs the
# BuildRequires, as the interpreter is not in the chroot yet. Install it
# first, then rebuild in that chroot.
OSPYTHON="$(sed -n 's|^sh: \(line [0-9]*: \)\?\(/usr/bin/python3[.0-9]*\): No such file or directory$|\2|p' \
    "$RESULT_DIR/build.log" | head -1)"
if [ -z "$OSPYTHON" ]; then
    exit 1
fi
echo "=== $OSPYTHON is needed at spec parse time; retrying with it installed ==="
"${MOCK[@]}" "${MOCK_ARGS[@]}" --init
"${MOCK[@]}" "${MOCK_ARGS[@]}" --install "$OSPYTHON"
"${MOCK[@]}" "${MOCK_ARGS[@]}" --no-clean --rebuild "$SRPM"
