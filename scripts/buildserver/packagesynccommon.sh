#!/usr/bin/bash

#########################################################
#							#
# Devrim Gündüz <devrim@gunduz.org> - 2024		#
#							#
#########################################################

# Include common values:
source ~/bin/global.sh

export COMMON_RPM_DIR=/var/lib/pgsql/rpmcommon/ALLRPMS
export COMMON_SRPM_DIR=/var/lib/pgsql/rpmcommon/ALLSRPMS
export COMMON_DEBUG_RPM_DIR=/var/lib/pgsql/rpmcommon/ALLDEBUGRPMS

# Create directories for binary and source RPMs. This directory will help us
# to create the repo files easily (though this can be done via ansible during initial installation:

mkdir -p $COMMON_RPM_DIR
mkdir -p $COMMON_SRPM_DIR
mkdir -p $COMMON_DEBUG_RPM_DIR

echo "${green}Syncing PostgreSQL common RPMs for $os - $osarch${reset}"

# rsync binary and source RPMs to their own directories:

rsync --checksum -av --delete --stats /var/lib/pgsql/rpmcommon/RPMS/$osarch/ /var/lib/pgsql/rpmcommon/RPMS/noarch/ $COMMON_RPM_DIR
rsync --checksum -av --delete --stats /var/lib/pgsql/rpmcommon/SRPMS/ $COMMON_SRPM_DIR

# Move debuginfo and debugsource packages to a separate directory.
# First clean the old ones, and then copy existing ones:
rm -rf $COMMON_DEBUG_RPM_DIR/*
mv $COMMON_RPM_DIR/*debuginfo* $COMMON_RPM_DIR/*debugsource* $COMMON_DEBUG_RPM_DIR/

# Now, create repo for RPMs and SRPMS:

createrepo --changelog-limit=3 --workers=4 -d --update $COMMON_RPM_DIR
createrepo --changelog-limit=3 --workers=4 -d --update $COMMON_SRPM_DIR
createrepo --changelog-limit=3 --workers=4 -d --update $COMMON_DEBUG_RPM_DIR

echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $COMMON_RPM_DIR/repodata/repomd.xml
echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $COMMON_SRPM_DIR/repodata/repomd.xml
echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $COMMON_DEBUG_RPM_DIR/repodata/repomd.xml

# We currently pull packages from yonada, so skip the next line:
# rsync --checksum -ave ssh --delete $COMMON_RPM_DIR/ yumupload@yum.postgresql.org:yum/yum/common/$osdistro/$os-$osarch

# Sync SRPMs to S3 bucket:
aws s3 sync $COMMON_SRPM_DIR s3://dnf-srpms.postgresql.org20250313103537584600000001/srpms/common/$osdistro/$os-$osarch/ --exclude "*.html" --exclude "repodata"
aws s3 sync --delete $COMMON_SRPM_DIR/repodata/ s3://dnf-srpms.postgresql.org20250313103537584600000001/srpms/common/$packageSyncVersion/$osdistro/$os-$osarch/repodata/ --exclude "*.html"
aws cloudfront create-invalidation --distribution-id $CF_SRPM_DISTRO_ID --path /srpms/common/$packageSyncVersion/$osdistro/$os-$osarch/repodata/*

# Sync debug* RPMs to S3 bucket:
aws s3 sync $COMMON_DEBUG_RPM_DIR s3://dnf-debuginfo.postgresql.org20250312201116649700000001/debug/common/$osdistro/$os-$osarch/ --exclude "*.html" --exclude "repodata"
aws s3 sync --delete $COMMON_DEBUG_RPM_DIR/repodata/ s3://dnf-debuginfo.postgresql.org20250312201116649700000001/debug/common/$packageSyncVersion/$osdistro/$os-$osarch/repodata/ --exclude "*.html"
aws cloudfront create-invalidation --distribution-id $CF_DEBUG_DISTRO_ID --path /debug/common/$packageSyncVersion/$osdistro/$os-$osarch/repodata/*

exit 0
