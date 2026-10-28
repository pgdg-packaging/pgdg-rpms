%pgdg_python3_setup

%global	modname tzlocal
%global	pymodname tzlocal

Name:		python%{python3_pkgversion}-%{modname}
Version:	5.4.5
Release:	43PGDG%{?dist}
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
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 5.4.5-43PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 5.4.5-42PGDG
- Add RHEL 10 support, without EPEL, and obsolete the EPEL python3-tzlocal
  package there. Start the release from 42, so that our packages win over
  EPEL's. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Fri Oct 23 2026 Devrim Gunduz <devrim@gunduz.org> - 5.4.5-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for pgcli on
  RHEL 8 (python3.12), without EPEL. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
