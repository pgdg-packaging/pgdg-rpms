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
JOBS="${MAX_PARALLEL:-1}"  # Max concurrent os/ver syncs (--jobs overrides config)
SYNC_OPTIONS=""  # Additional sync options (e.g., "--sync common 18")
declare -a SYNC_ITEMS_RAW=()  # --sync items collected so far, "pg" not yet expanded

# Help
usage() {
	cat <<EOF
Usage: $0 [--dry-run] [--debug] [--jobs N] [--sync item1 item2 ...]

Runs a full, unattended sync of every OS/version combination in
sync_pgdg_rpms_config.sh by invoking sync_pgdg_rpms.sh once per os/ver pair
(letting it fan out over that OS's architectures automatically). Up to
MAX_PARALLEL (see config) os/ver pairs are synced at the same time; the
output of each is printed as a block when it finishes.

Optional:
  --dry-run      Passed through to sync_pgdg_rpms.sh
  --debug        Passed through to sync_pgdg_rpms.sh
  --jobs N       Number of os/ver syncs to run in parallel (default:
                 MAX_PARALLEL from the config; 1 = sequential)
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
	--jobs|-j)
		if [[ $# -lt 2 || ! "$2" =~ ^[1-9][0-9]*$ ]]; then
			echo "ERROR: --jobs requires a positive integer" >&2
			usage
		fi
		JOBS="$2"
		shift 2
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

# Main loop - iterate through OS and versions only, running up to $JOBS
# syncs concurrently. The main script handles all architectures itself.
# Each job logs to its own file, which is printed (under a lock, so blocks do
# not interleave) once the job finishes; a ".failed" marker records errors.
# Refuse to run if a previous (real) run is still going. The lock is held on
# fd 200 for the life of this script and released automatically on exit.
# Dry runs change nothing, so they skip the lock.
if ! $DRY_RUN; then
	exec 200>"${CRON_LOCK_FILE:-/tmp/sync_pgdg_rpms_cron.lock}"
	if ! flock -n 200; then
		log "[WARN] Another sync_pgdg_rpms_cron.sh run is still in progress (lock: ${CRON_LOCK_FILE:-/tmp/sync_pgdg_rpms_cron.lock}), skipping this run."
		exit 0
	fi
fi

log "Starting cron sync operation (parallel jobs: $JOBS)"

WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT

run_job() {
	local os="$1"
	local ver="$2"
	local jobname="${os}-${ver}"
	local logfile="${WORK_DIR}/${jobname}.log"

	run_sync "$os" "$ver" >"$logfile" 2>&1 || touch "${WORK_DIR}/${jobname}.failed"

	(
		flock 9
		echo "===== $os $ver ====="
		cat "$logfile"
	) 9>"${WORK_DIR}/.output.lock"
}

for os in "${!OS_VERSIONS[@]}"; do
	for ver in ${OS_VERSIONS[$os]}; do
		# Throttle: wait for a slot once $JOBS jobs are running
		while (( $(jobs -rp | wc -l) >= JOBS )); do
			wait -n || true
		done
		run_job "$os" "$ver" &
	done
done

wait || true

shopt -s nullglob
failed=("$WORK_DIR"/*.failed)
if (( ${#failed[@]} > 0 )); then
	for f in "${failed[@]}"; do
		f="${f##*/}"
		log "[ERROR] Sync failed for ${f%.failed}"
	done
fi

log "All sync operations completed."

exit 0
