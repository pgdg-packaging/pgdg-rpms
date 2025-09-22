Name:		pgbouncer
Version:	1.24.1
Release:	43PGDG%{?dist}
Summary:	Lightweight connection pooler for PostgreSQL
License:	MIT and BSD
URL:		https://www.pgbouncer.org/
Source0:	https://www.pgbouncer.org/downloads/files/%{version}/%{name}-%{version}.tar.gz
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
Source4:	%{name}.service
Source5:	%{name}-sysusers.conf
Patch0:		%{name}-ini.patch

Requires:	python3 python3-psycopg2

BuildRequires:	libevent-devel >= 2.0
Requires:	libevent >= 2.0

BuildRequires:	openssl-devel pam-devel

%if 0%{?fedora} >= 41 || 0%{?rhel} >= 9
BuildRequires:	c-ares-devel >= 1.13
Requires:	c-ares >= 1.13
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	c-ares-devel >= 1.13
Requires:	libcares2 >= 1.19
%endif

BuildRequires:		systemd
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

%description
pgbouncer is a lightweight connection pooler for PostgreSQL.
pgbouncer uses libevent for low-level socket handling.

%prep
%setup -q
%patch -P 0 -p0

%build
sed -i.fedora \
 -e 's|-fomit-frame-pointer||' \
 -e '/BININSTALL/s|-s||' \
 configure

# c-ares >= 1.16 is needed for proper c-ares support. Currently
# only RHEL 8 does not have it, so use libevent only on RHEL 8.
# Per https://redmine.postgresql.org/issues/6315
%configure \
	--datadir=%{_datadir} \
%if 0%{?rhel} <= 8
	--without-cares \
%else
	--with-cares --disable-evdns \
%endif

%{__make} %{?_smp_mflags} V=1

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
# Install sysconfig file
%{__install} -p -d %{buildroot}%{_sysconfdir}/%{name}/
%{__install} -p -d %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -p -m 644 etc/pgbouncer.ini %{buildroot}%{_sysconfdir}/%{name}
%{__install} -p -m 700 etc/mkauth.py %{buildroot}%{_sysconfdir}/%{name}/

%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/%{name}.service

# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}%{_tmpfilesdir}
cat > %{buildroot}%{_tmpfilesdir}/%{name}.conf <<EOF
d %{_rundir}/%{name} 0700 pgbouncer pgbouncer -
EOF

# Install sysusers.d config file to allow rpm to create users/groups automatically.
%{__install} -m 0644 -D %{SOURCE5} %{buildroot}%{_sysusersdir}/%{name}-pgdg.conf

# Create the directory for the pid files (defined in pgbouncer.ini)
%{__install} -d -m 755 %{buildroot}/var/run/%{name}

# Install logrotate file:
%{__install} -p -d %{buildroot}%{_sysconfdir}/logrotate.d
%{__install} -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# It seems we need to do this manually on SuSE:
%if 0%{?suse_version}
%{__mkdir} -p %{buildroot}%{_defaultdocdir}
%{__mv} %{buildroot}/usr/share/doc/%{name} %{buildroot}%{_defaultdocdir}/
%endif

%post
%systemd_post %{name}.service

if [ ! -d %{_localstatedir}/log/pgbouncer ] ; then
%{__mkdir} -m 700 %{_localstatedir}/log/pgbouncer
fi
%{__chown} -R pgbouncer:pgbouncer %{_localstatedir}/log/pgbouncer
%{__chown} -R pgbouncer:pgbouncer %{_rundir}/%{name} >/dev/null 2>&1 || :

%pre
groupadd -r pgbouncer >/dev/null 2>&1 || :
useradd -m -g pgbouncer -r -s /bin/bash \
	-c "PgBouncer Server" pgbouncer >/dev/null 2>&1 || :

%preun
%systemd_preun %{name}.service

