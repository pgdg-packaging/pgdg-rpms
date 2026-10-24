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
%if 0%{?rhel} == 9
%global __python3 %{_bindir}/python3.12
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
Release:	4PGDG%{?dist}
Summary:	Non-validating SQL parser module for Python

License:	BSD-3-Clause
URL:		https://github.com/andialbrecht/%{sname}
Source0:	https://files.pythonhosted.org/packages/source/s/%{sname}/%{sname}-%{version}.tar.gz
BuildArch:	noarch

%if 0%{?rhel} == 10
# Up to 0.5.5 this package was named python3-sqlparse. On RHEL 10 python3 is
# python3.12, so the old package installs the same files; replace it on upgrade.
Obsoletes:	python3-%{sname} < 0.6.0-2
%endif

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
# SUSE's Python dependency generators. python3-devel pulls this in, but
# python%%{python3_pkgversion}-devel does not.
BuildRequires:	python-rpm-packaging
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
%if 0%{?rhel} == 8 || 0%{?rhel} == 9
# Only the module is needed there, for pgcli. The python3-sqlparse package
# of EPEL also ships sqlformat:
%{__rm} -f %{buildroot}%{_bindir}/sqlformat
%endif

%files
%license LICENSE
%doc AUTHORS CHANGELOG README.md
%if 0%{?rhel} != 8 && 0%{?rhel} != 9
%{_bindir}/sqlformat
%endif
%{python3_sitelib}/%{sname}/
%{python3_sitelib}/%{sname}-%{version}.dist-info/

%changelog
* Sat Oct 24 2026 Devrim Gündüz <devrim@gunduz.org> - 0.6.0-4PGDG
- Add RHEL 8 and 9 support, for pgcli. Build with python3.12 on RHEL 9,
  whose python3 is 3.9, and do not ship sqlformat there, which conflicts
  with the one of EPEL's python3-sqlparse. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Wed Sep 23 2026 Devrim Gündüz <devrim@gunduz.org> - 0.6.0-3PGDG
- BuildRequire python-rpm-packaging on SUSE, which python313-devel does
  not pull in, so that the Python dependency generators run there.

* Wed Sep 23 2026 Devrim Gündüz <devrim@gunduz.org> - 0.6.0-2PGDG
- Obsolete python3-sqlparse on RHEL 10, so that upgrades from 0.5.5
  replace the old package instead of conflicting with it.

* Wed Sep 23 2026 Devrim Gündüz <devrim@gunduz.org> - 0.6.0-1PGDG
- Update to 0.6.0
- Rename package as pgcli is looking for some specific Python versions.

* Sat Sep 19 2026 Devrim Gündüz <devrim@gunduz.org> - 0.5.5-1PGDG
- Add back to the repository, to satisfy the pgcli dependency on
  platforms where the OS does not ship it (e.g. RHEL 10).
