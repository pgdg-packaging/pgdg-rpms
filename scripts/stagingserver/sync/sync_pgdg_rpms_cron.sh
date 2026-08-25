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
OS_VERSIONS[amzn]="${VALID_VER_amzn[*]}"

# Flags
DRY_RUN=false
DEBUG=false
SYNC_OPTIONS=""  # Additional sync options (e.g., "--sync common 18")
declare -a SYNC_ITEMS_RAW=()  # --sync items collected so far, "pg" not yet expanded

# Help
usage() {
	cat <<EOF
Usage: $0 [--dry-run] [--debug] [--sync item1 item2 ...]

Runs a full, unattended sync of every OS/version combination in
sync_pgdg_rpms_config.sh by invoking sync_pgdg_rpms.sh once per os/ver pair
(letting it fan out over that OS's architectures automatically).

Optional:
  --dry-run      Passed through to sync_pgdg_rpms.sh
  --debug        Passed through to sync_pgdg_rpms.sh
  --sync         Passed through to sync_pgdg_rpms.sh to limit what is synced
                 (e.g. --sync common 18 17). The special keyword "pg" expands
                 to every version in PG_ALL_VERSIONS (e.g. --sync pg common
                 syncs all PostgreSQL versions plus the common repo).

Examples:
  $0
  $0 --dry-run
  $0 --sync common
  $0 --sync pg common

EOF
	exit "${1:-1}"
}

# Parse CLI options
while [[ $# -gt 0 ]]; do
	case "$1" in
	--help|-h)
		usage 0
		;;
	--dry-run)
		DRY_RUN=true
		shift
		;;
	--debug)
		DEBUG=true
		shift
		;;
	--sync)
		# Collect all --sync arguments. Each token is re-split on
		# whitespace so this works whether items were passed as
		# separate words (--sync pg common) or as one quoted string
		# (--sync "pg common").
		shift
		while [[ $# -gt 0 && ! "$1" =~ ^-- ]]; do
			for word in $1; do
				SYNC_ITEMS_RAW+=("$word")
			done
			shift
		done
		;;
	*)
		echo "Unknown option: $1" >&2
		usage
		;;
	esac
done

# Expand the "pg" keyword to every version in PG_ALL_VERSIONS, then build
# the final --sync option string to pass through to sync_pgdg_rpms.sh.
if [[ ${#SYNC_ITEMS_RAW[@]} -gt 0 ]]; then
	declare -a SYNC_ITEMS_EXPANDED=()
	for item in "${SYNC_ITEMS_RAW[@]}"; do
		if [[ "$item" == "pg" ]]; then
			SYNC_ITEMS_EXPANDED+=("${PG_ALL_VERSIONS[@]}")
		else
			SYNC_ITEMS_EXPANDED+=("$item")
		fi
	done
	SYNC_OPTIONS="--sync ${SYNC_ITEMS_EXPANDED[*]}"
fi

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
