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
ARCH_LIST=()				# List of architectures to sync (populated based on --arch or all for OS)
DRY_RUN=false
DEBUG=false
SYNC_ITEMS=()				# Items to sync (common, extras, testing, non-free, or PG versions)
SYNC_PG_VERSIONS=()			# PG versions to sync based on --sync option

# Help
usage() {
	cat <<EOF
Usage: $0 --os <os> --ver <version> [options]

Required:
  --os           Operating system: ${VALID_OS[*]}

Optional:
  --ver          OS version: redhat (${VALID_VER_redhat[*]}), fedora (${VALID_VER_fedora[*]}), sles (${VALID_VER_sles[*]}), opensuse (${VALID_VER_opensuse[*]})
                 If not specified, syncs all versions for the OS

Optional:
  --arch         Architecture: aarch64, ppc64le, x86_64
                 If not specified, syncs all supported architectures for the OS
  --sync         Sync specific items: common, extras, testing, non-free, or PG version (e.g. 18)
                 Can specify multiple items (e.g. --sync common 18 17)
                 If not specified, syncs all available repos
  --dry-run      Simulate the sync without transferring files
  --debug        Show detailed debug output

Examples:
  $0 --os redhat --ver 9.7 --sync common
  $0 --os sles --ver 15.6 --arch x86_64 --sync 18 17
  $0 --os fedora --ver 43 --sync common extras testing

EOF
	exit 1
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

# Determine OS-specific settings
case "$OS" in
redhat)
	VALID_ARCH=("${VALID_ARCH_redhat[@]}")
	VALID_VER=("${VALID_VER_redhat[@]}")
	osname="${OSNAME_redhat}"
	osdistro="${OSDISTRO_redhat}"
	EXTRASREPOSENABLED=${EXTRASREPOSENABLED_redhat}
	SYNCTESTINGREPOS=${SYNCTESTINGREPOS_redhat}
	SYNCNONFREEREPOS=${SYNCNONFREEREPOS_redhat}
	;;
fedora)
	VALID_ARCH=("${VALID_ARCH_fedora[@]}")
	VALID_VER=("${VALID_VER_fedora[@]}")
	osname="${OSNAME_fedora}"
	osdistro="${OSDISTRO_fedora}"
	EXTRASREPOSENABLED=${EXTRASREPOSENABLED_fedora}
	SYNCTESTINGREPOS=${SYNCTESTINGREPOS_fedora}
	SYNCNONFREEREPOS=${SYNCNONFREEREPOS_fedora}
	;;
sles)
	VALID_ARCH=("${VALID_ARCH_sles[@]}")
	VALID_VER=("${VALID_VER_sles[@]}")
	osname="${OSNAME_sles}"
	osdistro="${OSDISTRO_sles}"
	EXTRASREPOSENABLED=${EXTRASREPOSENABLED_sles}
	SYNCTESTINGREPOS=${SYNCTESTINGREPOS_sles}
	SYNCNONFREEREPOS=${SYNCNONFREEREPOS_sles}
	;;
opensuse)
	VALID_ARCH=("${VALID_ARCH_opensuse[@]}")
	VALID_VER=("${VALID_VER_opensuse[@]}")
	osname="${OSNAME_opensuse}"
	osdistro="${OSDISTRO_opensuse}"
	EXTRASREPOSENABLED=${EXTRASREPOSENABLED_opensuse}
	SYNCTESTINGREPOS=${SYNCTESTINGREPOS_opensuse}
	SYNCNONFREEREPOS=${SYNCNONFREEREPOS_opensuse}
	;;
*)
	echo "Unsupported OS: $OS"
	usage
	;;
esac

# Validation
[[ -z "$OS" ]] && usage

if ! contains "$OS" "${VALID_OS[@]}"; then
	echo "Invalid OS: $OS"
	usage
fi

