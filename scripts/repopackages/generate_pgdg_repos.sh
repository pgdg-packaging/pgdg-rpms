#!/usr/bin/bash

#################################################
#						#
# Generate PGDG .repo files			#
# Devrim Gündüz <devrim@gunduz.org> - 2026	#
#						#
#################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source global.sh for color codes if running as postgres (uid 26)
# shellcheck source=/dev/null
[[ -f "${SCRIPT_DIR}/global.sh" ]] && [[ "$(id -u)" == "26" ]] && \
	source "${SCRIPT_DIR}/global.sh"

# Fallback color definitions - mirrors global.sh; no-op if already sourced above
: "${red:=$(tput setaf 1 2>/dev/null)}"
: "${green:=$(tput setaf 2 2>/dev/null)}"
: "${blue:=$(tput setaf 4 2>/dev/null)}"
: "${reset:=$(tput sgr0 2>/dev/null)}"

##############################################################
# Configuration
# Mirrors the logic in sync_pgdg_rpms_config.sh.
# Do NOT source that file - it lives on a different server.
##############################################################

# PostgreSQL versions
PG_ALL_VERSIONS=(18 17 16 15 14)		# Stable releases (all OS types)
PG_TEST_VERSIONS=(19 18 17 16 15 14)		# Testing repos for RHEL/Fedora

# Per-OS-version maximum supported PostgreSQL major version.
# Stanzas for PG versions above this limit are omitted from that OS's repo file.
# Variable naming: PG_MAX_VER_{osdistro}_{osmajor}  (leave unset = no restriction)
# SLES equivalent would be e.g. PG_MAX_VER_sles_15=18
PG_MAX_VER_redhat_8=18			# RHEL 8: PG19+ not supported

# RHEL: valid OS versions and architectures
VALID_VER_redhat=("10.2" "10.1" "10.0" "10" "9.8" "9.7" "9.6" "9" "8.10")
VALID_ARCH_redhat=("x86_64" "aarch64" "ppc64le")
EXTRASREPOSENABLED_redhat=1
SYNCTESTINGREPOS_redhat=1

# Fedora: version list is for reference/sync only; single file uses $releasever
VALID_VER_fedora=("44" "43")
VALID_ARCH_fedora=("x86_64")
EXTRASREPOSENABLED_fedora=0		# No extras repo for Fedora currently
SYNCTESTINGREPOS_fedora=1

# SLES: one file per major version (uses $releasever for minor versions)
VALID_SLES_MAJOR_VERSIONS=(15 16)	# Generates pgdg-suse-all-sles{N}.repo
VALID_ARCH_sles=("x86_64")
EXTRASREPOSENABLED_sles=1
SYNCTESTINGREPOS_sles=1
# PG version constraints differ from RHEL:
#   - Stable binary + stable debuginfo: all PG_ALL_VERSIONS (incl. PG14)
#   - Testing binary, source, and testing debuginfo: PG15 and above only
#   - Stable source: PG15 and above only (no pgdg14-source on SLES)
SLES_TEST_VERSIONS=(19 18 17 16 15)	# "Available for v15 and above"
SLES_SOURCE_VERSIONS=(18 17 16 15)	# Stable source; PG14 excluded

# openSUSE Leap: same constraints as SLES but different URL path
VALID_LEAP_MAJOR_VERSIONS=(16)		# Generates pgdg-opensuse-all-leap{N}.repo
VALID_ARCH_opensuse=("x86_64")
EXTRASREPOSENABLED_leap=1
SYNCTESTINGREPOS_leap=1

# Default output directory
OUTPUT_DIR="."

##############################################################
# Usage / option parsing
##############################################################

usage() {
	cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Generate PGDG .repo/.service files for all supported platforms.

Output filenames:
  pgdg-redhat-all-rhel{VER}.repo            (RHEL x86_64, default)
  pgdg-redhat-all-rhel{VER}-aarch64.repo
  pgdg-redhat-all-rhel{VER}-ppc64le.repo
  pgdg-fedora-all.repo                      (Fedora; version-agnostic via \$releasever)
  pgdg-suse-all-sles{N}.repo               (SLES 15, 16)
  pgdg-opensuse-all-leap{N}.repo           (openSUSE Leap 16)

Options:
  -O, --os OS             Generate only for this OS type; repeatable
                          Valid: redhat fedora sles opensuse
  -o, --output-dir DIR    Output directory (default: current directory)
  -v, --ver VERSION       RHEL only: filter to this OS version (e.g. 10.0)
  -a, --arch ARCH         RHEL only: filter to this architecture (e.g. aarch64)
  -n, --dry-run           List files that would be generated without writing them
  -h, --help              Show this help

Notes:
  -v and -a apply only to RHEL. For other OS types, use -O to select which
  platforms to generate. Without -O, all platforms are generated.
  Fedora, SLES, and Leap files are skipped when -v is given (RHEL-specific)
  or when -a specifies a non-x86_64 arch, unless explicitly requested via -O.

Valid RHEL versions : ${VALID_VER_redhat[*]}
Valid RHEL arches  : ${VALID_ARCH_redhat[*]}
Valid Fedora vers. : ${VALID_VER_fedora[*]} (reference only; single output file)
Valid Fedora arches: ${VALID_ARCH_fedora[*]}
Valid SLES major   : ${VALID_SLES_MAJOR_VERSIONS[*]}
Valid SLES arches  : ${VALID_ARCH_sles[*]}
Valid Leap major   : ${VALID_LEAP_MAJOR_VERSIONS[*]}
Valid Leap arches  : ${VALID_ARCH_opensuse[*]}

Examples:
  $(basename "$0")                        # All platforms
  $(basename "$0") -O redhat              # RHEL only
  $(basename "$0") -O sles -O opensuse    # SLES + Leap only
  $(basename "$0") -O redhat -v 10.0      # RHEL 10.0 all arches
  $(basename "$0") -O redhat -v 10.0 -a x86_64
  $(basename "$0") -o /srv/repofiles      # Custom output directory
EOF
}

