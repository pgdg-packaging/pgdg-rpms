%if 0%{?fedora} && 0%{?fedora} == 45
%global __ospython %{_bindir}/python3.15
%global python3_pkgversion 3.15
%endif
%if 0%{?fedora} && 0%{?fedora} <= 44
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
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
%global sname pglast

Name:		pglast
Version:	7.11
Release:	1PGDG%{?dist}
Summary:	PostgreSQL Languages AST and statements prettifier
License:	GPLv3+
Url:		https://github.com/lelit/%{sname}
# The GitHub tag archive does not include the libpg_query git submodule
# content that this package needs to build against, so we use the PyPI
# sdist instead, which bundles a private copy of the libpg_query sources.
Source0:	https://files.pythonhosted.org/packages/source/p/%{sname}/%{sname}-%{version}.tar.gz
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

BuildRequires:	gcc
BuildRequires:	make

%description
pglast is a Python module able to parse PostgreSQL's SQL statements
and return their Abstract Syntax Tree, exposing it as a nested
structure of dataclass-like Python objects.

It builds on the low level PostgreSQL query parser extracted from the
actual PostgreSQL server source code (bundled here as libpg_query),
and can be used to programmatically inspect, rewrite or prettify SQL
code, as well as building tools such as pgspot.

%prep
%setup -q -n %{sname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%defattr(-,root,root,0755)
%doc README.rst CHANGES.rst
%{_bindir}/pgpp
%{python3_sitearch}/%{sname}/
%{python3_sitearch}/%{sname}-%{version}.dist-info/

%changelog
* Wed Sep 16 2026 Devrim Gunduz <devrim@gunduz.org> - 7.11-1PGDG
- Initial packaging for the PostgreSQL RPM repository