%postun
if [ $1 -eq 0 ]; then
%{__rm} -rf %{_rundir}/%{name}
fi
%systemd_postun_with_restart %{name}.service

%files
%doc %{_defaultdocdir}/pgbouncer
%license COPYRIGHT
%dir %{_sysconfdir}/%{name}
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.ini
%ghost %{_rundir}/%{name}
%{_tmpfilesdir}/%{name}.conf
%{_sysusersdir}/%{name}-pgdg.conf
%attr(644,root,root) %{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_mandir}/man1/%{name}.*
%{_mandir}/man5/%{name}.*
%{_sysconfdir}/%{name}/mkauth.py*
%attr(755,pgbouncer,pgbouncer) %dir /var/run/%{name}

%changelog
* Mon Sep 22 2025 Devrim Gündüz <devrim@gunduz.org> - 1.24.1-43PGDG
- Add sysusers.d config file to allow rpm to create users/groups automatically.
- Add c-ares support to SLES 15 as well.

* Wed Apr 16 2025 Devrim Gündüz <devrim@gunduz.org> - 1.24.1-42PGDG
- Update to 1.24.1, per changes described at:
  http://www.pgbouncer.org/changelog.html#pgbouncer-124x

* Fri Jan 10 2025 Devrim Gündüz <devrim@gunduz.org> - 1.24.0-42PGDG
- Update to 1.24.0, per changes described at:
  http://www.pgbouncer.org/changelog.html#pgbouncer-124x

* Fri Aug 2 2024 Devrim Gündüz <devrim@gunduz.org> - 1.23.1-42PGDG
- Update to 1.23.1, per changes described at:
  http://www.pgbouncer.org/changelog.html#pgbouncer-123x
- Remove RHEL 7 and SLES 12 support from the spec file.

* Fri Jul 5 2024 Devrim Gündüz <devrim@gunduz.org> - 1.23.0-42PGDG
- Update to 1.23.0, per changes described at:
  http://www.pgbouncer.org/changelog.html#pgbouncer-123x

* Mon Mar 4 2024 Devrim Gündüz <devrim@gunduz.org> - 1.22.1-42PGDG
- Update to 1.22.1, per changes described at:
  https://www.pgbouncer.org/2024/03/pgbouncer-1-22-1

* Thu Feb 1 2024 Devrim Gündüz <devrim@gunduz.org> - 1.22.0-42PGDG
- Update to 1.22.0, per changes described at:
  https://www.pgbouncer.org/changelog.html#pgbouncer-122x
- Merge systemd unit file changes from upstream.
- Cleanup rpmlint warnings

* Tue Oct 17 2023 Devrim Gündüz <devrim@gunduz.org> - 1.21.0-42PGDG
- Update to 1.21.0, per changes described at:
  https://www.pgbouncer.org/changelog.html#pgbouncer-121x

* Wed Aug 9 2023 Devrim Gündüz <devrim@gunduz.org> - 1.20.1-42PGDG
- Update to 1.20.1, per changes described at:
  https://www.pgbouncer.org/changelog.html#pgbouncer-120x

* Mon Jul 24 2023 Devrim Gündüz <devrim@gunduz.org> - 1.20.0-42PGDG
- Update to 1.20.0, per changes described at:
  https://www.pgbouncer.org/changelog.html#pgbouncer-120x
- Add PGDG branding

* Tue Jun 6 2023 Devrim Gündüz <devrim@gunduz.org> - 1.19.1-42.1
- Add libevent dependency to all platforms, per
  https://github.com/pgbouncer/pgbouncer/issues/861

* Wed May 31 2023 Devrim Gündüz <devrim@gunduz.org> - 1.19.1-42
- Update to 1.19.1, per changes described at:
  https://www.pgbouncer.org/changelog.html#pgbouncer-119x