FILTER_OS=()
FILTER_VER=""
FILTER_ARCH=""
DRY_RUN=0

while [[ $# -gt 0 ]]; do
	case "$1" in
		-O|--os)		FILTER_OS+=("$2"); shift 2 ;;
		-o|--output-dir)	OUTPUT_DIR="$2";   shift 2 ;;
		-v|--ver)		FILTER_VER="$2";   shift 2 ;;
		-a|--arch)		FILTER_ARCH="$2";  shift 2 ;;
		-n|--dry-run)		DRY_RUN=1;         shift   ;;
		-h|--help)		usage; exit 0 ;;
		*)
			echo "${red}ERROR:${reset} Unknown option: $1"
			echo
			usage
			exit 1
			;;
	esac
done

##############################################################
# Helper functions
##############################################################

in_array() {
	local needle="$1"; shift
	local v
	for v in "$@"; do [[ "$v" == "$needle" ]] && return 0; done
	return 1
}

# Returns 0 if pgver is supported for the given OS type + major version.
# Reads PG_MAX_VER_{osdistro}_{osmajor}; if unset, all versions are supported.
pg_supported() {
	local osdistro="$1" osmajor="$2" pgver="$3"
	local max_var="PG_MAX_VER_${osdistro}_${osmajor}"
	local max_pg="${!max_var}"
	[[ -n "$max_pg" && "$pgver" -gt "$max_pg" ]] && return 1
	return 0
}

# Returns 0 if the given OS type should be generated.
# If FILTER_OS is empty: all OS types are enabled, subject to -v/-a heuristics.
# If FILTER_OS is set: only explicitly listed OS types are enabled.
os_enabled() {
	local os="$1"
	[[ "${#FILTER_OS[@]}" -eq 0 ]] && return 0
	in_array "$os" "${FILTER_OS[@]}"
}

# Returns 0 if a single-file OS (Fedora, SLES, Leap) should be generated.
# When called without --os, respects -v and -a as implicit RHEL-only signals.
# When called with explicit --os X, always generates regardless of -v/-a.
should_gen_singlefile_os() {
	local os="$1"
	# If explicitly requested via --os, always generate
	in_array "$os" "${FILTER_OS[@]}" && return 0
	# If --os is given but doesn't include this OS, skip
	[[ "${#FILTER_OS[@]}" -gt 0 ]] && return 1
	# No --os: skip if -v is set (implies RHEL-specific run)
	[[ -n "$FILTER_VER" ]] && return 1
	# No --os: skip if -a is set to an arch not supported by this OS.
	# Uses bash indirect expansion so updating VALID_ARCH_fedora /
	# VALID_ARCH_sles / VALID_ARCH_opensuse is all that's needed here.
	if [[ -n "$FILTER_ARCH" ]]; then
		local arch_var="VALID_ARCH_${os}[@]"
		in_array "$FILTER_ARCH" "${!arch_var}" || return 1
	fi
	return 0
}

# Return the correct GPG key filename for a given RHEL architecture
get_rhel_gpgkey() {
	case "$1" in
		aarch64)	echo "PGDG-RPM-GPG-KEY-AARCH64-RHEL" ;;
		*)		echo "PGDG-RPM-GPG-KEY-RHEL" ;;
	esac
}

# Append a blank line + one or more comment lines to a file
write_comment() {
	local f="$1"; shift
	echo >> "$f"
	local line
	for line in "$@"; do printf '# %s\n' "$line" >> "$f"; done
}

# Append a blank line + a DNF/YUM stanza (RHEL/Fedora style)
# 7th arg (type): "rhel" (default) or "fedora"
#   rhel:   gpgcheck=1
#   fedora: pkg_gpgcheck=1 + priority=1
write_stanza() {
	local f="$1" id="$2" name="$3" baseurl="$4" enabled="$5" gpgkey="$6"
	local type="${7:-rhel}"
	{
		printf '\n[%s]\n'                             "$id"
		printf 'name=%s\n'                            "$name"
		printf 'baseurl=%s\n'                         "$baseurl"
		printf 'enabled=%s\n'                         "$enabled"
		if [[ "$type" == "fedora" ]]; then
			printf 'pkg_gpgcheck=1\n'
		else
			printf 'gpgcheck=1\n'
		fi
		printf 'gpgkey=file:///etc/pki/rpm-gpg/%s\n' "$gpgkey"
		printf 'repo_gpgcheck = 1\n'
		[[ "$type" == "fedora" ]] && printf 'priority=1\n'
	} >> "$f"
}

# Append a blank line + a zypper stanza (SLES/Leap style)
# autorefresh: 1 for main/extras/stable stanzas; 0 for testing/source/debuginfo
# gpgkey path is /etc/pki/ (no rpm-gpg subdirectory, unlike RHEL)
write_suse_stanza() {
	local f="$1" id="$2" name="$3" baseurl="$4" enabled="$5" gpgkey="$6" autorefresh="$7"
	{
		printf '\n[%s]\n'                        "$id"
		printf 'name=%s\n'                       "$name"
		printf 'baseurl=%s\n'                    "$baseurl"
		printf 'enabled=%s\n'                    "$enabled"
		printf 'autorefresh=%s\n'                "$autorefresh"
		printf 'type=rpm-md\n'
		printf 'gpgcheck=1\n'
		printf 'gpgkey=file:///etc/pki/%s\n'     "$gpgkey"
		printf 'keeppackages=0\n'
		printf 'priority=1\n'
	} >> "$f"
}

