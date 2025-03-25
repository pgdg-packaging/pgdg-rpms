#!/usr/bin/bash

#########################################################
#							#
# Devrim Gündüz <devrim@gunduz.org> - 2024		#
#							#
#########################################################

# Include common values:
source ~/bin/global.sh

# if less than two arguments supplied, throw an error:
	if [  $# -le 1 ]
	then
		echo
		echo "${red}ERROR:${reset} This script must be run with at least two parameters:"
		echo "       package name, package version"
		echo "       and optional: The actual package name to sign, and also the PostgreSQL version to build against"
		echo
	exit 1
	fi

# The name of the package in the git tree (pgpool-II-41, postgresql-14, etc)
packagename=$1
# Actual package name to sign (pgpool-II, postgis, etc).
signPackageName=$2

# Build, sign the package and exit safely:
if [ -x ~/git/pgrpms/rpm/redhat/main/extras/$packagename/$git_os ]
then
echo "${green}Building $packagename on $os for extras repo.${reset}"
sleep 1
       	cd ~/git/pgrpms/rpm/redhat/main/extras/$packagename/$git_os
        time make extrasbuild
	# Get the package version after building the package so that we get the latest version:
	packageVersion=`rpmspec --define "pgmajorversion ${pgAlphaVersion}" -q --qf "%{name}: %{Version}\n" *.spec |head -n 1 | awk -F ': ' '{print $2}'`
	sign_package pgdg.$osshort.extras
	exit 0
fi
