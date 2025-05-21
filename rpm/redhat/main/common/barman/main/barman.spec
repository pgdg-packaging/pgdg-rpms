%if 0%{?fedora} && 0%{?fedora} <= 42
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?suse_version} >= 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif

%{expand: %%global pybasever %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}

%global python_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Summary:	Backup and Recovery Manager for PostgreSQL
Name:		barman
Version:	3.14.0
Release:	42PGDG%{?dist}
License:	GPLv3
Url:		https://www.pgbarman.org/
Source0:	https://github.com/EnterpriseDB/%{name}/archive/refs/tags/release/%{version}.tar.gz
Source1:	%{name}.logrotate
Source2:	%{name}.cron
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel python%{python3_pkgversion}-setuptools

Requires:	/usr/sbin/useradd rsync >= 3.0.4
Requires:	python3-barman = %{version}

%description
Barman (Backup and Recovery Manager) is an open-source administration tool for
disaster recovery of PostgreSQL servers written in Python. It allows your
organization to perform remote backups of multiple servers in business
critical environments to reduce risk and help DBAs during the recovery phase.

Barman is distributed under GNU GPL 3 and maintained by EnterpriseDB.

%package -n barman-cli
Summary:	Client Utilities for Barman, Backup and Recovery Manager for PostgreSQL
Requires:	python3-barman = %{version}
%description -n barman-cli
Client utilities for the integration of Barman in PostgreSQL clusters.

%package -n python3-barman
Summary:	The shared libraries required for Barman family components
Requires:	python%{python3_pkgversion}-setuptools

%if 0%{?rhel} && 0%{?rhel} <= 9
Requires:	python%{python3_pkgversion}-dateutil
Requires:	python%{python3_pkgversion}-psycopg2 >= 2.9.9
Requires:	python%{python3_pkgversion}-six
%endif

%if 0%{?fedora} && 0%{?fedora} <= 42
Requires:	python3-argcomplete python3-dateutil
Requires:	python3-psycopg2 >= 2.9.9 python3-six
%endif

%if 0%{?rhel} && 0%{?rhel} >= 10
Requires:	python3-argcomplete python3-dateutil
Requires:	python3-psycopg2 >= 2.9.9 python3-six
%endif

%if 0%{?suse_version} >= 1500
Requires:	python%{python3_pkgversion}-argcomplete
Requires:	python%{python3_pkgversion}-python-dateutil
Requires:	python%{python3_pkgversion}-psycopg2 >= 2.9.9
Requires:	python%{python3_pkgversion}-six
%endif

%description -n python3-barman
Python libraries used by Barman.

