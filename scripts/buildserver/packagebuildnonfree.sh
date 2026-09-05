#!/usr/bin/bash

#########################################################
#							#
# Devrim Gündüz <devrim@gunduz.org> - 2026		#
#							#
#########################################################

# Include common values:
source ~/bin/global.sh

# Parse command line arguments
force_mode=0
while [[ $# -gt 0 ]]; do
	case $1 in
		--force)
			force_mode=1
			shift
			;;
		*)
			break
			;;
	esac
done

# Throw an error if less than two arguments are supplied:
if [ $# -le 1 ]
then
	echo
	echo "${red}ERROR:${reset} This script must be run with at least two parameters:"
	echo "       [--force] package name, package version"
	echo "       and optional: The actual package name to sign, and also the PostgreSQL version to build against"
	echo
	exit 1
fi

# The name of the package in the git tree (pgpool-II-41, postgresql-16, etc)
packagename=$1
# Actual package name to sign (postgresql16, pgpool-II, postgis34, etc).
signPackageName=$2
# Optional: The PostgreSQL major version the package will be built against.
# Leave empty to build against all supported PostgreSQL versions.
buildVersion=$3

#################################
#	Build packages		#
#################################

#########################
#   Non-Free repo	#
#########################

# If the package is in "non-free", then search the package for all of the values in the
# "pgStableBuilds" parameter (a.k.a. supported versions), and build them. After all of the
# packages are built, sign them.

if [ -x ~/git/pgrpms/rpm/redhat/main/non-free/$packagename/$git_os ]
then
	# Build package against all PostgreSQL versions if 4th parameter is not given:
	if [ "${buildVersion}" == "" ]
	then
		:
	else
		if [[ "${pgStableBuilds[@]}" =~ "${buildVersion}" ]]
		then
			declare -a pgStableBuilds=("${buildVersion}")
		else
			echo "${red}ERROR:${reset} PostgreSQL version ${buildVersion} is not supported."
			exit 1
		fi
	fi

	for packageBuildVersion in ${pgStableBuilds[@]}
	do
		if [ -x ~/git/pgrpms/rpm/redhat/$packageBuildVersion/$packagename/$git_os ]
		then
			cd ~/git/pgrpms/rpm/redhat/$packageBuildVersion/$packagename/$git_os
			if [ $force_mode -eq 0 ] && is_already_built ~/rpm${packageBuildVersion}/RPMS $packageBuildVersion; then
				echo "${yellow}$packagename is already built ($already_built_version) against PostgreSQL $packageBuildVersion. Skipping (use --force to rebuild).${reset}"
				cd
				continue
			fi
			echo "${green}Ok, building $packagename on $git_os against PostgreSQL $packageBuildVersion${reset}"
			sleep 1
			echo "time make build${packageBuildVersion}"
			if ! time make build${packageBuildVersion}; then
				packageVersion=`rpmspec --define "pgmajorversion ${pgAlphaVersion}" -q --qf "%{name}: %{Version}\n" *.spec 2>/dev/null |head -n 1 | awk -F ': ' '{print $2}'`
				cd
				log_build_failure "$packagename" "$packageBuildVersion" "non-free"
				exit 1
			fi
			# Get the package version after building the package so that we get the latest version:
			packageVersion=`rpmspec --define "pgmajorversion ${pgAlphaVersion}" -q --qf "%{name}: %{Version}\n" *.spec |head -n 1 | awk -F ': ' '{print $2}'`
			cd
			sign_package rpm${packageBuildVersion}
		else
			echo "${yellow}Skipping PostgreSQL $packageBuildVersion - package not available for this version${reset}"
		fi
	done
	exit 0
fi # End of non-free build

#################################
#   Package is not available!	#
#################################

echo "${red}ERROR:${reset} Package does not exist in any of the repos"
exit 1
