#!/usr/bin/bash

#########################################################
#							#
# Devrim Gündüz <devrim@gunduz.org> - 2025		#
#							#
#########################################################

# Enable strict error handling
set -euo pipefail

# Logging function with timestamps
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*"
}

error() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $*" >&2
}

# Check if global.sh exists before sourcing
if [ ! -f ~/bin/global.sh ]; then
    error "global.sh not found at ~/bin/global.sh"
    exit 1
fi

# Include common values:
source ~/bin/global.sh

# Build the full OS version string used in S3/CloudFront paths.
# Fedora only has a major version (e.g. "fedora-43"), while RHEL and SLES
# also carry a minor version (e.g. "rhel-10.1"). When osminversion is set
# and non-empty we append it; otherwise we use the major version alone.
if [ -n "${osminversion}" ]; then
    export osfullversion="${os}.${osminversion}"
else
    export osfullversion="${os}"
fi

# Validate required variables from global.sh
: "${pgStableBuilds:?pgStableBuilds is not set in global.sh}"
: "${GPG_PASSWORD:?GPG_PASSWORD is not set in global.sh}"
: "${awssrpmurl:?awssrpmurl is not set in global.sh}"
: "${awsdebuginfourl:?awsdebuginfourl is not set in global.sh}"
: "${CF_SRPM_DISTRO_ID:?CF_SRPM_DISTRO_ID is not set in global.sh}"
: "${CF_DEBUG_DISTRO_ID:?CF_DEBUG_DISTRO_ID is not set in global.sh}"
: "${osarch:?osarch is not set in global.sh}"
: "${osdistro:?osdistro is not set in global.sh}"
: "${os:?os is not set in global.sh}"
: "${osminversion:?osminversion is not set in global.sh}"

# Validate AWS CLI is available and configured
if ! command -v aws &> /dev/null; then
    error "AWS CLI is not installed"
    exit 1
fi

if ! aws sts get-caller-identity &> /dev/null; then
    error "AWS credentials are not configured or invalid"
    exit 1
fi

# Validate required commands are available
for cmd in rsync createrepo gpg2; do
    if ! command -v "$cmd" &> /dev/null; then
        error "Required command '$cmd' is not installed"
        exit 1
    fi
done

log "Starting package sync process..."

# Copy all packages in rpmcommon directory to each major version first:
log "Copying packages from rpmcommon to version-specific directories..."

