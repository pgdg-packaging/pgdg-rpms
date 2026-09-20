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

# Print the file names of the binary RPMs that the spec file in the current
# directory produces, named exactly the way rpmbuild names them, one per
# line (e.g. "foo-1.0-1PGDG.f45.x86_64.rpm").
# Usage: spec_rpm_files <pgmajorversion>
spec_rpm_files() {
	local pg_version="$1"
	local specfile
	specfile=$(ls *.spec 2>/dev/null | head -n 1)

	[ -z "$specfile" ] && return 1

	rpmspec --define "pgmajorversion ${pg_version}" \
		--define "pginstdir /usr/pgsql-${pg_version}" \
		--define "pgpackageversion ${pg_version}" \
		-q --qf "%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}.rpm\n" "$specfile" 2>/dev/null
}

# Check whether every binary RPM a spec file would produce already exists
# in the given RPMS directory, so that packagebuild.sh (and friends) can
# skip a rebuild that would otherwise just re-stamp already-published RPMs
# and break mirror timestamps. Use packagebuild.sh's --force to bypass.
# Usage: is_already_built <rpms_dir> <pgmajorversion>
# Must be called from inside the package's build directory (the one
# containing the *.spec file).
# On success (return 0), sets the global $already_built_version to the
# package's "version-release" (e.g. "2.4.0-1PGDG.f44") so callers can
# include it in their skip message.
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
	expected_rpms=$(spec_rpm_files "$pg_version")

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

	already_built_version=$(rpmspec --define "pgmajorversion ${pg_version}" \
		--define "pginstdir /usr/pgsql-${pg_version}" \
		--define "pgpackageversion ${pg_version}" \
		-q --qf "%{VERSION}-%{RELEASE}\n" "$specfile" 2>/dev/null | head -n 1)

	return 0
}

# Read RPM paths from stdin (one per line) and print the ones which are not
# signed yet, so that rpmsign only runs for those. Starting rpmsign for every
# RPM is much slower than this, as the RPMs are queried in batches and only
# the header of each RPM is read. Anything that cannot be confirmed as signed (unsigned,
# unreadable, or a file name that is not NAME-VERSION-RELEASE.ARCH.rpm) is
# printed as well, so it goes to rpmsign, which then signs it or reports why not.
list_unsigned_rpms() {
	local paths
	local qf='%|RSAHEADER?{s}:{%|DSAHEADER?{s}:{n}|}| %{NAME}-%{VERSION}-%{RELEASE}.%|SOURCERPM?{%{ARCH}}:{src}|.rpm\n'

	paths=$(grep -v '^$')
	[ -z "$paths" ] && return 0

	# One stream for awk: the names of the signed RPMs ("S") first, then the paths ("P").
	{
		echo "$paths" | xargs -d '\n' -r rpm -qp --nosignature --qf "$qf" 2>/dev/null | sed -n 's/^s /S\t/p'
		echo "$paths" | awk -F/ '{ print "P\t" $NF "\t" $0 }'
	} | awk -F'\t' '$1 == "S" { signed[$2]; next } !($2 in signed) { print $3 }'
}

# Check that a gpg-agent is running to sign with. The build scripts call this
# at the start, so that a long build is not wasted on packages which then
# cannot be signed.
check_gpg_agent() {
	if ! pgrep -x gpg-agent > /dev/null; then
		echo "${red}ERROR:${reset} GPG agent is not running. Start it with: gpg-agent --daemon"
		return 1
	fi
	return 0
}

# Remove the leftovers which get in the way of signing.
clean_signing_leftovers() {
	# Remove all files with .sig suffix. They are leftovers which appear
	# when signing process is not completed. Signing will be broken when
	# they exist.
	find ~/rpm* pgdg* -iname "*.sig" -print0 | xargs -0 /bin/rm -v -rf

	# Remove all buildreqs.nosrc packages:
	find ~/rpm* pgdg* -iname "*buildreqs.nosrc*" -print0 | xargs -0 /bin/rm -v -rf
}

# Read RPM paths from stdin (one per line) and sign the ones that are not
# signed yet with rpmsign, using gpg-agent (the passphrase should be preset in
# the agent cache). Packages which already carry a signature are skipped. Set
# FORCE_RESIGN=1 to run rpmsign on all of them anyway.
# A package that cannot be signed does not stop the others from being signed.
# The ones that failed are listed at the end, and the function returns 1.
sign_rpm_files() {
	local all_packages to_sign failed_list="" rpm_path

	all_packages=$(grep -v '^$')
	if [ "${FORCE_RESIGN:-0}" == 1 ]; then
		to_sign="$all_packages"
	else
		to_sign=$(echo "$all_packages" | list_unsigned_rpms)
		echo "Already signed, skipping: $(( $(echo "$all_packages" | grep -c .) - $(echo "$to_sign" | grep -c .) ))"
	fi

	for rpm_path in $to_sign; do
		echo "Signing: $rpm_path"
		if ! rpmsign --addsign "$rpm_path"; then
			echo "${red}ERROR:${reset} Failed to sign $rpm_path"
			failed_list="$failed_list $rpm_path"
		fi
	done

	if [ -n "$failed_list" ]; then
		echo "${red}ERROR:${reset} These packages are NOT signed:"
		for rpm_path in $failed_list; do
			echo "  $rpm_path"
		done
		return 1
	fi

	echo "${green}Package signing completed${reset}"
	return 0
}

