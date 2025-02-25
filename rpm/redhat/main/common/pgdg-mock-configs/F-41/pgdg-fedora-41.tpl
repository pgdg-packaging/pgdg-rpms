config_opts['chroot_setup_cmd'] = " install bash bzip2 coreutils cpio diffutils findutils gawk glibc-minimal-langpack grep gzip info lua patch pgdg-srpm-macros python3 redhat-rpm-config rpm-build sed tar unzip util-linux which xz"
config_opts['macros']['%pgmajorversion'] = "17"
config_opts['macros']['%pginstdir'] = "/usr/pgsql-17"
config_opts['macros']['%__brp_check_rpaths'] = "/usr/bin/true"

config_opts['root'] = 'fedora-{{ releasever }}-{{ target_arch }}'

config_opts['description'] = 'Fedora {{ releasever }}'
# fedora 31+ isn't mirrored, we need to run from koji
config_opts['mirrored'] = config_opts['target_arch'] != 'i686'

config_opts['chroot_setup_cmd'] = 'install @{% if mirrored %}buildsys-{% endif %}build'

config_opts['dist'] = 'fc{{ releasever }}'  # only useful for --resultdir variable subst
config_opts['extra_chroot_dirs'] = [ '/run/lock', ]

# https://fedoraproject.org/wiki/Changes/BuildWithDNF5 for Fedora 40+
config_opts['package_manager'] = '{% if releasever|int >= 40 %}dnf5{% else %}dnf{% endif %}'

config_opts['bootstrap_image'] = 'registry.fedoraproject.org/fedora:{{ releasever }}'
config_opts['bootstrap_image_ready'] = int(config_opts['releasever']) >= 41