# Populate VER_LIST based on --ver parameter
declare -a VER_LIST
if [[ -z "$VER" ]]; then
	# If no version specified, sync all versions for this OS
	VER_LIST=("${VALID_VER[@]}")
	echo "No version specified, will sync all versions for $OS: ${VER_LIST[*]}"
else
	# Validate the specified version
	if ! contains "$VER" "${VALID_VER[@]}"; then
		echo "Invalid version '$VER' for OS '$OS'"
		echo "Valid versions: ${VALID_VER[*]}"
		exit 1
	fi
	VER_LIST=("$VER")
fi

# Populate ARCH_LIST based on --arch parameter
if [[ -z "$ARCH" ]]; then
	# If no arch specified, sync all architectures for this OS
	ARCH_LIST=("${VALID_ARCH[@]}")
	echo "No architecture specified, will sync all architectures for $OS: ${ARCH_LIST[*]}"
else
	# Validate the specified architecture
	if ! contains "$ARCH" "${VALID_ARCH[@]}"; then
		echo "Invalid arch: $ARCH"
		usage
	fi
	ARCH_LIST=("$ARCH")
fi

# Process SYNC_ITEMS to determine what to sync
SYNC_COMMON=0
SYNC_EXTRAS=0
SYNC_TESTING=0
SYNC_NONFREE=0

