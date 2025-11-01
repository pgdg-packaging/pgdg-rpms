%global _vpath_builddir .
%global sname	pgagent

Summary:	Job scheduler for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	4.2.3
Release:	5PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/pgadmin-org/%{sname}/archive/refs/tags/%{sname}-%{version}.tar.gz
Source2:	%{sname}-%{pgmajorversion}.service
Source6:	%{sname}-sysusers.conf
Source7:	%{sname}-tmpfiles.d
URL:		https://github.com/pgadmin-org/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	cmake >= 3.0.0

%if 0%{?suse_version} == 1500
BuildRequires:	libboost_date_time1_66_0 libboost_thread1_66_0
BuildRequires:	libboost_system1_66_0 libboost_serialization1_66_0
BuildRequires:	libboost_serialization1_66_0-devel libboost_atomic1_66_0-devel
%endif
%if 0%{?suse_version} == 1600
BuildRequires:	libboost_date_time1_86_0 libboost_thread1_86_0
BuildRequires:	libboost_system1_86_0 libboost_serialization1_86_0
BuildRequires:	libboost_serialization1_86_0-devel libboost_atomic1_86_0-devel
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	boost-thread, boost-system, boost-date-time, boost-serialization
%endif

BuildRequires:		systemd, systemd-devel
Requires:		systemd
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd

%description
pgAgent is a job scheduler for PostgreSQL which may be managed
using pgAdmin.

pgAgent is managed using pgAdmin (http://www.pgadmin.org). The pgAdmin
documentation contains details of the setup and use of pgAgent with your
PostgreSQL system.

%pre
if [ $1 -eq 1 ] ; then
%sysusers_create_package %{name} %SOURCE6
touch /var/log/pgagent_%{pgmajorversion}.log
fi
%{__chown} pgagent:pgagent /var/log/pgagent_%{pgmajorversion}.log
%{__chmod} 0700 /var/log/pgagent_%{pgmajorversion}.log

%prep
%setup -q -n %{sname}-%{sname}-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS -fPIC -pie"
CXXFLAGS="$RPM_OPT_FLAGS -fPIC -pie -pthread -std=c++11"
export CFLAGS
export CXXFLAGS
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1500
cmake \
%endif
%else
%cmake3 \
%endif
	-D CMAKE_INSTALL_PREFIX:PATH=/usr \
	-D PG_CONFIG_PATH:FILEPATH=%{pginstdir}/bin/pg_config \
	-D STATIC_BUILD:BOOL=OFF .

%install
%{__rm} -rf %{buildroot}
%{__make} -C "%{_vpath_builddir}" DESTDIR=%{buildroot} install

# Rename pgagent binary, so that we can have parallel installations:
%{__mv} -f %{buildroot}%{_bindir}/%{sname} %{buildroot}%{_bindir}/%{name}
# Remove some cruft, and also install doc related files to appropriate directory:
%{__mkdir} -p %{buildroot}%{_datadir}/%{name}-%{version}
%{__rm} -f %{buildroot}/usr/LICENSE
%{__rm} -f %{buildroot}/usr/README
%{__mv} -f %{buildroot}%{_datadir}/pgagent*.sql %{buildroot}%{_datadir}/%{name}-%{version}/

# Install unit file
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{sname}_%{pgmajorversion}.service
# Install conf file
%{__install} -p -d %{buildroot}%{_sysconfdir}/%{sname}/
cat > %{buildroot}%{_sysconfdir}/%{sname}/%{name}.conf <<EOF
DBNAME=postgres
DBUSER=postgres
DBHOST=127.0.0.1
DBPORT=5432
LOGFILE=/var/log/pgagent_%{pgmajorversion}.log
EOF

%{__install} -m 0644 -D %{SOURCE6} %{buildroot}%{_sysusersdir}/%{name}-pgdg.conf

%{__mkdir} -p %{buildroot}/%{_tmpfilesdir}
%{__install} -m 0644 %{SOURCE7} %{buildroot}/%{_tmpfilesdir}/%{sname}_%{pgmajorversion}.conf

# Install logrotate file:
%{__install} -p -d %{buildroot}%{_sysconfdir}/logrotate.d
cat > %{buildroot}%{_sysconfdir}/logrotate.d/%{name} <<EOF
/var/log/pgagent_%{pgmajorversion}.log {
    missingok
    compress
    notifempty
    sharedscripts
    create 0640 pgagent pgagent
    nodateext
    weekly
    rotate 5
}
EOF

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-, root, root)
%doc README
%license LICENSE
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_datadir}/%{name}-%{version}/%{sname}*.sql
%ghost %{_rundir}/%{sname}
%{_sysusersdir}/%{name}-pgdg.conf
%{_tmpfilesdir}/%{sname}_%{pgmajorversion}.conf
%{_unitdir}/%{sname}_%{pgmajorversion}.service
%dir %{_sysconfdir}/%{sname}/
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/%{sname}/%{name}.conf
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Sat Nov 1 2025 Devrim Gunduz <devrim@gunduz.org> - 4.2.3-5PGDG
- Fix name of the tmpfiles.d file

* Tue Oct 28 2025 Devrim Gunduz <devrim@gunduz.org> - 4.2.3-4PGDG
- Fix tmpfiles.d file