# Common function to sign packages using GPG agent.
# Usage: sign_package <rpm_location>
# Signs the RPMs under ~/<rpm_location>*/ that match the $signPackageName and
# $packageVersion patterns (signallpackages.sh sets both to "*" to sign
# everything). The build scripts do not use this: they use sign_built_rpms.
sign_package() {
	# The first parameter refers to the location of the RPMs:
	local rpm_location="$1"

	clean_signing_leftovers

	check_gpg_agent || return 1

	echo "${green}Signing packages in ${rpm_location}...${reset}"

	find ~/"${rpm_location}"* -iname "*${signPackageName}*${packageVersion}*.rpm" | grep -v ALL | sign_rpm_files
}

# Print the file name patterns of every RPM that the spec file in the current
# directory can produce, one per line: for the name of each binary package and
# of the source package, the RPM itself plus its -debuginfo and -debugsource
# RPMs, each with the version and release from the spec file, e.g.
# "foo-libs-1.0-1PGDG.f45.*.rpm". Everything comes from the spec file, so
# nothing has to be typed by a human, and only the RPMs of this package match,
# even if other packages are built into the same directory at the same time.
# Usage: spec_rpm_patterns <pgmajorversion>
spec_rpm_patterns() {
	local pg_version="$1"
	local specfile version_release name suffix
	local -a defines=(--define "pgmajorversion ${pg_version}" \
		--define "pginstdir /usr/pgsql-${pg_version}" \
		--define "pgpackageversion ${pg_version}")

	specfile=$(ls *.spec 2>/dev/null | head -n 1)
	[ -z "$specfile" ] && return 1

	version_release=$(rpmspec "${defines[@]}" -q --qf "%{VERSION}-%{RELEASE}\n" "$specfile" 2>/dev/null | head -n 1)
	[ -z "$version_release" ] && return 1

	{
		rpmspec "${defines[@]}" -q --qf "%{NAME}\n" "$specfile" 2>/dev/null
		rpmspec --srpm "${defines[@]}" -q --qf "%{NAME}\n" "$specfile" 2>/dev/null
	} | sort -u | while IFS= read -r name; do
		[ -z "$name" ] && continue
		for suffix in "" "-debuginfo" "-debugsource"; do
			echo "${name}${suffix}-${version_release}.*.rpm"
		done
	done
}

# Check that the RPMs of the spec file in the current directory (every binary
# RPM from spec_rpm_files, plus the source RPM) exist below ~/<rpm_location>*/
# and are signed. This does not depend on any name typed by a human, so it
# catches a package which was left unsigned for any reason. Lists what is
# missing or NOT signed, and returns 1 if there is anything.
# Usage: verify_built_rpms <rpm_location> <pgmajorversion>
verify_built_rpms() {
	local rpm_location="$1"
	local pg_version="$2"
	local specfile expected rpm_file matches found_list="" unsigned bad=0

	specfile=$(ls *.spec 2>/dev/null | head -n 1)
	expected=$(spec_rpm_files "$pg_version")
	if [ -z "$expected" ]; then
		echo "${red}ERROR:${reset} Cannot tell which RPMs ${specfile:-the spec file} produces, so cannot check that they are signed."
		return 1
	fi
	expected="$expected"$'\n'$(rpmspec --srpm --define "pgmajorversion ${pg_version}" \
		--define "pginstdir /usr/pgsql-${pg_version}" \
		--define "pgpackageversion ${pg_version}" \
		-q --qf "%{NAME}-%{VERSION}-%{RELEASE}.src.rpm\n" "$specfile" 2>/dev/null)

	while IFS= read -r rpm_file; do
		[ -z "$rpm_file" ] && continue
		matches=$(find ~/"${rpm_location}"* -name "$rpm_file" -not -path '*/ALL*' 2>/dev/null)
		if [ -z "$matches" ]; then
			echo "${red}ERROR:${reset} $rpm_file was not found in ~/${rpm_location}*"
			bad=1
		else
			found_list="$found_list$matches"$'\n'
		fi
	done <<< "$expected"

	unsigned=$(echo "$found_list" | list_unsigned_rpms)
	if [ -n "$unsigned" ]; then
		echo "${red}ERROR:${reset} These RPMs are NOT signed:"
		echo "$unsigned" | sed 's/^/  /'
		bad=1
	fi

	if [ $bad -ne 0 ]; then
		return 1
	fi

	echo "${green}All RPMs of this package are signed.${reset}"
	return 0
}

# Sign the RPMs of the spec file in the current directory (found with
# spec_rpm_patterns, so no name is needed), and then check that all of them
# are there and signed. The build scripts call it after a successful build,
# and where they skip a package because it is "already built", so an RPM that
# was left unsigned by a failed signing earlier gets signed on the next run.
# Must be called from inside the package's build directory. Returns 1 if
# something is not signed.
# Usage: sign_built_rpms <rpm_location> <pgmajorversion>
sign_built_rpms() {
	local rpm_location="$1"
	local pg_version="$2"
	local pattern rc=0
	local -a find_args=()

	while IFS= read -r pattern; do
		if [ ${#find_args[@]} -gt 0 ]; then find_args+=(-o); fi
		find_args+=(-name "$pattern")
	done < <(spec_rpm_patterns "$pg_version")

	if [ ${#find_args[@]} -eq 0 ]; then
		echo "${red}ERROR:${reset} Cannot tell which RPMs the spec file produces, so cannot sign them."
		return 1
	fi

	clean_signing_leftovers
	check_gpg_agent || return 1

	echo "${green}Signing packages in ${rpm_location}...${reset}"
	find ~/"${rpm_location}"* \( "${find_args[@]}" \) -not -path '*/ALL*' | sign_rpm_files || rc=1
	verify_built_rpms "$rpm_location" "$pg_version" || rc=1

	return $rc
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
