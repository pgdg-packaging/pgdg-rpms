%global _vpath_builddir build
%global _vpath_srcdir .

Summary:	Reliable PostgreSQL Backup & Restore
Name:		pgbackrest
Version:	2.55.0
Release:	1PGDG%{?dist}
License:	MIT
Url:		http://www.pgbackrest.org/
Source0:	https://github.com/pgbackrest/pgbackrest/archive/release/%{version}.tar.gz
Source1:	%{name}-conf.patch
Source2:	%{name}-tmpfiles.d
Source3:	%{name}.logrotate
Source4:	%{name}.service

BuildRequires:	openssl-devel zlib-devel postgresql%{pgmajorversion}-devel
BuildRequires:	libzstd-devel libxml2-devel libyaml-devel libssh2-devel
BuildRequires:	meson

%if 0%{?fedora} >= 37 || 0%{?rhel} >= 8
Requires:	lz4-libs libzstd libssh2
BuildRequires:	lz4-devel bzip2-devel ninja-build
%endif
%if 0%{?suse_version} && 0%{?suse_version} <= 1499
Requires:	liblz4-1_7 libzstd1 libssh2-1
BuildRequires:	liblz4-devel libbz2-devel ninja
%endif
%if 0%{?suse_version} && 0%{?suse_version} >= 1500
Requires:	liblz4-1 libzstd1 libssh2-1
BuildRequires:	liblz4-devel libbz2-devel ninja
%endif

Requires:	postgresql-libs
Requires(pre):	/usr/sbin/useradd /usr/sbin/groupadd

BuildRequires:		systemd, systemd-devel
# We require this to be present for %%{_prefix}/lib/tmpfiles.d
Requires:		systemd
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
Requires(post):		systemd-sysvinit
%endif
%else
Requires(post):		systemd-sysv
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
%endif

%description
pgBackRest aims to be a simple, reliable backup and restore system that can
seamlessly scale up to the largest databases and workloads.

Instead of relying on traditional backup tools like tar and rsync, pgBackRest
implements all backup features internally and uses a custom protocol for
communicating with remote systems. Removing reliance on tar and rsync allows
for better solutions to database-specific backup challenges. The custom remote
protocol allows for more flexibility and limits the types of connections that
are required to perform a backup which increases security.

%prep
%setup -q -n %{name}-release-%{version}

%build
%{__install} -d build
%meson
%meson_build

%install
%meson_install
%{__install} -D -d -m 0700 %{buildroot}/%{_sharedstatedir}/%{name}
%{__install} -D -d -m 0700 %{buildroot}/var/log/%{name}
%{__install} -D -d -m 0700 %{buildroot}/var/spool/%{name}
%{__install} -D -d -m 0755 %{buildroot}%{_sysconfdir}
%{__install} -m 0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/%{name}.conf

#Install logrotate file:
%{__install} -p -d %{buildroot}%{_sysconfdir}/logrotate.d
%{__install} -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}/%{_tmpfilesdir}
%{__install} -m 0644 %{SOURCE2} %{buildroot}/%{_tmpfilesdir}/%{name}.conf

# Install unit file:
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/%{name}.service

%pre
# PGDATA needs removal of group and world permissions due to pg_pwd hole.
%{__install} -d -m 700 /var/lib/pgsql/
groupadd -g 26 -o -r postgres >/dev/null 2>&1 || :
useradd -M -g postgres -o -r -d /var/lib/pgsql -s /bin/bash \
	-c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || :
%{__chown} postgres: /var/lib/pgsql

%post
if [ $1 -eq 1 ] ; then
   /bin/systemctl daemon-reload >/dev/null 2>&1 || :
   %if 0%{?suse_version}
   %if 0%{?suse_version} >= 1315
   %service_add_pre %{name}.service
   %endif
   %else
   %systemd_post %{name}.service
   %endif
fi

%preun
if [ $1 -eq 0 ] ; then
	# Package removal, not upgrade
	/bin/systemctl --no-reload disable %{name}.service >/dev/null 2>&1 || :
	/bin/systemctl stop %{name}.service >/dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

