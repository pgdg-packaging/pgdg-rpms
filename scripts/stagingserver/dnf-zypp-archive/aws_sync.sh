#!/usr/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/aws_sync_config.sh"

# Default/empty variables
os=""
arch=""
ver=""
pg=""
extras=""
non_free=0
dry_run=0
debug=0

BASE_DIR=""
S3_BUCKET=""

osdistro=""
osname=""
any_sync_done=0

usage() {
  cat <<EOF
Usage: $0 --os <os> --ver <version> [--arch <arch>] [--pg <pg_version>] [options]

Required:
  --os         OS name (rhel, fedora, or sles)
  --ver        OS version (e.g., 8, 9, 10, 41, 42, 43)

Optional:
  --arch       Architecture (${VALID_ARCH[*]})
               If omitted, all architectures are synced.
  --pg         PostgreSQL version ($(IFS="|"; echo "${VALID_PG_VERSIONS[*]}"))
               If omitted, only the common repo is synced.
  --extras=1   Sync extras (redhat only)
  --non-free   Sync non-free repos for all PG versions (redhat only)
  --dry-run    Show commands without running
  --debug      Print debug output
  --help       Show this help
EOF
  exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --os) os="$2"; shift ;;
    --arch) arch="$2"; shift ;;
    --ver) ver="$2"; shift ;;
    --pg) pg="$2"; shift ;;
    --extras=*) extras="${1#*=}" ;;
    --non-free) non_free=1 ;;
    --dry-run) dry_run=1 ;;
    --debug) debug=1 ;;
    --help) usage ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
  shift
done

# Validate required parameters
if [[ -z "$os" || -z "$ver" ]]; then
  echo "Missing required parameters."
  usage
fi

# --non-free is mutually exclusive with --extras only
if [[ $non_free -eq 1 && "$extras" == "1" ]]; then
  echo "--non-free cannot be combined with --extras."
  exit 1
fi

# Validate architecture if provided
if [[ -n "$arch" ]] && ! is_valid "$arch" "${VALID_ARCH[@]}"; then
  echo "Invalid architecture: $arch"
  echo "Valid architectures: ${VALID_ARCH[*]}"
  exit 1
fi

# Validate pg version if provided
if [[ -n "$pg" ]] && ! is_valid "$pg" "${VALID_PG_VERSIONS[@]}"; then
  echo "Invalid PostgreSQL version: $pg"
  echo "Valid versions: ${VALID_PG_VERSIONS[*]}"
  exit 1
fi

# Map os to osdistro and osname (the directory name used in repo paths)
case "$os" in
  rhel)     osdistro="redhat";  osname="rhel" ;;
  fedora)   osdistro="fedora";  osname="fedora" ;;
  sles)     osdistro="suse";    osname="sles" ;;
  opensuse) osdistro="opensuse"; osname="leap" ;;
  *) echo "Unsupported OS: $os"; exit 1 ;;
esac

# Resolve base dir and S3 bucket from config
BASE_DIR_var="BASE_DIR_${osdistro}"
S3_BUCKET_var="S3_BUCKET_${osdistro}"
BASE_DIR="${!BASE_DIR_var}"
S3_BUCKET="${!S3_BUCKET_var}"

if [[ -z "$BASE_DIR" || -z "$S3_BUCKET" ]]; then
  echo "No BASE_DIR or S3_BUCKET configured for osdistro: $osdistro"
  exit 1
fi

# Resolve arch list: single value or all
archs=("$arch")
[[ -z "$arch" ]] && archs=("${VALID_ARCH[@]}")

# Debug info
if [[ $debug -eq 1 ]]; then
  echo "Debug Info:"
  echo "  OS: $os"
  echo "  OS Distro: $osdistro"
  echo "  OS Name (path): $osname"
  echo "  Arch(es): ${archs[*]}"
  echo "  Version: $ver"
  echo "  PG Version: ${pg:-<not set>}"
  echo "  Extras: $extras"
  echo "  Non-free: $non_free"
  echo "  Dry Run: $dry_run"
  echo ""
