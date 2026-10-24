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

%global	modname pytz

Name:		python%{python3_pkgversion}-%{modname}
Version:	2025.2
Release:	42PGDG%{?dist}
Summary:	World timezone definitions for Python

License:	MIT
URL:		https://pythonhosted.org/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/p/%{modname}/%{modname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-pytz < %{version}-%{release}
%endif

%description
pytz brings the Olson tz database into Python. This library allows accurate
and cross platform timezone calculations.

%prep
%autosetup -n %{modname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE.txt
%doc README.rst
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}-%{version}.dist-info/

%changelog
* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 2025.2-42PGDG
- Add RHEL 10 support, without EPEL, and obsolete the EPEL python3-pytz
  package there. Start the release from 42, so that our packages win over
  EPEL's. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 2025.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  pandas dependency (for pg_statviz) on RHEL 9 (python3.12). Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
