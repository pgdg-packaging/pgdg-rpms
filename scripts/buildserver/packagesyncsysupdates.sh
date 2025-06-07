#!/usr/bin/bash

#########################################################
#							#
# Devrim Gündüz <devrim@gunduz.org> - 2024		#
#							#
#########################################################

# Include common values:
source ~/bin/global.sh

export BASE_DIR=/var/lib/pgsql/$ossysupdates-sysupdates

export SYSUPDATES_RPM_DIR=$BASE_DIR/ALLRPMS
export SYSUPDATES_SRPM_DIR=$BASE_DIR/ALLSRPMS

# Create directories for binary and source RPMs. This directory will help us
# to create the repo files easily (though this can be done via ansible during initial installation:

mkdir -p $SYSUPDATES_RPM_DIR
mkdir -p $SYSUPDATES_SRPM_DIR

echo "${green}Syncing PostgreSQL sysupdates RPMs for $os - $osarch${reset}"

# rsync binary and source RPMs to their own directories:

rsync --checksum -av --delete --stats $BASE_DIR/RPMS/$osarch/ $BASE_DIR/RPMS/noarch/ $SYSUPDATES_RPM_DIR
rsync --checksum -av --delete --stats $BASE_DIR/SRPMS/ $SYSUPDATES_SRPM_DIR

# Now, create repo for RPMs and SRPMS:

createrepo --changelog-limit=3 --workers=4 -d --update $SYSUPDATES_RPM_DIR
createrepo --changelog-limit=3 --workers=4 -d --update $SYSUPDATES_SRPM_DIR

echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $SYSUPDATES_RPM_DIR/repodata/repomd.xml
echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $SYSUPDATES_SRPM_DIR/repodata/repomd.xml

# We currently sync only x86_64 packages to yonada. The rest is pulled from yonada:
if [ "$osarch" = "x86_64" ]
then
	# Finally, perform the rsync:
	rsync -ave ssh --delete $SYSUPDATES_RPM_DIR/ yumupload@yum.postgresql.org:yum/yum/common/pgdg-$ossysupdates-sysupdates/$osdistro/$os-$osarch
fi

# Sync SRPMs to S3 bucket:
aws s3 sync $SYSUPDATES_SRPM_DIR s3://dnf-srpms.postgresql.org20250313103537584600000001/srpms/common/pgdg-$ossysupdates-sysupdates/$osdistro/$os-$osarch --exclude "*.html"
aws cloudfront create-invalidation --distribution-id $CF_SRPM_DISTRO_ID --path /srpms/$packageSyncVersion/$osdistro/$os-$osarch/repodata/*

exit 0
