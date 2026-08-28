%global sname	mysql-replication

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

Name:		python%{python3_pkgversion}-%{sname}
Version:	1.0.15
Release:	6PGDG%{?dist}
Summary:	Pure Python Implementation of MySQL replication protocol build on top of PyMYSQL
License:	Apache-2.0
URL:		https://github.com/noplay/python-%{sname}
Source0:	https://github.com/noplay/python-%{sname}/archive/%{version}.tar.gz
BuildArch:	noarch

Provides:	python3-%{sname}

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
# python%%{python3_pkgversion}-devel is what pulls python3-rpm-generators
# into the buildroot on RHEL/Fedora; pyproject-rpm-macros alone does not.
# Without it, neither python(abi) nor python%%{python3_pkgversion}dist(...)
# get generated. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/228
BuildRequires:	python%{python3_pkgversion}-devel
%endif

BuildRequires:	python%{python3_pkgversion}-pip python%{python3_pkgversion}-wheel

Requires:	python%{python3_pkgversion}-PyMySQL

%description
Pure Python Implementation of MySQL replication protocol build on top of
PyMYSQL. This allow you to receive event like insert, update, delete with
their datas and raw SQL queries.
 Use cases
  -  MySQL to NoSQL database replication
  -  MySQL to search engine replication
  -  Invalidate cache when something change in database
  -  Audit
  -  Real time analytics

%prep
%setup -q -n python-%{sname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%{python3_sitelib}/mysql_replication-%{version}.dist-info/
%{python3_sitelib}/pymysqlreplication/*.py*
%{python3_sitelib}/pymysqlreplication/__pycache__/*.py*
%{python3_sitelib}/pymysqlreplication/constants/*.py*
%{python3_sitelib}/pymysqlreplication/constants/__pycache__/*.py*
%{python3_sitelib}/pymysqlreplication/tests/*.py*
%{python3_sitelib}/pymysqlreplication/tests/__pycache__/*.py*
%{python3_sitelib}/pymysqlreplication/util/*.py*
%{python3_sitelib}/pymysqlreplication/util/__pycache__/*.py*

%changelog
* Fri Aug 28 2026 Devrim Gunduz <devrim@gunduz.org> - 1.0.15-6PGDG
- Package the .dist-info directory itself instead of globbing only its
  contents (dist-info/*), so RHEL/Fedora's pythondist.attr generator
  (which is anchored on the .dist-info directory entry) actually fires
  and emits the correct runtime Requires. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226
- Add back python%{python3_pkgversion}-devel as a BuildRequires on the
  non-SLES branch, needed to pull python3-rpm-generators into the
  buildroot for this pyproject build. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/228

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 1.0.15-5PGDG
- Also set __python3 (not just __ospython) for Amazon Linux 2023, so
  %pyproject_wheel/%pyproject_install actually build against python3.13
  instead of silently falling back to the system default python3
  (__ospython only affects this repo's own macro computations, not
  RPM's own pyproject/site-packages macros).

* Tue Aug 25 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0.15-4PGDG
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Thu May 7 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0.15-3PGDG
- Add missing BRs

* Tue Apr 28 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0.15-2PGDG
- Use Python 3.14 on Fedora 44. Many BRs and Requires are not ready
  for 3.15.

* Sat Mar 28 2026 - Devrim Gündüz <devrim@gunduz.org> 1.0.15-1PGDG
- Update to 1.0.15
- Add Fedora 44 support.
- Change package name to match other "PGDG" branded Python packages

* Sat Nov 8 2025 - Devrim Gündüz <devrim@gunduz.org> 1.0.9-1PGDG
- Update to 1.0.9
- Add SLES 16 support

* Sun Dec 29 2024 - Devrim Gündüz <devrim@gunduz.org> 1.0.2-2PGDG
- Add RHEL 10 support

* Wed Oct 18 2023 - Devrim Gündüz <devrim@gunduz.org> 1.0.2-1PGDG
- Update to 1.0.2
- Add PGDG branding

* Thu Mar 30 2023 - Devrim Gündüz <devrim@gunduz.org> 0.31-1
- Update to 0.31

* Mon Feb 7 2022 - Devrim Gündüz <devrim@gunduz.org> 0.26-1
- Update to 0.26
- Add Python 3.10 fixes to spec file

* Wed Dec 9 2020 - Devrim Gündüz <devrim@gunduz.org> 0.22-1
- Initial packaging for PostgreSQL RPM repository, to satisfy
  pg_chameleon dependency.