##############################################################
# Generate one RHEL .repo file (one OS version × one arch)
##############################################################

generate_redhat_repo() {
	local osver="$1" arch="$2"

	local osmajor="${osver%%.*}"
	local gpgkey; gpgkey=$(get_rhel_gpgkey "$arch")

	# x86_64 is the default — no arch suffix in the filename
	local archsuffix=""
	[[ "$arch" != "x86_64" ]] && archsuffix="-${arch}"
	local outfile="${OUTPUT_DIR}/pgdg-redhat-all-rhel${osver}${archsuffix}.repo"

	# Human-readable OS label used in stanza name= fields
	local osdesc="RHEL / Rocky Linux / AlmaLinux ${osver}"

	# $basearch is a DNF/YUM variable resolved at install time — escape from bash
	local OSURL="redhat/rhel-${osver}-\$basearch"
	local YUM_BASE="https://download.postgresql.org/pub/repos/yum"
	local SRPM_BASE="https://dnf-srpms.postgresql.org/srpms"
	local DBG_BASE="https://dnf-debuginfo.postgresql.org"

	if [[ "$DRY_RUN" -eq 1 ]]; then
		echo "${blue}[dry-run]${reset} $(basename "$outfile")"
		return 0
	fi

	echo "${green}Generating:${reset} $(basename "$outfile")"

	# ── File header ──────────────────────────────────────────────────
	{
		printf '#########################################################################\n'
		printf '# PGDG Red Hat Enterprise Linux / Rocky Linux / AlmaLinux repositories\t#\n'
		printf '#########################################################################\n'
		printf '\n'
		printf '# PGDG Red Hat Enterprise Linux / Rocky Linux / AlmaLinux stable common\n'
		printf '# repository for all PostgreSQL versions\n'
	} > "$outfile"

	# ── Common ───────────────────────────────────────────────────────
	write_stanza "$outfile" \
		"pgdg-common" \
		"PostgreSQL common RPMs for ${osdesc} - \$basearch" \
		"${YUM_BASE}/common/${OSURL}" \
		1 "$gpgkey"

	# ── Extras ───────────────────────────────────────────────────────
	if [[ "${EXTRASREPOSENABLED_redhat}" -eq 1 ]]; then
		write_comment "$outfile" \
			"We provide extra packages to support some of the RPMs in the PostgreSQL RPM" \
			"repo, like consul, etcd, haproxy, etc."
		write_stanza "$outfile" \
			"pgdg-rhel${osmajor}-extras" \
			"Extra packages to support some RPMs in the PostgreSQL RPM repo for ${osdesc} - \$basearch" \
			"${YUM_BASE}/extras/${OSURL}" \
			0 "$gpgkey"
		write_stanza "$outfile" \
			"pgdg-rhel${osmajor}-extras-testing" \
			"Extra packages to support some RPMs in the PostgreSQL RPM repo for ${osdesc} - \$basearch - Updates testing" \
			"${YUM_BASE}/testing/extras/${OSURL}" \
			0 "$gpgkey"
	fi

	# ── Stable per-version repos ──────────────────────────────────────
	write_comment "$outfile" \
		"PGDG Red Hat Enterprise Linux / Rocky Linux / AlmaLinux stable repositories:"
	local pgver
	for pgver in "${PG_ALL_VERSIONS[@]}"; do
		pg_supported "redhat" "$osmajor" "$pgver" || continue
		write_stanza "$outfile" \
			"pgdg${pgver}" \
			"PostgreSQL ${pgver} for ${osdesc} - \$basearch" \
			"${YUM_BASE}/${pgver}/${OSURL}" \
			1 "$gpgkey"
	done

	# ── Testing repos ─────────────────────────────────────────────────
	if [[ "${SYNCTESTINGREPOS_redhat}" -eq 1 ]]; then
		write_comment "$outfile" \
			"PGDG RHEL / Rocky Linux / AlmaLinux Updates Testing common repositories."
		write_stanza "$outfile" \
			"pgdg-common-testing" \
			"PostgreSQL common testing RPMs for ${osdesc} - \$basearch" \
			"${YUM_BASE}/testing/common/${OSURL}" \
			0 "$gpgkey"

		write_comment "$outfile" \
			"PGDG RHEL / Rocky Linux / AlmaLinux Updates Testing repositories. (These packages should not be used in production)" \
			"Available for PostgreSQL 14 and above."
		for pgver in "${PG_TEST_VERSIONS[@]}"; do
			pg_supported "redhat" "$osmajor" "$pgver" || continue
			write_stanza "$outfile" \
				"pgdg${pgver}-updates-testing" \
				"PostgreSQL ${pgver} for ${osdesc} - \$basearch - Updates testing" \
				"${YUM_BASE}/testing/${pgver}/${OSURL}" \
				0 "$gpgkey"
		done
	fi

	# ── Source (SRPM) repos ───────────────────────────────────────────
	write_comment "$outfile" \
		"PGDG Red Hat Enterprise Linux / Rocky Linux / AlmaLinux SRPM testing common repository"
	write_stanza "$outfile" \
		"pgdg-common-source" \
		"PostgreSQL common SRPMs for ${osdesc} - \$basearch - Source" \
		"${SRPM_BASE}/common/${OSURL}" \
		0 "$gpgkey"

	if [[ "${EXTRASREPOSENABLED_redhat}" -eq 1 ]]; then
		write_comment "$outfile" \
			"PGDG RHEL / Rocky Linux / AlmaLinux Extras SRPM repository"
		write_stanza "$outfile" \
			"pgdg-rhel${osmajor}-extras-source" \
			"SRPMs of the Extras packages to support some RPMs in the PostgreSQL RPM repo ${osdesc} - \$basearch" \
			"${SRPM_BASE}/extras/${OSURL}" \
			0 "$gpgkey"
	fi

	if [[ "${SYNCTESTINGREPOS_redhat}" -eq 1 ]]; then
		write_comment "$outfile" \
			"PGDG RHEL / Rocky Linux / AlmaLinux testing common SRPM repository for all PostgreSQL versions"
		write_stanza "$outfile" \
			"pgdg-common-testing-source" \
			"PostgreSQL common testing SRPMs for ${osdesc} - \$basearch" \
			"${SRPM_BASE}/testing/common/${OSURL}" \
			0 "$gpgkey"

		if [[ "${EXTRASREPOSENABLED_redhat}" -eq 1 ]]; then
			write_comment "$outfile" \
				"PGDG RHEL / Rocky Linux / AlmaLinux Extras Testing SRPM repository"
			write_stanza "$outfile" \
				"pgdg-rhel${osmajor}-extras-testing-source" \
				"SRPMs of the Extras packages to support some RPMs in the PostgreSQL RPM repo ${osdesc} - \$basearch" \
				"${SRPM_BASE}/testing/extras/${OSURL}" \
				0 "$gpgkey"
		fi
	fi

	# Source RPMs: testing-only versions first, then stable interleaved
	write_comment "$outfile" "PGDG Source RPMs (SRPMS) and their testing repositories:"

	if [[ "${SYNCTESTINGREPOS_redhat}" -eq 1 ]]; then
		for pgver in "${PG_TEST_VERSIONS[@]}"; do
			pg_supported "redhat" "$osmajor" "$pgver" || continue
			if ! in_array "$pgver" "${PG_ALL_VERSIONS[@]}"; then
				write_stanza "$outfile" \
					"pgdg${pgver}-updates-testing-source" \
					"PostgreSQL ${pgver} for ${osdesc} - \$basearch - Source updates testing" \
					"${SRPM_BASE}/testing/${pgver}/${OSURL}" \
					0 "$gpgkey"
			fi
		done
	fi

	for pgver in "${PG_ALL_VERSIONS[@]}"; do
		pg_supported "redhat" "$osmajor" "$pgver" || continue
		write_stanza "$outfile" \
			"pgdg${pgver}-source" \
			"PostgreSQL ${pgver} for ${osdesc} - \$basearch - Source" \
			"${SRPM_BASE}/${pgver}/${OSURL}" \
			0 "$gpgkey"
		if [[ "${SYNCTESTINGREPOS_redhat}" -eq 1 ]]; then
			write_stanza "$outfile" \
				"pgdg${pgver}-updates-testing-source" \
				"PostgreSQL ${pgver} for ${osdesc} - \$basearch - Source updates testing" \
				"${SRPM_BASE}/testing/${pgver}/${OSURL}" \
				0 "$gpgkey"
		fi
	done

	# ── Debuginfo repos ───────────────────────────────────────────────
	write_comment "$outfile" \
		"Debuginfo / debugsource repositories for the common repo"
	write_stanza "$outfile" \
		"pgdg-common-debuginfo" \
		"PostgreSQL common RPMs for ${osdesc} - \$basearch - Debuginfo" \
		"${DBG_BASE}/debug/common/${OSURL}" \
		0 "$gpgkey"

	write_comment "$outfile" \
		"Debuginfo / debugsource packages for stable repos"
	for pgver in "${PG_ALL_VERSIONS[@]}"; do
		pg_supported "redhat" "$osmajor" "$pgver" || continue
		write_stanza "$outfile" \
			"pgdg${pgver}-debuginfo" \
			"PostgreSQL ${pgver} for ${osdesc} - \$basearch - Debuginfo" \
			"${DBG_BASE}/debug/${pgver}/${OSURL}" \
			0 "$gpgkey"
	done

	if [[ "${SYNCTESTINGREPOS_redhat}" -eq 1 ]]; then
		write_comment "$outfile" \
			"Debuginfo / debugsource packages for testing repos" \
			"Available for PostgreSQL 14 and above."
		for pgver in "${PG_TEST_VERSIONS[@]}"; do
			pg_supported "redhat" "$osmajor" "$pgver" || continue
			write_stanza "$outfile" \
				"pgdg${pgver}-updates-testing-debuginfo" \
				"PostgreSQL ${pgver} for ${osdesc} - \$basearch - Debuginfo" \
				"${DBG_BASE}/testing/debug/${pgver}/${OSURL}" \
				0 "$gpgkey"
		done
	fi

	echo "${green}Done:${reset}       $(basename "$outfile")"
}

