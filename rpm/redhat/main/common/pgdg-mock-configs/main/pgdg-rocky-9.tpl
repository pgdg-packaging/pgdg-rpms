config_opts['chroot_setup_cmd'] = " install bash bzip2 coreutils cpio diffutils findutils gawk glibc-minimal-langpack grep gzip info lua patch pgdg-srpm-macros python3 redhat-rpm-config rpm-build sed tar unzip util-linux which xz"
config_opts['macros']['%pgmajorversion'] = "17"
config_opts['macros']['%pginstdir'] = "/usr/pgsql-17"
config_opts['macros']['%__brp_check_rpaths'] = "/usr/bin/true"

config_opts['dist'] = 'rhel9'  # only useful for --resultdir variable subst
config_opts['releasever'] = '9'
config_opts['package_manager'] = 'dnf'
config_opts['extra_chroot_dirs'] = [ '/run/lock', ]
config_opts['bootstrap_image'] = 'quay.io/rockylinux/rockylinux:9'


config_opts['dnf.conf'] = """
[main]
keepcache=1
debuglevel=2
reposdir=/dev/null
logfile=/var/log/yum.log
retries=20
obsoletes=1
gpgcheck=0
assumeyes=1
syslog_ident=mock
syslog_device=
metadata_expire=0
mdpolicy=group:primary
best=1
install_weak_deps=0
protected_packages=
module_platform_id=platform:el9
user_agent={{ user_agent }}

#########################################################################
# PGDG Red Hat Enterprise Linux / Rocky / AlmaLinux repositories.	#
#########################################################################

# PGDG Red Hat Enterprise Linux / Rocky stable common repository for all PostgreSQL versions

[pgdg-common]
name=PostgreSQL common RPMs for RHEL / Rocky / AlmaLinux $releasever - $basearch
baseurl=https://download.postgresql.org/pub/repos/yum/common/redhat/rhel-$releasever-$basearch
enabled=1
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

# Red Hat recently breaks compatibility between 9.n and 9.n+1. PGDG repo is
# affected with the LLVM packages. This is a band aid repo for the llvmjit users
# whose installations cannot be updated.

[pgdg-rhel9-sysupdates]
name=PostgreSQL Supplementary ucommon RPMs for RHEL / Rocky / AlmaLinux $releasever - $basearch
baseurl=https://download.postgresql.org/pub/repos/yum/common/pgdg-rocky9-sysupdates/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

# We provide extra package to support some RPMs in the PostgreSQL RPM repo, like
# consul, haproxy, etc.

[pgdg-rhel9-extras]
name=Extra packages to support some RPMs in the PostgreSQL RPM repo RHEL / Rocky / AlmaLinux $releasever - $basearch
baseurl=https://download.postgresql.org/pub/repos/yum/common/pgdg-rhel$releasever-extras/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

# PGDG Red Hat Enterprise Linux / Rocky stable repositories:

[pgdg17]
name=PostgreSQL 17 for RHEL / Rocky / AlmaLinux $releasever - $basearch
baseurl=https://download.postgresql.org/pub/repos/yum/17/redhat/rhel-$releasever-$basearch
enabled=1
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg16]
name=PostgreSQL 16 for RHEL / Rocky / AlmaLinux $releasever - $basearch
baseurl=https://download.postgresql.org/pub/repos/yum/16/redhat/rhel-$releasever-$basearch
enabled=1
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg15]
name=PostgreSQL 15 for RHEL / Rocky / AlmaLinux $releasever - $basearch
baseurl=https://download.postgresql.org/pub/repos/yum/15/redhat/rhel-$releasever-$basearch
enabled=1
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg14]
name=PostgreSQL 14 for RHEL / Rocky / AlmaLinux $releasever - $basearch
baseurl=https://download.postgresql.org/pub/repos/yum/14/redhat/rhel-$releasever-$basearch
enabled=1
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg13]
name=PostgreSQL 13 for RHEL / Rocky / AlmaLinux $releasever - $basearch
baseurl=https://download.postgresql.org/pub/repos/yum/13/redhat/rhel-$releasever-$basearch
enabled=1
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

# PGDG RHEL / Rocky / AlmaLinux Updates Testing common repositories.

[pgdg-common-testing]
name=PostgreSQL common testing RPMs for RHEL / Rocky / AlmaLinux $releasever - $basearch
baseurl=https://download.postgresql.org/pub/repos/yum/testing/common/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

# PGDG RHEL / Rocky / AlmaLinux Updates Testing repositories. (These packages should not be used in production)
# Available for 13 and above.

[pgdg18-updates-testing]
name=PostgreSQL 18 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Updates testing
baseurl=https://download.postgresql.org/pub/repos/yum/testing/18/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=0
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg17-updates-testing]
name=PostgreSQL 17 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Updates testing
baseurl=https://download.postgresql.org/pub/repos/yum/testing/17/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg16-updates-testing]
name=PostgreSQL 16 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Updates testing
baseurl=https://download.postgresql.org/pub/repos/yum/testing/16/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg15-updates-testing]
name=PostgreSQL 15 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Updates testing
baseurl=https://download.postgresql.org/pub/repos/yum/testing/15/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg14-updates-testing]
name=PostgreSQL 14 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Updates testing
baseurl=https://download.postgresql.org/pub/repos/yum/testing/14/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg13-updates-testing]
name=PostgreSQL 13 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Updates testing
baseurl=https://download.postgresql.org/pub/repos/yum/testing/13/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

# PGDG Red Hat Enterprise Linux / Rocky SRPM testing common repository

[pgdg-source-common]
name=PostgreSQL common for RHEL / Rocky / AlmaLinux $releasever - $basearch - Source
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/common/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

# PGDG RHEL / Rocky / AlmaLinux testing common SRPM repository for all PostgreSQL versions

[pgdg-common-srpm-testing]
name=PostgreSQL common testing SRPMs for RHEL / Rocky / AlmaLinux $releasever - $basearch
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/testing/common/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

# PGDG Source RPMs (SRPMS), and their testing repositories:

[pgdg18-source-updates-testing]
name=PostgreSQL 18 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Source updates testing
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/testing/18/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=0
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg17-source]
name=PostgreSQL 17 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Source
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/17/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg17-source-updates-testing]
name=PostgreSQL 17 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Source updates testing
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/testing/17/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg16-source]
name=PostgreSQL 16 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Source
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/16/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg16-source-updates-testing]
name=PostgreSQL 16 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Source updates testing
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/testing/16/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg15-source]
name=PostgreSQL 15 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Source
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/15/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg15-source-updates-testing]
name=PostgreSQL 15 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Source updates testing
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/testing/15/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg14-source]
name=PostgreSQL 14 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Source
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/14/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg14-source-updates-testing]
name=PostgreSQL 14 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Source updates testing
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/testing/14/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg13-source]
name=PostgreSQL 13 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Source
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/13/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg13-source-updates-testing]
name=PostgreSQL 13 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Source updates testing
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/testing/13/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

# Debuginfo/debugsource repositories for the common repo

[pgdg-common-debuginfo]
name=PostgreSQL common RPMs for RHEL / Rocky / AlmaLinux $releasever - $basearch - Debuginfo
baseurl=https://dnf-debuginfo.postgresql.org/debug/common/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

# Debuginfo/debugsource packages for stable repos

[pgdg17-debuginfo]
name=PostgreSQL 17 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Debuginfo
baseurl=https://dnf-debuginfo.postgresql.org/debug/17/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg16-debuginfo]
name=PostgreSQL 16 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Debuginfo
baseurl=https://dnf-debuginfo.postgresql.org/debug/16/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg15-debuginfo]
name=PostgreSQL 15 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Debuginfo
baseurl=https://dnf-debuginfo.postgresql.org/debug/15/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg14-debuginfo]
name=PostgreSQL 14 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Debuginfo
baseurl=https://dnf-debuginfo.postgresql.org/debug/14/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg13-debuginfo]
name=PostgreSQL 13 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Debuginfo
baseurl=https://dnf-debuginfo.postgresql.org/debug/13/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

# Debuginfo/debugsource packages for testing repos
# Available for 13 and above.

[pgdg18-updates-testing-debuginfo]
name=PostgreSQL 18 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Debuginfo
baseurl=https://dnf-debuginfo.postgresql.org/testing/debug/18/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=0
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg17-updates-testing-debuginfo]
name=PostgreSQL 17 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Debuginfo
baseurl=https://dnf-debuginfo.postgresql.org/testing/debug/17/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg16-updates-testing-debuginfo]
name=PostgreSQL 16 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Debuginfo
baseurl=https://dnf-debuginfo.postgresql.org/testing/debug/16/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg15-updates-testing-debuginfo]
name=PostgreSQL 15 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Debuginfo
baseurl=https://dnf-debuginfo.postgresql.org/testing/debug/15/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg14-updates-testing-debuginfo]
name=PostgreSQL 14 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Debuginfo
baseurl=https://dnf-debuginfo.postgresql.org/testing/debug/14/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[pgdg13-updates-testing-debuginfo]
name=PostgreSQL 13 for RHEL / Rocky / AlmaLinux $releasever - $basearch - Debuginfo
baseurl=https://dnf-debuginfo.postgresql.org/testing/debug/13/redhat/rhel-$releasever-$basearch
enabled=0
gpgcheck=1
gpgkey=https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
repo_gpgcheck = 1

[baseos]
name=Rocky Linux $releasever - BaseOS
mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=$basearch&repo=BaseOS-$releasever
#baseurl=http://dl.rockylinux.org/pub/rocky/$releasever/BaseOS/$basearch/os/
gpgcheck=1
enabled=1
metadata_expire=6h
gpgkey=file:///usr/share/distribution-gpg-keys/rocky/RPM-GPG-KEY-Rocky-9

[appstream]
name=Rocky Linux $releasever - AppStream
mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=$basearch&repo=AppStream-$releasever
#baseurl=http://dl.rockylinux.org/pub/rocky/$releasever/AppStream/$basearch/os/
gpgcheck=1
enabled=1
metadata_expire=6h
gpgkey=file:///usr/share/distribution-gpg-keys/rocky/RPM-GPG-KEY-Rocky-9

[crb]
name=Rocky Linux $releasever - CRB
mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=$basearch&repo=CRB-$releasever
#baseurl=http://dl.rockylinux.org/pub/rocky/$releasever/CRB/$basearch/os/
gpgcheck=1
enabled=1
metadata_expire=6h
gpgkey=file:///usr/share/distribution-gpg-keys/rocky/RPM-GPG-KEY-Rocky-9

[extras]
name=Rocky Linux $releasever - Extras
mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=$basearch&repo=extras-$releasever
#baseurl=http://dl.rockylinux.org/pub/rocky/$releasever/extras/$basearch/os/
gpgcheck=1
enabled=1
metadata_expire=6h
gpgkey=file:///usr/share/distribution-gpg-keys/rocky/RPM-GPG-KEY-Rocky-9

[devel]
name=Rocky Linux $releasever - Devel WARNING! FOR BUILDROOT ONLY DO NOT LEAVE ENABLED
mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=$basearch&repo=devel-$releasever
#baseurl=http://dl.rockylinux.org/pub/rocky/$releasever/devel/$basearch/os/
gpgcheck=1
enabled=0
gpgkey=file:///usr/share/distribution-gpg-keys/rocky/RPM-GPG-KEY-Rocky-9

[highavailability]
name=Rocky Linux $releasever - High Availability
mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=$basearch&repo=HighAvailability-$releasever
#baseurl=http://dl.rockylinux.org/$contentdir/$releasever/HighAvailability/$basearch/os/
gpgcheck=1
enabled=0
metadata_expire=6h
gpgkey=file:///usr/share/distribution-gpg-keys/rocky/RPM-GPG-KEY-Rocky-9

[resilientstorage]
name=Rocky Linux $releasever - Resilient Storage
mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=$basearch&repo=ResilientStorage-$releasever
#baseurl=http://dl.rockylinux.org/$contentdir/$releasever/ResilientStorage/$basearch/os/
gpgcheck=1
enabled=0
metadata_expire=6h
gpgkey=file:///usr/share/distribution-gpg-keys/rocky/RPM-GPG-KEY-Rocky-9

[nfv]
name=Rocky Linux $releasever - NFV
mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=$basearch&repo=NFV-$releasever
#baseurl=http://dl.rockylinux.org/$contentdir/$releasever/NFV/$basearch/os/
gpgcheck=1
enabled=0
metadata_expire=6h
gpgkey=file:///usr/share/distribution-gpg-keys/rocky/RPM-GPG-KEY-Rocky-9

[rt]
name=Rocky Linux $releasever - Realtime
mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=$basearch&repo=RT-$releasever
#baseurl=http://dl.rockylinux.org/$contentdir/$releasever/RT/$basearch/os/
gpgcheck=1
enabled=0
metadata_expire=6h
gpgkey=file:///usr/share/distribution-gpg-keys/rocky/RPM-GPG-KEY-Rocky-9

[baseos-debug]
name=Rocky Linux $releasever - BaseOS - Debug
mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=$basearch&repo=BaseOS-$releasever-debug
#baseurl=http://dl.rockylinux.org/pub/rocky/$releasever/BaseOS/$basearch/debug/tree/
gpgcheck=1
enabled=0
metadata_expire=6h
gpgkey=file:///usr/share/distribution-gpg-keys/rocky/RPM-GPG-KEY-Rocky-9

[baseos-source]
name=Rocky Linux $releasever - BaseOS - Source
mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=source&repo=BaseOS-$releasever-source
#baseurl=http://dl.rockylinux.org/pub/rocky/$releasever/BaseOS/source/tree/
gpgcheck=1
enabled=0
metadata_expire=6h
gpgkey=file:///usr/share/distribution-gpg-keys/rocky/RPM-GPG-KEY-Rocky-9

[appstream-debug]
name=Rocky Linux $releasever - AppStream - Debug
mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=$basearch&repo=AppStream-$releasever-debug
#baseurl=http://dl.rockylinux.org/pub/rocky/$releasever/AppStream/$basearch/debug/tree/
gpgcheck=1
enabled=0
metadata_expire=6h
gpgkey=file:///usr/share/distribution-gpg-keys/rocky/RPM-GPG-KEY-Rocky-9

[appstream-source]
name=Rocky Linux $releasever - AppStream - Source
mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=source&repo=AppStream-$releasever-source
#baseurl=http://dl.rockylinux.org/pub/rocky/$releasever/AppStream/source/tree/
gpgcheck=1
enabled=0
metadata_expire=6h
gpgkey=file:///usr/share/distribution-gpg-keys/rocky/RPM-GPG-KEY-Rocky-9

[crb-debug]
name=Rocky Linux $releasever - CRB - Debug
mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=$basearch&repo=CRB-$releasever-debug
#baseurl=http://dl.rockylinux.org/pub/rocky/$releasever/CRB/$basearch/debug/tree/
gpgcheck=1
enabled=0
metadata_expire=6h
gpgkey=file:///usr/share/distribution-gpg-keys/rocky/RPM-GPG-KEY-Rocky-9

[crb-source]
name=Rocky Linux $releasever - CRB - Source
mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=source&repo=CRB-$releasever-source
#baseurl=http://dl.rockylinux.org/pub/rocky/$releasever/CRB/source/tree/
gpgcheck=1
enabled=0
metadata_expire=6h
gpgkey=file:///usr/share/distribution-gpg-keys/rocky/RPM-GPG-KEY-Rocky-9

[extras-debug]
name=Rocky Linux $releasever - Extras Debug
mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=$basearch&repo=extras-$releasever-debug
#baseurl=http://dl.rockylinux.org/pub/rocky/$releasever/extras/$basearch/debug/tree/
gpgcheck=1
enabled=0
metadata_expire=6h
gpgkey=file:///usr/share/distribution-gpg-keys/rocky/RPM-GPG-KEY-Rocky-9

[extras-source]
name=Rocky Linux $releasever - Extras Source
mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=$basearch&repo=extras-$releasever-source
#baseurl=http://dl.rockylinux.org/pub/rocky/$releasever/extras/source/tree/
gpgcheck=1
enabled=0
metadata_expire=6h
gpgkey=file:///usr/share/distribution-gpg-keys/rocky/RPM-GPG-KEY-Rocky-9

[highavailability-debug]
name=Rocky Linux $releasever - High Availability - Debug
mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=$basearch&repo=HighAvailability-$releasever-debug$rltype
#baseurl=http://dl.rockylinux.org/$contentdir/$releasever/HighAvailability/$basearch/debug/tree/
gpgcheck=1
enabled=0
metadata_expire=6h
gpgkey=file:///usr/share/distribution-gpg-keys/rocky/RPM-GPG-KEY-Rocky-9

[highavailability-source]
name=Rocky Linux $releasever - High Availability - Source
mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=source&repo=HighAvailability-$releasever-source$rltype
#baseurl=http://dl.rockylinux.org/$contentdir/$releasever/HighAvailability/source/tree/
gpgcheck=1
enabled=0
metadata_expire=6h
gpgkey=file:///usr/share/distribution-gpg-keys/rocky/RPM-GPG-KEY-Rocky-9

[resilientstorage-debug]
name=Rocky Linux $releasever - Resilient Storage - Debug
mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=$basearch&repo=ResilientStorage-$releasever-debug$rltype
#baseurl=http://dl.rockylinux.org/$contentdir/$releasever/ResilientStorage/$basearch/debug/tree/
gpgcheck=1
enabled=0
metadata_expire=6h
gpgkey=file:///usr/share/distribution-gpg-keys/rocky/RPM-GPG-KEY-Rocky-9

[resilientstorage-source]
name=Rocky Linux $releasever - Resilient Storage - Source
mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=source&repo=ResilientStorage-$releasever-source$rltype
#baseurl=http://dl.rockylinux.org/$contentdir/$releasever/ResilientStorage/source/tree/
gpgcheck=1
enabled=0
metadata_expire=6h
gpgkey=file:///usr/share/distribution-gpg-keys/rocky/RPM-GPG-KEY-Rocky-9

[nfv-debug]
name=Rocky Linux $releasever - NFV Debug
mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=$basearch&repo=RT-$releasever-debug$rltype
#baseurl=http://dl.rockylinux.org/$contentdir/$releasever/NFV/$basearch/debug/tree/
gpgcheck=1
enabled=0
metadata_expire=6h
gpgkey=file:///usr/share/distribution-gpg-keys/rocky/RPM-GPG-KEY-Rocky-9

[nfv-source]
name=Rocky Linux $releasever - NFV Source
mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=$basearch&repo=RT-$releasever-source$rltype
#baseurl=http://dl.rockylinux.org/$contentdir/$releasever/NFV/source/tree/
gpgcheck=1
enabled=0
metadata_expire=6h
gpgkey=file:///usr/share/distribution-gpg-keys/rocky/RPM-GPG-KEY-Rocky-9

[rt-debug]
name=Rocky Linux $releasever - Realtime Debug
mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=$basearch&repo=RT-$releasever-debug$rltype
#baseurl=http://dl.rockylinux.org/$contentdir/$releasever/RT/$basearch/debug/tree/
gpgcheck=1
enabled=0
metadata_expire=6h
gpgkey=file:///usr/share/distribution-gpg-keys/rocky/RPM-GPG-KEY-Rocky-9

[rt-source]
name=Rocky Linux $releasever - Realtime Source
mirrorlist=https://mirrors.rockylinux.org/mirrorlist?arch=$basearch&repo=RT-$releasever-source$rltype
#baseurl=http://dl.rockylinux.org/$contentdir/$releasever/RT/source/tree/
gpgcheck=1
enabled=0
metadata_expire=6h
gpgkey=file:///usr/share/distribution-gpg-keys/rocky/RPM-GPG-KEY-Rocky-9


"""
