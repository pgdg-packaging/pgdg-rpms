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

%global	modname contourpy

Name:		python%{python3_pkgversion}-%{modname}
# RHEL 9: 1.3 and later need numpy >= 1.25, RHEL 9 has 1.24 for python3.12.
%if 0%{?rhel} == 9
Version:	1.2.1
%else
Version:	1.3.3
%endif
Release:	1PGDG%{?dist}
Summary:	Python library for calculating contours in 2D quadrilateral grids

License:	BSD-3-Clause
URL:		https://github.com/contourpy/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/c/%{modname}/%{modname}-%{version}.tar.gz

BuildRequires:	python%{python3_pkgversion}-devel
%if ! 0%{?suse_version}
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-meson-python >= 0.13.1
%if 0%{?rhel} == 9
BuildRequires:	python%{python3_pkgversion}-pybind11-devel
%else
BuildRequires:	python%{python3_pkgversion}-pybind11 >= 2.13.2
%endif
BuildRequires:	python%{python3_pkgversion}-numpy
BuildRequires:	gcc-c++ ninja-build pkgconfig

%if 0%{?rhel} == 9
Requires:	python%{python3_pkgversion}-numpy >= 1.20
%else
Requires:	python%{python3_pkgversion}-numpy >= 1.25
%endif

%description
ContourPy is a Python library for calculating contours of 2D quadrilateral
grids. It is written in C++11 and wrapped using pybind11. It is used by
matplotlib.

%prep
%autosetup -n %{modname}-%{version}

%build
export PKG_CONFIG_PATH=$(%{__python3} -m pybind11 --pkgconfigdir)
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.md
%{python3_sitearch}/%{modname}/
%{python3_sitearch}/%{modname}-%{version}.dist-info/

%changelog
* Tue Oct 06 2026 Devrim Gunduz <devrim@gunduz.org> - 1.3.3-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  pg_statviz dependency on Amazon Linux 2023.
- Add RHEL 9 support (python3.12), with 1.2.1, for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