##############################################################
# Generate the single Fedora repo file
# (version-agnostic; $releasever and $basearch resolved by DNF)
##############################################################

generate_fedora_repo() {
	local gpgkey="PGDG-RPM-GPG-KEY-Fedora"
	local outfile="${OUTPUT_DIR}/pgdg-fedora-all.repo"

	# Both $releasever and $basearch are DNF variables — escape both from bash
	local osdesc="Fedora \$releasever"
	local OSURL="fedora/fedora-\$releasever-\$basearch"
	local YUM_BASE="https://download.postgresql.org/pub/repos/yum"
	local SRPM_BASE="https://dnf-srpms.postgresql.org/srpms"
	local DBG_BASE="https://dnf-debuginfo.postgresql.org"

	if [[ "$DRY_RUN" -eq 1 ]]; then
		echo "${blue}[dry-run]${reset} $(basename "$outfile")"
		return 0
	fi

	echo "${green}Generating:${reset} $(basename "$outfile")"

	# ── File header ──────────────────────────────────────────────────
	{
		printf '#################################\n'
		printf '# PGDG Fedora repositories\t#\n'
		printf '#################################\n'
		printf '\n'
		printf '# PGDG Fedora stable common repository for all PostgreSQL versions\n'
	} > "$outfile"

	# ── Common ───────────────────────────────────────────────────────
	write_stanza "$outfile" \
		"pgdg-common" \
		"PostgreSQL common RPMs for ${osdesc} - \$basearch" \
		"${YUM_BASE}/common/${OSURL}" \
		1 "$gpgkey" "fedora"

	# ── Extras (disabled; placeholder for future use) ─────────────────
	if [[ "${EXTRASREPOSENABLED_fedora}" -eq 1 ]]; then
		write_comment "$outfile" \
			"We provide extra packages to support some of the RPMs in the PostgreSQL RPM" \
			"repo, like consul, etcd, haproxy, etc."
		write_stanza "$outfile" \
			"pgdg-fedora-extras" \
			"Extra packages to support some RPMs in the PostgreSQL RPM repo for ${osdesc} - \$basearch" \
			"${YUM_BASE}/extras/${OSURL}" \
			0 "$gpgkey" "fedora"
		write_stanza "$outfile" \
			"pgdg-fedora-extras-testing" \
			"Extra packages to support some RPMs in the PostgreSQL RPM repo for ${osdesc} - \$basearch - Updates testing" \
			"${YUM_BASE}/testing/extras/${OSURL}" \
			0 "$gpgkey" "fedora"
	fi

	# ── Stable per-version repos ──────────────────────────────────────
	write_comment "$outfile" "PGDG Fedora stable repositories"
	local pgver
	for pgver in "${PG_ALL_VERSIONS[@]}"; do
		write_stanza "$outfile" \
			"pgdg${pgver}" \
			"PostgreSQL ${pgver} for ${osdesc} - \$basearch" \
			"${YUM_BASE}/${pgver}/${OSURL}" \
			1 "$gpgkey" "fedora"
	done

	# ── Testing repos ─────────────────────────────────────────────────
	if [[ "${SYNCTESTINGREPOS_fedora}" -eq 1 ]]; then
		write_comment "$outfile" "PGDG Fedora testing common repository"
		write_stanza "$outfile" \
			"pgdg-common-testing" \
			"PostgreSQL common testing RPMs for ${osdesc} - \$basearch" \
			"${YUM_BASE}/testing/common/${OSURL}" \
			0 "$gpgkey" "fedora"

		write_comment "$outfile" \
			"PGDG Fedora Updates Testing repositories (These packages should not be used in production)." \
			"Available for PostgreSQL 14 and above."
		for pgver in "${PG_TEST_VERSIONS[@]}"; do
			write_stanza "$outfile" \
				"pgdg${pgver}-updates-testing" \
				"PostgreSQL ${pgver} for ${osdesc} - \$basearch - Updates testing" \
				"${YUM_BASE}/testing/${pgver}/${OSURL}" \
				0 "$gpgkey" "fedora"
		done
	fi

	# ── Source (SRPM) repos ───────────────────────────────────────────
	# Note: pgdg-common-source name has no "- Source" suffix (Fedora convention)
	write_comment "$outfile" \
		"PGDG Fedora stable common SRPM repository for all PostgreSQL versions"
	write_stanza "$outfile" \
		"pgdg-common-source" \
		"PostgreSQL common SRPMs for ${osdesc} - \$basearch" \
		"${SRPM_BASE}/common/${OSURL}" \
		0 "$gpgkey" "fedora"

	if [[ "${SYNCTESTINGREPOS_fedora}" -eq 1 ]]; then
		write_comment "$outfile" \
			"PGDG Fedora testing common SRPM repository for all PostgreSQL versions"
		write_stanza "$outfile" \
			"pgdg-common-testing-source" \
			"PostgreSQL common testing SRPMs for ${osdesc} - \$basearch" \
			"${SRPM_BASE}/testing/common/${OSURL}" \
			0 "$gpgkey" "fedora"
	fi

	# Source RPMs: testing-only versions first, then stable interleaved
	write_comment "$outfile" "Source RPMs (SRPM), and their testing repositories"

	if [[ "${SYNCTESTINGREPOS_fedora}" -eq 1 ]]; then
		for pgver in "${PG_TEST_VERSIONS[@]}"; do
			if ! in_array "$pgver" "${PG_ALL_VERSIONS[@]}"; then
				write_stanza "$outfile" \
					"pgdg${pgver}-updates-testing-source" \
					"PostgreSQL ${pgver} for ${osdesc} - \$basearch - Source updates testing" \
					"${SRPM_BASE}/testing/${pgver}/${OSURL}" \
					0 "$gpgkey" "fedora"
			fi
		done
	fi

	for pgver in "${PG_ALL_VERSIONS[@]}"; do
		write_stanza "$outfile" \
			"pgdg${pgver}-source" \
			"PostgreSQL ${pgver} for ${osdesc} - \$basearch - Source" \
			"${SRPM_BASE}/${pgver}/${OSURL}" \
			0 "$gpgkey" "fedora"
		if [[ "${SYNCTESTINGREPOS_fedora}" -eq 1 ]]; then
			write_stanza "$outfile" \
				"pgdg${pgver}-updates-testing-source" \
				"PostgreSQL ${pgver} for ${osdesc} - \$basearch - Source updates testing" \
				"${SRPM_BASE}/testing/${pgver}/${OSURL}" \
				0 "$gpgkey" "fedora"
		fi
	done

	# ── Debuginfo repos ───────────────────────────────────────────────
	# Note: Fedora uses "Debuginfo/debugsource" (no spaces) and testing stanza
	# names end in "- Debuginfo testing" (not "- Debuginfo")
	write_comment "$outfile" \
		"Debuginfo/debugsource repositories for the common repo"
	write_stanza "$outfile" \
		"pgdg-common-debuginfo" \
		"PostgreSQL common RPMs for ${osdesc} - \$basearch - Debuginfo" \
		"${DBG_BASE}/debug/common/${OSURL}" \
		0 "$gpgkey" "fedora"

	write_comment "$outfile" \
		"Debuginfo/debugsource repositories for stable repos"
	for pgver in "${PG_ALL_VERSIONS[@]}"; do
		write_stanza "$outfile" \
			"pgdg${pgver}-debuginfo" \
			"PostgreSQL ${pgver} for ${osdesc} - \$basearch - Debuginfo" \
			"${DBG_BASE}/debug/${pgver}/${OSURL}" \
			0 "$gpgkey" "fedora"
	done

	if [[ "${SYNCTESTINGREPOS_fedora}" -eq 1 ]]; then
		write_comment "$outfile" \
			"Debuginfo/debugsource repositories for testing repos"
		for pgver in "${PG_TEST_VERSIONS[@]}"; do
			write_stanza "$outfile" \
				"pgdg${pgver}-updates-testing-debuginfo" \
				"PostgreSQL ${pgver} for ${osdesc} - \$basearch - Debuginfo testing" \
				"${DBG_BASE}/testing/debug/${pgver}/${OSURL}" \
				0 "$gpgkey" "fedora"
		done
	fi

	echo "${green}Done:${reset}       $(basename "$outfile")"
}

