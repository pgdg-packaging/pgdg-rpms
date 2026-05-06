#!/usr/bin/bash

#########################################################
#							#
# Devrim Gündüz <devrim@gunduz.org> - 2026		#
#							#
# Merged package sync script with configurable options	#
# Supports both production and testing repositories	#
#							#
#########################################################

# Include common values:
source ~/bin/global.sh

# Set the remote base path on yum.postgresql.org based on the distro.
# SLES uses the zypp/zypp tree; all others (RHEL, Fedora) use yum/yum.
if [ "$osdistro" == "suse" ] || [ "$osdistro" == "opensuse" ]; then
	export sync_base="zypp/zypp"
else
	export sync_base="yum/yum"
fi

# Build the full OS version string used in S3/CloudFront paths.
# Fedora only has a major version (e.g. "fedora-43"), while RHEL and SLES
# also carry a minor version (e.g. "rhel-10.1"). When osminversion is set
# and non-empty we append it; otherwise we use the major version alone.
if [ -n "${osminversion}" ]; then
	export osfullversion="${os}.${osminversion}"
else
	export osfullversion="${os}"
fi

# Global flag for testing mode
TESTING_MODE=0

# Function to display usage
usage() {
	echo "Usage: $0 [--testing] [--sync=<option> [option2 ...]]"
	echo ""
	echo "Options:"
	echo "  --testing            Enable testing mode (syncs to testing repositories)"
	echo ""
	echo "Sync Options:"
	echo "  --sync=all           Sync common, extras, and all PostgreSQL versions"
	echo "  --sync=common        Sync only common RPMs"
	echo "  --sync=extras        Sync only extras RPMs (if enabled)"
	echo "  --sync=pg            Sync all PostgreSQL versions (no common/extras)"
	echo "  --sync=alpha         Sync alpha builds (PostgreSQL ${pgAlphaVersion})"
	echo "  --sync=beta          Sync beta builds (PostgreSQL ${pgBetaVersion})"
	echo "  --sync=<version>     Sync specific PostgreSQL version (e.g., --sync=18)"
	echo "  --sync=\"ver1 ver2\"  Sync multiple specific versions/targets (space-separated)"
	echo ""
	echo "Multiple targets can be combined (space-separated):"
	echo "  - Version numbers (e.g., 18, 17, 16)"
	echo "  - 'common' keyword"
	echo "  - 'extras' keyword (requires extrasrepoenabled=1 in global.sh)"
	echo "  - 'alpha' keyword (PostgreSQL ${pgAlphaVersion} alpha builds)"
	echo "  - 'beta' keyword (PostgreSQL ${pgBetaVersion} beta builds)"
	echo "  - 'pg' keyword (all versions)"
	echo ""
	echo "Examples:"
	echo "  $0 --sync=all"
	echo "  $0 --sync=common"
	echo "  $0 --sync=extras"
	echo "  $0 --sync=pg"
	echo "  $0 --sync=18"
	echo "  $0 --sync=alpha"
	echo "  $0 --sync=beta"
	echo "  $0 --sync=\"18 common\""
	echo "  $0 --sync=\"alpha common\""
	echo "  $0 --sync=\"beta extras\""
	echo "  $0 --sync=\"pg common extras\""
	echo ""
	echo "Testing mode examples:"
	echo "  $0 --testing --sync=18"
	echo "  $0 --testing --sync=pg"
	echo "  $0 --testing --sync=\"17 18\""
	exit 1
}

