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

# Refuse to run with the placeholder values of global-local.sh.example (and of
# the Ansible setup playbook), e.g. a forgotten GPG_PASSWORD only shows up
# later as "gpg: signing failed: Operation cancelled".
_placeholder_found=0
if [ "$GPG_PASSWORD" == "foobar" ]; then
	echo "${red}ERROR:${reset} GPG_PASSWORD in ~/bin/global-local.sh is still the placeholder (foobar)" 1>&2
	_placeholder_found=1
fi
for _cf_var in CF_DEBUG_DISTRO_ID CF_SRPM_DISTRO_ID
do
	if [[ "${!_cf_var}" =~ ^X+$ ]]; then
		echo "${red}ERROR:${reset} ${_cf_var} in ~/bin/global-local.sh is still the placeholder (${!_cf_var})" 1>&2
		_placeholder_found=1
	fi
done
if [ $_placeholder_found -ne 0 ]; then
	exit 1
fi
unset _placeholder_found _cf_var

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

# PostgreSQL Build Versions. One array element per version: quoted expansions
# ("${pgStableBuilds[@]}") must see each version separately.
declare -a pgStableBuilds=(18 17 16 15 14)
declare -a pgTestBuilds=(19 18 17 16 15 14)
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

# Extra arguments for every rpmspec call below, for builds that rpmbuild with
# more than the default macros, so that the RPM names match what was built.
# reporpmbuild.sh sets it to (--load ~/.rpmmacros-<OS major version>), the
# same file its make targets load.
rpmspec_extra_args=()

# Print the file names of the binary RPMs that the spec file in the current
# directory produces, named exactly the way rpmbuild names them, one per
# line (e.g. "foo-1.0-1PGDG.f45.x86_64.rpm"). --builtrpms leaves out the
# (sub)packages without a %files section, which rpmbuild does not produce
# (e.g. the main CGAL package of CGAL56, which only has subpackages).
# Usage: spec_rpm_files <pgmajorversion>
spec_rpm_files() {
	local pg_version="$1"
	local specfile
	specfile=$(ls *.spec 2>/dev/null | head -n 1)

	[ -z "$specfile" ] && return 1

	rpmspec "${rpmspec_extra_args[@]}" --define "pgmajorversion ${pg_version}" \
		--define "pginstdir /usr/pgsql-${pg_version}" \
		--define "pgpackageversion ${pg_version}" \
		-q --builtrpms --qf "%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}.rpm\n" "$specfile" 2>/dev/null
}

# rpmspec lists a -debuginfo RPM for every arch dependent (sub)package and a
# -debugsource one, but rpmbuild skips the ones that would be empty (e.g.
# python3-psycopg3-debuginfo on EL 9, as only python3-psycopg3-c has binaries),
# so these may be missing.
# Usage: is_optional_rpm <rpm file name>
is_optional_rpm() {
	case "$1" in
		*-debuginfo-*|*-debugsource-*) return 0 ;;
	esac
	return 1
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
		if [ ! -f "${rpms_dir}/${arch}/${rpm_file}" ] && ! is_optional_rpm "$rpm_file"; then
			return 1
		fi
	done <<< "$expected_rpms"

	already_built_version=$(rpmspec "${rpmspec_extra_args[@]}" --define "pgmajorversion ${pg_version}" \
		--define "pginstdir /usr/pgsql-${pg_version}" \
		--define "pgpackageversion ${pg_version}" \
		-q --qf "%{VERSION}-%{RELEASE}\n" "$specfile" 2>/dev/null | head -n 1)

	return 0
}