##############################################################
# Generate one SLES or openSUSE Leap repo file
#
# osmajor : 15 or 16
# ostype  : "sles" or "leap"
#
# Key differences between SLES 15 and SLES 16 / Leap 16:
#   - GPG key:   PGDG-RPM-GPG-KEY-SLES15  vs  PGDG-RPM-GPG-KEY-SLES16
#   - Stanza IDs: SLES15 uses "pgdg-{VER}" and "pgdg-{VER}-updates-testing"
#                 SLES16/Leap use "pgdg{VER}" and "pgdg{VER}-updates-testing"
#                 (stable source and all debuginfo use no-dash style in both)
#   - URL path:  suse/sles-$releasever-$basearch  vs  opensuse/leap-$releasever-$basearch
#
# SLES PG version scope (differs from RHEL/Fedora):
#   - Stable binary + stable debuginfo: all PG_ALL_VERSIONS (incl. PG14)
#   - Testing binary, source, testing debuginfo: SLES_TEST_VERSIONS (PG15+)
#   - Stable source: SLES_SOURCE_VERSIONS (PG15+; no pgdg14-source on SLES)
##############################################################

generate_suse_repo() {
	local osmajor="$1" ostype="$2"

	local gpgkey="PGDG-RPM-GPG-KEY-SLES${osmajor}"

	# Resolve OS-type-specific values
	local outfile urlpath
	if [[ "$ostype" == "sles" ]]; then
		outfile="${OUTPUT_DIR}/pgdg-suse-all-sles${osmajor}.repo"
		urlpath="suse/sles-\$releasever-\$basearch"
	else
		outfile="${OUTPUT_DIR}/pgdg-opensuse-all-leap${osmajor}.repo"
		urlpath="opensuse/leap-\$releasever-\$basearch"
	fi

	# Feature flags: resolve per-ostype values without eval
	local extras_enabled sync_testing
	case "$ostype" in
		sles)
			extras_enabled=$EXTRASREPOSENABLED_sles
			sync_testing=$SYNCTESTINGREPOS_sles
			;;
		leap)
			extras_enabled=$EXTRASREPOSENABLED_leap
			sync_testing=$SYNCTESTINGREPOS_leap
			;;
	esac

	# SLES 15 uses dashes before PG version numbers in certain stanza IDs;
	# SLES 16 and Leap 16 do not. The prefix variable vpfx captures this.
	# Stanzas affected:   stable binary, testing binary, testing source
	# Stanzas NOT affected (always no-dash): stable source, all debuginfo
	local vpfx
	[[ "$osmajor" == "15" ]] && vpfx="pgdg-" || vpfx="pgdg"

	local YUM_BASE="https://download.postgresql.org/pub/repos/zypp"
	local DBG_BASE="https://zypp-debuginfo.postgresql.org"
	# Note: SLES SRPMs are served from the same zypp base (not a separate host)
	local SRPM_BASE="${YUM_BASE}/srpms"

	# Both $releasever and $basearch are zypper variables — escape from bash
	local OSURL="${urlpath}"	# already contains \$releasever and \$basearch

	if [[ "$DRY_RUN" -eq 1 ]]; then
		echo "${blue}[dry-run]${reset} $(basename "$outfile")"
		return 0
	fi

	echo "${green}Generating:${reset} $(basename "$outfile")"

	# ── File header ──────────────────────────────────────────────────
	{
		printf '#################################################\n'
		printf '# PGDG SuSE Enterprise Linux repositories.\t#\n'
		printf '#################################################\n'
		printf '\n'
		printf '# PGDG SuSE Enterprise Linux stable common repository for all PostgreSQL versions\n'
	} > "$outfile"

	# ── Common (autorefresh=1) ────────────────────────────────────────
	write_suse_stanza "$outfile" \
		"pgdg-common" \
		"PostgreSQL common RPMs for SLES \$releasever - \$basearch" \
		"${YUM_BASE}/common/${OSURL}" \
		1 "$gpgkey" 1

	# ── Extras (autorefresh=1 even when disabled) ─────────────────────
	if [[ "${extras_enabled}" -eq 1 ]]; then
		write_comment "$outfile" \
			"We provide extra packages to support some RPMs in the PostgreSQL RPM repo, like" \
			"consul, haproxy, etc."
		write_suse_stanza "$outfile" \
			"pgdg-sles${osmajor}-extras" \
			"Extra packages to support some RPMs in the PostgreSQL RPM repo SLES \$releasever - \$basearch" \
			"${YUM_BASE}/extras/${OSURL}" \
			0 "$gpgkey" 1
		write_suse_stanza "$outfile" \
			"pgdg-sles${osmajor}-extras-testing" \
			"Extra packages to support some RPMs in the PostgreSQL RPM repo SLES \$releasever - \$basearch - Updates testing" \
			"${YUM_BASE}/testing/extras/${OSURL}" \
			0 "$gpgkey" 0
	fi

	# ── Stable per-version repos (autorefresh=1) ──────────────────────
	write_comment "$outfile" "PGDG SuSE Enterprise Linux stable repositories:"
	local pgver
	for pgver in "${PG_ALL_VERSIONS[@]}"; do
		pg_supported "$ostype" "$osmajor" "$pgver" || continue
		write_suse_stanza "$outfile" \
			"${vpfx}${pgver}" \
			"PostgreSQL ${pgver} SLES \$releasever - \$basearch" \
			"${YUM_BASE}/${pgver}/${OSURL}" \
			1 "$gpgkey" 1
	done

	# ── Testing repos (autorefresh=1 for common, 0 for per-version) ───
	if [[ "${sync_testing}" -eq 1 ]]; then
		write_comment "$outfile" \
			"PGDG SuSE Enterprise Linux Updates Testing common repositories."
		write_suse_stanza "$outfile" \
			"pgdg-common-testing" \
			"PostgreSQL common testing RPMs for SuSE Enterprise Linux \$releasever - \$basearch" \
			"${YUM_BASE}/testing/common/${OSURL}" \
			0 "$gpgkey" 1

		write_comment "$outfile" \
			"PGDG SuSE Enterprise Linux Updates Testing repositories. (These packages should not be used in production)" \
			"Available for v15 and above."
		for pgver in "${SLES_TEST_VERSIONS[@]}"; do
			pg_supported "$ostype" "$osmajor" "$pgver" || continue
			write_suse_stanza "$outfile" \
				"${vpfx}${pgver}-updates-testing" \
				"PostgreSQL ${pgver} SLES \$releasever - \$basearch - Updates testing" \
				"${YUM_BASE}/testing/${pgver}/${OSURL}" \
				0 "$gpgkey" 0
		done
	fi

	# ── Source (SRPM) repos (all autorefresh=0) ───────────────────────
	write_comment "$outfile" \
		"PGDG SuSE Enterprise Linux SRPM testing common repository"
	write_suse_stanza "$outfile" \
		"pgdg-source-common" \
		"PostgreSQL common repository for SuSE Enterprise Linux \$releasever - \$basearch - Source" \
		"${SRPM_BASE}/common/${OSURL}" \
		0 "$gpgkey" 0

	if [[ "${sync_testing}" -eq 1 ]]; then
		write_comment "$outfile" \
			"PGDG SuSE Enterprise Linux testing common SRPM repository for all PostgreSQL versions"
		write_suse_stanza "$outfile" \
			"pgdg-common-srpm-testing" \
			"PostgreSQL common testing SRPMs for SuSE Enterprise Linux \$releasever - \$basearch" \
			"${SRPM_BASE}/testing/common/${OSURL}" \
			0 "$gpgkey" 0
	fi

	# Source RPMs: testing-only versions first (PG19), then stable interleaved
	# Stable source covers SLES_SOURCE_VERSIONS only (no pgdg14-source on SLES)
	write_comment "$outfile" "PGDG Source RPMs (SRPMS), and their testing repositories:"

	if [[ "${sync_testing}" -eq 1 ]]; then
		# Testing-only versions: those in SLES_TEST_VERSIONS but not SLES_SOURCE_VERSIONS
		for pgver in "${SLES_TEST_VERSIONS[@]}"; do
			pg_supported "$ostype" "$osmajor" "$pgver" || continue
			if ! in_array "$pgver" "${SLES_SOURCE_VERSIONS[@]}"; then
				write_suse_stanza "$outfile" \
					"${vpfx}${pgver}-source-updates-testing" \
					"PostgreSQL ${pgver} SLES \$releasever - \$basearch - SRPM Updates testing" \
					"${SRPM_BASE}/testing/${pgver}/${OSURL}" \
					0 "$gpgkey" 0
			fi
		done
	fi

	# Stable source versions interleaved with their testing counterparts
	# Note: stable source stanzas always use "pgdg{VER}-source" (no vpfx dash)
	for pgver in "${SLES_SOURCE_VERSIONS[@]}"; do
		pg_supported "$ostype" "$osmajor" "$pgver" || continue
		write_suse_stanza "$outfile" \
			"pgdg${pgver}-source" \
			"PostgreSQL ${pgver} for SuSE Enterprise Linux \$releasever - \$basearch - Source" \
			"${SRPM_BASE}/${pgver}/${OSURL}" \
			0 "$gpgkey" 0
		if [[ "${sync_testing}" -eq 1 ]]; then
			write_suse_stanza "$outfile" \
				"${vpfx}${pgver}-source-updates-testing" \
				"PostgreSQL ${pgver} SLES \$releasever - \$basearch - SRPM Updates testing" \
				"${SRPM_BASE}/testing/${pgver}/${OSURL}" \
				0 "$gpgkey" 0
		fi
	done

	# ── Debuginfo repos (all autorefresh=0) ───────────────────────────
	# Stable debuginfo covers ALL PG_ALL_VERSIONS (incl. PG14, unlike source)
	# Debuginfo stanza IDs always use no-dash style (even in SLES 15)
	write_comment "$outfile" "Debuginfo/debugsource packages for stable repos"
	for pgver in "${PG_ALL_VERSIONS[@]}"; do
		pg_supported "$ostype" "$osmajor" "$pgver" || continue
		write_suse_stanza "$outfile" \
			"pgdg${pgver}-debuginfo" \
			"PostgreSQL ${pgver} for SuSE Enterprise Linux \$releasever - \$basearch - Debuginfo" \
			"${DBG_BASE}/debug/${pgver}/${OSURL}" \
			0 "$gpgkey" 0
	done

	if [[ "${sync_testing}" -eq 1 ]]; then
		write_comment "$outfile" \
			"Debuginfo/debugsource packages for testing repos" \
			"Available for v15 and above."
		for pgver in "${SLES_TEST_VERSIONS[@]}"; do
			pg_supported "$ostype" "$osmajor" "$pgver" || continue
			write_suse_stanza "$outfile" \
				"pgdg${pgver}-updates-testing-debuginfo" \
				"PostgreSQL ${pgver} for SuSE Enterprise Linux \$releasever - \$basearch - Debuginfo" \
				"${DBG_BASE}/testing/debug/${pgver}/${OSURL}" \
				0 "$gpgkey" 0
		done
	fi

	echo "${green}Done:${reset}       $(basename "$outfile")"
}

