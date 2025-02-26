%global sname repmgr
%global unitname	%{sname}-%{pgmajorversion}

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	5.5.0
Release:	3PGDG%{?dist}
Summary:	Replication Manager for PostgreSQL Clusters
License:	GPLv3
URL:		https://github.com/enterpriseDB/%{sname}
Source0:	https://github.com/EnterpriseDB/%{sname}/archive/refs/tags/v%{version}.tar.gz
Source1:	repmgr-pg%{pgmajorversion}.service
Source3:	repmgr-pg%{pgmajorversion}.sysconfig
Patch0:		repmgr-pg%{pgmajorversion}-conf.sample.patch
Patch1:		repmgr-pg%{pgmajorversion}-config-file-location.patch

BuildRequires:	systemd systemd-devel flex krb5-devel libcurl-devel
%if 0%{?suse_version} >= 1500
BuildRequires:	libjson-c-devel
%else
BuildRequires:	json-c-devel
%endif
# All supported distros have libselinux-devel package:
BuildRequires:	libselinux-devel >= 2.0.93
# SLES: SLES 15 does not have selinux-policy packageç
# RHEL/Fedora has selinux-policy:
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	selinux-policy >= 3.9.13
%endif
# lz4 dependency
%if 0%{?suse_version} >= 1500
BuildRequires:	liblz4-devel
Requires:	liblz4-1
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	lz4-devel
Requires:	lz4-libs
%endif
# We require this to be present for %%{_prefix}/lib/tmpfiles.d
Requires:		systemd
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1500
Requires(post):		systemd-sysvinit
%endif
%else
Requires(post):		systemd-sysv
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
%endif

BuildRequires:	postgresql%{pgmajorversion} postgresql%{pgmajorversion}-devel
BuildRequires:	libxslt-devel pam-devel readline-devel
BuildRequires:	libmemcached-devel libicu-devel
Requires:	postgresql%{pgmajorversion}-server

%if 0%{?suse_version} >= 1500
Requires:	libopenssl1_1
%else
Requires:	openssl-libs >= 1.0.2k
%endif

BuildRequires:	openssl-devel

%description
repmgr is an open-source tool suite for managing replication and failover in
cluster of PostgreSQL servers. It enhances PostgreSQL's built-in hot-standby
capabilities with tools to set up standby servers, monitor replication, and
perform administrative tasks such as failover or manual switchover operations.


%package devel
Summary:	Development header files of repmgr
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The repmgr-devel package contains the header files needed to compile C or C++
applications which will directly interact with repmgr.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for repmgr
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 17.0 clang-devel >= 17.0
Requires:	llvm => 17.0
%endif

%description llvmjit
This package provides JIT support for repmgr
%endif

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p0
%patch -P 1 -p1

export PG_CONFIG=%{pginstdir}/bin/pg_config
%configure

%build
USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__mkdir} -p %{buildroot}/%{pginstdir}/bin/
# Use new %%make_install macro:
USE_PGXS=1 %make_install DESTDIR=%{buildroot}

%{__mkdir} -p %{buildroot}/%{pginstdir}/bin/
# Install sample conf file
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/%{sname}/%{pgpackageversion}/
%{__install} -m 644 repmgr.conf.sample %{buildroot}/%{_sysconfdir}/%{sname}/%{pgpackageversion}/%{sname}.conf

# Create the directory for sockets.
%{__install} -d -m 0755 %{buildroot}%{_rundir}/%{sname}

%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{unitname}.service

# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}%{_tmpfilesdir}
cat > %{buildroot}%{_tmpfilesdir}/%{name}.conf <<EOF
d %{_rundir}/%{sname} 0755 postgres postgres -
EOF

%pre
if [ ! -x /var/log/repmgr ]
then
	%{__mkdir} -m 700 /var/log/repmgr
	%{__chown} -R postgres: /var/log/repmgr
fi

