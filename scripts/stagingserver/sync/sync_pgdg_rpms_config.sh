#!/usr/bin/bash
# sync_pgdg_rpms_config.sh
# Central configuration file for sync_pgdg_rpms scripts
# Source this file in all related scripts to maintain consistency

# PostgreSQL versions
PG_ALL_VERSIONS=(18 17 16 15 14)     # All supported stable versions
PG_TEST_VERSIONS=(20 19 18 17 16 15 14)    # Versions available in testing repos

# Valid operating systems
VALID_OS=("redhat" "fedora" "sles" "opensuse")

# Valid architectures per OS
VALID_ARCH_redhat=("aarch64" "ppc64le" "x86_64")
VALID_ARCH_fedora=("x86_64")
VALID_ARCH_sles=("x86_64")
VALID_ARCH_opensuse=("x86_64")

# Valid versions per OS
VALID_VER_redhat=("10.2" "10.1" "10.0" "9.8" "9.7" "9.6" "8.10")
VALID_VER_fedora=("44" "43")
VALID_VER_sles=("15.6" "15.7" "16.0")
VALID_VER_opensuse=("16.0")

# Base directories per OS
BASE_DIR_redhat="/srv/yum/yum"
BASE_DIR_fedora="/srv/yum/yum"
BASE_DIR_sles="/srv/zypp/zypp"
BASE_DIR_opensuse="/srv/zypp/zypp"

# Feature flags per OS
EXTRASREPOSENABLED_redhat=1
EXTRASREPOSENABLED_fedora=0
EXTRASREPOSENABLED_sles=1
EXTRASREPOSENABLED_opensuse=1

SYNCTESTINGREPOS_redhat=1
SYNCTESTINGREPOS_fedora=1
SYNCTESTINGREPOS_sles=0
SYNCTESTINGREPOS_opensuse=0

SYNCNONFREEREPOS_redhat=1
SYNCNONFREEREPOS_fedora=0
SYNCNONFREEREPOS_sles=0
SYNCNONFREEREPOS_opensuse=0

# Non-free repos are only available for a limited subset of OS versions and
# architectures, independent of VALID_VER_<os>/VALID_ARCH_<os> above (which
# describe the regular repos). Only list versions/architectures here that
# actually have a non-free repo; anything not listed is skipped when
# syncing non-free.
VALID_NONFREE_VER_redhat=("10.2" "10.1" "9.8" "9.7" "8.10")
VALID_NONFREE_VER_fedora=()
VALID_NONFREE_VER_sles=()
VALID_NONFREE_VER_opensuse=()

VALID_NONFREE_ARCH_redhat=("x86_64")
VALID_NONFREE_ARCH_fedora=()
VALID_NONFREE_ARCH_sles=()
VALID_NONFREE_ARCH_opensuse=()

# OS-specific naming
OSNAME_redhat="rhel"
OSNAME_fedora="fedora"
OSNAME_sles="sles"
OSNAME_opensuse="leap"

OSDISTRO_redhat="redhat"
OSDISTRO_fedora="fedora"
OSDISTRO_sles="suse"
OSDISTRO_opensuse="opensuse"

# Per-(OS,version) architecture overrides.
#
# VALID_ARCH_<os> lists the architectures an OS supports in general, but not
# every version of that OS necessarily ships all of them (e.g. a brand-new
# RHEL release may ship x86_64 packages before aarch64/ppc64le catch up).
# List only the exceptions here; any "os:ver" pair not present here uses the
# full VALID_ARCH_<os> list unchanged.
#
# Key format: "<os>:<ver>"   Value: space-separated architecture list
#
# Example:
#   [redhat:10.0]="x86_64 aarch64"    # ppc64le not yet available for 10.0
declare -A VALID_ARCH_OVERRIDES=(
)

# Resolve the valid architecture list for a given OS/version pair into the
# array named by $3 (nameref), honoring VALID_ARCH_OVERRIDES when present
# and falling back to VALID_ARCH_<os> otherwise.
get_valid_arch_for() {
	local os="$1" ver="$2" outvar="$3"
	local -n _get_valid_arch_out="$outvar"
	local key="${os}:${ver}"

	if [[ -n "${VALID_ARCH_OVERRIDES[$key]:-}" ]]; then
		_get_valid_arch_out=(${VALID_ARCH_OVERRIDES[$key]})
	else
		local -n _get_valid_arch_default="VALID_ARCH_${os}"
		_get_valid_arch_out=("${_get_valid_arch_default[@]}")
	fi
}
