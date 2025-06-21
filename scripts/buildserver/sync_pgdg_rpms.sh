#!/usr/bin/bash

set -euo pipefail

sync_had_errors=0

# Defaults
OS=""
ARCH=""
VER=""
DRY_RUN=false
DEBUG=false
BASE_DIR="/srv/yum/yum"
PG_VERSIONS=()
PG_TEST_VERSIONS=(18 17 16 15 14 13)
EXTRASREPOSENABLED=0
SYSUPDATESREPOSENABLED=0
SYNCTESTINGREPOS=0

# Valid values
VALID_OS=("redhat" "fedora")
VALID_ARCH_redhat=("aarch64" "ppc64le" "x86_64")
VALID_ARCH_fedora=("x86_64")
VALID_VER_redhat=("10" "9" "8")
VALID_VER_fedora=("42" "41")

# Help
usage() {
	cat <<EOF
Usage: $0 --os <os> --arch <arch> --ver <version> [options]

Required:
  --os           Operating system: redhat or fedora
  --arch         Architecture: aarch64, ppc64le, x86_64
  --ver          OS version: redhat (10,9,8,7), fedora (42,41)

Optional:
  --pg-versions  List of PostgreSQL versions to sync (e.g. 13 14 15)
  --base-dir     Base destination directory (default: /srv/yum/yum)
  --dry-run      Simulate the sync without transferring files
  --debug        Show detailed debug output

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
# Parse args
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
	--base-dir)
		BASE_DIR="$2"
		shift 2
		;;
	--pg-versions)
		shift
		while [[ $# -gt 0 && ! "$1" =~ ^-- ]]; do
			PG_VERSIONS+=("$1")
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

if [[ "$OS" == "redhat" ]]; then
	if [[ "$VER" -eq "8" ]]; then
		ossysupdates="centos8"
	elif [[ "$VER" -eq "9" ]]; then
		ossysupdates="rocky9"
	elif [[ "$VER" -eq "10" ]]; then
		ossysupdates="rhel10"
	else
		:
	fi
fi

# Determine OS-specific prefix and extras repo availability
case "$OS" in
redhat)
	VALID_ARCH=("${VALID_ARCH_redhat[@]}")
	VALID_VER=("${VALID_VER_redhat[@]}")
	osname="rhel"
	osdistro="redhat"
	EXTRASREPOSENABLED=1
	SYSUPDATESREPOSENABLED=1
	SYNCTESTINGREPOS=1
	;;
fedora)
	VALID_ARCH=("${VALID_ARCH_fedora[@]}")
	VALID_VER=("${VALID_VER_fedora[@]}")
	osname="fedora"
	osdistro="fedora"
	EXTRASREPOSENABLED=0
	SYSUPDATESREPOSENABLED=0
	SYNCTESTINGREPOS=1
	;;
*)
	echo "Unsupported OS: $OS"
	usage
	;;
esac

# Validation
[[ -z "$OS" || -z "$ARCH" || -z "$VER" ]] && usage

if ! contains "$OS" "${VALID_OS[@]}"; then
	echo "Invalid OS: $OS"
	usage
fi

if ! contains "$ARCH" "${VALID_ARCH[@]}"; then
	echo "Invalid arch: $ARCH"
	usage
fi

if ! contains "$VER" "${VALID_VER[@]}"; then
	echo "Invalid version '$VER' for OS '$OS'"
	echo "Valid versions: ${VALID_VER[*]}"
	exit 1
fi

if [[ "$OS" == "redhat" && ! " ${VALID_VER[*]} " =~ " $VER " ]]; then
	echo "Invalid version: $VER for redhat"
	usage
elif [[ "$OS" == "fedora" && ! " ${VALID_VER[*]} " =~ " $VER " ]]; then
	echo "Invalid version: $VER for fedora"
	usage
fi

# Validate arch and ver
if ! contains "$ARCH" "${VALID_ARCH[@]}"; then
	echo "Invalid architecture '$ARCH' for OS '$OS'"
	echo "Valid: ${VALID_ARCH[*]}"
	exit 1
fi

if ! contains "$VER" "${VALID_VER[@]}"; then
	echo "Invalid version '$VER' for OS '$OS'"
	echo "Valid: ${VALID_VER[*]}"
	exit 1
fi

# Debug output
if $DEBUG; then
	echo "[DEBUG] OS:   $OS"
	echo "[DEBUG] ARCH: $ARCH"
	echo "[DEBUG] VER:  $VER"
	echo "[DEBUG] osname: $osname"
	echo "[DEBUG] osdistro: $osdistro"
	echo "[DEBUG] EXTRASREPOSENABLED: $EXTRASREPOSENABLED"
	echo "[DEBUG] SYSUPDATESREPOENABLED: $SYSUPDATESREPOENABLED"
	echo "[DEBUG] Dry run:    $DRY_RUN"
fi

# Determine source host based on OS
if [[ "$OS" == "redhat" ]]; then
	SOURCE_HOST="pgrpms-el${VER}-${ARCH}.postgresql.org"
