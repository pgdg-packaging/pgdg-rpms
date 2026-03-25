#!/usr/bin/bash
# sync_pgdg_rpms_config.sh
# Central configuration file for sync_pgdg_rpms scripts
# Source this file in all related scripts to maintain consistency

# PostgreSQL versions
PG_ALL_VERSIONS=(18 17 16 15 14)     # All supported stable versions
PG_TEST_VERSIONS=(19 18 17 16 15 14)    # Versions available in testing repos

# Valid operating systems
VALID_OS=("redhat" "fedora" "sles" "opensuse")

# Valid architectures per OS
VALID_ARCH_redhat=("aarch64" "ppc64le" "x86_64")
VALID_ARCH_fedora=("x86_64")
VALID_ARCH_sles=("x86_64")
VALID_ARCH_opensuse=("x86_64")

# Valid versions per OS
VALID_VER_redhat=("10.1" "10.0" "9.7" "9.6" "8.10")
VALID_VER_fedora=("43" "42")
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

# OS-specific naming
OSNAME_redhat="rhel"
OSNAME_fedora="fedora"
OSNAME_sles="sles"
OSNAME_opensuse="leap"

OSDISTRO_redhat="redhat"
OSDISTRO_fedora="fedora"
OSDISTRO_sles="suse"
OSDISTRO_opensuse="opensuse"