fi

run_sync_cmd() {
  local src="$1"
  local dst="$2"

  if [[ $dry_run -eq 1 ]]; then
    echo "[Dry-run] aws s3 sync $src $dst"
  else
    echo "Running: aws s3 sync $src $dst"
    aws s3 sync "$src" "$dst"
  fi
  any_sync_done=1
}

sync_common_repo() {
  local a="$1"
  local path="$BASE_DIR/common/$osdistro/$osname-$ver-$a"
  if [[ -d "$path" ]]; then
    echo "Syncing common repo: $path"
    run_sync_cmd "$path" "$S3_BUCKET/common/$osdistro/$osname-$ver-$a"
  else
    echo "[Skip] Missing common repo dir: $path"
  fi
}

sync_pg_repo() {
  local pgver="$1"
  local a="$2"
  local path="$BASE_DIR/$pgver/$osdistro/$osname-$ver-$a"
  if [[ -d "$path" ]]; then
    echo "Syncing PG $pgver repo: $path"
    run_sync_cmd "$path" "$S3_BUCKET/$pgver/$osdistro/$osname-$ver-$a/"
  else
    echo "[Skip] Missing PG $pgver repo dir: $path"
  fi
}

sync_non_free_repos() {
  local pgver_filter="$1"  # if set, sync only this PG version; otherwise sync all
  if [[ "$osdistro" != "redhat" ]]; then
    echo "[Skip] Non-free repos are only supported for redhat."
    return
  fi
  local versions=("${VALID_PG_VERSIONS[@]}")
  [[ -n "$pgver_filter" ]] && versions=("$pgver_filter")
  for pgver in "${versions[@]}"; do
    for a in "${archs[@]}"; do
      local path="$BASE_DIR_non_free/$pgver/$osdistro/$osname-$ver-$a"
      if [[ -d "$path" ]]; then
        echo "Syncing non-free PG $pgver repo: $path"
        run_sync_cmd "$path" "$S3_BUCKET/non-free/$pgver/$osdistro/$osname-$ver-$a"
      else
        echo "[Skip] Missing non-free repo dir: $path"
      fi
    done
  done
}

cleanup_testing_repos() {
  local a="$1"
  echo "Cleaning testing repos for arch: $a"
  for pgv in "${VALID_PG_VERSIONS[@]}"; do
    for subdir in "" "common/" "debug/"; do
      local path="$BASE_DIR/testing/${subdir}$pgv/$osdistro/$osname-$ver-$a"
      if [[ -d "$path" ]]; then
        if [[ $dry_run -eq 1 ]]; then
          echo "[Dry-run] /bin/rm -rvf $path"
        else
          /bin/rm -rvf "$path"
        fi
      fi
    done
  done
}

# non-free is fully independent of the normal arch-scoped sync path.
if [[ $non_free -eq 1 ]]; then
  sync_non_free_repos "$pg"
else
  # Main sync loop over all target architectures
  for a in "${archs[@]}"; do
    echo "--- Arch: $a ---"

    if [[ -z "$pg" ]]; then
      sync_common_repo "$a"
    else
      sync_pg_repo "$pg" "$a"
    fi

    # Clean up testing repos only if something was synced for this arch
    if [[ $any_sync_done -eq 1 ]]; then
      cleanup_testing_repos "$a"
    fi

    if [[ "$extras" == "1" ]]; then
      echo "Syncing extras repo for arch: $a"
      run_sync_cmd "$BASE_DIR/extras/$osdistro/$a" "$S3_BUCKET/extras/$osdistro/$a"
    fi
  done
fi

if [[ $any_sync_done -eq 0 ]]; then
  echo -e "\n[Info] No sync was performed. Skipping cleanup."
fi

exit 0