if [ $1 -ge 1 ] ; then
	# Package upgrade, not uninstall
	/bin/systemctl try-restart %{name}.service >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/%{name}
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{name}.service
%attr(-,postgres,postgres) /var/log/%{name}
%attr(-,postgres,postgres) %{_sharedstatedir}/%{name}
%attr(-,postgres,postgres) /var/spool/%{name}

%changelog
* Tue Apr 22 2025 Devrim Gündüz <devrim@gunduz.org> - 2.55.0-1PGDG
- Update to 2.55.0, per changes described at:
  https://pgbackrest.org/release.html#2.55.0

* Mon Jan 20 2025 Devrim Gündüz <devrim@gunduz.org> - 2.54.2-1PGDG
- Update to 2.54.2, per changes described at:
  https://pgbackrest.org/release.html#2.54.2

* Mon Dec 16 2024 Devrim Gündüz <devrim@gunduz.org> - 2.54.1-1PGDG
- Update to 2.54.1, per changes described at:
  https://pgbackrest.org/release.html#2.54.1

* Mon Oct 21 2024 Devrim Gündüz <devrim@gunduz.org> - 2.54.0-1PGDG
- Update to 2.54.0, per changes described at:
  https://pgbackrest.org/release.html#2.54.0

* Mon Aug 19 2024 Devrim Gündüz <devrim@gunduz.org> - 2.53.1-1PGDG
- Update to 2.53.1, per changes described at:
  https://pgbackrest.org/release.html#2.53.1

* Mon Jul 22 2024 Devrim Gündüz <devrim@gunduz.org> - 2.53-1PGDG
- Update to 2.53, per changes described at:
  https://pgbackrest.org/release.html#2.53
- Remove RHEL 7 support.

* Tue Jun 25 2024 Devrim Gündüz <devrim@gunduz.org> - 2.52.1-1PGDG
- Update to 2.52.1 per changes described at:
  https://pgbackrest.org/release.html#2.52.1

* Mon May 27 2024 Devrim Gündüz <devrim@gunduz.org> - 2.52-1PGDG
- Update to 2.52, per changes described at:
  https://pgbackrest.org/release.html#2.52

* Mon May 27 2024 Devrim Gündüz <devrim@gunduz.org> - 2.51-2PGDG
- Override PostgreSQL version macros on RHEL 7 so that we can build
  pgbackrest it on this platform. Per report from Magnus.

* Mon Mar 25 2024 Devrim Gündüz <devrim@gunduz.org> - 2.51-1PGDG
- Update to 2.51, per changes described at:
  https://pgbackrest.org/release.html#2.51

* Mon Jan 22 2024 Devrim Gündüz <devrim@gunduz.org> - 2.50-1PGDG
- Update to 2.50, per changes described at:
  https://pgbackrest.org/release.html#2.50

* Tue Nov 28 2023 Devrim Gündüz <devrim@gunduz.org> - 2.49-1PGDG
- Update to 2.49, per changes described at:
  https://pgbackrest.org/release.html#2.49

* Mon Sep 25 2023 Devrim Gündüz <devrim@gunduz.org> - 2.48-1PGDG
- Update to 2.48, per changes described at:
  https://pgbackrest.org/release.html#2.48

* Mon Aug 21 2023 Devrim Gündüz <devrim@gunduz.org> 2.47-2PGDG
- Remove RHEL 6 bits

* Mon Jul 24 2023 Devrim Gündüz <devrim@gunduz.org> - 2.47-1PGDG
- Update to 2.47, per changes described at:
  https://pgbackrest.org/release.html#2.47
- Add PGDG branding

* Thu May 25 2023 Devrim Gündüz <devrim@gunduz.org> - 2.46-3
- Fix libssh2 dependency name on SLES.

* Wed May 24 2023 Devrim Gündüz <devrim@gunduz.org> - 2.46-2
- Add libssh2 dependency to fix sftp support. Per report from
  David Steele and Stefan Fercot.

* Mon May 22 2023 Devrim Gündüz <devrim@gunduz.org> - 2.46-1
- Update to 2.46, per changes described at:
  https://pgbackrest.org/release.html#2.46