%prep
%setup -q -n barman-release-%{version}

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}
%{__mkdir} -p %{buildroot}%{_sysconfdir}/bash_completion.d
%{__mkdir} -p %{buildroot}%{_sysconfdir}/cron.d/
%{__mkdir} -p %{buildroot}%{_sysconfdir}/logrotate.d/
%{__mkdir} -p %{buildroot}%{_sysconfdir}/barman.d/
%{__mkdir} -p %{buildroot}/var/lib/barman
%{__mkdir} -p %{buildroot}/var/log/barman
%{__install} -pm 644 docs/barman.conf %{buildroot}%{_sysconfdir}/barman.conf
%{__install} -pm 644 docs/barman.d/* %{buildroot}%{_sysconfdir}/barman.d/
%{__install} -pm 644 scripts/barman.bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/barman
%{__install} -pm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/barman
%{__install} -pm 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/cron.d/barman
touch %{buildroot}/var/log/barman/barman.log

%pre
groupadd -f -r barman >/dev/null 2>&1 || :
useradd -M -g barman -r -d /var/lib/barman -s /bin/bash \
	-c "Backup and Recovery Manager for PostgreSQL" barman >/dev/null 2>&1 || :

%files
%defattr(-,root,root)
%doc RELNOTES.md README.rst
%{_bindir}/%{name}
%doc %{_mandir}/man1/%{name}.1.gz
%doc %{_mandir}/man5/%{name}.5.gz
%config(noreplace) %{_sysconfdir}/bash_completion.d/
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/cron.d/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/barman.d/
%attr(700,barman,barman) %dir /var/lib/%{name}
%attr(755,barman,barman) %dir /var/log/%{name}
%attr(600,barman,barman) %ghost /var/log/%{name}/%{name}.log

%files -n barman-cli
%defattr(-,root,root)
%doc RELNOTES.md README.rst
%{_bindir}/barman-wal-archive
%{_bindir}/barman-wal-restore
%{_bindir}/barman-cloud-backup
%{_bindir}/barman-cloud-backup-delete
%{_bindir}/barman-cloud-backup-keep
%{_bindir}/barman-cloud-backup-show
%{_bindir}/barman-cloud-check-wal-archive
%{_bindir}/barman-cloud-wal-archive
%{_bindir}/barman-cloud-backup-list
%{_bindir}/barman-cloud-restore
%{_bindir}/barman-cloud-wal-restore
%doc %{_mandir}/man1/barman*

%files -n python3-barman
%defattr(-,root,root)
%doc RELNOTES.md README.rst
%{python_sitelib}/%{name}-%{version}%{?extra_version:%{extra_version}}-py%{pybasever}.egg-info
%{python_sitelib}/%{name}/

%changelog
* Wed May 21 2025 Devrim Gündüz <devrim@gunduz.org> - 3.14.0-43PGDG
- Fix setuptools dependency of python3-barman package. Per report from
  Matthew Gwillam-Kelly

* Fri May 16 2025 Devrim Gündüz <devrim@gunduz.org> - 3.14.0-42PGDG
- Update to 3.14.0, per changes described at:
  https://github.com/EnterpriseDB/barman/releases/tag/release%2F3.14.0
- Build with Python 3.12 on RHEL 9 & 8 and Python 3.11 on SLES 15.

* Mon May 5 2025 Devrim Gündüz <devrim@gunduz.org> - 3.13.3-43PGDG
- Rebuild on RHEL 8 per:
  https://github.com/EnterpriseDB/barman/issues/1084
  https://github.com/pgdg-packaging/pgdg-rpms/issues/5

* Thu Apr 24 2025 Devrim Gündüz <devrim@gunduz.org> - 3.13.3-42PGDG
- Update to 3.13.3, per changes described at:
  https://github.com/EnterpriseDB/barman/releases/tag/release%2F3.13.3

* Fri Mar 28 2025 Devrim Gündüz <devrim@gunduz.org> - 3.13.2-42PGDG
- Update to 3.13.2, per changes described at:
  https://github.com/EnterpriseDB/barman/releases/tag/release%2F3.13.2

* Sat Mar 22 2025 Devrim Gündüz <devrim@gunduz.org> - 3.13.1-42PGDG
- Update to 3.13.1, per changes described at:
  https://github.com/EnterpriseDB/barman/releases/tag/release%2F3.13.1

* Thu Feb 20 2025 Devrim Gündüz <devrim@gunduz.org> - 3.13.0-42PGDG
- Update to 3.13.0, per changes described at:
  https://github.com/EnterpriseDB/barman/releases/tag/release%2F3.13.0

* Sun Jan 5 2025 Devrim Gündüz <devrim@gunduz.org> - 3.12.1-43PGDG
- Add RHEL 10 support

* Mon Dec 9 2024 Devrim Gündüz <devrim@gunduz.org> - 3.12.1-42PGDG
- Update to 3.12.1, per changes described at:
  https://github.com/EnterpriseDB/barman/releases/tag/release%2F3.12.1

* Fri Nov 22 2024 Devrim Gündüz <devrim@gunduz.org> - 3.12.0-42PGDG
- Update to 3.12.0, per changes described at:
  https://github.com/EnterpriseDB/barman/releases/tag/release%2F3.12.0
- Remove RHEL 7 and SLES 12 bits

* Fri Aug 23 2024 Devrim Gündüz <devrim@gunduz.org> - 3.11.1-1PGDG
- Update to 3.11.1, per changes described at:
  https://github.com/EnterpriseDB/barman/releases/tag/release%2F3.11.1
  https://github.com/EnterpriseDB/barman/releases/tag/release%2F3.11.0

* Mon Jun 17 2024 Devrim Gündüz <devrim@gunduz.org> - 3.10.1-1PGDG
- Update to 3.10.1, per changes described at:
  https://github.com/EnterpriseDB/barman/releases/tag/release%2F3.10.1

* Fri Feb 9 2024 Devrim Gündüz <devrim@gunduz.org> - 3.10.0-42PGDG
- Bump up release number to override OS packages.

* Mon Jan 29 2024 Devrim Gündüz <devrim@gunduz.org> - 3.10.0-1PGDG
- Update to 3.10.0, per changes described at:
  https://github.com/EnterpriseDB/barman/releases/tag/release%2F3.10.0
- Fix rpmlint warning

* Thu Oct 5 2023 Devrim Gündüz <devrim@gunduz.org> - 3.9.0-1PGDG
- Update to 3.9.0, per changes described at:
  https://github.com/EnterpriseDB/barman/releases/tag/release%2F3.9.0

* Wed Sep 13 2023 Devrim Gündüz <devrim@gunduz.org> - 3.8.0-1PGDG
- Update to 3.8.0, per changes described at:
  https://github.com/EnterpriseDB/barman/releases/tag/release%2F3.8.0

,* Wed Jul 26 2023 Devrim Gündüz <devrim@gunduz.org> - 3.7.0-1PGDG
- Update to 3.7.0, per changes described at:
  https://github.com/EnterpriseDB/barman/releases/tag/release%2F3.7.0
- Add PGDG branding

* Thu Jun 15 2023 Devrim Gündüz <devrim@gunduz.org> - 3.6.0-1
- Update to 3.6.0, per changes described at:
  https://github.com/EnterpriseDB/barman/releases/tag/release%2F3.6.0

* Thu May 25 2023 Devrim Gündüz <devrim@gunduz.org> - 3.5.0-3
- Fix RHEL 7 dependency

* Fri Mar 31 2023 Devrim Gündüz <devrim@gunduz.org> - 3.5.0-2
- Fix psycopg2 dependency version.

* Thu Mar 30 2023 Devrim Gündüz <devrim@gunduz.org> - 3.5.0-1
- Update to 3.5.0, per changes described at:
  https://github.com/EnterpriseDB/barman/releases/tag/release%2F3.5.0
- Remove Python2 support from the spec file. Upstream now supports
  Python 3.6+.

* Fri Jan 27 2023 Devrim Gündüz <devrim@gunduz.org> - 3.4.0-1
- Update to 3.4.0, per changes described at:
  https://github.com/EnterpriseDB/barman/releases/tag/release%2F3.4.0

* Wed Dec 14 2022 Devrim Gündüz <devrim@gunduz.org> - 3.3.0-1
- Update to 3.3.0, per changes described at:
  https://github.com/EnterpriseDB/barman/releases/tag/release%2F3.3.0

* Fri Oct 21 2022 Devrim Gündüz <devrim@gunduz.org> - 3.2.0-1
- Update to 3.2.0, per changes described at:
  https://github.com/EnterpriseDB/barman/releases/tag/release%2F3.2.0

* Fri Sep 16 2022 Devrim Gündüz <devrim@gunduz.org> - 3.1.0-1
- Update to 3.1.0, per changes described at:
  https://github.com/EnterpriseDB/barman/releases/tag/release%2F3.1.0

* Wed Jun 29 2022 Devrim Gündüz <devrim@gunduz.org> - 3.0.1-1
- Update to 3.0.1, per changes described at:
  https://github.com/EnterpriseDB/barman/releases/tag/release%2F3.0.1

* Fri Jun 24 2022 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-1
- Update to 3.0.0, per changes described at:
  https://github.com/EnterpriseDB/barman/releases/tag/release%2F3.0.0

* Thu Mar 10 2022 Devrim Gündüz <devrim@gunduz.org> - 2.19-1
- Update to 2.19, per changes described at:
  https://github.com/EnterpriseDB/barman/releases/tag/release%2F2.19

* Mon Feb 21 2022 Devrim Gündüz <devrim@gunduz.org> - 2.18-2
- Remove argh dependency, per report from Michael Wallace.

* Mon Jan 24 2022 Devrim Gündüz <devrim@gunduz.org> - 2.18-1
- Update to 2.18, per changes described at:
  https://github.com/EnterpriseDB/barman/releases/tag/release%2F2.18

* Mon Dec 13 2021 Devrim Gündüz <devrim@gunduz.org> - 2.17-2
- Add argcomplete dependency to SLES 15, per report from
  Tiago ANASTACIO.

* Wed Dec 1 2021 Devrim Gündüz <devrim@gunduz.org> - 2.17-1
- Update to 2.17

* Mon Nov 29 2021 Devrim Gündüz <devrim@gunduz.org> - 2.16-2
- Un-break RHEL-7 upgrades.

* Mon Nov 29 2021 Devrim Gündüz <devrim@gunduz.org> - 2.16-1
- Update to 2.16

* Thu Nov 25 2021 Devrim Gündüz <devrim@gunduz.org> - 2.15-4
- Add RHEL 9 support

* Thu Nov 25 2021 Devrim Gündüz <devrim@gunduz.org> - 2.15-3
- Fix useradd for SLES

* Thu Nov 25 2021 Devrim Gündüz <devrim@gunduz.org> - 2.15-2
- Fix SLES 15 dependency

* Sat Oct 16 2021 Devrim Gündüz <devrim@gunduz.org> - 2.15-1
- Update to 2.15

* Thu Sep 23 2021 Devrim Gündüz <devrim@gunduz.org> - 2.14-1
- Update to 2.14

* Sun Aug 1 2021 Devrim Gündüz <devrim@gunduz.org> - 2.13-2
- Remove duplicate binaries from main package, per report from
  Abhijit Menon-Sen.

* Mon Jul 26 2021 Devrim Gündüz <devrim@gunduz.org> - 2.13-1
- Update to 2.13

* Thu Jul 1 2021 Devrim Gündüz <devrim@gunduz.org> - 2.12.1-1
- Update to 2.12.1
- Update Source URL

* Mon Nov 9 2020 Devrim Gündüz <devrim@gunduz.org> - 2.12-1
- Update to 2.12

* Fri Jul 10 2020 Devrim Gündüz <devrim@gunduz.org> - 2.11-1
- Update to 2.11

* Tue Dec 10 2019 Devrim Gündüz <devrim@gunduz.org> - 2.10-2
- Fix SLES 12 dependency.

* Tue Dec 10 2019 Devrim Gündüz <devrim@gunduz.org> - 2.10-1
- Update to 2.10, per changes described at:
  https://www.pgbarman.org/barman-2-10-released/#release-notes
- Add a temp patch, per https://redmine.postgresql.org/issues/4992#note-2
- Relax SLES 12 dependencies. Per #4910

* Mon Aug 5 2019 Devrim Gündüz <devrim@gunduz.org> - 2.9-2
- Un-break RHEL 6 packages. Per https://redmine.postgresql.org/issues/4767

* Mon Aug 5 2019 Devrim Gündüz <devrim@gunduz.org> - 2.9-1
- Update to 2.9

* Wed May 15 2019 Marco Nenciarini <marco.nenciarini@2ndquadrant.it> 2.8-1
- New upstream version 2.8
- Add python3-barman and barman-cli binaries
- Build with python3 on FC > 27 and RHEL >= 8

* Sun Mar 24 2019 Devrim Gündüz <devrim@gunduz.org> - 2.7-1
- Update to 2.7

* Tue Feb 5 2019 Devrim Gündüz <devrim@gunduz.org> - 2.6-1
- Update to 2.6

* Sat Dec 1 2018 Devrim Gündüz <devrim@gunduz.org> - 2.5-2
- Fix RHEL 6 builds

* Fri Nov 16 2018 Devrim Gündüz <devrim@gunduz.org> - 2.5-1
- Update to 2.5

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.4-1.1
- Rebuild against PostgreSQL 11.0

* Wed Jun 6 2018 - Devrim Gündüz <devrim@gunduz.org> 2.4-1
- Update to 2.4, per #3402
- Perform a cleanup in th spec file, use macros for some binaries, remove

* Wed Sep 13 2017 - Devrim Gündüz <devrim@gunduz.org> 2.3-1
- Update to 2.3, per #2682.
- Perform a cleanup in th spec file, use macros for some binaries, remove
  RHEL 5 references, and remove excessive macro usage in version and release
  number.
- Use separate sources for logrotate and cron files.

* Tue Jul 18 2017 - Devrim Gündüz <devrim@gunduz.org> 2.2-1
- Update to 2.2

* Fri Jan 6 2017 - Devrim Gündüz <devrim@gunduz.org> 2.1-1
- Update to 2.1

* Tue Sep 27 2016 - Gabriele Bartolini <gabriele.bartolini@2ndquadrant.it> 2.0-1
- New release 2.0-1
- Trim changelog for releases 1.X
