%pgdg_python3_setup

%global	modname contourpy

Name:		python%{python3_pkgversion}-%{modname}
# RHEL 9: 1.3 and later need numpy >= 1.25, RHEL 9 has 1.24 for python3.12.
# RHEL 10: they also need pybind11 >= 2.13, RHEL 10 has 2.11.
%if 0%{?rhel} >= 9
Version:	1.2.1
%else
Version:	1.3.3
%endif
Release:	43PGDG%{?dist}
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
%endif
%if 0%{?rhel} >= 10
BuildRequires:	python%{python3_pkgversion}-pybind11 pybind11-devel
%endif
%if ! 0%{?rhel}
BuildRequires:	python%{python3_pkgversion}-pybind11 >= 2.13.2
%endif
BuildRequires:	python%{python3_pkgversion}-numpy
BuildRequires:	gcc-c++ ninja-build pkgconfig

%if 0%{?rhel} == 9
Requires:	python%{python3_pkgversion}-numpy >= 1.20
%else
Requires:	python%{python3_pkgversion}-numpy >= 1.25
%endif

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-contourpy < %{version}-%{release}
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
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 1.3.3-43PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 1.3.3-42PGDG
- Add RHEL 10 support, without EPEL: build 1.2.1 there, as on RHEL 9, as
  1.3 needs pybind11 >= 2.13 and RHEL 10 has 2.11, and obsolete the EPEL
  python3-contourpy package. Start the release from 42, so that our
  packages win over EPEL's. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Tue Oct 06 2026 Devrim Gunduz <devrim@gunduz.org> - 1.3.3-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  pg_statviz dependency on Amazon Linux 2023.
- Add RHEL 9 support (python3.12), with 1.2.1, for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