* Tue Mar 21 2023 Devrim Gündüz <devrim@gunduz.org> - 2.45-1
- Update to 2.45, per changes described at:
  https://pgbackrest.org/release.html#2.45

* Mon Jan 30 2023 Devrim Gündüz <devrim@gunduz.org> - 2.44-1
- Update to 2.44, per changes described at:
  https://pgbackrest.org/release.html#2.44

* Tue Dec 6 2022 Devrim Gündüz <devrim@gunduz.org> - 2.43-2
- Remove Advance Toolchain support from RHEL 7 - ppc64le.

* Mon Nov 28 2022 Devrim Gündüz <devrim@gunduz.org> - 2.43-1
- Update to 2.43, per changes described at:
  https://pgbackrest.org/release.html#2.43

* Wed Nov 23 2022 Devrim Gündüz <devrim@gunduz.org> - 2.42-1
- Update to 2.42, per changes described at:
  https://pgbackrest.org/release.html#2.42

* Mon Sep 19 2022 Devrim Gündüz <devrim@gunduz.org> - 2.41-1
- Update to 2.41, per changes described at:
  https://pgbackrest.org/release.html#2.41

* Tue Jul 19 2022 Devrim Gündüz <devrim@gunduz.org> - 2.40-1
- Update to 2.40, per changes described at:
  https://pgbackrest.org/release.html#2.40

* Tue May 17 2022 Devrim Gündüz <devrim@gunduz.org> - 2.39-1
- Update to 2.39, per changes described at:
  https://pgbackrest.org/release.html#2.39

* Sun Mar 6 2022 Devrim Gündüz <devrim@gunduz.org> - 2.38-1
- Update to 2.38, per changes described at:
  https://pgbackrest.org/release.html#2.38

* Tue Jan 4 2022 Devrim Gündüz <devrim@gunduz.org> - 2.37-2
- Add unit file and systemd support for the TLS server feature.

* Mon Jan 3 2022 Devrim Gündüz <devrim@gunduz.org> - 2.37-1
- Update to 2.37, per changes described at:
  https://pgbackrest.org/release.html#2.37

* Mon Nov 1 2021 Devrim Gündüz <devrim@gunduz.org> - 2.36-1
- Update to 2.36, per changes described at:
  https://pgbackrest.org/release.html#2.36

* Tue Aug 24 2021 Devrim Gündüz <devrim@gunduz.org> - 2.35-1
- Update to 2.35, per changes described at:
  https://pgbackrest.org/release.html#2.35

* Mon Jun 7 2021 Devrim Gündüz <devrim@gunduz.org> - 2.34-1
- Update to 2.34, per changes described at:
  https://pgbackrest.org/release.html#2.34

* Tue Apr 6 2021 Devrim Gündüz <devrim@gunduz.org> - 2.33-1
- Update to 2.33

* Thu Feb 11 2021 Devrim Gündüz <devrim@gunduz.org> - 2.32-2
- Adjust dependencies for SLES 15 support.

* Tue Feb 9 2021 Devrim Gündüz <devrim@gunduz.org> - 2.32-1
- Update to 2.32, per changes described here:
  https://pgbackrest.org/release.html#2.32

* Wed Jan 6 2021 Devrim Gündüz <devrim@gunduz.org> - 2.31-2
- Add RHEL 7 - ppc64le support. While adding it, fix
  build issue on this platform, per report from Gunnar "Nick" Bluth.
  Patch from Debian folks.

* Tue Dec 8 2020 Devrim Gündüz <devrim@gunduz.org> - 2.31-1
- Update to 2.31

* Thu Oct 22 2020 Devrim Gündüz <devrim@gunduz.org> - 2.30-4
- User creation, etc. must be in pre part, which I broke in recent
  commits.

* Thu Oct 22 2020 Devrim Gündüz <devrim@gunduz.org> - 2.30-3
- Also create postgres' home directory, per Stefan Fercot

* Tue Oct 20 2020 Devrim Gündüz <devrim@gunduz.org> - 2.30-2
- Create postgres user, if it does not exist. Per report by Magnus.

