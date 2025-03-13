#!/usr/bin/bash

#########################################################
#							#
# Devrim Gündüz <devrim@gunduz.org> - 2024		#
#							#
#########################################################

# Include common values:
source ~/bin/global.sh

export TESTING_COMMON_RPM_DIR=/var/lib/pgsql/rpmcommontesting/ALLRPMS
export TESTING_COMMON_SRPM_DIR=/var/lib/pgsql/rpmcommontesting/ALLSRPMS
export TESTING_COMMON_DEBUG_RPM_DIR=/var/lib/pgsql/rpmcommontesting/ALLDEBUGRPMS

# Create directories for binary and source RPMs. This directory will help us
# to create the repo files easily (though this can be done via ansible during initial installation:

mkdir -p $TESTING_COMMON_RPM_DIR
mkdir -p $TESTING_COMMON_SRPM_DIR
mkdir -p $TESTING_COMMON_DEBUG_RPM_DIR

echo "${green}Syncing PostgreSQL common RPMs for $os - $osarch${reset}"

# rsync binary and source RPMs to their own directories:

rsync --checksum -av --delete --stats /var/lib/pgsql/rpmcommontesting/RPMS/$osarch/ /var/lib/pgsql/rpmcommontesting/RPMS/noarch/ $TESTING_COMMON_RPM_DIR
rsync --checksum -av --delete --stats /var/lib/pgsql/rpmcommontesting/SRPMS/ $TESTING_COMMON_SRPM_DIR

# Move debuginfo and debugsource packages to a separate directory.
# First clean the old ones, and then copy existing ones:
rm -rf $TESTING_COMMON_DEBUG_RPM_DIR/*
mv $TESTING_COMMON_RPM_DIR/*debuginfo* $TESTING_COMMON_RPM_DIR/*debugsource* $TESTING_COMMON_DEBUG_RPM_DIR/

# Now, create repo for RPMs and SRPMS:

createrepo --changelog-limit=3 --workers=4 -d --update $TESTING_COMMON_RPM_DIR
createrepo --changelog-limit=3 --workers=4 -d --update $TESTING_COMMON_SRPM_DIR
createrepo --changelog-limit=3 --workers=4 -d --update $TESTING_COMMON_DEBUG_RPM_DIR

echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $TESTING_COMMON_RPM_DIR/repodata/repomd.xml
echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $TESTING_COMMON_SRPM_DIR/repodata/repomd.xml
echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $TESTING_COMMON_DEBUG_RPM_DIR/repodata/repomd.xml

# Finally, perform the rsync:

rsync --checksum -ave ssh --delete $TESTING_COMMON_RPM_DIR/ yumupload@yum.postgresql.org:/srv/yum/yum/testing/common/$osdistro/$os-$osarch
rsync --checksum -ave ssh --delete $TESTING_COMMON_SRPM_DIR/ yumupload@yum.postgresql.org:/srv/yum/yum/srpms/testing/common/$osdistro/$os-$osarch

# Sync SRPMs to S3 bucket:
aws s3 sync $STESTING_COMMON_SRPM_DIR s3://dnf-srpms.postgresql.org20250313103537584600000001/srpms/testing/$packageSyncVersion/$osdistro/$os-$osarch
aws cloudfront create-invalidation --distribution-id $S3_DISTRO_ID --path /srpms/testing/$packageSyncVersion/$osdistro/$os-$osarch/repodata/*

# Sync debug* RPMs to S3 bucket:
aws s3 sync $TESTING_COMMON_DEBUG_RPM_DIR s3://dnf-debuginfo.postgresql.org20250312201116649700000001/testing/debug/common/$osdistro/$os-$osarch/
aws cloudfront create-invalidation --distribution-id $S3_DISTRO_ID --path /testing/debug/common/$osdistro/$os-$osarch/repodata/*

exit 0
