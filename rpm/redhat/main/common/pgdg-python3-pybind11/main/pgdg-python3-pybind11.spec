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

%global	modname pybind11

Name:		python%{python3_pkgversion}-%{modname}
Version:	2.13.6
Release:	1PGDG%{?dist}
Summary:	Seamless operability between C++11 and Python

License:	BSD-3-Clause
URL:		https://github.com/pybind/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/p/%{modname}/%{modname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

%description
pybind11 is a lightweight header-only library that exposes C++ types in
Python and vice versa, mainly to create Python bindings of existing C++
code.

This package installs pybind11 for Python %{python3_pkgversion}. The
pkg-config file is in the directory printed by
"python%{python3_pkgversion} -m pybind11 --pkgconfigdir".

%prep
%autosetup -n %{modname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
# Remove pybind11-config, it conflicts with the python3-pybind11 package
# of the OS. Use "python%{python3_pkgversion} -m pybind11" instead.
%{__rm} -f %{buildroot}%{_bindir}/%{modname}-config

%files
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}-%{version}.dist-info/

%changelog
* Tue Oct 06 2026 Devrim Gunduz <devrim@gunduz.org> - 2.13.6-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  pg_statviz dependency on Amazon Linux 2023.
