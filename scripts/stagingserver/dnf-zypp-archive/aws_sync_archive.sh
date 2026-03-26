#!/usr/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/aws_sync_config.sh"

# Default values
OS_NAME=""
ARCH=""
OS_VERSION=""
PG_VERSION=""
DEBUG=0
DRY_RUN=0
extras=""
non_free=0

usage() {
  cat <<EOF
Usage: $0 --os-name <fedora|redhat> [--arch <arch>] [--os-version <ver>] [--pg-version <pg>] [--dry-run] [--debug]

Required:
  --os-name        fedora, redhat, sles, or opensuse

Optional:
  --arch           aarch64, ppc64le, x86_64 (default: all)
  --os-version     OS version (if omitted, runs for all valid versions)
  --pg-version     PostgreSQL version (if omitted, runs for all)
  --dry-run        Simulate the operations
  --debug          Show debug output

Redhat only:
  --extras=1
  --non-free
EOF
  exit 1
}

# Parse CLI
while [[ $# -gt 0 ]]; do
  case "$1" in
    --os-name) OS_NAME="$2"; shift ;;
    --arch) ARCH="$2"; shift ;;
    --os-version) OS_VERSION="$2"; shift ;;
    --pg-version) PG_VERSION="$2"; shift ;;
    --extras=*) extras="${1#*=}" ;;
    --non-free) non_free=1 ;;
    --dry-run) DRY_RUN=1 ;;
    --debug) DEBUG=1 ;;
    --help) usage ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
  shift
done

# Validate OS_NAME
if [[ -z "$OS_NAME" ]]; then
  echo "--os-name is required."
  usage
fi

if [[ "$OS_NAME" != "fedora" && "$OS_NAME" != "redhat" && "$OS_NAME" != "sles" && "$OS_NAME" != "opensuse" ]]; then
  echo "Invalid OS name: $OS_NAME"
  exit 1
fi

# Set OS-specific variables
if [[ "$OS_NAME" == "redhat" ]]; then
  osdistro="redhat"
  os="rhel"
  VALID_OS_VERSIONS=("${VALID_REDHAT_OS_VERSIONS[@]}")
elif [[ "$OS_NAME" == "sles" ]]; then
  osdistro="suse"
  os="sles"
  VALID_OS_VERSIONS=("${VALID_SLES_OS_VERSIONS[@]}")
elif [[ "$OS_NAME" == "opensuse" ]]; then
  osdistro="opensuse"
  os="opensuse"
  VALID_OS_VERSIONS=("${VALID_OPENSUSE_OS_VERSIONS[@]}")
else
  osdistro="fedora"
  os="fedora"
  VALID_OS_VERSIONS=("${VALID_FEDORA_OS_VERSIONS[@]}")
fi

# Validate arch if provided
if [[ -n "$ARCH" ]] && ! is_valid "$ARCH" "${VALID_ARCH[@]}"; then
  echo "Invalid arch: $ARCH"
  echo "Valid architectures: ${VALID_ARCH[*]}"
  exit 1
fi

# Validate pg version if provided
if [[ -n "$PG_VERSION" ]] && ! is_valid "$PG_VERSION" "${VALID_PG_VERSIONS[@]}"; then
  echo "Invalid pg-version: $PG_VERSION"
  echo "Valid versions: ${VALID_PG_VERSIONS[*]}"
  exit 1
fi

# Validate non-free is only used with redhat
if [[ $non_free -eq 1 && "$OS_NAME" != "redhat" ]]; then
  echo "--non-free is only supported with --os-name redhat."
  exit 1
fi

# --non-free is mutually exclusive with --extras only
if [[ $non_free -eq 1 && -n "$extras" ]]; then
  echo "--non-free cannot be combined with --extras."
  exit 1
fi

# Confirm before looping over multiple combinations
if [[ -z "$PG_VERSION" || -z "$OS_VERSION" ]]; then
  echo "You're about to run sync for multiple combinations."
  echo -n "Are you sure? [Y/n]: "
  read -r ans
  [[ "$ans" != "Y" ]] && echo "Aborted." && exit 1
fi

# Build combinations (use all valid values when a dimension is unspecified)
pg_versions=("${PG_VERSION:-}")
[[ -z "$PG_VERSION" ]] && pg_versions=("${VALID_PG_VERSIONS[@]}")

os_versions=("$OS_VERSION")
[[ -z "$OS_VERSION" ]] && os_versions=("${VALID_OS_VERSIONS[@]}")

# Run syncs — arch is handled inside aws_sync.sh when --arch is omitted.
for pg in "${pg_versions[@]}"; do
  for osv in "${os_versions[@]}"; do
    cmd="$SCRIPT_DIR/aws_sync.sh --os $os --ver $osv --pg $pg"
    [[ -n "$ARCH"   ]] && cmd+=" --arch $ARCH"
    [[ -n "$extras"  ]] && cmd+=" --extras=$extras"
    [[ $non_free -eq 1 ]] && cmd+=" --non-free"
    [[ $DRY_RUN -eq 1 ]] && cmd+=" --dry-run"
    [[ $DEBUG   -eq 1 ]] && cmd+=" --debug"

    echo "Running: $cmd"
    if ! eval "$cmd"; then
      echo "[FAIL] $cmd" >> "$SCRIPT_DIR/aws_sync_archive_failures.log"
    fi
  done
done

exit 0