# Read RPM paths from stdin (one per line) and print the ones which are not
# signed yet, so that rpmsign only runs for those. Starting rpmsign for every
# RPM is much slower than this, as the RPMs are queried in batches and only
# the header of each RPM is read. Each answer is matched to its path, not to
# its file name, as the same RPM can be in more than one directory (e.g. rpm14
# and rpm14testing) with only one of the copies signed. Anything that cannot be
# confirmed as signed (unsigned or unreadable) is printed as well, so it goes
# to rpmsign, which then signs it or reports why not.
list_unsigned_rpms() {
	local paths answers rpm_path
	local qf='%|RSAHEADER?{s}:{%|DSAHEADER?{s}:{n}|}|\n'

	paths=$(grep -v '^$')
	[ -z "$paths" ] && return 0

	# rpm prints one line per RPM, in the order of the paths, unless an RPM
	# cannot be read. Then the lines cannot be matched to the paths, so ask
	# for each RPM on its own.
	if answers=$(echo "$paths" | xargs -d '\n' -r rpm -qp --nosignature --qf "$qf" 2>/dev/null) \
		&& [ "$(echo "$answers" | grep -c .)" -eq "$(echo "$paths" | grep -c .)" ]; then
		paste -d '\t' <(echo "$answers") <(echo "$paths") | awk -F'\t' '$1 != "s" { print $2 }'
	else
		while IFS= read -r rpm_path; do
			[ "$(rpm -qp --nosignature --qf "$qf" "$rpm_path" 2>/dev/null)" == "s" ] || echo "$rpm_path"
		done <<< "$paths"
	fi
}

# Read RPM paths from stdin (one per line) and print the ones which are
# corrupt: their header or payload digests do not match, e.g. because rpmbuild
# was interrupted while writing the RPM, so that it is truncated. rpm -q only
# reads the header, so it does not notice a truncated payload. This reads each
# RPM in full, so only pass the RPMs which are about to be signed or synced.
# The signature is not checked here. rpm runs once per RPM, as its output
# cannot be matched to the paths when it cannot open one of them.
list_corrupt_rpms() {
	local rpm_path

	while IFS= read -r rpm_path; do
		[ -z "$rpm_path" ] && continue
		rpm -K --nosignature "$rpm_path" > /dev/null 2>&1 || echo "$rpm_path"
	done
}

# Check that the RPMs whose file names are read from stdin (one
# per line) are signed and not corrupt. Repo files have pkg_gpgcheck=1, so
# clients refuse unsigned packages; they must never get into the repos. This
# only checks that a PGP signature is present, not who made it or whether it
# is valid. The header and payload digests of each RPM are checked as well, so
# that a truncated RPM (e.g. from an interrupted rpmbuild) is not synced.
# Returns 1 if any RPM is unsigned, cannot be read or is corrupt.
verify_signed() {
	local line paths output corrupt total queried=0 unsigned=0 bad=0
	local qf='%|RSAHEADER?{%{RSAHEADER:pgpsig}}:{%|DSAHEADER?{%{DSAHEADER:pgpsig}}:{(none)}|}| %{NAME}-%{VERSION}-%{RELEASE}.%|SOURCERPM?{%{ARCH}}:{src}|.rpm\n'

	# Both stdout and stderr are read, so that an RPM which cannot be read
	# is reported (rpm prints "error: ..." for it) and not skipped. A here-string,
	# not process substitution, as the scripts also run under "sh" (POSIX mode),
	# where process substitution does not exist in bash 4.4:
	paths=$(cat)
	total=$(echo "$paths" | grep -c .)
	output=$(echo "$paths" | xargs -d '\n' -r rpm -qp --nosignature --qf "$qf" 2>&1)
	while IFS= read -r line
	do
		case "$line" in
			"")
				continue
				;;
			"(none) "*)
				echo "${red}UNSIGNED:${reset} ${line#"(none) "}"
				queried=$((queried + 1))
				unsigned=$((unsigned + 1))
				;;
			error:*)
				# rpm can print more than one error for an RPM:
				echo "${red}UNREADABLE:${reset} ${line}"
				;;
			*)
				queried=$((queried + 1))
				;;
		esac
	done <<< "$output"

	# The RPMs which rpm could not read printed no line:
	bad=$((unsigned + total - queried))
	if [ $bad -gt 0 ]; then
		echo "${red}ERROR:${reset} $bad of $total new RPMs are unsigned or unreadable."
	fi

	echo "${green}Checking the digests of the $total new RPMs...${reset}"
	corrupt=$(echo "$paths" | list_corrupt_rpms)
	if [ -n "$corrupt" ]; then
		echo "$corrupt" | sed "s/^/${red}CORRUPT:${reset} /"
		echo "${red}ERROR:${reset} $(echo "$corrupt" | grep -c .) of $total new RPMs are corrupt (rpm -K: digests NOT OK). Rebuild them."
		bad=1
	fi

	if [ $bad -gt 0 ]; then
		return 1
	fi

	echo "${green}All $total new RPMs are signed and not corrupt.${reset}"
	return 0
}

