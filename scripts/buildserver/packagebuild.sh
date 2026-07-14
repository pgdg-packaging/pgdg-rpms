#!/usr/bin/bash

#########################################################
#							#
# Devrim Gündüz <devrim@gunduz.org> - 2026		#
#							#
#########################################################

# Include common values:
source ~/bin/global.sh

# Parse command line arguments
beta_mode=0
testing_mode=0
while [[ $# -gt 0 ]]; do
	case $1 in
		--beta)
			beta_mode=1
			shift
			;;
		--testing)
			testing_mode=1
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
		echo "       [--beta] [--testing] package name, package version"
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

#################################
#	Beta repo		#
#################################

if [ $beta_mode -eq 1 ]
then
	# Check if pgBetaVersion is defined and not empty
	if [ -z "${pgBetaVersion}" ]
	then
		echo "${red}ERROR:${reset} Beta mode requested but pgBetaVersion is not defined in global.sh"
		exit 1
	fi

	if [ -x ~/git/pgrpms/rpm/redhat/$pgBetaVersion/$packagename/$git_os ]
	then
		echo "${green}Ok, building $packagename on $git_os for PostgreSQL $pgBetaVersion beta:${reset}"
		sleep 1
		cd ~/git/pgrpms/rpm/redhat/$pgBetaVersion/$packagename/$git_os
		if ! time make "build${pgBetaVersion}testing"; then
			packageVersion=`rpmspec --define "pgmajorversion ${pgBetaVersion}" -q --qf "%{name}: %{Version}\n" *.spec 2>/dev/null |head -n 1 | awk -F ': ' '{print $2}'`
			cd
			log_build_failure "$packagename" "$pgBetaVersion" "beta_testing"
			exit 1
		fi
		packageVersion=`rpmspec --define "pgmajorversion ${pgBetaVersion}" -q --qf "%{name}: %{Version}\n" *.spec |head -n 1 | awk -F ': ' '{print $2}'`
		cd
		sign_package "rpm${pgBetaVersion}testing"
		exit 0
	else
		echo "${red}ERROR:${reset} Package does not exist in PostgreSQL $pgBetaVersion beta"
		exit 1
	fi
fi

# Stable packages can be in 3 places: Either in "common", "non-common" or "extras" directories.
# This script currently ignores "non-free" repo.

#################
# Common repo	#
#################

# If the package is in common, then build it, sign it and exit safely:
if [ -x ~/git/pgrpms/rpm/redhat/main/common/$packagename/$git_os ]
then
	# pgdg-yum is a "common" package on disk, but it doesn't build against a PostgreSQL
	# major version like other common packages do -- it builds against the OS release
	# (repobuild<osmajorversion>.<osminversion>). Use reporpmbuild.sh for that instead:
	if [ "$packagename" == "pgdg-yum" ]
	then
		echo "${red}ERROR:${reset} pgdg-yum is a repo RPM, not a common package build."
		echo "       Use ~/bin/reporpmbuild.sh instead."
		exit 1
	fi

	if [ $testing_mode -eq 1 ]
	then
		echo "${green}Ok, this is a common package, and I am building $packagename for $git_os for common testing repo.${reset}"
		sleep 1
		cd ~/git/pgrpms/rpm/redhat/main/common/$packagename/$git_os
		if ! time make commonbuildtesting; then
			packageVersion=`rpmspec --define "pgmajorversion ${pgAlphaVersion}" -q --qf "%{name}: %{Version}\n" *.spec 2>/dev/null |head -n 1 | awk -F ': ' '{print $2}'`
			cd
			log_build_failure "$packagename" "common" "common_testing"
			exit 1
		fi
	else
		echo "${green}Ok, this is a common package, and I am building $packagename for $git_os for common repo.${reset}"
		sleep 1
		cd ~/git/pgrpms/rpm/redhat/main/common/$packagename/$git_os
		if ! time make commonbuild; then
			packageVersion=`rpmspec --define "pgmajorversion ${pgAlphaVersion}" -q --qf "%{name}: %{Version}\n" *.spec 2>/dev/null |head -n 1 | awk -F ': ' '{print $2}'`
			cd
			log_build_failure "$packagename" "common" "common"
			exit 1
		fi
	fi
	# Get the package version after building the package so that we get the latest version:
	packageVersion=`rpmspec --define "pgmajorversion ${pgAlphaVersion}" -q --qf "%{name}: %{Version}\n" *.spec |head -n 1 | awk -F ': ' '{print $2}'`
	cd
	if [ $testing_mode -eq 1 ]
	then
		sign_package rpmcommontesting
	else
		sign_package rpmcommon
	fi
	exit 0