elif [[ "$OS" == "fedora" ]]; then
	SOURCE_HOST="pgrpms-fedora${VER}-${ARCH}.postgresql.org"
else
	echo "Unsupported OS: $OS"
	exit 1
fi

# Dry-run mode
if $DRY_RUN; then
	echo "[DRY-RUN] Would sync $OS $VER $ARCH"
	exit 0
fi

# Run the sync command. This is the main loop.
echo "Starting sync operation for $OS $VER $ARCH"

osdistro=$OS
osarch=$ARCH
distrover=$VER
sleep 1
echo "Syncing : $osname-$distrover"

# Sync non-common repo
for pgrelease in 13 14 15 16 17; do
	echo "Syncing : $osname-$distrover-PG$pgrelease"

	RPM_DIR=/var/lib/pgsql/rpm$pgrelease/ALLRPMS

	if ! rsync -ave ssh --delete --delete-missing-args "$SOURCE_HOST":$RPM_DIR/ /srv/yum/yum/$pgrelease/$osdistro/$osname-$distrover-$osarch; then
		echo "[ERROR] Rsync failed for PG $pgrelease ($osname-$distrover-$osarch)" >&2
		sync_had_errors=1
	fi

done
# Sync common repo

echo "Syncing : $osname-$distrover-common repo"
COMMON_RPM_DIR=/var/lib/pgsql/rpmcommon/ALLRPMS

if ! rsync -ave ssh --delete --delete-missing-args "$SOURCE_HOST":$COMMON_RPM_DIR/ /srv/yum/yum/common/$osdistro/$osname-$distrover-$osarch; then
	echo "[ERROR] Rsync failed for common repo ($osname-$distrover-$osarch)" >&2
	sync_had_errors=1
fi

if [[ "$EXTRASREPOSENABLED" -eq 1 ]]; then
	# Sync extras repo
	echo "Syncing : $osname-$distrover-extras repo"
	EXTRAS_RPM_DIR=/var/lib/pgsql/pgdg.rhel$distrover.extras/ALLRPMS

	if ! rsync -ave ssh --delete --delete-missing-args "$SOURCE_HOST":$EXTRAS_RPM_DIR/ /srv/yum/yum/common/pgdg-rhel$distrover-extras/$osdistro/$osname-$distrover-$osarch; then
		echo "[ERROR] Rsync failed for Extras repo ($osname-$distrover-$osarch)" >&2
		sync_had_errors=1
	fi
fi

if [[ "$SYSUPDATESREPOSENABLED" -eq 1 ]]; then
	# Sync sysupdates repo
	echo "Syncing : $osname-$distrover-sysupdates repo"

	export BASE_DIR=/var/lib/pgsql/$ossysupdates-sysupdates
	export SYSUPDATES_RPM_DIR=$BASE_DIR/ALLRPMS

	if ! rsync -ave ssh --delete --delete-missing-args "$SOURCE_HOST":$SYSUPDATES_RPM_DIR/ /srv/yum/yum/common/pgdg-$ossysupdates-sysupdates/$osdistro/$osname-$distrover-$osarch; then
		echo "[ERROR] Rsync failed for sysupdates repo ($osname-$distrover-$osarch)" >&2
		sync_had_errors=1
	fi
fi

if [[ "$SYNCTESTINGREPOS" -eq 1 ]]; then
	# Sync testing repos

	echo "Syncing : $osname-$distrover-common testing repo"
	COMMONTESTING_RPM_DIR=/var/lib/pgsql/rpmcommontesting/ALLRPMS

	if ! rsync -ave ssh --delete --delete-missing-args "$SOURCE_HOST":$COMMONTESTING_RPM_DIR/ /srv/yum/yum/testing/common/$osdistro/$osname-$distrover-$osarch; then
		echo "[ERROR] Rsync failed for commontesting repo ($osname-$distrover-$osarch)" >&2
		sync_had_errors=1
	fi

	# Sync testing repos
	for pgtestrelease in "${PG_TEST_VERSIONS[@]}"; do
		echo "Syncing : $osname-$distrover-PG$pgtestrelease testing repo"
		testdir="rpm${pgtestrelease}testing"
		TESTING_RPM_DIR=/var/lib/pgsql/$testdir/ALLRPMS

		if ! rsync -ave ssh --delete --delete-missing-args "$SOURCE_HOST":$TESTING_RPM_DIR/ /srv/yum/yum/testing/$pgtestrelease/$osdistro/$osname-$distrover-$osarch; then
			echo "[ERROR] Rsync failed for PG $pgrelease testing repo ($osname-$distrover-$osarch)" >&2
			sync_had_errors=1
		fi
	done
fi

# Finally tell us if there is an error in at least one of the steps above:

if [[ "$sync_had_errors" -eq 1 ]]; then
	echo "[WARN] One or more sync operations failed."
	exit 1
else
	echo "All syncs completed successfully."
	exit 0
fi
