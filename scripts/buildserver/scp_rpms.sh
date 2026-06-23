#!/usr/bin/env bash
# scp-rpms.sh — Transfer PostgreSQL RPMs to a target host
# Used to transfer RHEL n-2 and n-1 (S)RPMs to RHEL n host
# Usage: scp-rpms.sh [OPTIONS]

set -euo pipefail

# ─── Load shared configuration ────────────────────────────────────────────────
# Provides: red/green/blue/reset colors, UID guard, osarch, pgStableBuilds, …

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=global.sh
source "${SCRIPT_DIR}/global.sh"

# ─── Configuration ────────────────────────────────────────────────────────────

TARGET_IP="192.168.122.160"
TARGET_USER=""				# empty = same as local user
SSH_PORT=22
ARCH="${osarch}"			# from global.sh (osarch); override with --arch
# pgStableBuilds in global.sh is a single-element array containing a
# space-separated string. Unquoted expansion intentionally lets word splitting
# flatten it into proper individual array elements here.
PG_VERSIONS=(${pgStableBuilds[@]})	# from global.sh; override with --versions
LOCAL_BASE="${HOME}"
REMOTE_BASE="~"
RPM_DIR_PREFIX="rpm"                    # directories are rpm18, rpm17, …
COMMON_DIR="rpmcommon"			# common repo, synced outside version loop
EXTRAS_DIR="pgdg.extras"		# extras repo, synced outside version loop

SYNC_ARCH_RPMS=true
SYNC_NOARCH_RPMS=true
SYNC_SRPMS=true

SCP_OPTS="-p"				# -p preserves timestamps; add -q to silence

# ─── Helpers ──────────────────────────────────────────────────────────────────

usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Options:
  -t, --target IP        Target host IP or hostname  (default: ${TARGET_IP})
  -u, --user   USER      Remote SSH user             (default: current user)
  -p, --port   PORT      SSH port                    (default: ${SSH_PORT})
  -a, --arch   ARCH      RPM architecture            (default: ${ARCH})
  -v, --versions LIST    Comma-separated PG versions (default: $(IFS=,; echo "${PG_VERSIONS[*]}"))
  -l, --local  DIR       Local base directory        (default: ${LOCAL_BASE})
  -r, --remote DIR       Remote base directory       (default: ${REMOTE_BASE})
      --no-arch          Skip arch-specific RPMs
      --no-noarch        Skip noarch RPMs
      --no-srpms         Skip SRPMs
  -n, --dry-run          Print commands without executing
  -h, --help             Show this help
EOF
    exit 0
}

DRY_RUN=false

run() {
    if "${DRY_RUN}"; then
        echo "[dry-run] $*"
    else
        "$@"
    fi
}

# ─── Argument parsing ─────────────────────────────────────────────────────────

while [[ $# -gt 0 ]]; do
    case "$1" in
	-t|--target)    TARGET_IP="$2";   shift 2 ;;
	-u|--user)      TARGET_USER="$2"; shift 2 ;;
	-p|--port)      SSH_PORT="$2";    shift 2 ;;
	-a|--arch)      ARCH="$2";        shift 2 ;;
	-v|--versions)  IFS=',' read -ra PG_VERSIONS <<< "$2"; shift 2 ;;
	-l|--local)     LOCAL_BASE="$2";  shift 2 ;;
	-r|--remote)    REMOTE_BASE="$2"; shift 2 ;;
	--no-arch)      SYNC_ARCH_RPMS=false;   shift ;;
	--no-noarch)    SYNC_NOARCH_RPMS=false;  shift ;;
	--no-srpms)     SYNC_SRPMS=false;        shift ;;
	-n|--dry-run)   DRY_RUN=true;    shift ;;
	-h|--help)      usage ;;
	*) echo "Unknown option: $1" >&2; usage ;;
    esac
done

# ─── Derived values ───────────────────────────────────────────────────────────

TARGET_HOST="${TARGET_IP}"
[[ -n "${TARGET_USER}" ]] && TARGET_HOST="${TARGET_USER}@${TARGET_IP}"