if [[ ${#SYNC_ITEMS[@]} -eq 0 ]]; then
	# If no --sync specified, sync everything available
	SYNC_COMMON=1
	SYNC_EXTRAS=$EXTRASREPOSENABLED
	SYNC_TESTING=$SYNCTESTINGREPOS
	SYNC_NONFREE=$SYNCNONFREEREPOS
	SYNC_PG_VERSIONS=("${PG_ALL_VERSIONS[@]}")
else
	# Parse SYNC_ITEMS
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

# Debug output
if $DEBUG; then
	echo "[DEBUG] OS:   $OS"
	echo "[DEBUG] ARCH: $ARCH"
	echo "[DEBUG] ARCH_LIST: ${ARCH_LIST[*]}"
	echo "[DEBUG] VER:  $VER"
	echo "[DEBUG] VER_LIST: ${VER_LIST[*]}"
	echo "[DEBUG] osname: $osname"
	echo "[DEBUG] osdistro: $osdistro"
	echo "[DEBUG] EXTRASREPOSENABLED: $EXTRASREPOSENABLED"
	echo "[DEBUG] SYNCTESTINGREPOS: $SYNCTESTINGREPOS"
	echo "[DEBUG] SYNC_COMMON: $SYNC_COMMON"
	echo "[DEBUG] SYNC_EXTRAS: $SYNC_EXTRAS"
	echo "[DEBUG] SYNC_TESTING: $SYNC_TESTING"
	echo "[DEBUG] SYNC_NONFREE: $SYNC_NONFREE"
	echo "[DEBUG] SYNC_PG_VERSIONS: ${SYNC_PG_VERSIONS[*]}"
	echo "[DEBUG] Dry run:    $DRY_RUN"
fi

# Dry-run mode
if $DRY_RUN; then
	echo "[DRY-RUN] Would sync $OS versions: ${VER_LIST[*]}"
	echo "[DRY-RUN] Architectures: ${ARCH_LIST[*]}"
	echo "[DRY-RUN] SYNC_COMMON: $SYNC_COMMON"
	echo "[DRY-RUN] SYNC_EXTRAS: $SYNC_EXTRAS"
	echo "[DRY-RUN] SYNC_TESTING: $SYNC_TESTING"
	echo "[DRY-RUN] SYNC_NONFREE: $SYNC_NONFREE"
	echo "[DRY-RUN] SYNC_PG_VERSIONS: ${SYNC_PG_VERSIONS[*]}"
	exit 0
fi

# Run the sync command. This is the main loop.
echo "Starting sync operation for $OS"
echo "Versions to sync: ${VER_LIST[*]}"
echo "Architectures to sync: ${ARCH_LIST[*]}"

# Loop through each version
for VER in "${VER_LIST[@]}"; do
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
		if [[ ${#SYNC_PG_VERSIONS[@]} -gt 0 ]]; then
			for pgrelease in "${SYNC_PG_VERSIONS[@]}"; do
				echo "  Syncing : $osname-$distrover-PG$pgrelease"

				RPM_DIR=/var/lib/pgsql/rpm$pgrelease/ALLRPMS

				if ! rsync -ave ssh --delete --delete-missing-args "$SOURCE_HOST":$RPM_DIR/ $BASE_DIR_OS/$pgrelease/$osdistro/$osname-$distrover-$osarch; then
					echo "  [ERROR] Rsync failed for PG $pgrelease ($osname-$distrover-$osarch)" >&2
					sync_had_errors=1
				fi
			done
		fi

		# Sync common repo
		if [[ "$SYNC_COMMON" -eq 1 ]]; then
			echo "  Syncing : $osname-$distrover-common repo"
			COMMON_RPM_DIR=/var/lib/pgsql/rpmcommon/ALLRPMS

			if ! rsync -ave ssh --delete --delete-missing-args "$SOURCE_HOST":$COMMON_RPM_DIR/ $BASE_DIR_OS/common/$osdistro/$osname-$distrover-$osarch; then
				echo "  [ERROR] Rsync failed for common repo ($osname-$distrover-$osarch)" >&2
				sync_had_errors=1
			fi
		fi

		# Sync extras repo
		if [[ "$SYNC_EXTRAS" -eq 1 ]]; then
			echo "  Syncing : $osname-$distrover-extras repo"
			EXTRAS_RPM_DIR=/var/lib/pgsql/pgdg.extras/ALLRPMS

			if ! rsync -ave ssh --delete --delete-missing-args "$SOURCE_HOST":$EXTRAS_RPM_DIR/ $BASE_DIR_OS/extras/$osdistro/$osname-$distrover-$osarch; then
				echo "  [ERROR] Rsync failed for Extras repo ($osname-$distrover-$osarch)" >&2
				sync_had_errors=1
			fi
		fi

		# Sync testing repos
		if [[ "$SYNC_TESTING" -eq 1 ]]; then
			echo "  Syncing : $osname-$distrover-common testing repo"
			COMMONTESTING_RPM_DIR=/var/lib/pgsql/rpmcommontesting/ALLRPMS

			if ! rsync -ave ssh --delete --delete-missing-args "$SOURCE_HOST":$COMMONTESTING_RPM_DIR/ $BASE_DIR_OS/testing/common/$osdistro/$osname-$distrover-$osarch; then
				echo "  [ERROR] Rsync failed for commontesting repo ($osname-$distrover-$osarch)" >&2
				sync_had_errors=1
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

		# Sync non-free repos
		if [[ "$SYNC_NONFREE" -eq 1 ]]; then
			# Determine non-free source host based on OS and arch
			if [[ "$OS" == "redhat" ]]; then
				NONFREE_SOURCE_HOST="pgrpms-non-free-el${VER}-${osarch}.postgresql.org"
			elif [[ "$OS" == "fedora" ]]; then
				NONFREE_SOURCE_HOST="pgrpms-non-free-fedora${VER}-${osarch}.postgresql.org"
			elif [[ "$OS" == "sles" ]]; then
				NONFREE_SOURCE_HOST="pgrpms-non-free-sles${VER}-${osarch}.postgresql.org"
			elif [[ "$OS" == "opensuse" ]]; then
				NONFREE_SOURCE_HOST="pgrpms-non-free-opensuse${VER}-${osarch}.postgresql.org"
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
	done  # End of ARCH_LIST loop
done  # End of VER_LIST loop

# Finally tell us if there is an error in at least one of the steps above:

if [[ "$sync_had_errors" -eq 1 ]]; then
	echo "[WARN] One or more sync operations failed."
	exit 1
else
	echo "All syncs completed successfully."
	exit 0
fi