* Mon Oct 6 2025 Devrim Gunduz <devrim@gunduz.org> - 4.2.3-3PGDG
- Add SLES 16 support
- Add sysusers.d and tmpfiles.d config file to allow rpm to create
  users/groups automatically.

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 4.2.3-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Mon Jan 6 2025 Devrim Gündüz <devrim@gunduz.org> - 4.2.3-1PGDG
- Update to 4.2.3 per changes described at
  https://github.com/pgadmin-org/pgagent/releases/tag/pgagent-4.2.3

* Sat Jan 4 2025 Devrim Gündüz <devrim@gunduz.org> - 4.2.2-6GDG
- Remove RHEL 7 and SLES 12 support.

* Thu Feb 22 2024 Devrim Gündüz <devrim@gunduz.org> - 4.2.2-5GDG
- Relax boost dependency on SLES 15 a bit. 1.66 is the version in the
  main SLES repos, so use that.

* Wed Feb 7 2024 Devrim Gündüz <devrim@gunduz.org> - 4.2.2-4PGDG
- Add SLES 15 support
- Add PGDG branding

* Sat Feb 4 2023 Devrim Gündüz <devrim@gunduz.org> - 4.2.2-3
- Switch on C++11 support on older GCC versions (in this case,
  RHEL 7).

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 4.2.2-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Sep 14 2022 Devrim Gündüz <devrim@gunduz.org> - 4.2.2-1
- Update to 4.2.2
- Update URLs

* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> - 4.2.1-1
- Move .conf and .logrotate files to spec file, so that we
  do less work during each PostgreSQL major release.

* Thu Apr 1 2021 Devrim Gündüz <devrim@gunduz.org> - 4.2.1-0
- Update to 4.2.1

* Thu Oct 29 2020 Devrim Gündüz <devrim@gunduz.org> - 4.0.0-5
- Use cmake3 macro to build packages, and define vpath_builddir macro
  manually. This will solve the FTBFS issue on Fedora 33, per:
  https://fedoraproject.org/wiki/Changes/CMake_to_do_out-of-source_builds
  Also works on the other distros.

* Mon Mar 23 2020 Devrim Gündüz <devrim@gunduz.org> - 4.0.0-4
- Make sure that pgAgent restarts itself after a failure.

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 4.0.0-3.1
- Rebuild for PostgreSQL 12

* Fri Apr 12 2019 Devrim Gündüz <devrim@gunduz.org> - 4.0.0-3
- Really fix pgAgent tmpfiles.d directory.

* Fri Jan 4 2019 Devrim Gündüz <devrim@gunduz.org> - 4.0.0-2
- Fix/update pgAgent tmpfiles.d directory.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 4.0.0-1.1
- Rebuild against PostgreSQL 11.0

* Thu Aug 9 2018 Devrim Gündüz <devrim@gunduz.org> 4.0.0-1
- Update to 4.0.0
- Add -pthread to CXXFLAGS

* Tue Oct 17 2017 Devrim Gündüz <devrim@gunduz.org> 3.4.0-10
- Move configuration parameters out of the unit file to a
  new config file.
- Add a new patch to fix builds against PostgreSQL 10

* Sun Jul 30 2017 Devrim Gündüz <devrim@gunduz.org> 3.4.0-9
- Install a logrotate file.

* Fri Jul 28 2017 Devrim Gündüz <devrim@gunduz.org> 3.4.0-8
- Improve unit file, so that pgagent actually stops.

* Mon Jul 24 2017 Devrim Gündüz <devrim@gunduz.org> 3.4.0-7
- Fix unit file name in spec file, per Fahar Abbas (EDB QA testing)

* Tue Jul 18 2017 Devrim Gündüz <devrim@gunduz.org> 3.4.0-6
- Add wxBase dependency, per Fahar Abbas (EDB QA testing)

* Fri Nov 11 2016 Devrim Gündüz <devrim@gunduz.org> 3.4.0-5
- Install init script on RHEL <= 6, not unit file.

* Wed Oct 19 2016 Devrim Gündüz <devrim@gunduz.org> 3.4.0-4
- Fix PostgreSQL version in unit file and init script. Per
  report from Alf Normann Klausen, pgsql bug #14370.

* Fri Jan 22 2016 Devrim Gündüz <devrim@gunduz.org> 3.4.0-3
- Create unified spec file that works with all distros.
- Fix an issue with user and group creation.

* Wed Dec 30 2015 Devrim Gündüz <devrim@gunduz.org> 3.4.0-2
- Build with -fPIC, per Fedora 23+ guidelines.
- Use more macros.
- Update license.
- Update download URL.

* Fri Oct 17 2014 Devrim Gündüz <devrim@gunduz.org> 3.4.0-1
- Update to 3.4.0
- Use macros for pgagent, where appropriate.
- Switch to systemd, and use unit file instead of sysV init
  script.
- Add PostgreSQL major version number to pgagent binary, to
  enable parallel installations.

* Mon Sep 17 2012 Devrim Gündüz <devrim@gunduz.org> 3.3.0-1
- Update to 3.3.0

* Wed Sep 12 2012 Devrim Gündüz <devrim@gunduz.org> 3.2.1-1
- Various updates from David Wheeler
- Update to 3.2.1
- Improve init script

* Tue Dec 6 2011 Devrim Gündüz <devrim@gunduz.org> 3.0.1-1
- Initial packaging

