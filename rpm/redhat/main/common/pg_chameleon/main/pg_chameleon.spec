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
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?suse_version} == 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Summary:	MySQL to PostgreSQL replica system
Name:		pg_chameleon
Version:	2.0.21
Release:	8PGDG%{?dist}
License:	BSD
Source0:	https://github.com/the4thdoctor/%{name}/archive/v%{version}.tar.gz
URL:		https://github.com/the4thdoctor/%{name}
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-pip python%{python3_pkgversion}-wheel
# python%%{python3_pkgversion}-devel is what pulls python3-rpm-generators
# into the buildroot on RHEL/Fedora; pyproject builds alone do not.
# Without it, neither python(abi) nor python%%{python3_pkgversion}dist(...)
# get generated. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/228
%if !0%{?suse_version}
BuildRequires:	python%{python3_pkgversion}-devel
%endif


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
%{python3_sitelib}/%{name}-%{version}.dist-info/
%{python3_sitelib}/%{name}/*.py
%{python3_sitelib}/%{name}/__pycache__/*.pyc
%{python3_sitelib}/%{name}/configuration/config-example.yml
%{python3_sitelib}/%{name}/lib/*.py
%{python3_sitelib}/%{name}/lib/__pycache__/*.pyc
%{python3_sitelib}/%{name}/sql/*.sql
%{python3_sitelib}/%{name}/sql/upgrade/*.sql

%changelog
* Fri Aug 28 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0.21-8PGDG
- Package the .dist-info directory itself instead of globbing only its
  contents (dist-info/*), so RHEL/Fedora's pythondist.attr generator
  (which is anchored on the .dist-info directory entry) actually fires
  and emits the correct runtime Requires. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226
- Add back python%{python3_pkgversion}-devel as a BuildRequires on the
  non-SLES branch, needed to pull python3-rpm-generators into the
  buildroot for this pyproject build. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/228

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0.21-7PGDG
- Also set __python3 (not just __ospython) for Amazon Linux 2023, so
  %pyproject_wheel/%pyproject_install actually build against python3.13
  instead of silently falling back to the system default python3.
  This one already had its own local sitelib override, so the
  mismatch was active (not just cosmetic): pip would install via 3.9
  while %files looked for files under python3.13's site-packages.

* Tue Aug 25 2026 Devrim Gündüz <devrim@gunduz.org> - 2.0.21-6PGDG
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Thu May 7 2026 Devrim Gündüz <devrim@gunduz.org> - 2.0.21-5PGDG
- Add missing BRs

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