* Tue Oct 6 2020 Devrim Gündüz <devrim@gunduz.org> - 2.30-1
- Update to 2.30

* Wed Sep 2 2020 Devrim Gündüz <devrim@gunduz.org> - 2.29-1
- Update to 2.29

- Add zstd library support
* Sun Jul 26 2020 Devrim Gündüz <devrim@gunduz.org> - 2.28-1
- Update to 2.28
- Add zstd library support

* Mon Jun 1 2020 Devrim Gündüz <devrim@gunduz.org> - 2.27-2
- Add a logrotate file

* Wed May 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.27-1
- Update to 2.27

* Mon Apr 20 2020 Devrim Gündüz <devrim@gunduz.org> - 2.26-1
- Update to 2.26

* Fri Mar 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.25-2
- Add SLES-12 support

* Thu Mar 26 2020 Devrim Gündüz <devrim@gunduz.org> - 2.25-1
- Update to 2.25

* Wed Feb 26 2020 Devrim Gündüz <devrim@gunduz.org> - 2.24-1
- Update to 2.24

* Tue Jan 28 2020 Devrim Gündüz <devrim@gunduz.org> - 2.23-1
- Update to 2.23

* Sat Jan 25 2020 Devrim Gündüz <devrim@gunduz.org> - 2.22-1
- Update to 2.22

* Thu Jan 16 2020 Devrim Gündüz <devrim@gunduz.org> - 2.21-1
- Update to 2.21

* Tue Nov 12 2019 Devrim Gündüz <devrim@gunduz.org> - 2.19-1
- Update to 2.19

* Wed Oct 2 2019 Devrim Gündüz <devrim@gunduz.org> - 2.18-1
- Update to 2.18
- Require versionless -libs subpackage. Fixes
  https://redmine.postgresql.org/issues/4799

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 2.17-1.1
- Rebuild for PostgreSQL 12

* Tue Sep 3 2019 Devrim Gündüz <devrim@gunduz.org> - 2.17-1
- Update to 2.17

* Fri Aug 9 2019 Devrim Gündüz <devrim@gunduz.org> - 2.16-1
- Update to 2.16

* Thu Jun 27 2019 Devrim Gündüz <devrim@gunduz.org> - 2.15.1-1
- Update to 2.15.1, which fixes an upstream tag issue.

* Tue Jun 25 2019 Devrim Gündüz <devrim@gunduz.org> - 2.15-1
- Update to 2.15

* Wed May 22 2019 Devrim Gündüz <devrim@gunduz.org> - 2.14-1
- Update to 2.14

* Fri Apr 19 2019 Devrim Gündüz <devrim@gunduz.org> - 2.13-1
- Update to 2.13

* Thu Apr 11 2019 Devrim Gündüz <devrim@gunduz.org> - 2.12-1
- Update to 2.12

* Mon Mar 11 2019 Devrim Gündüz <devrim@gunduz.org> - 2.11-1
- Update to 2.11

* Mon Feb 11 2019 Devrim Gündüz <devrim@gunduz.org> - 2.10-1
- Update to 2.10

* Thu Jan 31 2019 Devrim Gündüz <devrim@gunduz.org> - 2.09-1
- Update to 2.09

* Fri Jan 4 2019 Devrim Gündüz <devrim@gunduz.org> - 2.08-1
- Update to 2.08

* Sun Nov 18 2018 Devrim Gündüz <devrim@gunduz.org> - 2.07-1
- Update to 2.07

* Sun Oct 28 2018 Devrim Gündüz <devrim@gunduz.org> - 2.06-2
- Add missing BR

* Tue Oct 16 2018 Devrim Gündüz <devrim@gunduz.org> - 2.06-1
- Update to 2.06

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.05-1.1
- Rebuild against PostgreSQL 11.0

* Thu Sep 6 2018 - Devrim Gündüz <devrim@gunduz.org> 2.05-1
- Update to 2.05, per #3614.

* Sat Jul 14 2018 - Devrim Gündüz <devrim@gunduz.org> 2.04-1
- Update to 2.04, per #3474.

* Wed Jun 13 2018 - Devrim Gündüz <devrim@gunduz.org> 2.03-4
- Move perl-Time-HiRes dependency to global list, per
  https://github.com/pgbackrest/pgbackrest/issues/544