%post
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
   /bin/systemctl daemon-reload >/dev/null 2>&1 || :
   %if 0%{?suse_version}
   %if 0%{?suse_version} >= 1500
    %service_add_pre %{sname}-%{pgmajorversion}.service
   %endif
   %else
    %systemd_post %{sname}-%{pgmajorversion}.service
   %endif
fi

%postun -p /sbin/ldconfig

%files
%doc CREDITS HISTORY README.md
%license COPYRIGHT LICENSE
%dir %{pginstdir}/bin
%dir %{_sysconfdir}/%{sname}/%{pgpackageversion}/
%attr(755,postgres,postgres) %dir %{_rundir}/%{sname}
%config(noreplace) %{_sysconfdir}/%{sname}/%{pgpackageversion}/%{sname}.conf
%{pginstdir}/bin/repmgr
%{pginstdir}/bin/repmgrd
%{pginstdir}/lib/repmgr.so
%{pginstdir}/share/extension/repmgr.control
%{pginstdir}/share/extension/repmgr*sql
%{_tmpfilesdir}/%{name}.conf
%attr (644, root, root) %{_unitdir}/%{unitname}.service

%files devel
%defattr(-,root,root,-)

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Wed Feb 26 2025 - Devrim Gündüz <devrim@gunduz.org> - 5.5.0-3PGDG
- Add missing BRs and Requires

* Wed Jan 29 2025 - Devrim Gündüz <devrim@gunduz.org> - 5.5.0-2PGDG
- Update package description
- Remove redundant BR

* Sat Nov 23 2024 - Devrim Gündüz <devrim@gunduz.org> - 5.5.0-1PGDG
- Update to 5.5.0, per changes described at:
  https://repmgr.org/docs/current/release-5.5.0.html
- Remove SLES 12 support

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 5.4.1-3PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Tue Dec 5 2023 - Devrim Gündüz <devrim@gunduz.org> - 5.4.1-2PGDG
- Update legacy path /var/run to /run.

* Mon Jul 24 2023 - Devrim Gündüz <devrim@gunduz.org> - 5.4.1-1PGDG
- Update to 5.4.1, per changes described at:
  https://repmgr.org/docs/current/release-5.4.1.html
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 5.4.0-1.1
- Rebuild against LLVM 15 on SLES 15

* Tue May 23 2023 - Devrim Gündüz <devrim@gunduz.org> - 5.4.0-1
- Update to 5.4.0, per changes described at:
  https://repmgr.org/docs/current/release-5.4.0.html

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 5.3.3-3.1
- Modernise %%patch usage, which has been deprecated in Fedora 38

* Sun Apr 23 2023 Devrim Gündüz <devrim@gunduz.org> - 5.3.3-3
- Fix rpm build warning, remove duplicate file.

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 5.3.3-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue Oct 18 2022 - Devrim Gündüz <devrim@gunduz.org> - 5.3.3-1
- Update to 5.3.3, per changes described at:
  https://repmgr.org/docs/current/release-5.3.3.html

* Thu Sep 29 2022 - Devrim Gündüz <devrim@gunduz.org> - 5.3.2-2
- Remove RHEL 6 support.

* Fri May 27 2022 - Devrim Gündüz <devrim@gunduz.org> - 5.3.2-1
- Update to 5.3.2, per changes described at:
  https://repmgr.org/docs/current/release-5.3.2.html

* Wed Feb 16 2022 - Devrim Gündüz <devrim@gunduz.org> 5.3.1-1
- Update to 5.3.1, per changes described at:
  https://repmgr.org/docs/current/release-5.3.1.html

* Sat Oct 16 2021 - Devrim Gündüz <devrim@gunduz.org> 5.3.1-1
- Fix OpenSSL dependencies on SLES.

* Thu Oct 14 2021 - Devrim Gündüz <devrim@gunduz.org> 5.3.0-1
- Update to 5.3.0, per changes described at:
  https://repmgr.org/docs/current/release-5.3.0.html

* Wed Jun 2 2021 - Devrim Gündüz <devrim@gunduz.org> 5.2.1-3
- Fix unit file path.

