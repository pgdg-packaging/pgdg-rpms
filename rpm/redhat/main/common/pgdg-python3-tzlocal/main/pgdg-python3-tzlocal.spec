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
%if 0%{?rhel} == 9
%global	__python3 %{_bindir}/python3.12
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

%global	modname tzlocal
%global	pymodname tzlocal

Name:		python%{python3_pkgversion}-%{modname}
Version:	5.4.5
Release:	42PGDG%{?dist}
Summary:	A Python module that tries to figure out what your local timezone is

License:	MIT
URL:		https://github.com/regebro/tzlocal
Source0:	https://files.pythonhosted.org/packages/source/t/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-setuptools >= 64
BuildRequires:	python%{python3_pkgversion}-wheel

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-tzlocal < %{version}-%{release}
%endif

%description
This Python module returns the IANA time zone name for your local time
zone, or a tzinfo object with the local timezone information, under Unix
and Windows.

%prep
%autosetup -n %{pymodname}-%{version}
# The SPDX license expression needs setuptools 77; RHEL 8 has 68. Use the
# license table:
%{__sed} -i 's/^license = "MIT"$/license = { text = "MIT" }/' pyproject.toml
grep -q '^license = { text = "MIT" }$' pyproject.toml

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE.txt
%doc README.rst
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 5.4.5-42PGDG
- Add RHEL 10 support, without EPEL, and obsolete the EPEL python3-tzlocal
  package there. Start the release from 42, so that our packages win over
  EPEL's. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Fri Oct 23 2026 Devrim Gunduz <devrim@gunduz.org> - 5.4.5-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for pgcli on
  RHEL 8 (python3.12), without EPEL. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
