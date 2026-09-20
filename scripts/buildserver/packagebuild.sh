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
force_mode=0
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
		--force)
			force_mode=1
			shift
			;;
		*)
			break
			;;
	esac
done

# Throw an error if no package name is supplied:
	if [ $# -lt 1 ]
	then
		echo
		echo "${red}ERROR:${reset} This script must be run with at least the name of the package:"
		echo "       $0 [--beta] [--testing] [--force] <git-package-name> [sign-name] [pg-version]"
		echo "       sign-name is not used any more, as the RPMs to sign come from the spec file."
		echo "       It is only accepted so that existing commands keep working. Give '-' for it"
		echo "       if you need pg-version, which restricts the build to one PostgreSQL major version."
		echo
	exit 1
	fi

# Stop now if packages cannot be signed, instead of after a long build:
check_gpg_agent || exit 1

# Set when a package which was built is not signed, so that the script exits
# with an error at the end:
sign_failed=0

# The name of the package in the git tree (pgpool-II-41, postgresql-16, etc)
packagename=$1
# Not used any more (was: the package name to sign, e.g. postgresql16), as the
# RPMs to sign come from the spec file. Kept so that existing commands still work.
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
		cd ~/git/pgrpms/rpm/redhat/$pgBetaVersion/$packagename/$git_os
		if [ $force_mode -eq 0 ] && is_already_built ~/rpm${pgBetaVersion}testing/RPMS $pgBetaVersion; then
			echo "${yellow}$packagename is already built ($already_built_version) for PostgreSQL $pgBetaVersion beta. Skipping (use --force to rebuild).${reset}"
			sign_built_rpms "rpm${pgBetaVersion}testing" $pgBetaVersion
			cd
			exit 0
		fi
		echo "${green}Ok, building $packagename on $git_os for PostgreSQL $pgBetaVersion beta:${reset}"
		sleep 1
		if ! time make "build${pgBetaVersion}testing"; then
			packageVersion=`rpmspec --define "pgmajorversion ${pgBetaVersion}" -q --qf "%{name}: %{Version}\n" *.spec 2>/dev/null |head -n 1 | awk -F ': ' '{print $2}'`
			cd
			log_build_failure "$packagename" "$pgBetaVersion" "beta_testing"
			exit 1
		fi
		packageVersion=`rpmspec --define "pgmajorversion ${pgBetaVersion}" -q --qf "%{name}: %{Version}\n" *.spec |head -n 1 | awk -F ': ' '{print $2}'`
		sign_built_rpms "rpm${pgBetaVersion}testing" $pgBetaVersion || sign_failed=1
		cd
		exit $sign_failed
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
		cd ~/git/pgrpms/rpm/redhat/main/common/$packagename/$git_os
		if [ $force_mode -eq 0 ] && is_already_built ~/rpmcommontesting/RPMS $pgAlphaVersion; then
			echo "${yellow}$packagename is already built ($already_built_version) for the common testing repo. Skipping (use --force to rebuild).${reset}"
			sign_built_rpms rpmcommontesting $pgAlphaVersion
			cd
			exit 0
		fi
		echo "${green}Ok, this is a common package, and I am building $packagename for $git_os for common testing repo.${reset}"
		sleep 1
		if ! time make commonbuildtesting; then
			packageVersion=`rpmspec --define "pgmajorversion ${pgAlphaVersion}" -q --qf "%{name}: %{Version}\n" *.spec 2>/dev/null |head -n 1 | awk -F ': ' '{print $2}'`
			cd
			log_build_failure "$packagename" "common" "common_testing"
			exit 1
		fi
	else
		cd ~/git/pgrpms/rpm/redhat/main/common/$packagename/$git_os
		if [ $force_mode -eq 0 ] && is_already_built ~/rpmcommon/RPMS $pgAlphaVersion; then
			echo "${yellow}$packagename is already built ($already_built_version) for the common repo. Skipping (use --force to rebuild).${reset}"
			sign_built_rpms rpmcommon $pgAlphaVersion
			cd
			exit 0
		fi
		echo "${green}Ok, this is a common package, and I am building $packagename for $git_os for common repo.${reset}"
		sleep 1
		if ! time make commonbuild; then
			packageVersion=`rpmspec --define "pgmajorversion ${pgAlphaVersion}" -q --qf "%{name}: %{Version}\n" *.spec 2>/dev/null |head -n 1 | awk -F ': ' '{print $2}'`
			cd
			log_build_failure "$packagename" "common" "common"
			exit 1
		fi
	fi
	# Get the package version after building the package so that we get the latest version:
	packageVersion=`rpmspec --define "pgmajorversion ${pgAlphaVersion}" -q --qf "%{name}: %{Version}\n" *.spec |head -n 1 | awk -F ': ' '{print $2}'`
	if [ $testing_mode -eq 1 ]
	then
		sign_built_rpms rpmcommontesting $pgAlphaVersion || sign_failed=1
	else
		sign_built_rpms rpmcommon $pgAlphaVersion || sign_failed=1
	fi
	cd
	exit $sign_failed
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
			cd ~/git/pgrpms/rpm/redhat/$packageBuildVersion/$packagename/$git_os
			if [ $testing_mode -eq 1 ]
			then
				if [ $force_mode -eq 0 ] && is_already_built ~/rpm${packageBuildVersion}testing/RPMS $packageBuildVersion; then
					echo "${yellow}$packagename is already built ($already_built_version) against PostgreSQL $packageBuildVersion testing. Skipping (use --force to rebuild).${reset}"
					sign_built_rpms rpm${packageBuildVersion} $packageBuildVersion
					cd
					continue
				fi
				echo "${green}Ok, building $packagename on $git_os against PostgreSQL $packageBuildVersion testing${reset}"
				sleep 1
				if ! time make build${packageBuildVersion}testing; then
					packageVersion=`rpmspec --define "pgmajorversion ${pgAlphaVersion}" -q --qf "%{name}: %{Version}\n" *.spec 2>/dev/null |head -n 1 | awk -F ': ' '{print $2}'`
					cd
					log_build_failure "$packagename" "$packageBuildVersion" "testing"
					exit 1
				fi
			else
				if [ $force_mode -eq 0 ] && is_already_built ~/rpm${packageBuildVersion}/RPMS $packageBuildVersion; then
					echo "${yellow}$packagename is already built ($already_built_version) against PostgreSQL $packageBuildVersion. Skipping (use --force to rebuild).${reset}"
					sign_built_rpms rpm${packageBuildVersion} $packageBuildVersion
					cd
					continue
				fi
				echo "${green}Ok, building $packagename on $git_os against PostgreSQL $packageBuildVersion${reset}"
				sleep 1
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
			sign_built_rpms rpm${packageBuildVersion} $packageBuildVersion || sign_failed=1
			cd
		else
			echo "${yellow}Skipping PostgreSQL $packageBuildVersion - package not available for this version${reset}"
		fi
	done
exit $sign_failed
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
			cd ~/git/pgrpms/rpm/redhat/main/extras/$packagename/$git_os
			if [ $force_mode -eq 0 ] && is_already_built ~/pgdg.extrastesting/RPMS $pgAlphaVersion; then
				echo "${yellow}$packagename is already built ($already_built_version) for the extras testing repo. Skipping (use --force to rebuild).${reset}"
				sign_built_rpms pgdg $pgAlphaVersion
				cd
				exit 0
			fi
			echo "${green}Ok, building $packagename on $git_os testing repo:${reset}"
			sleep 1
			if ! time make extrasbuildtesting; then
				packageVersion=`rpmspec --define "pgmajorversion ${pgAlphaVersion}" -q --qf "%{name}: %{Version}\n" *.spec 2>/dev/null |head -n 1 | awk -F ': ' '{print $2}'`
				cd
				log_build_failure "$packagename" "extras" "extras_testing"
				exit 1
			fi
		else
			cd ~/git/pgrpms/rpm/redhat/main/extras/$packagename/$git_os
			if [ $force_mode -eq 0 ] && is_already_built ~/pgdg.extras/RPMS $pgAlphaVersion; then
				echo "${yellow}$packagename is already built ($already_built_version) for the extras repo. Skipping (use --force to rebuild).${reset}"
				sign_built_rpms pgdg $pgAlphaVersion
				cd
				exit 0
			fi
			echo "${green}Ok, building $packagename on $git_os:${reset}"
			sleep 1
			if ! time make extrasbuild; then
				packageVersion=`rpmspec --define "pgmajorversion ${pgAlphaVersion}" -q --qf "%{name}: %{Version}\n" *.spec 2>/dev/null |head -n 1 | awk -F ': ' '{print $2}'`
				cd
				log_build_failure "$packagename" "extras" "extras"
				exit 1
			fi
		fi
		packageVersion=`rpmspec --define "pgmajorversion ${pgAlphaVersion}" -q --qf "%{name}: %{Version}\n" *.spec |head -n 1 | awk -F ': ' '{print $2}'`
		sign_built_rpms pgdg $pgAlphaVersion || sign_failed=1
		cd
		exit $sign_failed
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