* Fri Jan 22 2021 - Devrim Gündüz <devrim@gunduz.org> 5.2.1-2
- Make sure that the socket dir is created, per report from
  Greg Clough.

* Tue Dec 8 2020 - Devrim Gündüz <devrim@gunduz.org> 5.2.1-1
- Update to 5.2.1
- Fix unit file breakage caused by
  ba535ce9740f23ead60b001a43898bf3b4ffef8e .

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 5.2.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Oct 22 2020 - Devrim Gündüz <devrim@gunduz.org> 5.2.0-1
- Update to 5.2.0

* Mon Apr 13 2020 - Devrim Gündüz <devrim@gunduz.org> 5.1.0-1
- Update to 5.1.0

* Wed Oct 16 2019 - Devrim Gündüz <devrim@gunduz.org> 5.0.0-1
- Update to 5.0.0

* Thu Jun 27 2019 - Devrim Gündüz <devrim@gunduz.org> 4.4.0-1
- Update to 4.4.0

* Fri Apr 12 2019 - Devrim Gündüz <devrim@gunduz.org> 4.3.0-2
- Fix tmpfilesd directory. Per https://redmine.postgresql.org/issues/4156

* Wed Apr 3 2019 - Devrim Gündüz <devrim@gunduz.org> 4.3.0-1
- Update to 4.3.0
- Fix https://redmine.postgresql.org/issues/3717. Patch from Ian
  Barwick.
- Fix https://redmine.postgresql.org/issues/3718. Patch from Ian
  Barwick.

* Sat Dec 22 2018 - Devrim Gündüz <devrim@gunduz.org> 4.2.0-2
- Fix path in tmpfiles.d drop-in file

* Tue Nov 6 2018 - Devrim Gündüz <devrim@gunduz.org> 4.2.0-1
- Update to 4.2.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Thu Sep 6 2018 - Devrim Gündüz <devrim@gunduz.org> 4.1.1-1
- Update to 4.1.1, per #3623
- Add -devel subpackage for v11+

* Wed Aug 1 2018 - Devrim Gündüz <devrim@gunduz.org> 4.1.0-1
- Update to 4.1.0, per #3530

* Thu Jun 14 2018 - Devrim Gündüz <devrim@gunduz.org> 4.0.6-1
- Update to 4.0.6, per #3419

* Fri May 4 2018 - Devrim Gündüz <devrim@gunduz.org> 4.0.5-1
- Update to 4.0.5

* Mon Apr 16 2018 - Devrim Gündüz <devrim@gunduz.org> 4.0.4-1
- Update to 4.0.4, per #3264.

* Thu Feb 22 2018 - Devrim Gündüz <devrim@gunduz.org> 4.0.3-1
- Update to 4.0.3

* Thu Jan 18 2018 - Devrim Gündüz <devrim@gunduz.org> 4.0.2-1
- Update to 4.0.2

* Tue Jan 2 2018 - Devrim Gündüz <devrim@gunduz.org> 4.0.1-1
- Update to 4.0.1

* Tue Nov 21 2017 - Devrim Gündüz <devrim@gunduz.org> 4.0.0-1
- Update to 4.0.0
- Remove patch0, not needed anymore.

* Sun Jun 11 2017 - Devrim Gündüz <devrim@gunduz.org> 3.3.2-1
- Update to 3.3.2, per #2472 .

* Sun Apr 2 2017 - Devrim Gündüz <devrim@gunduz.org> 3.3.1-1
- Update to 3.3.1, per #2296 .

* Mon Mar 13 2017 - Devrim Gündüz <devrim@gunduz.org> 3.3-2
- Fix quoting bug in sample conf file patch. Per report from Magnus.
  Fixes #2248.

* Fri Jan 6 2017 - Devrim Gündüz <devrim@gunduz.org> 3.3-1
- Update to 3.3

* Thu Oct 27 2016 - Devrim Gündüz <devrim@gunduz.org> 3.2.1-1
- Update to 3.2.1. Fixes #1897

