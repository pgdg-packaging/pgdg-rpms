#!/usr/bin/bash

#########################################################
#							#
# Devrim Gündüz <devrim@gunduz.org> - 2026		#
#							#
#########################################################

# Include common values:
source ~/bin/global.sh

# reporpmbuild.sh builds the pgdg-yum repo RPM against the OS major version defined
# in global.sh, instead of against a PostgreSQL major version like packagebuild.sh
# does for regular packages.
#
# There is one repo RPM per OS major version, built on every minor version builder:
# the RHEL / Rocky Linux / AlmaLinux repo files use $releasever_major.$releasever_minor,
# so the same package works on all minor versions and follows OS minor updates. Per
# minor version repo RPMs are gone: all minor versions of the OS share the latest
# minor version's common repo (rhel-9 is a symlink to rhel-9.8, etc.), where the
# pinned build always sorted higher than the major version one. Per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/215

# Parse command line arguments
testing_mode=0
force_mode=0
while [[ $# -gt 0 ]]; do
	case $1 in
		--testing)
			testing_mode=1
			shift
			;;
		--force)
			force_mode=1
			shift
			;;
		*)
			break
			;;
	esac
done

# Stop now if packages cannot be signed, instead of after the build:
check_gpg_agent || exit 1

packagename="pgdg-yum"

osrelease="${osmajorversion}"

#################################
#	Repo RPM (pgdg-yum)	#
#################################

if [ -x ~/git/pgrpms/rpm/redhat/main/common/$packagename/$git_os ]
then
	if [ $testing_mode -eq 1 ]
	then
		cd ~/git/pgrpms/rpm/redhat/main/common/$packagename/$git_os
		if [ $force_mode -eq 0 ] && is_already_built ~/rpmcommontesting/RPMS $pgAlphaVersion; then
			echo "${yellow}$packagename is already built ($already_built_version) for OS release $osrelease (testing repo). Skipping (use --force to rebuild).${reset}"
			cd
			exit 0
		fi
		echo "${green}Ok, building $packagename on $git_os for OS release $osrelease (testing repo):${reset}"
		sleep 1
		if ! time make repobuild${osrelease}testing; then
			packageVersion=`rpmspec -q --qf "%{name}: %{Version}\n" *.spec 2>/dev/null |head -n 1 | awk -F ': ' '{print $2}'`
			cd
			log_build_failure "$packagename" "$osrelease" "repo_testing"
			exit 1
		fi
	else
		cd ~/git/pgrpms/rpm/redhat/main/common/$packagename/$git_os
		if [ $force_mode -eq 0 ] && is_already_built ~/rpmcommon/RPMS $pgAlphaVersion; then
			echo "${yellow}$packagename is already built ($already_built_version) for OS release $osrelease. Skipping (use --force to rebuild).${reset}"
			cd
			exit 0
		fi
		echo "${green}Ok, building $packagename on $git_os for OS release $osrelease:${reset}"
		sleep 1
		if ! time make repobuild${osrelease}; then
			packageVersion=`rpmspec -q --qf "%{name}: %{Version}\n" *.spec 2>/dev/null |head -n 1 | awk -F ': ' '{print $2}'`
			cd
			log_build_failure "$packagename" "$osrelease" "repo"
			exit 1
		fi
	fi

	# Get the package version after building the package so that we get the latest version:
	packageVersion=`rpmspec -q --qf "%{name}: %{Version}\n" *.spec |head -n 1 | awk -F ': ' '{print $2}'`
	sign_failed=0
	if [ $testing_mode -eq 1 ]
	then
		sign_built_rpms rpmcommontesting $pgAlphaVersion || sign_failed=1
	else
		sign_built_rpms rpmcommon $pgAlphaVersion || sign_failed=1
	fi
	cd
	exit $sign_failed
else
	echo "${red}ERROR:${reset} $packagename does not exist for $git_os"
	exit 1
fi
