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

%global	modname prompt-toolkit
%global	pymodname prompt_toolkit

Name:		python%{python3_pkgversion}-%{modname}
Version:	3.0.53
Release:	1PGDG%{?dist}
Summary:	Library for building powerful interactive command lines in Python

License:	BSD-3-Clause
URL:		https://github.com/prompt-toolkit/python-prompt-toolkit
Source0:	https://files.pythonhosted.org/packages/source/p/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-setuptools >= 68
BuildRequires:	python%{python3_pkgversion}-wheel

# RHEL 8 has no automatic python3.12dist() requires:
Requires:	python%{python3_pkgversion}-wcwidth >= 0.1.4

%description
prompt_toolkit is a library for building powerful interactive command lines
and terminal applications in Python.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.rst AUTHORS.rst CHANGELOG
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Fri Oct 23 2026 Devrim Gunduz <devrim@gunduz.org> - 3.0.53-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for pgcli on
  RHEL 8 (python3.12), without EPEL. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