* Fri Oct 7 2016 - Devrim Gündüz <devrim@gunduz.org> 3.2-1
- Update to 3.2. Fixes #1836

* Fri Aug 26 2016 - Devrim Gündüz <devrim@gunduz.org> 3.1.5-1
- Update to 3.1.5

* Fri May 20 2016 - Devrim Gündüz <devrim@gunduz.org> 3.1.3-1
- Update to 3.1.3

* Mon May 02 2016 - Craig Ringer <craig.ringer@2ndquadrant.com> 3.1.2-2
- Fix shell redirection in systemd service file (#1052)

* Tue Mar 8 2016 - Craig Ringer <craig.ringer@2ndquadrant.com> 3.1.1-2
- Don't overwrite config files on upgrade, save as .rpmnew instead (#1029, per
  report by Brett Maton)
- sysconfig file should not be installed executable (#1030)
- Fix RPM group name (#1030)
- systemd service file should not be executable (#1030)

* Thu Feb 25 2016 - Craig Ringer <craig.ringer@2ndquadrant.com> 3.1.1-1
- Upstream release 3.1.1

* Mon Feb 22 2016 - Devrim Gündüz <devrim@gunduz.org> 3.0.3-3
- Fix permissions of sysconfig file. Per #1004.

* Tue Feb 16 2016 - Devrim Gündüz <devrim@gunduz.org> 3.0.3-2
- Install correct sysconfig file, instead of init script. Per
  bug report from Brett Maton.

* Tue Jan 5 2016 - Devrim Gündüz <devrim@gunduz.org> 3.0.3-1
- Update to 3.0.3
- Apply various fixes to init script, and also add sysconfig
  file. Patch from Martín Marqués.
- Fix some rpmlint warnings.

* Mon Nov 9 2015 - Devrim Gündüz <devrim@gunduz.org> 3.0.2-2
- Ensure that /var/run/repmgr exists. Per Guillaume Lelarge.
- Switch to postgres user while running the deamon, instead of
  repmgr user. Per recent complaints from Guillaume and Justin King.

* Tue Oct 6 2015 - Devrim Gündüz <devrim@gunduz.org> 3.0.2-1
- Update to 3.0.2

* Tue May 12 2015 - Devrim Gündüz <devrim@gunduz.org> 3.0.1-1
- Update to 3.0.1
- Update description and some other minor places.
- More for creating unified spec file for all distros, and put
  back some stuff into conditionals. Also, use %%license macro
  only on newer releases.

* Fri May 1 2015 - Devrim Gündüz <devrim@gunduz.org> 2.0.2-4
- chown pid file dir and fix its path.
- Fix unit file

* Wed Apr 29 2015 - Devrim Gündüz <devrim@gunduz.org> 2.0.2-3
- Add %%license macro
- Use %%make_install macro
- Omit %%clean
- No need to cleanup buildroot during %%install
- Run ldconfig

* Tue Mar 24 2015 - Devrim Gündüz <devrim@gunduz.org> 2.0.2-2
- Add unit file/init script for repmgr. This spec file can be
  used on all platforms.
- Updated BR, per mock build.

* Thu Feb 19 2015 - Devrim Gündüz <devrim@gunduz.org> 2.0.2-1
- Update to 2.0.2, per changes described at:
  http://www.repmgr.org/release-notes-2.0.2.html

* Thu Mar 20 2014 - Devrim Gündüz <devrim@gunduz.org> 2.0-1
- Update to 2.0

* Fri Jul 27 2012 - Devrim Gündüz <devrim@gunduz.org> 1.2.0-1
- Update to 1.2.0

* Tue Apr 3 2012 - Devrim Gündüz <devrim@gunduz.org> 1.1.0-2
- Spec file fixes by Satoshi Nagayasu
- Updated patch0 and renamed it for better convenience.
- Replaced postgresql-devel dependency with postgresql, since
  pg_config is now in main package.

* Wed Oct 19 2011 - Devrim Gündüz <devrim@gunduz.org> 1.1.0-1
- Initial packaging.
