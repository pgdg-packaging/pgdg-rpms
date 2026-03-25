#!/usr/bin/bash

set -euo pipefail

# Source central configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/sync_pgdg_rpms_config.sh"

if [[ ! -f "$CONFIG_FILE" ]]; then
	echo "ERROR: Configuration file not found: $CONFIG_FILE" >&2
	exit 1
fi

source "$CONFIG_FILE"

# Location of sync script
SYNC_SCRIPT="${SCRIPT_DIR}/sync_pgdg_rpms.sh"

# Build OS_VERSIONS associative array from config
declare -A OS_VERSIONS
OS_VERSIONS[redhat]="${VALID_VER_redhat[*]}"
OS_VERSIONS[fedora]="${VALID_VER_fedora[*]}"
OS_VERSIONS[sles]="${VALID_VER_sles[*]}"
OS_VERSIONS[opensuse]="${VALID_VER_opensuse[*]}"

# Flags
DRY_RUN=false
DEBUG=false
SYNC_OPTIONS=""  # Additional sync options (e.g., "--sync common 18")

# Parse CLI options
while [[ $# -gt 0 ]]; do
	case "$1" in
	--dry-run)
		DRY_RUN=true
		shift
		;;
	--debug)
		DEBUG=true
		shift
		;;
	--sync)
		# Collect all --sync arguments
		SYNC_OPTIONS="--sync"
		shift
		while [[ $# -gt 0 && ! "$1" =~ ^-- ]]; do
			SYNC_OPTIONS+=" $1"
			shift
		done
		;;
	*)
		echo "Unknown option: $1" >&2
		echo "Usage: $0 [--dry-run] [--debug] [--sync item1 item2 ...]"
		exit 1
		;;
	esac
done

# Logger
log() {
	echo "[$(date +'%F %T')] $*"
}

# Run the sync command safely
run_sync() {
	local os="$1"
	local ver="$2"

	# Build command - let main script handle all architectures
	local cmd="$SYNC_SCRIPT --os $os --ver $ver"

	# Add optional flags
	$DRY_RUN && cmd+=" --dry-run"
	$DEBUG && cmd+=" --debug"
	[[ -n "$SYNC_OPTIONS" ]] && cmd+=" $SYNC_OPTIONS"

	log "Running: $cmd"
	if ! eval "$cmd"; then
		log "[ERROR] Sync failed for $os $ver"
		return 1
	fi
	log "Successfully synced $os $ver (all architectures)"
}

# Main loop - iterate through OS and versions only
# The main script will handle all architectures automatically
log "Starting cron sync operation"

for os in "${!OS_VERSIONS[@]}"; do
	for ver in ${OS_VERSIONS[$os]}; do
		run_sync "$os" "$ver" || continue
	done
done

log "All sync operations completed."

exit 0
