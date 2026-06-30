#!/usr/bin/bash

#################################################
#						#
# Devrim Gündüz <devrim@gunduz.org> - 2026	#
#						#
#################################################

# Make sure only postgres user can run this script:
if [ "$(id -u)" != "26" ]; then
	clear
	echo
	echo "${red}ERROR:${reset} This script must be run as postgres user" 1>&2
	echo
	exit 1
fi

# Color schemes
red=$(tput setaf 1)
green=$(tput setaf 2)
blue=$(tput setaf 4)
reset=$(tput sgr0)

# OS Configuration
export osmajorversion=10			# Major version: 10, 9, 15, 43
export os="rhel-${osmajorversion}"		# rhel-9, sles-15, leap-16, fedora-43
export osminversion=1				# Will be used to support multiple OS minor versions like SLES 15.7, RHEL 10.1
export osislatest=0				# Is this the latest minor version of the OS or not? 1 or 0
						# CAUTION: Set this to 1 *only if* the OS is the latest stable minor version.
export osarch=x86_64				# x86_64, aarch64, ppc64le
export osdistro=redhat				# fedora, redhat, suse, opensuse
export git_os="EL-${osmajorversion}"		# EL-9, F-43, SLES-15
export extrasrepoenabled=1			# 1 or 0. Currently for RHEL, SLES and OpenSuSE..

# GPG Configuration
export GPG_TTY=$(tty)
# Note: GPG_PASSWORD is kept for backward compatibility with repomd.xml signing
# For package signing, we now use gpg-agent with preset passphrase
export GPG_PASSWORD=foobar
export GPG_KEY_ID=""				# Set this to your signing key ID

# AWS Configuration
export AWS_PAGER=""
export awssrpmurl="s3://dnf-srpms.postgresql.org20250313103537584600000001"		# s3://dnf-srpms.postgresql.org20250313103537584600000001 or s3://zypp-srpms.postgresql.org20250618120322107700000001
export awsdebuginfourl="s3://dnf-debuginfo.postgresql.org20250312201116649700000001"	# s3://dnf-debuginfo.postgresql.org20250312201116649700000001 or s3://zypp-debuginfo.postgresql.org20250312201116651400000002

# CloudFront Configuration
export CF_DEBUG_DISTRO_ID=XXXXXXXXXXXXXXXXXX
export CF_SRPM_DISTRO_ID=XXXXXXXXXXXXXXXXXX

# PostgreSQL Build Versions
declare -a pgStableBuilds=("18 17 16 15 14")
declare -a pgTestBuilds=("19 18 17 16 15 14")
declare -a pgBetaVersion=(19)
declare -a pgAlphaVersion=(20)

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
