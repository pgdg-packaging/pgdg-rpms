#!/usr/bin/bash

#################################################
#						#
# Devrim Gündüz <devrim@gunduz.org> - 2026	#
#						#
#################################################

# Color schemes (defined first -- referenced in the error message right below)
red=$(tput setaf 1)
green=$(tput setaf 2)
blue=$(tput setaf 4)
reset=$(tput sgr0)

# Make sure only postgres user can run this script:
if [ "$(id -u)" != "26" ]; then
	clear
	echo
	echo "${red}ERROR:${reset} This script must be run as postgres user" 1>&2
	echo
	exit 1
fi

#################################################
# Per-host configuration
#################################################
# Everything that differs between build instances (OS version, architecture,
# distro family, signing key, CloudFront distribution) lives in
# ~/bin/global-local.sh instead of here, so global.sh itself can be
# redeployed/updated across every instance without clobbering per-host
# settings. See global-local.sh.example for a template.

if [ ! -f ~/bin/global-local.sh ]; then
	clear
	echo
	echo "${red}ERROR:${reset} ~/bin/global-local.sh not found." 1>&2
	echo "       Copy global-local.sh.example to ~/bin/global-local.sh and" 1>&2
	echo "       fill in this host's OS configuration." 1>&2
	echo
	exit 1
fi

source ~/bin/global-local.sh

# Make sure global-local.sh actually set everything global.sh depends on.
# Uses ${!var+x} rather than -z so that legitimate falsy values like
# osislatest=0 or extrasrepoenabled=0 don't trip this check.
for _required_var in osmajorversion osminversion osislatest osarch osdistro git_os extrasrepoenabled CF_DEBUG_DISTRO_ID CF_SRPM_DISTRO_ID GPG_PASSWORD
do
	if [ -z "${!_required_var+x}" ]; then
		echo "${red}ERROR:${reset} ${_required_var} is not set in ~/bin/global-local.sh" 1>&2
		exit 1
	fi
done
unset _required_var

export osmajorversion osminversion osislatest osarch osdistro git_os extrasrepoenabled CF_DEBUG_DISTRO_ID CF_SRPM_DISTRO_ID GPG_PASSWORD

# GPG Configuration
export GPG_TTY=$(tty)
# GPG_PASSWORD is host-specific (comes from global-local.sh) and is kept
# for backward compatibility with repomd.xml signing. For package signing,
# we now use gpg-agent with preset passphrase.
# GPG_KEY_ID is also host-specific and comes from global-local.sh. Default to
# empty so hosts that don't set it (or haven't been updated yet) keep working.
export GPG_KEY_ID="${GPG_KEY_ID:-}"

# AWS Configuration
export AWS_PAGER=""

# SLES/openSUSE use the zypp buckets, every other distro uses the dnf buckets.
# Derived from osdistro (set in global-local.sh) instead of being hardcoded
# per host -- mirrors the same osdistro check packagesync.sh uses for sync_base.
if [ "$osdistro" == "suse" ] || [ "$osdistro" == "opensuse" ]; then
	export awssrpmurl="s3://zypp-srpms.postgresql.org20250618120322107700000001"
	export awsdebuginfourl="s3://zypp-debuginfo.postgresql.org20250312201116651400000002"
else
	export awssrpmurl="s3://dnf-srpms.postgresql.org20250313103537584600000001"
	export awsdebuginfourl="s3://dnf-debuginfo.postgresql.org20250312201116649700000001"
fi

# PostgreSQL Build Versions
declare -a pgStableBuilds=("18 17 16 15 14")
declare -a pgTestBuilds=("19 18 17 16 15 14")
declare -a pgBetaVersion=(19)
declare -a pgAlphaVersion=(20)

# Make sure the shared logs directory exists (used by packagebuild.sh and reporpmbuild.sh):
mkdir -p ~/bin/logs

# Common function to log build failures. Shared by packagebuild.sh and reporpmbuild.sh.
log_build_failure() {
	local package_name=$1
	local pg_version=$2
	local repo_type=$3
	local timestamp=$(date '+%Y%m%d_%H%M%S')

	# Construct log filename
	if [ -z "$pg_version" ] || [ "$pg_version" == "common" ] || [ "$pg_version" == "extras" ]; then
		log_file=~/bin/logs/${package_name}_${repo_type}_${timestamp}.log
	else
		log_file=~/bin/logs/${package_name}_pg${pg_version}_${timestamp}.log
	fi

	# Write failure information to log
	{
		echo "========================================="
		echo "Build Failure Report"
		echo "========================================="
		echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
		echo "Package: $package_name"
		echo "PostgreSQL Version: ${pg_version:-N/A}"
		echo "Repository Type: $repo_type"
		echo "OS: $git_os"
		echo "Package Version: ${packageVersion:-Unable to determine}"
		echo "========================================="
		echo ""
	} > "$log_file"

	echo "${red}Build failed. Log written to: $log_file${reset}"
}