* Thu May 4 2023 Devrim Gündüz <devrim@gunduz.org> - 1.19.0-42
- Update to 1.19.0, per changes described at:
  https://www.pgbouncer.org/changelog.html#pgbouncer-119x

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 1.18.0-11.1
- Modernise %%patch usage, which has been deprecated in Fedora 38

* Mon Dec 12 2022 Devrim Gündüz <devrim@gunduz.org> - 1.18.0-11
- Update to 1.18.0, per changes described at:
  https://www.pgbouncer.org/changelog.html#pgbouncer-118x
- Clean up pgbouncer service file after un-daemoninizing, per report
  from Jelte Fennema: https://redmine.postgresql.org/issues/7559

* Tue Dec 6 2022 Devrim Gündüz <devrim@gunduz.org> - 1.17.0-11
- Remove Advance Toolchain support from RHEL 7 - ppc64le.

* Fri Mar 25 2022 Devrim Gündüz <devrim@gunduz.org> - 1.17.0-10
- Update to 1.17.0, per changes described at:
  https://www.pgbouncer.org/changelog.html#pgbouncer-117x
- Remove patch1, no longer needed.

* Tue Feb 22 2022 Devrim Gündüz <devrim@gunduz.org> - 1.16.1-10
- Do not use c-ares on RHEL 8, per report from Jonathan Katz:
  https://redmine.postgresql.org/issues/6315

* Wed Jan 5 2022 Devrim Gündüz <devrim@gunduz.org> - 1.16.1-2
- Require python3 explicitly. Default and RHEL/Rocky 8 images
  install python39 as default, where psycopg2 uses 3.6. Requiring
  python3 installs python36 on RHEL 8.
- Remove RHEL 6 bits.

* Thu Nov 11 2021 Devrim Gündüz <devrim@gunduz.org> - 1.16.1-1
- Update to 1.16.1, per changes described at:
  http://www.pgbouncer.org/changelog.html#pgbouncer-116x

* Wed Aug 11 2021 Devrim Gündüz <devrim@gunduz.org> - 1.16.0-1
- Update to 1.16.0, per changes described at:
  http://www.pgbouncer.org/changelog.html#pgbouncer-116x

* Fri Feb 12 2021 Devrim Gündüz <devrim@gunduz.org> - 1.15.0-2
- Fix SLES 15 dependency.

* Thu Aug 13 2020 Devrim Gündüz <devrim@gunduz.org> - 1.15.0-1
- Update to 1.15.0, per changes described at:
  http://www.pgbouncer.org/changelog.html#pgbouncer-115x

* Thu Aug 13 2020 Devrim Gündüz <devrim@gunduz.org> - 1.14.0-3
- Build with systemd support, per
  https://bugzilla.redhat.com/show_bug.cgi?id=1858814

* Fri Aug 7 2020 Devrim Gündüz <devrim@gunduz.org> - 1.14.0-2
- Fix RHEL 6 dependency, per PG bug 16573.

* Thu Jun 11 2020 Devrim Gündüz <devrim@gunduz.org> - 1.14.0-1
- Update to 1.14.0

* Wed Apr 29 2020 Devrim Gündüz <devrim@gunduz.org> - 1.13.0-1
- Update to 1.13.0
- Switch to pgdg-srpm-macros

* Wed Feb 26 2020 Devrim Gündüz <devrim@gunduz.org> - 1.12.0-4
- Fix c-ares support. Per Peter:
  https://redmine.postgresql.org/issues/4808

* Thu Dec 19 2019 - John Harvey <john.harvey@crunchydata.com> 1.12.0-3
- Make sure that directory /var/run/pgbouncer is created with the RPM.
  This will ensure that pgbouncer.ini will work with its defaults.

* Thu Oct 17 2019 Devrim Gündüz <devrim@gunduz.org> - 1.12.0-2
- Use python3-psycopg2 as the dependency. instead of python-psycopg2.
  This will help us to solve conflict on Fedora 31 and onwards.
  All supported distros have this dependency anyway.

