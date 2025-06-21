#!/usr/bin/bash

set -euo pipefail

# Location of sync script
SYNC_SCRIPT="/home/yumupload/bin/sync_pgdg_rpms.sh"

# Supported OSes
VALID_OS=("redhat" "fedora")

# OS-specific versions
declare -A VALID_VER
VALID_VER[redhat]="10 9 8"
VALID_VER[fedora]="41 42"

# OS-specific architectures
declare -A VALID_ARCH
VALID_ARCH[redhat]="x86_64 aarch64 ppc64le"
VALID_ARCH[fedora]="x86_64"

# Flags
DRY_RUN=false
DEBUG=false

# Parse CLI options (optional: --dry-run, --debug)
while [[ $# -gt 0 ]]; do
	case "$1" in
	--dry-run) DRY_RUN=true ;;
	--debug) DEBUG=true ;;
	*)
		echo "Unknown option: $1" >&2
		exit 1
		;;
	esac
	shift
done

# Logger
log() {
	echo "[$(date +'%F %T')] $*"
}

# Run the sync command safely
run_sync() {
	local os="$1"
	local ver="$2"
	local arch="$3"

	local cmd="$SYNC_SCRIPT --os $os --ver $ver --arch $arch"
	$DRY_RUN && cmd+=" --dry-run"
	$DEBUG && cmd+=" --debug"

	log "Running: $cmd"
	if ! eval "$cmd"; then
		log "[ERROR] Sync failed for $os $ver $arch"
		return 1
	fi
}

# Main loop
for os in "${VALID_OS[@]}"; do
	for ver in ${VALID_VER[$os]}; do
		for arch in ${VALID_ARCH[$os]}; do
			run_sync "$os" "$ver" "$arch" || continue
		done
	done
done

log "All sync operations completed."

exit 0