SCP_OPTS="${SCP_OPTS} -P ${SSH_PORT}"

# ─── Main ─────────────────────────────────────────────────────────────────────

echo "Target  : ${TARGET_HOST}"
echo "Arch    : ${ARCH}"
echo "Versions: ${PG_VERSIONS[*]}"
echo "Dry-run : ${DRY_RUN}"
echo

for ver in "${PG_VERSIONS[@]}"; do
    dir="${RPM_DIR_PREFIX}${ver}"
    local_dir="${LOCAL_BASE}/${dir}"
    remote_dir="${REMOTE_BASE}/${dir}"

    if "${SYNC_ARCH_RPMS}"; then
        echo ">> PG${ver}  RPMS/${ARCH}"
        run scp ${SCP_OPTS} "${local_dir}/RPMS/${ARCH}/"* \
            "${TARGET_HOST}:${remote_dir}/RPMS/${ARCH}/"
    fi

    if "${SYNC_NOARCH_RPMS}"; then
        echo ">> PG${ver}  RPMS/noarch"
        run scp ${SCP_OPTS} "${local_dir}/RPMS/noarch/"* \
            "${TARGET_HOST}:${remote_dir}/RPMS/noarch/"
    fi

    if "${SYNC_SRPMS}"; then
        echo ">> PG${ver}  SRPMS"
        run scp ${SCP_OPTS} "${local_dir}/SRPMS/"* \
            "${TARGET_HOST}:${remote_dir}/SRPMS/"
    fi

    echo
done

# ─── Common repo (outside version loop) ───────────────────────────────────────

common_local="${LOCAL_BASE}/${COMMON_DIR}"
common_remote="${REMOTE_BASE}/${COMMON_DIR}"

echo ">> ${COMMON_DIR}"

if "${SYNC_ARCH_RPMS}"; then
    echo ">> ${COMMON_DIR}  RPMS/${ARCH}"
    run scp ${SCP_OPTS} "${common_local}/RPMS/${ARCH}/"* \
        "${TARGET_HOST}:${common_remote}/RPMS/${ARCH}/"
fi

if "${SYNC_NOARCH_RPMS}"; then
    echo ">> ${COMMON_DIR}  RPMS/noarch"
    run scp ${SCP_OPTS} "${common_local}/RPMS/noarch/"* \
        "${TARGET_HOST}:${common_remote}/RPMS/noarch/"
fi

if "${SYNC_SRPMS}"; then
    echo ">> ${COMMON_DIR}  SRPMS"
    run scp ${SCP_OPTS} "${common_local}/SRPMS/"* \
        "${TARGET_HOST}:${common_remote}/SRPMS/"
fi

echo

# ─── Extras repo (outside version loop) ───────────────────────────────────────

extras_local="${LOCAL_BASE}/${EXTRAS_DIR}"
extras_remote="${REMOTE_BASE}/${EXTRAS_DIR}"

echo ">> ${EXTRAS_DIR}"

if "${SYNC_ARCH_RPMS}"; then
    echo ">> ${EXTRAS_DIR}  RPMS/${ARCH}"
    run scp ${SCP_OPTS} "${extras_local}/RPMS/${ARCH}/"* \
        "${TARGET_HOST}:${extras_remote}/RPMS/${ARCH}/"
fi

if "${SYNC_NOARCH_RPMS}"; then
    echo ">> ${EXTRAS_DIR}  RPMS/noarch"
    run scp ${SCP_OPTS} "${extras_local}/RPMS/noarch/"* \
        "${TARGET_HOST}:${extras_remote}/RPMS/noarch/"
fi

if "${SYNC_SRPMS}"; then
    echo ">> ${EXTRAS_DIR}  SRPMS"
    run scp ${SCP_OPTS} "${extras_local}/SRPMS/"* \
        "${TARGET_HOST}:${extras_remote}/SRPMS/"
fi

echo

echo "Done."
