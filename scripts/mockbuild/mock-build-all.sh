#!/usr/bin/env bash
#
# mock-build-all.sh -d "opensuse-leap-16" [-k non-common] [-p "18 16"] [-o report.txt]
#
# Run mock-build-matrix.sh for every package under a given kind directory
# (non-common/ by default), restricted to the given distro(s), and collect
# every package's pass/fail status into a single combined report file.
#
# Each package's full raw output (SRPM build + mock logs) is also kept
# under logs/<kind>/<package>.log for later inspection of a FAIL.
#
# Run from anywhere inside a pgrpms checkout.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MOCK_SCRIPT="$SCRIPT_DIR/mock-build-matrix.sh"

KIND="non-common"
DISTROS_ARG=""
PG_ARG=""
REPORT=""

usage() {
    cat <<EOF >&2
Usage: $0 -d "opensuse-leap-16" [-k non-common] [-p "18 16"] [-o report.txt]

  -d, --distros "..."       Distro token(s) to mock-build against (space-separated,
                             passed through to mock-build-matrix.sh's -d). Required.
  -k, --kind common|non-common|non-free|extras
                             Which directory under rpm/redhat/main/ to sweep.
                             Default: non-common
  -p, --pg-versions "18 16" PostgreSQL major versions (passed through to
                             mock-build-matrix.sh's -p). Default: mock-build-matrix.sh's own default.
  -o, --output FILE         Combined report file. Default: mock-build-all-<kind>-<timestamp>.txt
EOF
    exit 1
}

while [ $# -gt 0 ]; do
    case "$1" in
        -d|--distros) DISTROS_ARG="$2"; shift 2 ;;
        -k|--kind) KIND="$2"; shift 2 ;;
        -p|--pg-versions) PG_ARG="$2"; shift 2 ;;
        -o|--output) REPORT="$2"; shift 2 ;;
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

[ -n "$REPORT" ] || REPORT="mock-build-all-${KIND}-$(date +%Y%m%d-%H%M%S).txt"
LOG_DIR="$SCRIPT_DIR/logs/$KIND"
mkdir -p "$LOG_DIR"

: > "$REPORT"

PASS_COUNT=0
FAIL_COUNT=0
TOTAL=0

for pkg_main in "$KIND_ROOT"/*/main; do
    [ -d "$pkg_main" ] || continue
    pkg="$(basename "$(dirname "$pkg_main")")"
    TOTAL=$((TOTAL + 1))
    log_file="$LOG_DIR/${pkg}.log"

    args=(-d "$DISTROS_ARG")
    [ -n "$PG_ARG" ] && args+=(-p "$PG_ARG")

    echo "=== [$TOTAL] $pkg ==="
    if "$MOCK_SCRIPT" "${args[@]}" "$pkg" > "$log_file" 2>&1; then
        script_status="ok"
    else
        script_status="script-error"
    fi

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

    if grep -q "FAIL" "$log_file" || [ "$script_status" = "script-error" ]; then
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