* Thu Oct 17 2019 Devrim Gündüz <devrim@gunduz.org> - 1.12.0-1
- Update to 1.12.0

* Tue Aug 27 2019 Devrim Gündüz <devrim@gunduz.org> - 1.11.0-1
- Update to 1.11.0

* Tue Jul 2 2019 Devrim Gündüz <devrim@gunduz.org> - 1.10.0-1
- Update to 1.10.0

* Thu Jun 27 2019 Devrim Gündüz <devrim@gunduz.org> - 1.9.0-3
- Change/Fix pgBouncer systemd configuration, per Peter:
  https://redmine.postgresql.org/issues/4398

* Fri Apr 12 2019 Devrim Gündüz <devrim@gunduz.org> - 1.9.0-2
- Fix tmpfiles.d directory.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.9.0-1.1
- Rebuild against PostgreSQL 11.0

* Tue Aug 21 2018 Devrim Gündüz <devrim@gunduz.org> - 1.9.0-1
- Update to 1.9.0

* Fri Mar 2 2018 Devrim Gündüz <devrim@gunduz.org> - 1.8.1-2
- Add python-psycopg2 as requires, for mkauth.py

* Wed Dec 20 2017 Devrim Gündüz <devrim@gunduz.org> - 1.8.1-1
- Update to 1.8.1, and enable pam support.

* Tue Jul 18 2017 Devrim Gündüz <devrim@gunduz.org> - 1.7.2-7
- Add libevent dependency, per Fahar Abbas (EDB QA testing)

* Wed Sep 28 2016 Devrim Gündüz <devrim@gunduz.org> - 1.7.2-6
- Depend on libevent2 on RHEL 6, which is available as of
  RHEL 6.8. This change means we ask all users to upgrade to
  at least to RHEL 6.8. We require this for other packages already,
  so it should not be an issue. This also will eliminate the need
  for compat-libevent14 package that we ship in our repo. Fixes #1718.

* Tue Aug 9 2016 Devrim Gündüz <devrim@gunduz.org> - 1.7.2-5
- Switch to c-ares. Per Omar Kilani. Fixes #1444

* Mon Jul 18 2016 Devrim Gündüz <devrim@gunduz.org> - 1.7.2-4
- Don't remove /var/run/pgbouncer directory on upgrade. Per
  report from Eric Radman.
- Attempt to create the log directory only if does not exist.

* Thu Jul 7 2016 Devrim Gündüz <devrim@gunduz.org> - 1.7.2-3
- Fix issues in systemd file, per report from Jehan-Guillaume,
  per #1339.

* Wed Mar 30 2016 Devrim Gündüz <devrim@gunduz.org> - 1.7.2-2
- Fix Reload in systemd unit file, per #1042.
  Analysis and fix by Jehan-Guillaume de Rorthais.

* Tue Mar 15 2016 Devrim Gündüz <devrim@gunduz.org> - 1.7.2-1
- Update to 1.7.2, per #1033.

* Mon Feb 22 2016 Devrim Gündüz <devrim@gunduz.org> - 1.7.1-1
- Update to 1.7.1, per #1011.
- Fix wrong log file name in sysconfig file, per #1008.
- Add openssl-devel as BR.
- Fix logrotate file, per #1009.

* Wed Dec 30 2015 Devrim Gündüz <devrim@gunduz.org> - 1.7-1
- Update to 1.7

* Mon Sep 7 2015 Devrim Gündüz <devrim@gunduz.org> - 1.6.1-1
- Update to 1.6.1
- Fix startup issues: The tmpfiles.d file was not created
  correctly, causing startup failures due to permissions.
- Fix systemd file: Use -q, not -v.

* Tue May 12 2015 Devrim Gündüz <devrim@gunduz.org> - 1.5.5-2
- Fix service file, per Peter Eisentraut.
- Fix permissions of unit file and logrotate conf file. Per
  Peter Eisentraut.