for packageSyncVersion in "${pgStableBuilds[@]}"
do
    # Non-free repo does not have a "common" repo, so copy all packages in
    # rpmcommon directory to each supported major PostgreSQL version:

    # Check if source directories exist
    if [ -d ~/rpmcommon/RPMS/x86_64 ]; then
        cp ~/rpmcommon/RPMS/x86_64/* ~/rpm"${packageSyncVersion}"/RPMS/x86_64/ 2>/dev/null || true
    fi

    if [ -d ~/rpmcommon/RPMS/noarch ]; then
        cp ~/rpmcommon/RPMS/noarch/* ~/rpm"${packageSyncVersion}"/RPMS/noarch/ 2>/dev/null || true
    fi
done

# All packages have been copied, so can be removed. No need to copy
# again and again:
rm -f ~/rpmcommon/RPMS/x86_64/* ~/rpmcommon/RPMS/noarch/* 2>/dev/null || true

# Figure out which major PostgreSQL version(s) will be used to sync:

if [ "$#" -eq 0 ]; then
    log "Processing all stable PostgreSQL builds: ${pgStableBuilds[*]}"
else
    if [[ " ${pgStableBuilds[*]} " =~ " $1 " ]]; then
        declare -a pgStableBuilds=("$1")
        log "Processing only PostgreSQL version: $1"
    else
        error "PostgreSQL version $1 is not supported."
        error "Supported versions: ${pgStableBuilds[*]}"
        exit 1
    fi
fi

# Start sync process:

for packageSyncVersion in "${pgStableBuilds[@]}"
do
    log "=========================================="
    log "Processing PostgreSQL ${packageSyncVersion}"
    log "=========================================="

    export BASE_DIR=/var/lib/pgsql/rpm"${packageSyncVersion}"

    export RPM_DIR="${BASE_DIR}"/ALLRPMS
    export DEBUG_RPM_DIR="${BASE_DIR}"/ALLDEBUGRPMS
    export SRPM_DIR="${BASE_DIR}"/ALLSRPMS

    # Validate BASE_DIR exists
    if [ ! -d "$BASE_DIR" ]; then
        error "Base directory does not exist: $BASE_DIR"
        continue
    fi

    # Create directories for binary and source RPMs. This directory will help us
    # to create the repo files easily:
    log "Creating directory structure..."
    mkdir -p "$RPM_DIR"
    mkdir -p "$SRPM_DIR"
    mkdir -p "$DEBUG_RPM_DIR"

    # rsync binary and source RPMs to their own directories:

    log "-------------------------------------------"
    log "Syncing PostgreSQL $packageSyncVersion RPMs"
    log "-------------------------------------------"

    # Check if source directories exist before syncing
    if [ ! -d "$BASE_DIR/RPMS/$osarch" ]; then
        error "Source directory does not exist: $BASE_DIR/RPMS/$osarch"
        continue
    fi

    if ! rsync --checksum -av --delete --stats "$BASE_DIR/RPMS/$osarch/" "$BASE_DIR/RPMS/noarch/" "$RPM_DIR"; then
        error "Failed to sync binary RPMs for PostgreSQL $packageSyncVersion"
        continue
    fi

    if ! rsync --checksum -av --delete --stats "$BASE_DIR/SRPMS/" "$SRPM_DIR"; then
        error "Failed to sync source RPMs for PostgreSQL $packageSyncVersion"
        continue
    fi

    # Move debuginfo and debugsource packages to a separate directory.
    # First clean the old ones, and then copy existing ones:
    log "Moving debug packages to separate directory..."
    rm -rf "${DEBUG_RPM_DIR:?}"/*

    # Enable nullglob to handle case where no debug packages exist
    shopt -s nullglob
    debug_files=("$RPM_DIR"/*debuginfo* "$RPM_DIR"/*debugsource*)
    if [ ${#debug_files[@]} -gt 0 ]; then
        mv "$RPM_DIR"/*debuginfo* "$RPM_DIR"/*debugsource* "$DEBUG_RPM_DIR/" 2>/dev/null || true
        log "Moved ${#debug_files[@]} debug package(s)"
    else
        log "No debug packages found"
    fi
    shopt -u nullglob

    # Now, create repo for RPMs and SRPMS:
    log "Creating repository metadata..."

    if ! createrepo --changelog-limit=3 --workers=4 -g /usr/local/etc/postgresqldbserver-"$packageSyncVersion".xml -d --update "$RPM_DIR"; then
        error "Failed to create repo for RPMs"
        continue
    fi

    if ! createrepo --changelog-limit=3 --workers=4 -g /usr/local/etc/postgresqldbserver-"$packageSyncVersion".xml -d --update "$DEBUG_RPM_DIR"; then
        error "Failed to create repo for debug RPMs"
        continue
    fi

    if ! createrepo --changelog-limit=3 --workers=4 -d --update "$SRPM_DIR"; then
        error "Failed to create repo for SRPMs"
        continue
    fi

    # Sign repository metadata
    log "Signing repository metadata..."

    if ! echo "$GPG_PASSWORD" | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 "$RPM_DIR/repodata/repomd.xml"; then
        error "Failed to sign RPM repository metadata"
        continue
    fi

    if ! echo "$GPG_PASSWORD" | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 "$DEBUG_RPM_DIR/repodata/repomd.xml"; then
        error "Failed to sign debug RPM repository metadata"
        continue
    fi

    if ! echo "$GPG_PASSWORD" | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 "$SRPM_DIR/repodata/repomd.xml"; then
        error "Failed to sign SRPM repository metadata"
        continue
    fi

    # We currently pull packages from yonada, so skip the next line:
    # rsync --checksum -ave ssh --delete "$RPM_DIR/" yumupload@yum.postgresql.org:yum/yum/non-free/"$packageSyncVersion"/"$osdistro"/"$os"."$osminversion"-"$osarch"

    # Sync SRPMs to S3 bucket:
    log "Syncing SRPMs to S3..."

    SRPM_S3_PATH="$awssrpmurl/srpms/non-free/$packageSyncVersion/$osdistro/$osfullversion-$osarch"

    if ! aws s3 sync "$SRPM_DIR" "$SRPM_S3_PATH" --exclude "*.html" --exclude "repodata"; then
        error "Failed to sync SRPMs to S3"
        continue
    fi

    if ! aws s3 sync --delete "$SRPM_DIR/repodata/" "$SRPM_S3_PATH/repodata/" --exclude "*.html"; then
        error "Failed to sync SRPM repodata to S3"
        continue
    fi

    log "Creating CloudFront invalidation for SRPMs..."
    if ! aws cloudfront create-invalidation --distribution-id "$CF_SRPM_DISTRO_ID" --paths "/srpms/non-free/$packageSyncVersion/$osdistro/$osfullversion-$osarch/repodata/*" > /dev/null; then
        error "Failed to create CloudFront invalidation for SRPMs"
        # Don't exit, this is not critical
    fi

    # S3 does not allow symlinks, so we have to sync the packages once again to the OS major version directory if this is the latest version of the OS:
    if [ "$osislatest" == 1 ]; then
        log "osislatest=1: syncing SRPMs to major-version path..."
        if ! aws s3 sync "$SRPM_DIR" "$awssrpmurl/srpms/non-free/$packageSyncVersion/$osdistro/$os-$osarch" --exclude "*.html" --exclude "repodata"; then
            error "Failed to sync SRPMs to S3 (major-version path)"
        fi
        if ! aws s3 sync --delete "$SRPM_DIR/repodata/" "$awssrpmurl/srpms/non-free/$packageSyncVersion/$osdistro/$os-$osarch/repodata/" --exclude "*.html"; then
            error "Failed to sync SRPM repodata to S3 (major-version path)"
        fi
        if ! aws cloudfront create-invalidation --distribution-id "$CF_SRPM_DISTRO_ID" --paths "/srpms/non-free/$packageSyncVersion/$osdistro/$os-$osarch/repodata/*" > /dev/null; then
            error "Failed to create CloudFront invalidation for SRPMs (major-version path)"
        fi
    fi

    # Sync debug* RPMs to S3 bucket:
    log "Syncing debug RPMs to S3..."

    DEBUG_S3_PATH="$awsdebuginfourl/debug/non-free/$packageSyncVersion/$osdistro/$osfullversion-$osarch"

    if ! aws s3 sync "$DEBUG_RPM_DIR" "$DEBUG_S3_PATH/" --exclude "*.html" --exclude "repodata"; then
        error "Failed to sync debug RPMs to S3"
        continue
    fi

    if ! aws s3 sync --delete "$DEBUG_RPM_DIR/repodata/" "$DEBUG_S3_PATH/repodata/" --exclude "*.html"; then
        error "Failed to sync debug RPM repodata to S3"
        continue
    fi

    log "Creating CloudFront invalidation for debug RPMs..."
    if ! aws cloudfront create-invalidation --distribution-id "$CF_DEBUG_DISTRO_ID" --paths "/debug/non-free/$packageSyncVersion/$osdistro/$osfullversion-$osarch/repodata/*" > /dev/null; then
        error "Failed to create CloudFront invalidation for debug RPMs"
        # Don't exit, this is not critical
    fi

    # S3 does not allow symlinks, so we have to sync the packages once again to the OS major version directory if this is the latest version of the OS:
    if [ "$osislatest" == 1 ]; then
        log "osislatest=1: syncing debug RPMs to major-version path..."
        if ! aws s3 sync "$DEBUG_RPM_DIR" "$awsdebuginfourl/debug/non-free/$packageSyncVersion/$osdistro/$os-$osarch/" --exclude "*.html" --exclude "repodata"; then
            error "Failed to sync debug RPMs to S3 (major-version path)"
        fi
        if ! aws s3 sync --delete "$DEBUG_RPM_DIR/repodata/" "$awsdebuginfourl/debug/non-free/$packageSyncVersion/$osdistro/$os-$osarch/repodata/" --exclude "*.html"; then
            error "Failed to sync debug RPM repodata to S3 (major-version path)"
        fi
        if ! aws cloudfront create-invalidation --distribution-id "$CF_DEBUG_DISTRO_ID" --paths "/debug/non-free/$packageSyncVersion/$osdistro/$os-$osarch/repodata/*" > /dev/null; then
            error "Failed to create CloudFront invalidation for debug RPMs (major-version path)"
        fi
    fi

    log "Successfully completed sync for PostgreSQL $packageSyncVersion"
done

log "=========================================="
log "Package sync completed successfully!"
log "=========================================="

exit 0
