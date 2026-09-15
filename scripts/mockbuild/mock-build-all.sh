#!/usr/bin/env bash
#
# mock-build-all.sh -d "opensuse-leap-16" [-k non-common] [-p "18 16"] [-j 4] [-o report.txt]
#
# Run mock-build-matrix.sh for every package under a given kind directory
# (non-common/ by default), restricted to the given distro(s), and collect
# every package's pass/fail status into a single combined report file.
#
# Each package's full raw output (SRPM build + mock logs) is also kept
# under <log-dir>/<kind>/<package>.log for later inspection of a FAIL.
# Logs and the combined report default to ~/mock-build-logs -- deliberately
# outside the pgrpms checkout, since this script may live inside the repo
# (scripts/mockbuild/) and we don't want build logs polluting `git status`.
#
# Packages can build in parallel (-j/--jobs, default 1). Every invocation
# of mock-build-matrix.sh is given -u "<package>" (mock's --uniqueext), so
# concurrent packages targeting the identical distro/PG-version chroot
# don't collide -- this is on unconditionally, not just when -j > 1, so
# bumping -j later can't reintroduce the collision by surprise. Report
# assembly itself stays serial: all package builds are launched (bounded by
# -j) and their raw output captured to per-package log files first, then
# the combined report is written from those logs after everything
# finishes, so concurrent writers never interleave into the same file.
#
# Run from anywhere inside a pgrpms checkout.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MOCK_SCRIPT="$SCRIPT_DIR/mock-build-matrix.sh"

KIND="non-common"
DISTROS_ARG=""
PG_ARG=""
REPORT=""
LOG_ROOT="$HOME/mock-build-logs"
JOBS=5

usage() {
    cat <<EOF >&2
Usage: $0 -d "opensuse-leap-16" [-k non-common] [-p "18 16"] [-j 4] [-o report.txt] [-l log-dir]

  -d, --distros "..."       Distro token(s) to mock-build against (space-separated,
                             passed through to mock-build-matrix.sh's -d). Required.
  -k, --kind common|non-common|non-free|extras
                             Which directory under rpm/redhat/main/ to sweep.
                             Default: non-common
  -p, --pg-versions "18 16" PostgreSQL major versions (passed through to
                             mock-build-matrix.sh's -p). Default: mock-build-matrix.sh's own default.
  -j, --jobs N              Number of packages to build concurrently. Default: 1 (serial).
                             Each concurrent mock build is CPU/IO/network-heavy -- raise this
                             cautiously and to no more than this host can actually sustain.
  -o, --output FILE         Combined report file. Default: <log-dir>/mock-build-all-<kind>-<timestamp>.txt
  -l, --log-dir DIR         Root directory for per-package logs and the default report.
                             Default: $LOG_ROOT (kept out of the git tree on purpose)
EOF
    exit 1
}

while [ $# -gt 0 ]; do
    case "$1" in
        -d|--distros) DISTROS_ARG="$2"; shift 2 ;;
        -k|--kind) KIND="$2"; shift 2 ;;
        -p|--pg-versions) PG_ARG="$2"; shift 2 ;;
        -j|--jobs) JOBS="$2"; shift 2 ;;
        -o|--output) REPORT="$2"; shift 2 ;;
        -l|--log-dir) LOG_ROOT="$2"; shift 2 ;;
        -h|--help) usage ;;
        *) echo "Unknown option: $1" >&2; usage ;;
    esac
done

if [ -z "$DISTROS_ARG" ]; then
    echo "Error: -d/--distros is required." >&2
    usage
fi

# Find the pgrpms checkout: use the current directory if it's inside one,
# otherwise fall back to ~/git/pgrpms, the checkout path every buildserver
# script in this repo assumes (see packagebuild.sh) -- needed because this
# script is typically deployed to ~/bin and invoked from elsewhere, so
# SCRIPT_DIR itself is not inside the checkout.
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [ -z "$REPO_ROOT" ] && [ -d "$HOME/git/pgrpms/.git" ]; then
    REPO_ROOT="$HOME/git/pgrpms"
fi
if [ -z "$REPO_ROOT" ]; then
    echo "Not inside a git repository, and no checkout found at ~/git/pgrpms." >&2
    exit 1
fi

KIND_ROOT="$REPO_ROOT/rpm/redhat/main/$KIND"
if [ ! -d "$KIND_ROOT" ]; then
    echo "No such directory: $KIND_ROOT" >&2
    exit 1
fi

LOG_DIR="$LOG_ROOT/$KIND"
mkdir -p "$LOG_DIR"
[ -n "$REPORT" ] || REPORT="$LOG_ROOT/mock-build-all-${KIND}-$(date +%Y%m%d-%H%M%S).txt"

: > "$REPORT"

ALL_PKGS=()
for pkg_main in "$KIND_ROOT"/*/main; do
    [ -d "$pkg_main" ] || continue
    ALL_PKGS+=("$(basename "$(dirname "$pkg_main")")")
done
TOTAL=${#ALL_PKGS[@]}

# Pass 1: launch every package's build, bounded to $JOBS concurrent, each
# writing its raw output to its own log file plus an exit-status marker.
# -u "$pkg" keeps concurrent packages from colliding on the same mock chroot.
launched=0
running=0
for pkg in "${ALL_PKGS[@]}"; do
    launched=$((launched + 1))
    log_file="$LOG_DIR/${pkg}.log"

    args=(-d "$DISTROS_ARG" -u "$pkg")
    [ -n "$PG_ARG" ] && args+=(-p "$PG_ARG")

    echo "=== [$launched/$TOTAL] launching $pkg ==="
    (
        if "$MOCK_SCRIPT" "${args[@]}" "$pkg" > "$log_file" 2>&1; then
            echo ok > "$log_file.status"
        else
            echo script-error > "$log_file.status"
        fi
    ) &

    running=$((running + 1))
    if [ "$running" -ge "$JOBS" ]; then
        wait -n
        running=$((running - 1))
    fi
done
wait

# Pass 2: assemble the combined report and counts serially, in the original
# order, from the logs Pass 1 produced -- avoids concurrent writers to $REPORT.
PASS_COUNT=0
FAIL_COUNT=0
for pkg in "${ALL_PKGS[@]}"; do
    log_file="$LOG_DIR/${pkg}.log"
    script_status="$(cat "$log_file.status" 2>/dev/null || echo script-error)"
    rm -f "$log_file.status"

    {
        echo "=============================================="
        echo "Package: $pkg  ($(date '+%Y-%m-%d %H:%M:%S'))  [full log: $log_file]"
        echo "=============================================="
        if [ "$script_status" = "script-error" ]; then
            echo "mock-build-matrix.sh exited non-zero before/without producing a results table."
            tail -20 "$log_file"
        else
            sed -n '/^=== Results ===$/,$p' "$log_file"
        fi
        echo
    } >> "$REPORT"

    if [ "$script_status" = "script-error" ] || grep -q "FAIL" "$log_file"; then
        FAIL_COUNT=$((FAIL_COUNT + 1))
    else
        PASS_COUNT=$((PASS_COUNT + 1))
    fi
done

{
    echo "=============================================="
    echo "SUMMARY: $TOTAL packages, $PASS_COUNT clean, $FAIL_COUNT with at least one FAIL/error"
    echo "=============================================="
} >> "$REPORT"

echo
echo "Done. $TOTAL packages, $PASS_COUNT clean, $FAIL_COUNT with at least one FAIL/error."
echo "Combined report: $REPORT"
echo "Per-package logs: $LOG_DIR/"
