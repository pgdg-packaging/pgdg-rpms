#!/usr/bin/bash

set -euo pipefail

sync_had_errors=0

# Source central configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/sync_pgdg_rpms_config.sh"

if [[ ! -f "$CONFIG_FILE" ]]; then
	echo "ERROR: Configuration file not found: $CONFIG_FILE" >&2
	exit 1
fi

source "$CONFIG_FILE"

# Runtime variables
OS=""
ARCH=""
VER=""
DRY_RUN=false
DEBUG=false
SYNC_ITEMS=()				# Items to sync (common, extras, testing, non-free, or PG versions)

# Help
usage() {
	cat <<EOF
Usage: $0 [--os <os>] [--ver <version>] [options]

Optional:
  --os           Operating system: ${VALID_OS[*]}
                 If not specified, syncs all supported operating systems

  --ver          OS version: redhat (${VALID_VER_redhat[*]}), fedora (${VALID_VER_fedora[*]}), sles (${VALID_VER_sles[*]}), opensuse (${VALID_VER_opensuse[*]}), amzn (${VALID_VER_amzn[*]})
                 If not specified, syncs all versions for the OS(es) being processed
                 If --os is also omitted, an OS for which this version is not valid is skipped

  --arch         Architecture: aarch64, ppc64le, x86_64
                 If not specified, syncs all supported architectures for the OS(es) being processed
                 If --os is also omitted, an OS for which this architecture is not valid is skipped

  --sync         Sync specific items: common, extras, testing, non-free, or PG version (e.g. 18)
                 Can specify multiple items (e.g. --sync common 18 17)
                 If not specified, syncs all available repos
  --dry-run      Simulate the sync without transferring files
  --debug        Show detailed debug output

Examples:
  $0 --os redhat --ver 9.7 --sync common
  $0 --os sles --ver 15.6 --arch x86_64 --sync 18 17
  $0 --os fedora --ver 43 --sync common extras testing
  $0 --sync common

EOF
	exit "${1:-1}"
}

# Contains helper
contains() {
	local val="$1"
	shift
	for item in "$@"; do [[ "$item" == "$val" ]] && return 0; done
	return 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
	case "$1" in
	--help|-h)
		usage 0
		;;
	--os)
		OS="$2"
		shift 2
		;;
	--arch)
		ARCH="$2"
		shift 2
		;;
	--ver)
		VER="$2"
		shift 2
		;;
	--sync)
		shift
		while [[ $# -gt 0 && ! "$1" =~ ^-- ]]; do
			SYNC_ITEMS+=("$1")
			shift
		done
		;;
	--dry-run)
		DRY_RUN=true
		shift
		;;
	--debug)
		DEBUG=true
		shift
		;;
	*)
		echo "Unknown option: $1"
		usage
		;;
	esac
done

# Validate --os, if given
if [[ -n "$OS" ]] && ! contains "$OS" "${VALID_OS[@]}"; then
	echo "Invalid OS: $OS"
	usage
fi

# Was --ver explicitly requested? Captured now, before VER_LIST/the version
# loop reuse "$VER" as a loop variable.
if [[ -n "$VER" ]]; then
	VER_EXPLICIT=true
else
	VER_EXPLICIT=false
fi

# Determine which OS(es) to process. If --os wasn't given, process all of
# them; a --ver/--arch that doesn't apply to a particular OS then just
# skips that OS rather than erroring out (see STRICT_OS below).
declare -a OS_LIST
if [[ -n "$OS" ]]; then
	OS_LIST=("$OS")
	STRICT_OS=true
else
	OS_LIST=("${VALID_OS[@]}")
	STRICT_OS=false
	echo "No OS specified, will sync all supported operating systems: ${OS_LIST[*]}"
fi

# Process SYNC_ITEMS to determine what to sync. This is OS-independent:
# the only OS-specific part is which defaults apply when --sync is omitted,
# which is resolved per-OS inside process_os().
SYNC_COMMON=0
SYNC_EXTRAS=0
SYNC_TESTING=0
SYNC_NONFREE=0
SYNC_PG_VERSIONS=()
HAVE_SYNC_ITEMS=false

if [[ ${#SYNC_ITEMS[@]} -gt 0 ]]; then
	HAVE_SYNC_ITEMS=true
	for item in "${SYNC_ITEMS[@]}"; do
		case "$item" in
		common)
			SYNC_COMMON=1
			;;
		extras)
			SYNC_EXTRAS=1
			;;
		testing)
			SYNC_TESTING=1
			;;
		non-free)
			SYNC_NONFREE=1
			;;
		18|17|16|15|14|13|12|11|10)
			SYNC_PG_VERSIONS+=("$item")
			;;
		*)
			echo "Invalid sync item: $item"
			echo "Valid items: common, extras, testing, non-free, or PG version (18, 17, 16, 15, 14, etc.)"
			exit 1
			;;
		esac
	done
