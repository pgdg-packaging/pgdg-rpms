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
	if [[ "${pgBetaVersion[@]}" =~ "$1" ]]
	then
		declare -a pgBetaVersion=("$1")
	else
		echo "${red}ERROR:${reset} PostgreSQL testing version $1 is not supported."
		exit 1
	fi
fi

for packageSyncVersion in ${pgBetaVersion[@]}
do
	export TESTING_BASE_DIR=/var/lib/pgsql/rpm${packageSyncVersion}testing
	export TESTING_RPM_DIR=$TESTING_BASE_DIR/ALLRPMS
	export TESTING_SRPM_DIR=$TESTING_BASE_DIR/ALLSRPMS
	export TESTING_DEBUG_RPM_DIR=$TESTING_BASE_DIR/ALLDEBUGRPMS

	# Create directories for binary and source RPMs. This directory will help us
	# to create the repo files easily:
	mkdir -vp $TESTING_RPM_DIR
	mkdir -vp $TESTING_SRPM_DIR
	mkdir -vp $TESTING_DEBUG_RPM_DIR

	rm $(repomanage --old --keep=2 $TESTING_RPM_DIR/) -f
	rm $(repomanage --old --keep=2 $TESTING_SRPM_DIR/) -f

	# rsync binary and source RPMs to their own directories:
	echo "--------------------------------------------------------------------"
	echo "${green}Syncing PostgreSQL $packageSyncVersion testing RPMs${reset}"
	echo "--------------------------------------------------------------------"

	rsync --checksum -av --delete --stats $TESTING_BASE_DIR/RPMS/$osarch/ $TESTING_BASE_DIR/RPMS/noarch/ $TESTING_RPM_DIR
	rsync --checksum -av --delete --stats $TESTING_BASE_DIR/SRPMS/ $TESTING_SRPM_DIR

	# Move debuginfo and debugsource packages to a separate directory.
	# First clean the old ones, and then copy existing ones:
	rm -rf $TESTING_DEBUG_RPM_DIR/*
	mv $TESTING_RPM_DIR/*debuginfo* $TESTING_RPM_DIR/*debugsource* $TESTING_DEBUG_RPM_DIR/

	createrepo --changelog-limit=3 --workers=4 --oldpackagedirs=$TESTING_RPM_DIR -g /usr/local/etc/postgresqldbserver-$packageSyncVersion.xml -d --update $TESTING_RPM_DIR
	createrepo --changelog-limit=3 --workers=4 --oldpackagedirs=$TESTING_SRPM_DIR -d --update $TESTING_SRPM_DIR
	createrepo --changelog-limit=3 --workers=4 --oldpackagedirs=$TESTING_DEBUG_RPM_DIR -g /usr/local/etc/postgresqldbserver-$packageSyncVersion.xml -d --update $TESTING_DEBUG_RPM_DIR

	echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $TESTING_RPM_DIR/repodata/repomd.xml
	echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $TESTING_SRPM_DIR/repodata/repomd.xml
	echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $TESTING_DEBUG_RPM_DIR/repodata/repomd.xml

	# Finally, perform the rssync:
	rsync --checksum -ave ssh --delete $TESTING_RPM_DIR/ yumupload@yum.postgresql.org:/srv/yum/yum/testing/$packageSyncVersion/$osdistro/$os-$osarch

	# Sync SRPMs to S3 bucket:
	aws s3 sync $TESTING_SRPM_DIR s3://dnf-srpms.postgresql.org20250313103537584600000001/srpms/testing/$packageSyncVersion/$osdistro/$os-$osarch
	aws cloudfront create-invalidation --distribution-id $CF_SRPM_DISTRO_ID --path /srpms/testing/$packageSyncVersion/$osdistro/$os-$osarch/repodata/*

	# Sync debug* RPMs to S3 bucket:
	aws s3 sync $TESTING_DEBUG_RPM_DIR s3://dnf-debuginfo.postgresql.org20250312201116649700000001/testing/debug/$packageSyncVersion/$osdistro/$os-$osarch/
	aws cloudfront create-invalidation --distribution-id $CF_DEBUG_DISTRO_ID --path /testing/debug/$packageSyncVersion/$osdistro/$os-$osarch/repodata/*
done

exit 0
