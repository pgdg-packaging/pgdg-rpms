%global sname sqlparse

%if 0%{?fedora} && 0%{?fedora} == 45
%global python3_pkgversion 3.15
%endif
%if 0%{?fedora} && 0%{?fedora} <= 44
%global python3_pkgversion 3.14
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global python3_pkgversion 3.12
%endif
%if 0%{?amzn} == 2023
%global __python3 %{_bindir}/python3.13
%global python3_pkgversion 3.13
%endif
%if 0%{?suse_version} == 1500
%global python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global python3_pkgversion 313
%endif

Name:		python%{python3_pkgversion}-%{sname}
Version:	0.6.0
Release:	1PGDG%{?dist}
Summary:	Non-validating SQL parser module for Python

License:	BSD-3-Clause
URL:		https://github.com/andialbrecht/%{sname}
Source0:	https://files.pythonhosted.org/packages/source/s/%{sname}/%{sname}-%{version}.tar.gz
BuildArch:	noarch

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-hatchling
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-wheel

%description
sqlparse is a non-validating SQL parser module for Python. It provides
support for parsing, splitting and formatting SQL statements.

%prep
%autosetup -n %{sname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc AUTHORS CHANGELOG README.md
%{_bindir}/sqlformat
%{python3_sitelib}/%{sname}/
%{python3_sitelib}/%{sname}-%{version}.dist-info/

%changelog
* Wed Sep 23 2026 Devrim Gündüz <devrim@gunduz.org> - 0.6.0-1PGDG
- Update to 0.6.0
- Rename package as pgcli is looking for some specific Python versions.

* Sat Sep 19 2026 Devrim Gündüz <devrim@gunduz.org> - 0.5.5-1PGDG
- Add back to the repository, to satisfy the pgcli dependency on
  platforms where the OS does not ship it (e.g. RHEL 10).