fi

#########################
#   Non-Common repo	#
#########################

# If the package is in "non-common", then search the package for all of the values in the
# "pgStableBuilds" parameter (a.k.a. supported versions), and build them. After all of the
# packages are built, sign them.

if [ -x ~/git/pgrpms/rpm/redhat/main/non-common/$packagename/$git_os ]
then
	# Select the appropriate build array based on testing mode
	if [ $testing_mode -eq 1 ]
	then
		buildArray=("${pgTestBuilds[@]}")
	else
		buildArray=("${pgStableBuilds[@]}")
	fi

	# Build package against all PostgreSQL versions if 4th parameter is not given:
	if [ "${buildVersion}" == "" ]
	then
		:
	else
		if [[ "${buildArray[@]}" =~ "${buildVersion}" ]]
		then
			declare -a buildArray=("${buildVersion}")
		else
			echo "${red}ERROR:${reset} PostgreSQL version ${buildVersion} is not supported."
			exit 1
		fi
	fi

	for packageBuildVersion in ${buildArray[@]}
	do
		if [ -x ~/git/pgrpms/rpm/redhat/$packageBuildVersion/$packagename/$git_os ]
		then
			if [ $testing_mode -eq 1 ]
			then
				echo "${green}Ok, building $packagename on $git_os against PostgreSQL $packageBuildVersion testing${reset}"
				sleep 1
				cd ~/git/pgrpms/rpm/redhat/$packageBuildVersion/$packagename/$git_os
				if ! time make build${packageBuildVersion}testing; then
					packageVersion=`rpmspec --define "pgmajorversion ${pgAlphaVersion}" -q --qf "%{name}: %{Version}\n" *.spec 2>/dev/null |head -n 1 | awk -F ': ' '{print $2}'`
					cd
					log_build_failure "$packagename" "$packageBuildVersion" "testing"
					exit 1
				fi
			else
				echo "${green}Ok, building $packagename on $git_os against PostgreSQL $packageBuildVersion${reset}"
				sleep 1
				cd ~/git/pgrpms/rpm/redhat/$packageBuildVersion/$packagename/$git_os
				echo "time make build${packageBuildVersion}"
				if ! time make build${packageBuildVersion}; then
					packageVersion=`rpmspec --define "pgmajorversion ${pgAlphaVersion}" -q --qf "%{name}: %{Version}\n" *.spec 2>/dev/null |head -n 1 | awk -F ': ' '{print $2}'`
					cd
					log_build_failure "$packagename" "$packageBuildVersion" "stable"
					exit 1
				fi
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
fi # End of non-common build

#################################
#	 Extras repo		#
#################################

# Build the package in the directly if it is in the "extras" repo.
if [ $extrasrepoenabled = 1 ]
then
# First make sure that extras repo is available for this platform:
	if [ -x ~/git/pgrpms/rpm/redhat/main/extras/$packagename/$git_os ]
	then
		if [ $testing_mode -eq 1 ]
		then
			echo "${green}Ok, building $packagename on $git_os testing repo:${reset}"
			sleep 1
			cd ~/git/pgrpms/rpm/redhat/main/extras/$packagename/$git_os
			if ! time make extrasbuildtesting; then
				packageVersion=`rpmspec --define "pgmajorversion ${pgAlphaVersion}" -q --qf "%{name}: %{Version}\n" *.spec 2>/dev/null |head -n 1 | awk -F ': ' '{print $2}'`
				cd
				log_build_failure "$packagename" "extras" "extras_testing"
				exit 1
			fi
		else
			echo "${green}Ok, building $packagename on $git_os:${reset}"
			sleep 1
			cd ~/git/pgrpms/rpm/redhat/main/extras/$packagename/$git_os
			if ! time make extrasbuild; then
				packageVersion=`rpmspec --define "pgmajorversion ${pgAlphaVersion}" -q --qf "%{name}: %{Version}\n" *.spec 2>/dev/null |head -n 1 | awk -F ': ' '{print $2}'`
				cd
				log_build_failure "$packagename" "extras" "extras"
				exit 1
			fi
		fi
		packageVersion=`rpmspec --define "pgmajorversion ${pgAlphaVersion}" -q --qf "%{name}: %{Version}\n" *.spec |head -n 1 | awk -F ': ' '{print $2}'`
		cd
		sign_package pgdg
		exit 0
	fi
else
	echo "${red}ERROR:${reset} Extras repo is not enabled on this platform"
	exit 1
fi

#################################
#   Package is not available!	#
#################################

echo "${red}ERROR:${reset} Package does not exist in any of the repos"
exit 1