# Function to sync common RPMs
sync_common() {
	if [ $TESTING_MODE -eq 1 ]; then
		echo "${green}=== Syncing PostgreSQL common RPMs for $os - $osarch (TESTING MODE) ===${reset}"
	else
		echo "${green}=== Syncing PostgreSQL common RPMs for $os - $osarch ===${reset}"
	fi

	if [ $TESTING_MODE -eq 1 ]; then
		export COMMON_RPM_DIR=/var/lib/pgsql/rpmcommontesting/ALLRPMS
		export COMMON_SRPM_DIR=/var/lib/pgsql/rpmcommontesting/ALLSRPMS
		export COMMON_DEBUG_RPM_DIR=/var/lib/pgsql/rpmcommontesting/ALLDEBUGRPMS
	else
		export COMMON_RPM_DIR=/var/lib/pgsql/rpmcommon/ALLRPMS
		export COMMON_SRPM_DIR=/var/lib/pgsql/rpmcommon/ALLSRPMS
		export COMMON_DEBUG_RPM_DIR=/var/lib/pgsql/rpmcommon/ALLDEBUGRPMS
	fi

	# Create directories for binary and source RPMs
	mkdir -p $COMMON_RPM_DIR
	mkdir -p $COMMON_SRPM_DIR
	mkdir -p $COMMON_DEBUG_RPM_DIR

	# rsync binary and source RPMs to their own directories:
	if [ $TESTING_MODE -eq 1 ]; then
		rsync --checksum -av --delete --stats /var/lib/pgsql/rpmcommontesting/RPMS/$osarch/ /var/lib/pgsql/rpmcommontesting/RPMS/noarch/ $COMMON_RPM_DIR
		rsync --checksum -av --delete --stats /var/lib/pgsql/rpmcommontesting/SRPMS/ $COMMON_SRPM_DIR
	else
		rsync --checksum -av --delete --stats /var/lib/pgsql/rpmcommon/RPMS/$osarch/ /var/lib/pgsql/rpmcommon/RPMS/noarch/ $COMMON_RPM_DIR
		rsync --checksum -av --delete --stats /var/lib/pgsql/rpmcommon/SRPMS/ $COMMON_SRPM_DIR
	fi

	# Move debuginfo and debugsource packages to a separate directory.
	# First clean the old ones, and then copy existing ones:
	rm -rf $COMMON_DEBUG_RPM_DIR/*
	mv $COMMON_RPM_DIR/*debuginfo* $COMMON_RPM_DIR/*debugsource* $COMMON_DEBUG_RPM_DIR/ 2>/dev/null || true

	# Now, create repo for RPMs and SRPMS:
	createrepo --changelog-limit=3 --workers=4 -d --update $COMMON_RPM_DIR
	createrepo --changelog-limit=3 --workers=4 -d --update $COMMON_SRPM_DIR
	createrepo --changelog-limit=3 --workers=4 -d --update $COMMON_DEBUG_RPM_DIR

	echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $COMMON_RPM_DIR/repodata/repomd.xml
	echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $COMMON_SRPM_DIR/repodata/repomd.xml
	echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $COMMON_DEBUG_RPM_DIR/repodata/repomd.xml

	if [ $TESTING_MODE -eq 1 ]; then
		# Testing mode: sync to testing paths
		# Sync SRPMs to S3 bucket:
		aws s3 sync $COMMON_SRPM_DIR $awssrpmurl/srpms/testing/common/$osdistro/$osfullversion-$osarch/ --exclude "*.html" --exclude "repodata"
		aws s3 sync --delete $COMMON_SRPM_DIR/repodata/ $awssrpmurl/srpms/testing/common/$osdistro/$osfullversion-$osarch/repodata/ --exclude "*.html"

		# Sync debug* RPMs to S3 bucket:
		aws s3 sync $COMMON_DEBUG_RPM_DIR $awsdebuginfourl/testing/debug/common/$osdistro/$osfullversion-$osarch/ --exclude "*.html" --exclude "repodata"
		aws s3 sync --delete $COMMON_DEBUG_RPM_DIR/repodata/ $awsdebuginfourl/testing/debug/common/$osdistro/$osfullversion-$osarch/repodata/ --exclude "*.html"

		# Invalidate the caches:
		aws cloudfront create-invalidation --distribution-id $CF_SRPM_DISTRO_ID --path /srpms/testing/common/$osdistro/$osfullversion-$osarch/repodata/*
		aws cloudfront create-invalidation --distribution-id $CF_DEBUG_DISTRO_ID --path /testing/debug/common/$osdistro/$osfullversion-$osarch/repodata/*

		# S3 does not allow symlinks, so we have to sync the packages once again to the OS major version directory if this is the latest version of the OS:
		if [ "$osislatest" == 1 ]
		then
			aws s3 sync $COMMON_SRPM_DIR $awssrpmurl/srpms/testing/common/$osdistro/$os-$osarch --exclude "*.html" --exclude "repodata"
			aws s3 sync --delete $COMMON_SRPM_DIR/repodata/ $awssrpmurl/srpms/testing/common/$osdistro/$os-$osarch/repodata/ --exclude "*.html"
			aws s3 sync $COMMON_DEBUG_RPM_DIR $awsdebuginfourl/testing/debug/common/$osdistro/$os-$osarch/ --exclude "*.html" --exclude "repodata"
			aws s3 sync --delete $COMMON_DEBUG_RPM_DIR/repodata/ $awsdebuginfourl/testing/debug/common/$osdistro/$os-$osarch/repodata/ --exclude "*.html"
			# Invalidate the caches:
			aws cloudfront create-invalidation --distribution-id $CF_SRPM_DISTRO_ID --path /srpms/testing/common/$osdistro/$os-$osarch/repodata/*
			aws cloudfront create-invalidation --distribution-id $CF_DEBUG_DISTRO_ID --path /testing/debug/common/$osdistro/$os-$osarch/repodata/*
		fi
	else
		# Production mode: sync to production paths
		# Sync SRPMs to S3 bucket:
		aws s3 sync $COMMON_SRPM_DIR $awssrpmurl/srpms/common/$osdistro/$osfullversion-$osarch/ --exclude "*.html" --exclude "repodata"
		aws s3 sync --delete $COMMON_SRPM_DIR/repodata/ $awssrpmurl/srpms/common/$osdistro/$osfullversion-$osarch/repodata/ --exclude "*.html"

		# Sync debug* RPMs to S3 bucket:
		aws s3 sync $COMMON_DEBUG_RPM_DIR $awsdebuginfourl/debug/common/$osdistro/$osfullversion-$osarch/ --exclude "*.html" --exclude "repodata"
		aws s3 sync --delete $COMMON_DEBUG_RPM_DIR/repodata/ $awsdebuginfourl/debug/common/$osdistro/$osfullversion-$osarch/repodata/ --exclude "*.html"

		# Invalidate the caches:
		aws cloudfront create-invalidation --distribution-id $CF_SRPM_DISTRO_ID --path /srpms/common/$osdistro/$osfullversion-$osarch/repodata/*
		aws cloudfront create-invalidation --distribution-id $CF_DEBUG_DISTRO_ID --path /debug/common/$osdistro/$osfullversion-$osarch/repodata/*

		# S3 does not allow symlinks, so we have to sync the packages once again to the OS major version directory if this is the latest version of the OS:
		if [ "$osislatest" == 1 ]
		then
			aws s3 sync $COMMON_SRPM_DIR $awssrpmurl/srpms/common/$osdistro/$os-$osarch --exclude "*.html" --exclude "repodata"
			aws s3 sync --delete $COMMON_SRPM_DIR/repodata/ $awssrpmurl/srpms/common/$osdistro/$os-$osarch/repodata/ --exclude "*.html"
			aws s3 sync $COMMON_DEBUG_RPM_DIR $awsdebuginfourl/debug/common/$osdistro/$os-$osarch/ --exclude "*.html" --exclude "repodata"
			aws s3 sync --delete $COMMON_DEBUG_RPM_DIR/repodata/ $awsdebuginfourl/debug/common/$osdistro/$os-$osarch/repodata/ --exclude "*.html"
			# Invalidate the caches:
			aws cloudfront create-invalidation --distribution-id $CF_SRPM_DISTRO_ID --path /srpms/common/$osdistro/$os-$osarch/repodata/*
			aws cloudfront create-invalidation --distribution-id $CF_DEBUG_DISTRO_ID --path /debug/common/$osdistro/$os-$osarch/repodata/*
		fi
	fi

	echo "${green}=== Common RPMs sync completed ===${reset}"
}

# Function to sync extras RPMs
sync_extras() {
	if [ $TESTING_MODE -eq 1 ]; then
		echo "${yellow}WARNING:${reset} Testing mode is not applicable for extras RPMs. Skipping."
		return 0
	fi

	# Check if extras repo is enabled
	if [ "$extrasrepoenabled" != 1 ]
	then
		echo "${red}ERROR:${reset} Extras repo is not enabled on this platform"
		echo "Set extrasrepoenabled=1 in global.sh to enable extras sync"
		return 1
	fi

	echo "${green}=== Syncing PostgreSQL extras RPMs for $os - $osarch ===${reset}"

	export BASE_DIR=/var/lib/pgsql/pgdg.extras

	export EXTRAS_RPM_DIR=$BASE_DIR/ALLRPMS
	export EXTRAS_SRPM_DIR=$BASE_DIR/ALLSRPMS
	export EXTRAS_DEBUG_RPM_DIR=$BASE_DIR/ALLDEBUGRPMS

	# Create directories for binary and source RPMs
	mkdir -p $EXTRAS_RPM_DIR
	mkdir -p $EXTRAS_SRPM_DIR
	mkdir -p $EXTRAS_DEBUG_RPM_DIR

	# rsync binary and source RPMs to their own directories:
	rsync --checksum -av --delete --stats $BASE_DIR/RPMS/$osarch/ $BASE_DIR/RPMS/noarch/ $EXTRAS_RPM_DIR
	rsync --checksum -av --delete --stats $BASE_DIR/SRPMS/ $EXTRAS_SRPM_DIR

	# Move debuginfo and debugsource packages to a separate directory.
	# First clean the old ones, and then copy existing ones:
	rm -rf $EXTRAS_DEBUG_RPM_DIR/*
	mv $EXTRAS_RPM_DIR/*debuginfo* $EXTRAS_RPM_DIR/*debugsource* $EXTRAS_DEBUG_RPM_DIR/ 2>/dev/null || true

	# Now, create repo for RPMs and SRPMS:
	createrepo --changelog-limit=3 --workers=4 -d --update $EXTRAS_RPM_DIR
	createrepo --changelog-limit=3 --workers=4 -d --update $EXTRAS_SRPM_DIR
	createrepo --changelog-limit=3 --workers=4 -d --update $EXTRAS_DEBUG_RPM_DIR

	echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $EXTRAS_RPM_DIR/repodata/repomd.xml
	echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $EXTRAS_SRPM_DIR/repodata/repomd.xml
	echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $EXTRAS_DEBUG_RPM_DIR/repodata/repomd.xml

	# Sync SRPMs to S3 bucket:
	aws s3 sync $EXTRAS_SRPM_DIR $awssrpmurl/srpms/extras/$osdistro/$osfullversion-$osarch --exclude "*.html" --exclude "repodata"
	aws s3 sync --delete $EXTRAS_SRPM_DIR/repodata/ $awssrpmurl/srpms/extras/$osdistro/$osfullversion-$osarch/repodata/ --exclude "*.html"
	aws cloudfront create-invalidation --distribution-id $CF_SRPM_DISTRO_ID --path /srpms/extras/$osdistro/$osfullversion-$osarch/repodata/*

	# Sync debug* RPMs to S3 bucket:
	aws s3 sync $EXTRAS_DEBUG_RPM_DIR $awsdebuginfourl/debug/extras/$osdistro/$osfullversion-$osarch/ --exclude "*.html" --exclude "repodata"
	aws s3 sync --delete $EXTRAS_DEBUG_RPM_DIR/repodata/ $awsdebuginfourl/debug/extras/$osdistro/$osfullversion-$osarch/repodata/ --exclude "*.html"
	aws cloudfront create-invalidation --distribution-id $CF_DEBUG_DISTRO_ID --path /debug/extras/$osdistro/$osfullversion-$osarch/repodata/*

	# S3 does not allow symlinks, so we have to sync the packages once again to the OS major version directory if this is the latest version of the OS:
	if [ "$osislatest" == 1 ]
	then
		aws s3 sync $EXTRAS_SRPM_DIR $awssrpmurl/srpms/extras/$osdistro/$os-$osarch --exclude "*.html" --exclude "repodata"
		aws s3 sync --delete $EXTRAS_SRPM_DIR/repodata/ $awssrpmurl/srpms/extras/$osdistro/$os-$osarch/repodata/ --exclude "*.html"

		aws s3 sync $EXTRAS_DEBUG_RPM_DIR $awsdebuginfourl/debug/extras/$osdistro/$os-$osarch/ --exclude "*.html" --exclude "repodata"
		aws s3 sync --delete $EXTRAS_DEBUG_RPM_DIR/repodata/ $awsdebuginfourl/debug/extras/$osdistro/$os-$osarch/repodata/ --exclude "*.html"
		# Invalidate the caches:
		aws cloudfront create-invalidation --distribution-id $CF_SRPM_DISTRO_ID --path /srpms/extras/$osdistro/$os-$osarch/repodata/*
		aws cloudfront create-invalidation --distribution-id $CF_DEBUG_DISTRO_ID --path /debug/extras/$osdistro/$os-$osarch/repodata/*
	fi

	echo "${green}=== Extras RPMs sync completed ===${reset}"
}

# Function to sync alpha/beta RPMs
sync_alpha_beta() {
	local build_type="$1"

	if [ $TESTING_MODE -eq 1 ]; then
		echo "${yellow}WARNING:${reset} Testing mode is not applicable for alpha/beta builds. Skipping."
		return 0
	fi

	# Determine version based on build type
	local packageSyncVersion
	if [[ "$build_type" == "alpha" ]]; then
		packageSyncVersion=$pgAlphaVersion
	elif [[ "$build_type" == "beta" ]]; then
		packageSyncVersion=$pgBetaVersion
	else
		echo "${red}ERROR:${reset} Invalid build type: $build_type"
		return 1
	fi

	echo "${green}=== Syncing PostgreSQL $packageSyncVersion $build_type RPMs ===${reset}"

	export BASE_DIR=/var/lib/pgsql/rpm${packageSyncVersion}testing

	export RPM_DIR=$BASE_DIR/ALLRPMS
	export DEBUG_RPM_DIR=$BASE_DIR/ALLDEBUGRPMS
	export SRPM_DIR=$BASE_DIR/ALLSRPMS

	# Create directories for binary and source RPMs
	mkdir -p $RPM_DIR
	mkdir -p $SRPM_DIR
	mkdir -p $DEBUG_RPM_DIR

	# rsync binary and source RPMs to their own directories:
	rsync --checksum -av --delete --stats $BASE_DIR/RPMS/$osarch/ $BASE_DIR/RPMS/noarch/ $RPM_DIR
	rsync --checksum -av --delete --stats $BASE_DIR/SRPMS/ $SRPM_DIR

	# Move debuginfo and debugsource packages to a separate directory.
	# First clean the old ones, and then copy existing ones:
	rm -rf $DEBUG_RPM_DIR/*
	mv $RPM_DIR/*debuginfo* $RPM_DIR/*debugsource* $DEBUG_RPM_DIR/ 2>/dev/null || true

	# Now, create repo for RPMs and SRPMS:
	createrepo --changelog-limit=3 --workers=4 -g /usr/local/etc/postgresqldbserver-$packageSyncVersion.xml -d --update $RPM_DIR
	createrepo --changelog-limit=3 --workers=4 -g /usr/local/etc/postgresqldbserver-$packageSyncVersion.xml -d --update $DEBUG_RPM_DIR
	createrepo --changelog-limit=3 --workers=4 -d --update $SRPM_DIR

	echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $RPM_DIR/repodata/repomd.xml
	echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $DEBUG_RPM_DIR/repodata/repomd.xml
	echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $SRPM_DIR/repodata/repomd.xml

	# Sync to testing directory instead of the version directory

	# Sync SRPMs to S3 bucket:
	aws s3 sync $SRPM_DIR $awssrpmurl/srpms/testing/$osdistro/$osfullversion-$osarch --exclude "*.html" --exclude "repodata"
	aws s3 sync --delete $SRPM_DIR/repodata/ $awssrpmurl/srpms/testing/$osdistro/$osfullversion-$osarch/repodata/ --exclude "*.html"

	# Sync debug* RPMs to S3 bucket:
	aws s3 sync $DEBUG_RPM_DIR $awsdebuginfourl/debug/testing/$osdistro/$osfullversion-$osarch/ --exclude "*.html" --exclude "repodata"
	aws s3 sync --delete $DEBUG_RPM_DIR/repodata/ $awsdebuginfourl/debug/testing/$osdistro/$osfullversion-$osarch/repodata/ --exclude "*.html"

	# Invalidate the caches:
	aws cloudfront create-invalidation --distribution-id $CF_SRPM_DISTRO_ID --path /srpms/testing/$osdistro/$osfullversion-$osarch/repodata/*
	aws cloudfront create-invalidation --distribution-id $CF_DEBUG_DISTRO_ID --path /debug/testing/$osdistro/$osfullversion-$osarch/repodata/*

	# S3 does not allow symlinks, so we have to sync the packages once again to the OS major version directory if this is the latest version of the OS:
	if [ "$osislatest" == 1 ]
	then
		aws s3 sync $SRPM_DIR $awssrpmurl/srpms/testing/$osdistro/$os-$osarch --exclude "*.html" --exclude "repodata"
		aws s3 sync --delete $SRPM_DIR/repodata/ $awssrpmurl/srpms/testing/$osdistro/$os-$osarch/repodata/ --exclude "*.html"
		aws s3 sync $DEBUG_RPM_DIR $awsdebuginfourl/debug/testing/$osdistro/$os-$osarch/ --exclude "*.html" --exclude "repodata"
		aws s3 sync --delete $DEBUG_RPM_DIR/repodata/ $awsdebuginfourl/debug/testing/$osdistro/$os-$osarch/repodata/ --exclude "*.html"

		# Invalidate the caches:
		aws cloudfront create-invalidation --distribution-id $CF_SRPM_DISTRO_ID --path /srpms/testing/$osdistro/$os-$osarch/repodata/*
		aws cloudfront create-invalidation --distribution-id $CF_DEBUG_DISTRO_ID --path /debug/testing/$osdistro/$os-$osarch/repodata/*
	fi

	echo "${green}=== PostgreSQL $packageSyncVersion $build_type RPMs sync completed ===${reset}"
}

# Function to sync PostgreSQL version-specific RPMs
sync_pg_version() {
	local packageSyncVersion=$1

	if [ $TESTING_MODE -eq 1 ]; then
		echo "${green}=== Syncing PostgreSQL $packageSyncVersion RPMs (TESTING MODE) ===${reset}"
	else
		echo "${green}=== Syncing PostgreSQL $packageSyncVersion RPMs ===${reset}"
	fi

	# Set BASE_DIR based on testing mode
	if [ $TESTING_MODE -eq 1 ]; then
		export BASE_DIR=/var/lib/pgsql/rpm${packageSyncVersion}testing
	else
		export BASE_DIR=/var/lib/pgsql/rpm${packageSyncVersion}
	fi

	export RPM_DIR=$BASE_DIR/ALLRPMS
	export DEBUG_RPM_DIR=$BASE_DIR/ALLDEBUGRPMS
	export SRPM_DIR=$BASE_DIR/ALLSRPMS

	# Create directories for binary and source RPMs
	mkdir -p $RPM_DIR
	mkdir -p $SRPM_DIR
	mkdir -p $DEBUG_RPM_DIR

	# rsync binary and source RPMs to their own directories:
	rsync --checksum -av --delete --stats $BASE_DIR/RPMS/$osarch/ $BASE_DIR/RPMS/noarch/ $RPM_DIR
	rsync --checksum -av --delete --stats $BASE_DIR/SRPMS/ $SRPM_DIR

	# Move debuginfo and debugsource packages to a separate directory.
	# First clean the old ones, and then copy existing ones:
	rm -rf $DEBUG_RPM_DIR/*
	mv $RPM_DIR/*debuginfo* $RPM_DIR/*debugsource* $DEBUG_RPM_DIR/ 2>/dev/null || true

	# Now, create repo for RPMs and SRPMS:
	createrepo --changelog-limit=3 --workers=4 -g /usr/local/etc/postgresqldbserver-$packageSyncVersion.xml -d --update $RPM_DIR
	createrepo --changelog-limit=3 --workers=4 -g /usr/local/etc/postgresqldbserver-$packageSyncVersion.xml -d --update $DEBUG_RPM_DIR
	createrepo --changelog-limit=3 --workers=4 -d --update $SRPM_DIR

	echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $RPM_DIR/repodata/repomd.xml
	echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $DEBUG_RPM_DIR/repodata/repomd.xml
	echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $SRPM_DIR/repodata/repomd.xml

	if [ $TESTING_MODE -eq 1 ]; then
		# Testing mode: Use legacy rsync to yum.postgresql.org and S3 sync with testing paths
		# Sync binary RPMs to yum.postgresql.org
		# rsync --checksum -ave ssh --delete $RPM_DIR/ yumupload@yum.postgresql.org:$sync_base/testing/$packageSyncVersion/$osdistro/$os-$osarch

		# Sync SRPMs to yum.postgresql.org
		# rsync --checksum -ave ssh --delete $SRPM_DIR/ yumupload@yum.postgresql.org:$sync_base/srpms/testing/$packageSyncVersion/$osdistro/$os-$osarch

		# Sync SRPMs to S3 bucket:
		aws s3 sync $SRPM_DIR $awssrpmurl/srpms/testing/$packageSyncVersion/$osdistro/$os-$osarch --exclude "*.html" --exclude "repodata"
		aws s3 sync --delete $SRPM_DIR/repodata/ $awssrpmurl/srpms/testing/$packageSyncVersion/$osdistro/$os-$osarch/repodata/ --exclude "*.html"

		# Sync debug* RPMs to S3 bucket:
		aws s3 sync $DEBUG_RPM_DIR $awsdebuginfourl/testing/debug/$packageSyncVersion/$osdistro/$os-$osarch/ --exclude "*.html" --exclude "repodata"
		aws s3 sync --delete $DEBUG_RPM_DIR/repodata/ $awsdebuginfourl/testing/debug/$packageSyncVersion/$osdistro/$os-$osarch/repodata/ --exclude "*.html"

		# Invalidate the caches:
		aws cloudfront create-invalidation --distribution-id $CF_SRPM_DISTRO_ID --path /srpms/testing/$packageSyncVersion/$osdistro/$os-$osarch/repodata/*
		aws cloudfront create-invalidation --distribution-id $CF_DEBUG_DISTRO_ID --path /testing/debug/$packageSyncVersion/$osdistro/$os-$osarch/repodata/*
	else
		# Production mode: Use standard S3 sync with CloudFront invalidation
		# Sync SRPMs to S3 bucket:
		aws s3 sync $SRPM_DIR $awssrpmurl/srpms/$packageSyncVersion/$osdistro/$osfullversion-$osarch --exclude "*.html" --exclude "repodata"
		aws s3 sync --delete $SRPM_DIR/repodata/ $awssrpmurl/srpms/$packageSyncVersion/$osdistro/$osfullversion-$osarch/repodata/ --exclude "*.html"

		# Sync debug* RPMs to S3 bucket:
		aws s3 sync $DEBUG_RPM_DIR $awsdebuginfourl/debug/$packageSyncVersion/$osdistro/$osfullversion-$osarch/ --exclude "*.html" --exclude "repodata"
		aws s3 sync --delete $DEBUG_RPM_DIR/repodata/ $awsdebuginfourl/debug/$packageSyncVersion/$osdistro/$osfullversion-$osarch/repodata/ --exclude "*.html"

		# Invalidate the caches:
		aws cloudfront create-invalidation --distribution-id $CF_SRPM_DISTRO_ID --path /srpms/$packageSyncVersion/$osdistro/$osfullversion-$osarch/repodata/*
		aws cloudfront create-invalidation --distribution-id $CF_DEBUG_DISTRO_ID --path /debug/$packageSyncVersion/$osdistro/$osfullversion-$osarch/repodata/*

		# S3 does not allow symlinks, so we have to sync the packages once again to the OS major version directory if this is the latest version of the OS:
		if [ "$osislatest" == 1 ]
		then
			aws s3 sync $SRPM_DIR $awssrpmurl/srpms/$packageSyncVersion/$osdistro/$os-$osarch --exclude "*.html" --exclude "repodata"
			aws s3 sync --delete $SRPM_DIR/repodata/ $awssrpmurl/srpms/$packageSyncVersion/$osdistro/$os-$osarch/repodata/ --exclude "*.html"
			aws s3 sync $DEBUG_RPM_DIR $awsdebuginfourl/debug/$packageSyncVersion/$osdistro/$os-$osarch/ --exclude "*.html" --exclude "repodata"
			aws s3 sync --delete $DEBUG_RPM_DIR/repodata/ $awsdebuginfourl/debug/$packageSyncVersion/$osdistro/$os-$osarch/repodata/ --exclude "*.html"

			# Invalidate the caches:
			aws cloudfront create-invalidation --distribution-id $CF_SRPM_DISTRO_ID --path /srpms/$packageSyncVersion/$osdistro/$os-$osarch/repodata/*
			aws cloudfront create-invalidation --distribution-id $CF_DEBUG_DISTRO_ID --path /debug/$packageSyncVersion/$osdistro/$os-$osarch/repodata/*
		fi
	fi

	if [ $TESTING_MODE -eq 1 ]; then
		echo "${green}=== PostgreSQL $packageSyncVersion TESTING RPMs sync completed ===${reset}"
	else
		echo "${green}=== PostgreSQL $packageSyncVersion RPMs sync completed ===${reset}"
	fi
}

# Parse command line arguments
SYNC_TARGETS=""

if [ $# -eq 0 ]; then
	usage
fi

for arg in "$@"
do
	case $arg in
		--testing)
			TESTING_MODE=1
			shift
			;;
		--sync=*)
			SYNC_TARGETS="${arg#*=}"
			shift
			;;
		*)
			echo "${red}ERROR:${reset} Unknown argument: $arg"
			usage
			;;
	esac
done

# Determine which version array to use based on testing mode
if [ $TESTING_MODE -eq 1 ]; then
	declare -a VERSIONS_ARRAY=("${pgTestBuilds[@]}")
	echo "${green}=== TESTING MODE ENABLED ===${reset}"
	echo "${green}Using pgTestBuilds versions: ${VERSIONS_ARRAY[@]}${reset}"
else
	declare -a VERSIONS_ARRAY=("${pgStableBuilds[@]}")
fi

# Process sync targets
declare -a sync_common_flag=0
declare -a sync_extras_flag=0
declare -a sync_alpha_flag=0
declare -a sync_beta_flag=0
declare -a versions_to_sync=()

# Handle special case: "all"
if [ "$SYNC_TARGETS" == "all" ]; then
	if [ $TESTING_MODE -eq 1 ]; then
		echo "${green}Starting sync: Common + All PostgreSQL testing versions${reset}"
		sync_common
		for version in ${VERSIONS_ARRAY[@]}
		do
			sync_pg_version $version
		done
	else
		echo "${green}Starting sync: Common + Extras + All PostgreSQL versions${reset}"
		sync_common
		sync_extras
		for version in ${VERSIONS_ARRAY[@]}
		do
			sync_pg_version $version
		done
	fi
else
	# Parse multiple targets (space-separated)
	for target in $SYNC_TARGETS
	do
		case $target in
			common)
				sync_common_flag=1
				;;
			extras)
				sync_extras_flag=1
				;;
			alpha)
				sync_alpha_flag=1
				;;
			beta)
				sync_beta_flag=1
				;;
			pg)
				# Add all PostgreSQL versions to the list
				for version in ${VERSIONS_ARRAY[@]}
				do
					versions_to_sync+=($version)
				done
				;;
			*)
				# Check if it's a specific version number
				if [[ "${VERSIONS_ARRAY[@]}" =~ (^|[[:space:]])"$target"($|[[:space:]]) ]]
				then
					versions_to_sync+=($target)
				else
					echo "${red}ERROR:${reset} Invalid sync option or unsupported PostgreSQL version: $target"
					echo ""
					if [ $TESTING_MODE -eq 1 ]; then
						echo "Supported PostgreSQL testing versions: ${VERSIONS_ARRAY[@]}"
					else
						echo "Supported PostgreSQL versions: ${VERSIONS_ARRAY[@]}"
					fi
					usage
				fi
				;;
		esac
	done

	# Execute syncs
	if [ $sync_common_flag -eq 1 ]; then
		sync_common
	fi

	if [ $sync_extras_flag -eq 1 ]; then
		sync_extras
	fi

	if [ $sync_alpha_flag -eq 1 ]; then
		sync_alpha_beta "alpha"
	fi

	if [ $sync_beta_flag -eq 1 ]; then
		sync_alpha_beta "beta"
	fi

	# Remove duplicates from versions array and sync each version
	if [ ${#versions_to_sync[@]} -gt 0 ]; then
		# Remove duplicates while preserving order
		declare -a unique_versions=()
		for version in "${versions_to_sync[@]}"
		do
			if [[ ! " ${unique_versions[@]} " =~ " ${version} " ]]; then
				unique_versions+=($version)
			fi
		done

		echo "${green}Syncing PostgreSQL versions: ${unique_versions[@]}${reset}"
		for version in "${unique_versions[@]}"
		do
			sync_pg_version $version
		done
	fi

	# Check if nothing was synced
	if [ $sync_common_flag -eq 0 ] && [ $sync_extras_flag -eq 0 ] && [ $sync_alpha_flag -eq 0 ] && [ $sync_beta_flag -eq 0 ] && [ ${#versions_to_sync[@]} -eq 0 ]; then
		echo "${red}ERROR:${reset} No valid sync targets specified"
		usage
	fi
fi

echo "${green}All sync operations completed successfully!${reset}"
exit 0