fi

# Process a single OS: resolves its version/arch/feature-flag settings,
# then runs the sync loop for it. Skips the OS (in non-strict/--os-omitted
# mode) if the requested --ver or --arch doesn't apply to it.
process_os() {
	local OS="$1"

	# Determine OS-specific settings
	local -n ver_ref="VALID_VER_${OS}"
	local -a VALID_VER=("${ver_ref[@]}")

	local -n nonfree_ver_ref="VALID_NONFREE_VER_${OS}"
	local -a VALID_NONFREE_VER=("${nonfree_ver_ref[@]}")
	local -n nonfree_arch_ref="VALID_NONFREE_ARCH_${OS}"
	local -a VALID_NONFREE_ARCH=("${nonfree_arch_ref[@]}")

	local osname_var="OSNAME_${OS}"
	local osname="${!osname_var}"
	local osdistro_var="OSDISTRO_${OS}"
	local osdistro="${!osdistro_var}"
	local extras_var="EXTRASREPOSENABLED_${OS}"
	local EXTRASREPOSENABLED="${!extras_var}"
	local testing_var="SYNCTESTINGREPOS_${OS}"
	local SYNCTESTINGREPOS="${!testing_var}"
	local nonfree_var="SYNCNONFREEREPOS_${OS}"
	local SYNCNONFREEREPOS="${!nonfree_var}"

	# Populate VER_LIST based on --ver parameter
	local -a VER_LIST
	if [[ -z "$VER" ]]; then
		VER_LIST=("${VALID_VER[@]}")
		echo "No version specified, will sync all versions for $OS: ${VER_LIST[*]}"
	else
		if ! contains "$VER" "${VALID_VER[@]}"; then
			if $STRICT_OS; then
				echo "Invalid version '$VER' for OS '$OS'"
				echo "Valid versions: ${VALID_VER[*]}"
				exit 1
			else
				$DEBUG && echo "[DEBUG] Version $VER not valid for $OS, skipping $OS"
				return 0
			fi
		fi
		VER_LIST=("$VER")
	fi

	# Resolve which repo types to sync for this OS (architecture-independent)
	local os_sync_common os_sync_extras os_sync_testing os_sync_nonfree
	local -a os_sync_pg_versions
	if $HAVE_SYNC_ITEMS; then
		os_sync_common=$SYNC_COMMON
		os_sync_extras=$SYNC_EXTRAS
		os_sync_testing=$SYNC_TESTING
		os_sync_nonfree=$SYNC_NONFREE
		os_sync_pg_versions=("${SYNC_PG_VERSIONS[@]}")
	else
		os_sync_common=1
		os_sync_extras=$EXTRASREPOSENABLED
		os_sync_testing=$SYNCTESTINGREPOS
		os_sync_nonfree=$SYNCNONFREEREPOS
		os_sync_pg_versions=("${PG_ALL_VERSIONS[@]}")
	fi

	echo "Starting sync operation for $OS"
	echo "Versions to sync: ${VER_LIST[*]}"

	# Loop through each version
	for VER in "${VER_LIST[@]}"; do
		# Resolve the architectures valid for this specific OS+version pair
		# (not every version supports every arch in VALID_ARCH_<os> — see
		# VALID_ARCH_OVERRIDES in sync_pgdg_rpms_config.sh)
		local -a ver_valid_arch
		get_valid_arch_for "$OS" "$VER" ver_valid_arch

		local -a ARCH_LIST
		if [[ -z "$ARCH" ]]; then
			ARCH_LIST=("${ver_valid_arch[@]}")
			echo "No architecture specified, will sync all architectures for $OS $VER: ${ARCH_LIST[*]}"
		else
			if ! contains "$ARCH" "${ver_valid_arch[@]}"; then
				if $STRICT_OS && $VER_EXPLICIT; then
					echo "Invalid arch '$ARCH' for $OS $VER"
					echo "Valid architectures for $OS $VER: ${ver_valid_arch[*]}"
					exit 1
				else
					$DEBUG && echo "[DEBUG] Arch $ARCH not valid for $OS $VER, skipping $OS $VER"
					continue
				fi
			fi
			ARCH_LIST=("$ARCH")
		fi

		# Debug output
		if $DEBUG; then
			echo "[DEBUG] OS:   $OS"
			echo "[DEBUG] VER:  $VER"
			echo "[DEBUG] ARCH: $ARCH"
			echo "[DEBUG] ARCH_LIST: ${ARCH_LIST[*]}"
			echo "[DEBUG] osname: $osname"
			echo "[DEBUG] osdistro: $osdistro"
			echo "[DEBUG] EXTRASREPOSENABLED: $EXTRASREPOSENABLED"
			echo "[DEBUG] SYNCTESTINGREPOS: $SYNCTESTINGREPOS"
			echo "[DEBUG] SYNC_COMMON: $os_sync_common"
			echo "[DEBUG] SYNC_EXTRAS: $os_sync_extras"
			echo "[DEBUG] SYNC_TESTING: $os_sync_testing"
			echo "[DEBUG] SYNC_NONFREE: $os_sync_nonfree"
			echo "[DEBUG] SYNC_PG_VERSIONS: ${os_sync_pg_versions[*]}"
			echo "[DEBUG] Dry run:    $DRY_RUN"
		fi

		# Dry-run mode
		if $DRY_RUN; then
			echo "[DRY-RUN] Would sync $OS $VER"
			echo "[DRY-RUN] Architectures: ${ARCH_LIST[*]}"
			echo "[DRY-RUN] SYNC_COMMON: $os_sync_common"
			echo "[DRY-RUN] SYNC_EXTRAS: $os_sync_extras"
			echo "[DRY-RUN] SYNC_TESTING: $os_sync_testing"
			echo "[DRY-RUN] SYNC_NONFREE: $os_sync_nonfree"
			echo "[DRY-RUN] SYNC_PG_VERSIONS: ${os_sync_pg_versions[*]}"
			continue
		fi

		echo ""
		echo "================================================"
		echo "Processing version: $OS $VER"
		echo "================================================"

		# Loop through each architecture
		for osarch in "${ARCH_LIST[@]}"; do
			echo ""
			echo "  =============================================="
			echo "  Processing architecture: $osarch"
			echo "  =============================================="

			# Determine source host based on OS and arch
			if [[ "$OS" == "redhat" ]]; then
				SOURCE_HOST="pgrpms-el${VER}-${osarch}.postgresql.org"
			elif [[ "$OS" == "fedora" ]]; then
				SOURCE_HOST="pgrpms-fedora${VER}-${osarch}.postgresql.org"
			elif [[ "$OS" == "sles" ]]; then
				SOURCE_HOST="pgrpms-sles${VER}-${osarch}.postgresql.org"
			elif [[ "$OS" == "opensuse" ]]; then
				SOURCE_HOST="pgrpms-opensuse${VER}-${osarch}.postgresql.org"
			elif [[ "$OS" == "amzn" ]]; then
				SOURCE_HOST="pgrpms-amzn${VER}-${osarch}.postgresql.org"
			else
				echo "Unsupported OS: $OS"
				exit 1
			fi

			distrover=$VER
			tmp_var="BASE_DIR_${OS}"
			BASE_DIR_OS="${!tmp_var}"
			sleep 1

			echo "  Syncing : $osname-$distrover ($osarch)"

			# Sync non-common repo (specific PG versions)
			if [[ ${#os_sync_pg_versions[@]} -gt 0 ]]; then
				for pgrelease in "${os_sync_pg_versions[@]}"; do
					echo "  Syncing : $osname-$distrover-PG$pgrelease"

					RPM_DIR=/var/lib/pgsql/rpm$pgrelease/ALLRPMS

					if ! rsync -ave ssh --delete --delete-missing-args "$SOURCE_HOST":$RPM_DIR/ $BASE_DIR_OS/$pgrelease/$osdistro/$osname-$distrover-$osarch; then
						echo "  [ERROR] Rsync failed for PG $pgrelease ($osname-$distrover-$osarch)" >&2
						sync_had_errors=1
					fi
				done
			fi

			# Sync common repo
			if [[ "$os_sync_common" -eq 1 ]]; then
				echo "  Syncing : $osname-$distrover-common repo"
				COMMON_RPM_DIR=/var/lib/pgsql/rpmcommon/ALLRPMS

				if ! rsync -ave ssh --delete --delete-missing-args "$SOURCE_HOST":$COMMON_RPM_DIR/ $BASE_DIR_OS/common/$osdistro/$osname-$distrover-$osarch; then
					echo "  [ERROR] Rsync failed for common repo ($osname-$distrover-$osarch)" >&2
					sync_had_errors=1
				fi
			fi

			# Sync extras repo
			if [[ "$os_sync_extras" -eq 1 ]]; then
				echo "  Syncing : $osname-$distrover-extras repo"
				EXTRAS_RPM_DIR=/var/lib/pgsql/pgdg.extras/ALLRPMS

				if ! rsync -ave ssh --delete --delete-missing-args "$SOURCE_HOST":$EXTRAS_RPM_DIR/ $BASE_DIR_OS/extras/$osdistro/$osname-$distrover-$osarch; then
					echo "  [ERROR] Rsync failed for Extras repo ($osname-$distrover-$osarch)" >&2
					sync_had_errors=1
				fi
			fi

			# Sync testing repos
			if [[ "$os_sync_testing" -eq 1 ]]; then
				echo "  Syncing : $osname-$distrover-common testing repo"
				COMMONTESTING_RPM_DIR=/var/lib/pgsql/rpmcommontesting/ALLRPMS

				if ! rsync -ave ssh --delete --delete-missing-args "$SOURCE_HOST":$COMMONTESTING_RPM_DIR/ $BASE_DIR_OS/testing/common/$osdistro/$osname-$distrover-$osarch; then
					echo "  [ERROR] Rsync failed for commontesting repo ($osname-$distrover-$osarch)" >&2
					sync_had_errors=1
				fi

				# Sync extras testing repo
				if [[ "$EXTRASREPOSENABLED" -eq 1 ]]; then
					echo "  Syncing : $osname-$distrover-extras testing repo"
					EXTRASTESTING_RPM_DIR=/var/lib/pgsql/pgdg.extrastesting/ALLRPMS

					if ! rsync -ave ssh --delete --delete-missing-args "$SOURCE_HOST":$EXTRASTESTING_RPM_DIR/ $BASE_DIR_OS/testing/extras/$osdistro/$osname-$distrover-$osarch; then
						echo "  [ERROR] Rsync failed for extras testing repo ($osname-$distrover-$osarch)" >&2
						sync_had_errors=1
					fi
				fi

				# Sync testing repos for specific PG versions
				for pgtestrelease in "${PG_TEST_VERSIONS[@]}"; do
					echo "  Syncing : $osname-$distrover-PG$pgtestrelease testing repo"
					testdir="rpm${pgtestrelease}testing"
					TESTING_RPM_DIR=/var/lib/pgsql/$testdir/ALLRPMS

					if ! rsync -ave ssh --delete --delete-missing-args "$SOURCE_HOST":$TESTING_RPM_DIR/ $BASE_DIR_OS/testing/$pgtestrelease/$osdistro/$osname-$distrover-$osarch; then
						echo "  [ERROR] Rsync failed for PG $pgtestrelease testing repo ($osname-$distrover-$osarch)" >&2
						sync_had_errors=1
					fi
				done
			fi

			# Sync non-free repos (only where a non-free repo actually
			# exists for this OS/version/arch combination)
			if [[ "$os_sync_nonfree" -eq 1 ]]; then
				if ! contains "$VER" "${VALID_NONFREE_VER[@]}"; then
					$DEBUG && echo "  [DEBUG] Non-free repo not available for $OS $VER, skipping"
				elif ! contains "$osarch" "${VALID_NONFREE_ARCH[@]}"; then
					$DEBUG && echo "  [DEBUG] Non-free repo not available for $OS $VER ($osarch), skipping"
				else
					# Determine non-free source host based on OS and arch
					if [[ "$OS" == "redhat" ]]; then
						NONFREE_SOURCE_HOST="pgrpms-non-free-el${VER}-${osarch}.postgresql.org"
					elif [[ "$OS" == "fedora" ]]; then
						NONFREE_SOURCE_HOST="pgrpms-non-free-fedora${VER}-${osarch}.postgresql.org"
					elif [[ "$OS" == "sles" ]]; then
						NONFREE_SOURCE_HOST="pgrpms-non-free-sles${VER}-${osarch}.postgresql.org"
					elif [[ "$OS" == "opensuse" ]]; then
						NONFREE_SOURCE_HOST="pgrpms-non-free-opensuse${VER}-${osarch}.postgresql.org"
					elif [[ "$OS" == "amzn" ]]; then
						NONFREE_SOURCE_HOST="pgrpms-non-free-amzn${VER}-${osarch}.postgresql.org"
					fi

					for pgnonfreerelease in "${PG_ALL_VERSIONS[@]}"; do
						echo "  Syncing : $osname-$distrover-PG$pgnonfreerelease non-free repo"
						NONFREE_RPM_DIR=/var/lib/pgsql/rpm${pgnonfreerelease}/ALLRPMS

						if ! rsync -ave ssh --delete --delete-missing-args "$NONFREE_SOURCE_HOST":$NONFREE_RPM_DIR/ $BASE_DIR_OS/non-free/$pgnonfreerelease/$osdistro/$osname-$distrover-$osarch; then
							echo "  [ERROR] Rsync failed for PG $pgnonfreerelease non-free repo ($osname-$distrover-$osarch)" >&2
							sync_had_errors=1
						fi
					done
				fi
			fi
		done  # End of ARCH_LIST loop
	done  # End of VER_LIST loop
}

for OS in "${OS_LIST[@]}"; do
	process_os "$OS"
done

# Finally tell us if there is an error in at least one of the steps above:

if [[ "$sync_had_errors" -eq 1 ]]; then
	echo "[WARN] One or more sync operations failed."
	exit 1
else
	echo "All syncs completed successfully."
	exit 0
fi