# Check whether every binary RPM a spec file would produce already exists
# in the given RPMS directory, so that packagebuild.sh (and friends) can
# skip a rebuild that would otherwise just re-stamp already-published RPMs
# and break mirror timestamps. Use packagebuild.sh's --force to bypass.
# Usage: is_already_built <rpms_dir> <pgmajorversion>
# Must be called from inside the package's build directory (the one
# containing the *.spec file).
is_already_built() {
	local rpms_dir="$1"
	local pg_version="$2"
	local specfile
	specfile=$(ls *.spec 2>/dev/null | head -n 1)

	if [ -z "$specfile" ] || [ ! -d "$rpms_dir" ]; then
		return 1
	fi

	# Ask rpmspec for every binary RPM this spec would produce, named
	# exactly the way rpmbuild would name them:
	local expected_rpms
	expected_rpms=$(rpmspec --define "pgmajorversion ${pg_version}" \
		--define "pginstdir /usr/pgsql-${pg_version}" \
		--define "pgpackageversion ${pg_version}" \
		-q --qf "%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}.rpm\n" "$specfile" 2>/dev/null)

	if [ -z "$expected_rpms" ]; then
		return 1
	fi

	local rpm_file arch
	while IFS= read -r rpm_file; do
		arch="${rpm_file%.rpm}"
		arch="${arch##*.}"
		if [ ! -f "${rpms_dir}/${arch}/${rpm_file}" ]; then
			return 1
		fi
	done <<< "$expected_rpms"

	return 0
}

# Common function to sign packages using GPG agent
sign_package() {
	# Remove all files with .sig suffix. They are leftovers which appear
	# when signing process is not completed. Signing will be broken when
	# they exist.
	find ~/rpm* pgdg* -iname "*.sig" -print0 | xargs -0 /bin/rm -v -rf

	# Remove all buildreqs.nosrc packages:
	find ~/rpm* pgdg* -iname "*buildreqs.nosrc*" -print0 | xargs -0 /bin/rm -v -rf

	# Find the packages and sign them using rpmsign with gpg-agent
	# The first parameter refers to the location of the RPMs:
	local rpm_location="$1"

	# Check if GPG agent is running
	if ! pgrep -x gpg-agent > /dev/null; then
		echo "${red}ERROR:${reset} GPG agent is not running. Start it with: gpg-agent --daemon"
		return 1
	fi

	echo "${green}Signing packages in ${rpm_location}...${reset}"

	# Use rpmsign with gpg-agent (passphrase should be preset in agent cache)
	for signpackagelist in $(find ~/"${rpm_location}"* -iname "*${signPackageName}*${packageVersion}*.rpm" | grep -v ALL); do
		echo "Signing: $signpackagelist"
		rpmsign --addsign "$signpackagelist"

		if [ $? -ne 0 ]; then
			echo "${red}ERROR:${reset} Failed to sign $signpackagelist"
			return 1
		fi
	done

	echo "${green}Package signing completed${reset}"
	return 0
}

# Function to preset GPG passphrase in agent (call this once per session)
preset_gpg_passphrase() {
	local keygrip="$1"

	if [ -z "$keygrip" ]; then
		echo "${red}ERROR:${reset} Keygrip is required"
		echo "Find your keygrip with: gpg --with-keygrip -K"
		return 1
	fi

	if [ -z "$GPG_PASSWORD" ]; then
		echo "${red}ERROR:${reset} GPG_PASSWORD is not set"
		return 1
	fi

	echo "$GPG_PASSWORD" | /usr/libexec/gpg-preset-passphrase --preset "$keygrip"		# Replace with /usr/lib/gpg-preset-passphrase on SLES 15. SLES 16 uses RHEL's path

	if [ $? -eq 0 ]; then
		echo "${green}GPG passphrase preset successfully${reset}"
		return 0
	else
		echo "${red}ERROR:${reset} Failed to preset GPG passphrase"
		return 1
	fi
}