- Fix logrotate configuration. Per Peter Eisentraut.
- Apply some spec file fixes so that we can use it on all
  platforms.

* Fri Apr 17 2015 Devrim Gündüz <devrim@gunduz.org> - 1.5.5-1
- Update to 1.5.5
- Update to new URL
- Revert chown'ing /etc/pgbouncer to pgbouncer user, and keep
  it as root.
- Add systemd support, and convert the spec file to unified
  spec file for all platforms

* Mon May 19 2014 Devrim Gündüz <devrim@gunduz.org> - 1.5.4-3
- Add logrotate file. It was already available in svn, but
  apparently I forgot to add it to spec file. Per an email from
  Jens Wilke.
- Change ownership of /etc/pgbouncer directory, to pgbouncer user.
  Per Jens Wilke.

* Mon Sep 16 2013 Devrim Gündüz <devrim@gunduz.org> - 1.5.4-2
- Update init script, per #138, which fixes the following.
  Contributed by Peter:
 - various legacy code of unknown purpose
 - no LSB header
 - used the script name as NAME, making it impossible to copy
   the script and run two pgbouncers
 - didn't use provided functions like daemon and killproc
 - incorrect exit codes when starting already started service and
   stopping already stopped service (nonstandard condstop action
   was a partial workaround?)
 - restart didn't make use of pgbouncer -R option

* Mon Dec 10 2012 Devrim Gündüz <devrim@gunduz.org> - 1.5.4-1
- Update to 1.5.4

* Wed Sep 12 2012 Devrim Gündüz <devrim@gunduz.org> - 1.5.3-1
- Update to 1.5.3, per changes described at:
  http://pgfoundry.org/forum/forum.php?forum_id=1981

* Tue Jul 31 2012 Devrim Gündüz <devrim@gunduz.org> - 1.5.2-3
- Add mkauth.py among installed files.

* Thu Jun 21 2012 Devrim Gündüz <devrim@gunduz.org> - 1.5.2-2
- Fix useradd line.

* Tue Jun 5 2012 Devrim Gündüz <devrim@gunduz.org> - 1.5.2-1
- Update to 1.5.2, per changes described at:
  http://pgfoundry.org/forum/forum.php?forum_id=1885

* Tue May 15 2012 Devrim Gündüz <devrim@gunduz.org> - 1.5.1-1
- Update to 1.5.1

* Sun Apr 08 2012 Devrim Gündüz <devrim@gunduz.org> - 1.5-2
-  Fix shell of pgbouncer user, to avoid startup errors.

* Fri Apr 6 2012 Devrim Gündüz <devrim@gunduz.org> - 1.5-1
- Update to 1.5, for the changes described here:
  http://pgfoundry.org/frs/shownotes.php?release_id=1920
- Trim changelog

* Fri Aug 12 2011 Devrim Gündüz <devrim@gunduz.org> - 1.4.2-1
- Update to 1.4.2, for the changes described here:
  http://pgfoundry.org/frs/shownotes.php?release_id=1863

* Mon Sep 13 2010 Devrim Gündüz <devrim@gunduz.org> - 1.3.4-1
- Update to 1.3.4, for the changes described here:
  http://pgfoundry.org/frs/shownotes.php?prelease_id=1698
* Fri Aug 06 2010 Devrim Gündüz <devrim@gunduz.org> - 1.3.3-2
- Sleep 2 seconds before getting pid during start(), like we do in PostgreSQL
  init script, to avoid false positive startup errors.

* Tue May 11 2010 Devrim Gündüz <devrim@gunduz.org> - 1.3.3-1
- Update to 1.3.3, per pgrpms.org #25, for the fixes described at:
  http://pgfoundry.org/frs/shownotes.php?release_id=1645

* Tue Mar 16 2010 Devrim Gündüz <devrim@gunduz.org> - 1.3.2-1
- Fix some issues in init script. Fixes pgrpms.org #9.
