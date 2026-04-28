%if 0%{?fedora} && 0%{?fedora} == 44
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?fedora} && 0%{?fedora} == 43
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?fedora} && 0%{?fedora} <= 42
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?suse_version} == 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

%if 0%{?fedora} >= 42 || 0%{?rhel} >= 10 || 0%{?suse_version} >= 1500
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Summary:	MySQL to PostgreSQL replica system
Name:		pg_chameleon
Version:	2.0.21
Release:	4PGDG%{?dist}
License:	BSD
Source0:	https://github.com/the4thdoctor/%{name}/archive/v%{version}.tar.gz
URL:		https://github.com/the4thdoctor/%{name}
BuildArch:	noarch

%if 0%{?fedora} >= 42 || 0%{?rhel} >= 8
Requires:	python3-pyyaml python3-parsy python3-daemonize
Requires:	python3-tabulate python3-psycopg2 python3-rollbar
Requires:	python3-PyMySQL python3-mysql-replication >= 0.31
%endif
%if 0%{?suse_version} >= 1500
Requires:	python3-PyYAML python%{python3_pkgversion}-parsy
Requires:	python%{python3_pkgversion}-daemonize python%{python3_pkgversion}-tabulate
Requires:	python%{python3_pkgversion}-psycopg2 python%{python3_pkgversion}-rollbar
Requires:	python%{python3_pkgversion}-PyMySQL python%{python3_pkgversion}-mysql-replication >= 0.31

%endif

%description
pg_chameleon is a MySQL to PostgreSQL replica system written in Python 3.
The system use the library mysql-replication to pull the row images from
MySQL which are stored into PostgreSQL as JSONB. A pl/pgsql function decodes
the jsonb values and replays the changes against the PostgreSQL database.

%prep
%setup -q -n %{name}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%defattr(-,root,root,755)
%doc docs/ README.rst
%license LICENSE.txt
%{_bindir}/chameleon
%{_bindir}/chameleon.py
%{python3_sitelib}/%{name}-%{version}.dist-info/*
%{python3_sitelib}/%{name}/*.py
%{python3_sitelib}/%{name}/__pycache__/*.pyc
%{python3_sitelib}/%{name}/configuration/config-example.yml
%{python3_sitelib}/%{name}/lib/*.py
%{python3_sitelib}/%{name}/lib/__pycache__/*.pyc
%{python3_sitelib}/%{name}/sql/*.sql
%{python3_sitelib}/%{name}/sql/upgrade/*.sql

%changelog
* Tue Apr 28 2026 Devrim Gündüz <devrim@gunduz.org> - 2.0.21-4PGDG
- Switch to pyproject build.
- Use Python 3.14 on Fedora 44.

* Sat Mar 28 2026 Devrim Gündüz <devrim@gunduz.org> - 2.0.21-3PGDG
- Fix SLES dependencies

* Mon Mar 23 2026 Devrim Gündüz <devrim@gunduz.org> - 2.0.21-2PGDG
- Add SLES 16 and Fedora 44 support

* Wed Jan 22 2025 Devrim Gündüz <devrim@gunduz.org> - 2.0.21-1PGDG
- Update to 2.0.21 per changes described at
  https://github.com/the4thdoctor/pg_chameleon/releases/tag/v2.0.21

* Wed Jan 1 2025 Devrim Gündüz <devrim@gunduz.org> - 2.0.20-1PGDG
- Update to 2.0.20 per changes described at
  https://github.com/the4thdoctor/pg_chameleon/releases/tag/v2.0.20

* Mon Feb 19 2024  Devrim Gündüz <devrim@gunduz.org> - 2.0.19-2PGDG
- Add PGDG branding

* Thu Mar 30 2023  Devrim Gündüz <devrim@gunduz.org> - 2.0.19-1
- Update to 2.0.19

* Wed Apr 20 2022  Devrim Gündüz <devrim@gunduz.org> - 2.0.18-1
- Update to 2.0.18

* Mon Feb 7 2022 Devrim Gündüz <devrim@gunduz.org> - 2.0.17-1
- Update to 2.0.17
- Add Python 3.10 support to the spec file.

* Mon Jan 3 2022 Devrim Gündüz <devrim@gunduz.org> - 2.0.16-4
- Fix SLES dependency, per https://redmine.postgresql.org/issues/7094

* Mon Nov 1 2021 Devrim Gündüz <devrim@gunduz.org> - 2.0.16-3
- Looks like we don't need python3-sphinx dependency.

* Thu Dec 10 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.16-2
- Fix RHEL 7 dependency

* Wed Dec 9 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.16-1
- Update to 2.0.16

* Wed Sep 23 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.15-1
- Update to 2.0.15

* Tue Aug 18 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.14-1
- Initial RPM packaging for PostgreSQL RPM Repository