* Wed Jun 6 2018 - Devrim Gündüz <devrim@gunduz.org> 2.03-3
- Fix dependencies for RHEL 6, per #3387.

* Mon May 28 2018 - Devrim Gündüz <devrim@gunduz.org> 2.03-2
- Add new dependencies

* Thu May 24 2018 - Devrim Gündüz <devrim@gunduz.org> 2.03-1
- Update to 2.03, per #3366

* Mon May 7 2018 - Devrim Gündüz <devrim@gunduz.org> 2.02-1
- Update to 2.02, per #3335.

* Thu Mar 22 2018 - Devrim Gündüz <devrim@gunduz.org> 2.01-1
- Update to 2.01, per #3223

* Mon Feb 26 2018 - David Steele <david@pgbackrest.org> 2.00-1
- Update to 2.00, per #3152
- Build C pgbackrest bin, remove Perl bin

* Sun Feb 4 2018 - Devrim Gündüz <devrim@gunduz.org> 1.28-1
- Update to 1.28, per #3078

* Wed Dec 27 2017 - Devrim Gündüz <devrim@gunduz.org> 1.27-1
- Update to 1.27, per #2968

* Thu Dec 7 2017 - David Steele <david@pgbackrest.org> 1.26-3
- Cleanly build/install LibC. Fixes #2914

* Sun Dec 3 2017 - Devrim Gündüz <devrim@gunduz.org> 1.26-2
- Dirty hack to install libc related files manually. Fixes #2914

* Sun Nov 26 2017 - Devrim Gündüz <devrim@gunduz.org> 1.26-1
- Update to 1.26, per #2889
- Add perl-libc related files.

* Thu Oct 26 2017 - Devrim Gündüz <devrim@gunduz.org> 1.25-1
- Update to 1.25, per #2823

* Sun Oct 1 2017 - Devrim Gündüz <devrim@gunduz.org> 1.24-1
- Update to 1.24, per #2743

* Wed Sep 13 2017 - Devrim Gündüz <devrim@gunduz.org> 1.23-1
- Update to 1.23, per #2675.

* Thu Aug 10 2017 - Devrim Gündüz <devrim@gunduz.org> 1.22-1
- Update to 1.22, per #2643.

* Thu Jun 29 2017 - Devrim Gündüz <devrim@gunduz.org> 1.20-1
- Update to 1.20, per #2517.

* Tue Jun 13 2017 - Devrim Gündüz <devrim@gunduz.org> 1.19-1
- Update to 1.19, per #2483.

* Wed May 10 2017 - Devrim Gündüz <devrim@gunduz.org> 1.18-1
- Update to 1.18

* Tue Mar 14 2017 - Devrim Gündüz <devrim@gunduz.org> 1.17-1
- Update to 1.17

* Fri Mar 3 2017 - Devrim Gündüz <devrim@gunduz.org> 1.16-1
- Update to 1.16

* Wed Feb 8 2017 - Devrim Gündüz <devrim@gunduz.org> 1.13-1
- Update to 1.13

* Thu Dec 22 2016 - Devrim Gündüz <devrim@gunduz.org> 1.12-1
- Update to 1.12

* Thu Nov 17 2016 - Devrim Gündüz <devrim@gunduz.org> 1.11-1
- Update to 1.11

* Tue Nov 8 2016 - Devrim Gündüz <devrim@gunduz.org> 1.10-1
- Update to 1.10

* Thu Nov 3 2016 - Devrim Gündüz <devrim@gunduz.org> 1.09-1
- Update to 1.09
- Install default conf file, per David Steele.
- Install default directories, per David Steele.

* Sun Sep 18 2016 - Devrim Gündüz <devrim@gunduz.org> 1.08-1
- Update to 1.08

* Fri Aug 12 2016 - Devrim Gündüz <devrim@gunduz.org> 1.05-1
- Update to 1.05

* Fri May 27 2016 - Devrim Gündüz <devrim@gunduz.org> 1.01-1
- Initial packaging for PostgreSQL RPM Repository