# Print the paths of the RPMs below the given directory (e.g.
# /var/lib/pgsql/rpm18) that are not in its staging directories (ALLRPMS,
# ALLDEBUGRPMS and ALLSRPMS) yet, so the RPMs that a sync would add. The debuginfo/debugsource RPMs live in ALLDEBUGRPMS after a
# sync, hence that directory is compared as well. RPMs which are staged
# already were checked when they were staged, so they are not checked again.
# RPMs are compared by file name, size and modification time (rsync -a keeps
# it), as rsync --checksum also replaces a staged RPM with a rebuilt one which
# has the same file name, and that one has to be checked, too.
list_new_rpms() {
	local base="$1"

	# One stream for awk, staged RPMs ("S") first, then the candidates ("C"),
	# so that it also works when the staging directories are empty:
	{
		find "$base/ALLRPMS" "$base/ALLDEBUGRPMS" "$base/ALLSRPMS" -name '*.rpm' -printf 'S\t%f\t%s\t%T@\n' 2>/dev/null
		find "$base/RPMS/$osarch" "$base/RPMS/noarch" "$base/SRPMS" -name '*.rpm' -printf 'C\t%f\t%s\t%T@\t%p\n' 2>/dev/null
	} | awk -F'\t' '{ key = $2 "\t" $3 "\t" int($4) } $1 == "S" { staged[key]; next } !(key in staged) { print $5 }'
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
	local all_packages to_sign corrupt failed_list="" rpm_path

	all_packages=$(grep -v '^$')
	if [ "${FORCE_RESIGN:-0}" == 1 ]; then
		to_sign="$all_packages"
	else
		to_sign=$(echo "$all_packages" | list_unsigned_rpms)
		echo "Already signed, skipping: $(( $(echo "$all_packages" | grep -c .) - $(echo "$to_sign" | grep -c .) ))"
	fi

	# Do not sign corrupt RPMs, so that they cannot be synced:
	corrupt=$(echo "$to_sign" | list_corrupt_rpms)
	for rpm_path in $corrupt; do
		echo "${red}ERROR:${reset} Not signing $rpm_path: it is corrupt (rpm -K: digests NOT OK). Rebuild it."
		failed_list="$failed_list $rpm_path"
	done

	for rpm_path in $to_sign; do
		case " $(echo $corrupt) " in
			*" $rpm_path "*) continue ;;
		esac
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

	version_release=$(rpmspec "${rpmspec_extra_args[@]}" "${defines[@]}" -q --qf "%{VERSION}-%{RELEASE}\n" "$specfile" 2>/dev/null | head -n 1)
	[ -z "$version_release" ] && return 1

	{
		rpmspec "${rpmspec_extra_args[@]}" "${defines[@]}" -q --builtrpms --qf "%{NAME}\n" "$specfile" 2>/dev/null
		rpmspec "${rpmspec_extra_args[@]}" --srpm "${defines[@]}" -q --qf "%{NAME}\n" "$specfile" 2>/dev/null
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
	expected="$expected"$'\n'$(rpmspec "${rpmspec_extra_args[@]}" --srpm --define "pgmajorversion ${pg_version}" \
		--define "pginstdir /usr/pgsql-${pg_version}" \
		--define "pgpackageversion ${pg_version}" \
		-q --qf "%{NAME}-%{VERSION}-%{RELEASE}.src.rpm\n" "$specfile" 2>/dev/null)

	while IFS= read -r rpm_file; do
		[ -z "$rpm_file" ] && continue
		matches=$(find ~/"${rpm_location}"* -name "$rpm_file" -not -path '*/ALL*' 2>/dev/null)
		if [ -z "$matches" ]; then
			is_optional_rpm "$rpm_file" && continue
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
	local patterns pattern rc=0
	local -a find_args=()

	# A here-string, not process substitution, as the scripts also run under
	# "sh" (POSIX mode), where process substitution does not exist in bash 4.4:
	patterns=$(spec_rpm_patterns "$pg_version")
	while IFS= read -r pattern; do
		[ -z "$pattern" ] && continue
		if [ ${#find_args[@]} -gt 0 ]; then find_args+=(-o); fi
		find_args+=(-name "$pattern")
	done <<< "$patterns"

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

	# gpg-preset-passphrase is in /usr/lib on SLES 15, and in /usr/libexec
	# on the other platforms, including SLES 16:
	local preset_cmd
	for preset_cmd in /usr/libexec/gpg-preset-passphrase /usr/lib/gpg-preset-passphrase ""
	do
		[ -x "$preset_cmd" ] && break
	done
	if [ -z "$preset_cmd" ]; then
		echo "${red}ERROR:${reset} gpg-preset-passphrase not found in /usr/libexec or /usr/lib"
		return 1
	fi

	if echo "$GPG_PASSWORD" | "$preset_cmd" --preset "$keygrip"; then
		echo "${green}GPG passphrase preset successfully${reset}"
		return 0
	else
		echo "${red}ERROR:${reset} Failed to preset GPG passphrase"
		return 1
	fi
}

# CloudFront invalidation paths queued by queue_cf_invalidation, per
# distribution. The sync scripts queue the paths while syncing, and send them
# with flush_cf_invalidations, as one invalidation request per distribution.
cf_srpm_invalidation_paths=()
cf_debug_invalidation_paths=()

# Queue the CloudFront invalidation of a repodata directory. Takes "srpm" or
# "debug" (the distribution) and the repodata directory path.
# Only repomd.xml and its signature are invalidated: createrepo puts the
# checksum in the names of the other repodata files, so new metadata never
# reuses a cached name. Do not use wildcard paths here: CloudFront allows only
# 15 wildcard paths in progress per distribution, which the builders syncing
# at the same time exceed, but 3000 file paths.
queue_cf_invalidation() {
	local path
	for path in "$2/repomd.xml" "$2/repomd.xml.asc"
	do
		case "$1" in
			srpm)	cf_srpm_invalidation_paths+=("$path") ;;
			debug)	cf_debug_invalidation_paths+=("$path") ;;
			*)	echo "${red}ERROR:${reset} Unknown CloudFront distribution: $1"; return 1 ;;
		esac
	done
}

# Send the queued CloudFront invalidation paths, one request per distribution,
# and empty the queues. Returns 1 if a request failed.
flush_cf_invalidations() {
	local rc=0

	if [ ${#cf_srpm_invalidation_paths[@]} -gt 0 ]; then
		echo "${green}Invalidating CloudFront caches: ${cf_srpm_invalidation_paths[*]}${reset}"
		aws cloudfront create-invalidation --distribution-id "$CF_SRPM_DISTRO_ID" --paths "${cf_srpm_invalidation_paths[@]}" > /dev/null || rc=1
		cf_srpm_invalidation_paths=()
	fi

	if [ ${#cf_debug_invalidation_paths[@]} -gt 0 ]; then
		echo "${green}Invalidating CloudFront caches: ${cf_debug_invalidation_paths[*]}${reset}"
		aws cloudfront create-invalidation --distribution-id "$CF_DEBUG_DISTRO_ID" --paths "${cf_debug_invalidation_paths[@]}" > /dev/null || rc=1
		cf_debug_invalidation_paths=()
	fi

	if [ $rc -ne 0 ]; then
		echo "${red}ERROR:${reset} Failed to create CloudFront invalidation(s)"
	fi
	return $rc
}