config_opts['dnf.conf'] = """
[main]
keepcache=1
system_cachedir=/var/cache/dnf
debuglevel=2
reposdir=/dev/null
logfile=/var/log/yum.log
retries=20
obsoletes=1
gpgcheck=0
assumeyes=1
syslog_ident=mock
syslog_device=
install_weak_deps=0
metadata_expire=0
best=1
module_platform_id=platform:f{{ releasever }}
protected_packages=
user_agent={{ user_agent }}


#################################
# PGDG Fedora repositories	#
#################################

# PGDG Fedora stable common repository for all PostgreSQL versions

[pgdg-common]
name=PostgreSQL common RPMs for Fedora $releasever - $basearch
baseurl=https://download.postgresql.org/pub/repos/yum/common/fedora/fedora-$releasever-$basearch
enabled=1
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

# PGDG Fedora stable repositories

[pgdg17]
name=PostgreSQL 17 for Fedora $releasever - $basearch
baseurl=https://download.postgresql.org/pub/repos/yum/17/fedora/fedora-$releasever-$basearch
enabled=1
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg16]
name=PostgreSQL 16 for Fedora $releasever - $basearch
baseurl=https://download.postgresql.org/pub/repos/yum/16/fedora/fedora-$releasever-$basearch
enabled=1
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg15]
name=PostgreSQL 15 for Fedora $releasever - $basearch
baseurl=https://download.postgresql.org/pub/repos/yum/15/fedora/fedora-$releasever-$basearch
enabled=1
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg14]
name=PostgreSQL 14 for Fedora $releasever - $basearch
baseurl=https://download.postgresql.org/pub/repos/yum/14/fedora/fedora-$releasever-$basearch
enabled=1
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg13]
name=PostgreSQL 13 for Fedora $releasever - $basearch
baseurl=https://download.postgresql.org/pub/repos/yum/13/fedora/fedora-$releasever-$basearch
enabled=1
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

# PGDG Fedora testing common repository

[pgdg-common-testing]
name=PostgreSQL common testing RPMs for Fedora $releasever - $basearch
baseurl=https://download.postgresql.org/pub/repos/yum/testing/common/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

# PGDG Fedora Updates Testing repositories (These packages should not be used in production).
# Available for 13 and above.

[pgdg18-updates-testing]
name=PostgreSQL 18 for Fedora $releasever - $basearch - Updates testing
baseurl=https://download.postgresql.org/pub/repos/yum/testing/18/fedora/fedora-$releasever-$basearch
enabled=1
gpgcheck=0
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg17-updates-testing]
name=PostgreSQL 17 for Fedora $releasever - $basearch - Updates testing
baseurl=https://download.postgresql.org/pub/repos/yum/testing/17/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg16-updates-testing]
name=PostgreSQL 16 for Fedora $releasever - $basearch - Updates testing
baseurl=https://download.postgresql.org/pub/repos/yum/testing/16/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg15-updates-testing]
name=PostgreSQL 15 for Fedora $releasever - $basearch - Updates testing
baseurl=https://download.postgresql.org/pub/repos/yum/testing/15/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg14-updates-testing]
name=PostgreSQL 14 for Fedora $releasever - $basearch - Updates testing
baseurl=https://download.postgresql.org/pub/repos/yum/testing/14/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg13-updates-testing]
name=PostgreSQL 13 for Fedora $releasever - $basearch - Updates testing
baseurl=https://download.postgresql.org/pub/repos/yum/testing/13/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

# PGDG Fedora stable common SRPM repository for all PostgreSQL versions

[pgdg-source-common]
name=PostgreSQL common SRPMs for Fedora $releasever - $basearch
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/common/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

# PGDG Fedora testing common SRPM repository for all PostgreSQL versions

[pgdg-common-srpm-testing]
name=PostgreSQL common testing SRPMs for Fedora $releasever - $basearch
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/testing/common/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

# Source RPMs (SRPM), and their testing repositories

[pgdg17-source]
name=PostgreSQL 17 for Fedora $releasever - $basearch - Source
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/17/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg17-source-updates-testing]
name=PostgreSQL 17 for Fedora $releasever - $basearch - Source updates testing
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/testing/17/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=0
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg16-source]
name=PostgreSQL 16 for Fedora $releasever - $basearch - Source
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/16/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg16-source-updates-testing]
name=PostgreSQL 16 for Fedora $releasever - $basearch - Source updates testing
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/testing/16/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg15-source]
name=PostgreSQL 15 for Fedora $releasever - $basearch - Source
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/15/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg15-source-updates-testing]
name=PostgreSQL 15 for Fedora $releasever - $basearch - Source updates testing
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/testing/15/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg14-source]
name=PostgreSQL 14 for Fedora $releasever - $basearch - Source
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/14/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg14-source-updates-testing]
name=PostgreSQL 14 for Fedora $releasever - $basearch - Source updates testing
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/testing/14/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg13-source]
name=PostgreSQL 13 for Fedora $releasever - $basearch - Source
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/13/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg13-source-updates-testing]
name=PostgreSQL 13 for Fedora $releasever - $basearch - Source updates testing
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/testing/13/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

# Debuginfo/debugsource repositories for the common repo

[pgdg-common-debuginfo]
name=PostgreSQL common RPMs for Fedora $releasever - $basearch - Debuginfo
baseurl=https://dnf-debuginfo.postgresql.org/debug/common/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

# Debuginfo/debugsource repositories for stable repos

[pgdg17-debuginfo]
name=PostgreSQL 17 for Fedora $releasever - $basearch - Debuginfo
baseurl=https://dnf-debuginfo.postgresql.org/debug/17/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg16-debuginfo]
name=PostgreSQL 16 for Fedora $releasever - $basearch - Debuginfo
baseurl=https://dnf-debuginfo.postgresql.org/debug/16/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg15-debuginfo]
name=PostgreSQL 15 for Fedora $releasever - $basearch - Debuginfo
baseurl=https://dnf-debuginfo.postgresql.org/debug/15/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg14-debuginfo]
name=PostgreSQL 14 for Fedora $releasever - $basearch - Debuginfo
baseurl=https://dnf-debuginfo.postgresql.org/debug/14/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg13-debuginfo]
name=PostgreSQL 13 for Fedora $releasever - $basearch - Debuginfo
baseurl=https://dnf-debuginfo.postgresql.org/debug/13/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

# Debuginfo/debugsource repositories for testing repos

[pgdg17-updates-testing-debuginfo]
name=PostgreSQL 17 for Fedora $releasever - $basearch - Debuginfo testing
baseurl=https://dnf-debuginfo.postgresql.org/testing/debug/17/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=0
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg16-updates-testing-debuginfo]
name=PostgreSQL 16 for Fedora $releasever - $basearch - Debuginfo testing
baseurl=https://dnf-debuginfo.postgresql.org/testing/debug/16/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg15-updates-testing-debuginfo]
name=PostgreSQL 15 for Fedora $releasever - $basearch - Debuginfo testing
baseurl=https://dnf-debuginfo.postgresql.org/testing/debug/15/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg14-updates-testing-debuginfo]
name=PostgreSQL 14 for Fedora $releasever - $basearch - Debuginfo testing
baseurl=https://dnf-debuginfo.postgresql.org/testing/debug/14/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg13-updates-testing-debuginfo]
name=PostgreSQL 13 for Fedora $releasever - $basearch - Debuginfo testing
baseurl=https://dnf-debuginfo.postgresql.org/testing/debug/13/fedora/fedora-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

# repos

[local]
name=local
baseurl=https://kojipkgs.fedoraproject.org/repos/f{{ releasever }}-build/latest/$basearch/
cost=2000
enabled={{ not mirrored }}
skip_if_unavailable=False

{% if mirrored %}
[fedora]
name=fedora
metalink=https://mirrors.fedoraproject.org/metalink?repo=fedora-$releasever&arch=$basearch
gpgkey=file:///usr/share/distribution-gpg-keys/fedora/RPM-GPG-KEY-fedora-{{ releasever }}-primary
gpgcheck=1
skip_if_unavailable=False

[updates]
name=updates
metalink=https://mirrors.fedoraproject.org/metalink?repo=updates-released-f$releasever&arch=$basearch
gpgkey=file:///usr/share/distribution-gpg-keys/fedora/RPM-GPG-KEY-fedora-{{ releasever }}-primary
gpgcheck=1
skip_if_unavailable=False

[updates-testing]
name=updates-testing
metalink=https://mirrors.fedoraproject.org/metalink?repo=updates-testing-f$releasever&arch=$basearch
enabled=0
gpgkey=file:///usr/share/distribution-gpg-keys/fedora/RPM-GPG-KEY-fedora-{{ releasever }}-primary
gpgcheck=1
skip_if_unavailable=False

[fedora-debuginfo]
name=fedora-debuginfo
metalink=https://mirrors.fedoraproject.org/metalink?repo=fedora-debug-$releasever&arch=$basearch
enabled=0
gpgkey=file:///usr/share/distribution-gpg-keys/fedora/RPM-GPG-KEY-fedora-{{ releasever }}-primary
gpgcheck=1
skip_if_unavailable=False

[updates-debuginfo]
name=updates-debuginfo
metalink=https://mirrors.fedoraproject.org/metalink?repo=updates-released-debug-f$releasever&arch=$basearch
enabled=0
gpgkey=file:///usr/share/distribution-gpg-keys/fedora/RPM-GPG-KEY-fedora-{{ releasever }}-primary
gpgcheck=1
skip_if_unavailable=False

[updates-testing-debuginfo]
name=updates-testing-debuginfo
metalink=https://mirrors.fedoraproject.org/metalink?repo=updates-testing-debug-f$releasever&arch=$basearch
enabled=0
gpgkey=file:///usr/share/distribution-gpg-keys/fedora/RPM-GPG-KEY-fedora-{{ releasever }}-primary
gpgcheck=1
skip_if_unavailable=False

[fedora-source]
name=fedora-source
metalink=https://mirrors.fedoraproject.org/metalink?repo=fedora-source-$releasever&arch=$basearch
gpgkey=file:///usr/share/distribution-gpg-keys/fedora/RPM-GPG-KEY-fedora-{{ releasever }}-primary
gpgcheck=1
enabled=0
skip_if_unavailable=False

[updates-source]
name=updates-source
metalink=https://mirrors.fedoraproject.org/metalink?repo=updates-released-source-f$releasever&arch=$basearch
gpgkey=file:///usr/share/distribution-gpg-keys/fedora/RPM-GPG-KEY-fedora-{{ releasever }}-primary
gpgcheck=1
enabled=0
skip_if_unavailable=False
{% endif %}
"""
