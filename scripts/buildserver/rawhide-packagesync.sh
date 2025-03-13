#!/usr/bin/bash

#########################################################
#							#
# Devrim Gündüz <devrim@gunduz.org> - 2024		#
#							#
#########################################################

# Include common values:
source ~/bin/global.sh

if [ "$1" == "" ]
then
	:
else
	if [[ "${pgTestBuilds[@]}" =~ "$1" ]]
	then
		declare -a pgTestBuilds=("$1")
	else
		echo "${red}ERROR:${reset} PostgreSQL version $1 is not supported."
		exit 1
		fi
fi

for packageSyncVersion in ${pgTestBuilds[@]}
do
	export BASE_DIR=/var/lib/pgsql/rpm${packageSyncVersion}testing

	export RPM_DIR=$BASE_DIR/ALLRPMS
	export DEBUG_RPM_DIR=$BASE_DIR/ALLDEBUGRPMS
	export SRPM_DIR=$BASE_DIR/ALLSRPMS

	# Create directories for binary and source RPMs. This directory will help us
	# to create the repo files easily:
	mkdir -p $RPM_DIR
	mkdir -p $SRPM_DIR
	mkdir -p $DEBUG_RPM_DIR

	# rsync binary and source RPMs to their own directories:
	echo "${green}Syncing PostgreSQL $packageSyncVersion RPMs${reset}"

	rsync --checksum -av --delete --stats $BASE_DIR/RPMS/$osarch/ $BASE_DIR/RPMS/noarch/ $RPM_DIR
	rsync --checksum -av --delete --stats $BASE_DIR/SRPMS/ $SRPM_DIR

	# Move debuginfo and debugsource packages to a separate directory.
	# First clean the old ones, and then copy existing ones:
	rm -rf $DEBUG_RPM_DIR/*
	mv $RPM_DIR/*debuginfo* $RPM_DIR/*debugsource* $DEBUG_RPM_DIR/

	# Now, create repo for RPMs and SRPMS:

	createrepo --changelog-limit=3 --workers=4 -g /usr/local/etc/postgresqldbserver-$packageSyncVersion.xml -d --update $RPM_DIR
	createrepo --changelog-limit=3 --workers=4 -g /usr/local/etc/postgresqldbserver-$packageSyncVersion.xml -d --update $DEBUG_RPM_DIR
	createrepo --changelog-limit=3 --workers=4 -d --update $SRPM_DIR

	echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $RPM_DIR/repodata/repomd.xml
	echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $DEBUG_RPM_DIR/repodata/repomd.xml
	echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $SRPM_DIR/repodata/repomd.xml

	# Finally, perform the rsync:
	rsync --checksum -ave ssh --delete $RPM_DIR/ yumupload@yum.postgresql.org:yum/yum/testing/$packageSyncVersion/$osdistro/$os-$osarch
	rsync --checksum -ave ssh --delete $SRPM_DIR/ yumupload@yum.postgresql.org:yum/yum/srpms/testing/$packageSyncVersion/$osdistro/$os-$osarch

	# Sync SRPMs to S3 bucket:
    	aws s3 sync $SRPM_DIR s3://dnf-srpms.postgresql.org20250313103537584600000001/srpms/testing/$packageSyncVersion/$osdistro/$os-$osarch
        aws cloudfront create-invalidation --distribution-id $CF_SRPM_DISTRO_ID --path /srpms/testing/$packageSyncVersion/$osdistro/$os-$osarch/repodata/*

	# Sync debug* RPMs to S3 bucket:
	aws s3 sync $DEBUG_RPM_DIR s3://dnf-debuginfo.postgresql.org20250312201116649700000001/testing/debug/$packageSyncVersion/$osdistro/$os-$osarch/
	aws cloudfront create-invalidation --distribution-id $CF_DEBUG_DISTRO_ID --path /testing/debug/$packageSyncVersion/$osdistro/$os-$osarch/repodata/*
done

exit 0
