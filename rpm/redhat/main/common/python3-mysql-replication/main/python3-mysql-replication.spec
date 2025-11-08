%global sname	mysql-replication

%if 0%{?fedora} && 0%{?fedora} == 43
%global python3_pkgversion 3.14
%endif
%if 0%{?fedora} && 0%{?fedora} <= 42
%global	python3_pkgversion 3.13
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	python3_pkgversion 3.12
%endif
%if 0%{?suse_version} == 1500
%global	python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global	python3_pkgversion 313
%endif

Name:		python3-%{sname}
Version:	1.0.9
Release:	1PGDG%{?dist}
Summary:	Pure Python Implementation of MySQL replication protocol build on top of PyMYSQL
License:	Apache-2.0
URL:		https://github.com/noplay/python-%{sname}
Source0:	https://github.com/noplay/python-%{sname}/archive/%{version}.tar.gz
BuildArch:	noarch

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif

Requires:	python3-PyMySQL

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
%{python3_sitelib}/mysql_replication-%{version}.dist-info/*
%{python3_sitelib}/pymysqlreplication/*.py*
%{python3_sitelib}/pymysqlreplication/__pycache__/*.py*
%{python3_sitelib}/pymysqlreplication/constants/*.py*
%{python3_sitelib}/pymysqlreplication/constants/__pycache__/*.py*
%{python3_sitelib}/pymysqlreplication/tests/*.py*
%{python3_sitelib}/pymysqlreplication/tests/__pycache__/*.py*
%{python3_sitelib}/pymysqlreplication/util/*.py*
%{python3_sitelib}/pymysqlreplication/util/__pycache__/*.py*

%changelog
* Sat Nov 6 2025 - Devrim Gündüz <devrim@gunduz.org> 1.0.9-1PGDG
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