##############################################################
# Validate options
##############################################################

for os_filter in "${FILTER_OS[@]}"; do
	if ! in_array "$os_filter" "redhat" "fedora" "sles" "opensuse"; then
		echo "${red}ERROR:${reset} Unknown OS type: ${os_filter}"
		echo "Valid OS types: redhat fedora sles opensuse"
		exit 1
	fi
done

if [[ -n "$FILTER_VER" ]] && ! in_array "$FILTER_VER" "${VALID_VER_redhat[@]}"; then
	echo "${red}ERROR:${reset} Unknown RHEL version: ${FILTER_VER}"
	echo "Valid versions: ${VALID_VER_redhat[*]}"
	exit 1
fi

if [[ -n "$FILTER_ARCH" ]] && ! in_array "$FILTER_ARCH" "${VALID_ARCH_redhat[@]}"; then
	echo "${red}ERROR:${reset} Unknown architecture: ${FILTER_ARCH}"
	echo "Valid architectures: ${VALID_ARCH_redhat[*]}"
	exit 1
fi

if [[ "$DRY_RUN" -eq 0 ]]; then
	mkdir -p "$OUTPUT_DIR" || {
		echo "${red}ERROR:${reset} Cannot create output directory: ${OUTPUT_DIR}"
		exit 1
	}
