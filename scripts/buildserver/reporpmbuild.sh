#!/usr/bin/bash

#########################################################
#							#
# Devrim Gündüz <devrim@gunduz.org> - 2026		#
#							#
#########################################################

# Include common values:
source ~/bin/global.sh

# reporpmbuild.sh builds the pgdg-yum repo RPM against the OS release defined in
# global.sh (osmajorversion.osminversion), instead of against a PostgreSQL major
# version like packagebuild.sh does for regular packages.

# Parse command line arguments
testing_mode=0
while [[ $# -gt 0 ]]; do
	case $1 in
		--testing)
			testing_mode=1
			shift
			;;
		*)
			break
			;;
	esac
done

packagename="pgdg-yum"

# Fedora and Amazon Linux have no minor version (osminversion is left empty
# in global-local.sh for those); append it only when set, same convention as
# osfullversion in packagesync.sh.
if [ -n "${osminversion}" ]; then
	osrelease="${osmajorversion}.${osminversion}"
else
	osrelease="${osmajorversion}"
fi

#################################
#	Repo RPM (pgdg-yum)	#
#################################

if [ -x ~/git/pgrpms/rpm/redhat/main/common/$packagename/$git_os ]
then
	if [ $testing_mode -eq 1 ]
	then
		echo "${green}Ok, building $packagename on $git_os for OS release $osrelease (testing repo):${reset}"
		sleep 1
		cd ~/git/pgrpms/rpm/redhat/main/common/$packagename/$git_os
		if ! time make repobuild${osrelease}testing; then
			packageVersion=`rpmspec -q --qf "%{name}: %{Version}\n" *.spec 2>/dev/null |head -n 1 | awk -F ': ' '{print $2}'`
			cd
			log_build_failure "$packagename" "$osrelease" "repo_testing"
			exit 1
		fi
	else
		echo "${green}Ok, building $packagename on $git_os for OS release $osrelease:${reset}"
		sleep 1
		cd ~/git/pgrpms/rpm/redhat/main/common/$packagename/$git_os
		if ! time make repobuild${osrelease}; then
			packageVersion=`rpmspec -q --qf "%{name}: %{Version}\n" *.spec 2>/dev/null |head -n 1 | awk -F ': ' '{print $2}'`
			cd
			log_build_failure "$packagename" "$osrelease" "repo"
			exit 1
		fi
	fi

	# Get the package version after building the package so that we get the latest version:
	packageVersion=`rpmspec -q --qf "%{name}: %{Version}\n" *.spec |head -n 1 | awk -F ': ' '{print $2}'`
	cd
	if [ $testing_mode -eq 1 ]
	then
		sign_package rpmcommontesting
	else
		sign_package rpmcommon
	fi
	exit 0
else
	echo "${red}ERROR:${reset} $packagename does not exist for $git_os"
	exit 1
fi