fi

##############################################################
# Main loop
##############################################################

echo "${blue}PGDG Repo File Generator${reset}"
echo "${blue}Output directory : ${OUTPUT_DIR}${reset}"
[[ "${#FILTER_OS[@]}" -gt 0 ]] && echo "${blue}Filter OS        : ${FILTER_OS[*]}${reset}"
[[ -n "$FILTER_VER" ]]         && echo "${blue}Filter version   : ${FILTER_VER}${reset}"
[[ -n "$FILTER_ARCH" ]]        && echo "${blue}Filter arch      : ${FILTER_ARCH}${reset}"
[[ "$DRY_RUN" -eq 1 ]]         && echo "${blue}Mode             : DRY RUN (no files will be written)${reset}"
echo

count=0

# RHEL (uses -v and -a filtering)
if os_enabled "redhat"; then
	for osver in "${VALID_VER_redhat[@]}"; do
		[[ -n "$FILTER_VER"  && "$osver" != "$FILTER_VER"  ]] && continue
		for arch in "${VALID_ARCH_redhat[@]}"; do
			[[ -n "$FILTER_ARCH" && "$arch" != "$FILTER_ARCH" ]] && continue
			generate_redhat_repo "$osver" "$arch"
			((count++))
		done
	done
fi

# Fedora: single version-agnostic file
if should_gen_singlefile_os "fedora"; then
	generate_fedora_repo
	((count++))
fi

# SLES: one file per major version
if should_gen_singlefile_os "sles"; then
	for osmajor in "${VALID_SLES_MAJOR_VERSIONS[@]}"; do
		generate_suse_repo "$osmajor" "sles"
		((count++))
	done
fi

# openSUSE Leap: one file per major version
if should_gen_singlefile_os "opensuse"; then
	for osmajor in "${VALID_LEAP_MAJOR_VERSIONS[@]}"; do
		generate_suse_repo "$osmajor" "leap"
		((count++))
	done
fi

echo
if [[ "$DRY_RUN" -eq 1 ]]; then
	echo "${green}Would generate ${count} file(s).${reset}"
else
	echo "${green}Generated ${count} file(s) in ${OUTPUT_DIR}.${reset}"
fi
