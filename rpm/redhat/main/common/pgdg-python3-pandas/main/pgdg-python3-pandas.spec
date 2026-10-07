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

%global	modname pandas

Name:		python%{python3_pkgversion}-%{modname}
# RHEL 9: pandas 2.2 and later need Cython 3 and numpy 2 to build, RHEL 9 has
# Cython 0.29 and numpy 1.24 (which python3.12-scipy and the GDAL Python
# bindings are built against) for python3.12. 2.1.4 builds with them.
%if 0%{?rhel} == 9
Version:	2.1.4
%else
Version:	2.3.3
%endif
Release:	2PGDG%{?dist}
Summary:	Python library providing high-performance data analysis tools

License:	BSD-3-Clause
URL:		https://pandas.pydata.org/
Source0:	https://files.pythonhosted.org/packages/source/p/%{modname}/%{modname}-%{version}.tar.gz

BuildRequires:	python%{python3_pkgversion}-devel
%if ! 0%{?suse_version}
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-meson-python >= 0.13.1
BuildRequires:	gcc gcc-c++
%if 0%{?suse_version}
BuildRequires:	python-rpm-macros ninja
BuildRequires:	python%{python3_pkgversion}-Cython >= 3.0
BuildRequires:	python%{python3_pkgversion}-numpy-devel >= 2.0
%endif
%if 0%{?rhel} == 9
BuildRequires:	ninja-build
BuildRequires:	python%{python3_pkgversion}-Cython
# Cython 0.29 imports distutils, which setuptools provides on Python 3.12:
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-numpy
%endif
%if 0%{?amzn} == 2023
BuildRequires:	ninja-build
BuildRequires:	python%{python3_pkgversion}-cython >= 3.0
BuildRequires:	python%{python3_pkgversion}-numpy >= 2.0
%endif

%if 0%{?rhel} == 9
Requires:	python%{python3_pkgversion}-numpy >= 1.24.4
%else
Requires:	python%{python3_pkgversion}-numpy >= 1.26.0
%endif
Requires:	python%{python3_pkgversion}-pytz >= 2020.1
%if 0%{?suse_version}
Requires:	python%{python3_pkgversion}-python-dateutil >= 2.8.2
Requires:	python%{python3_pkgversion}-tzdata
%else
Requires:	python%{python3_pkgversion}-dateutil >= 2.8.2
%endif

%description
pandas is a Python package providing fast, flexible, and expressive data
structures designed to make working with "relational" or "labeled" data both
easy and intuitive. It aims to be the fundamental high-level building block
for doing practical, real world data analysis in Python.

%prep
%autosetup -n %{modname}-%{version}

# The sdist ships _version_meson.py, so versioneer is not needed. Do not
# import it, it is not packaged for Amazon Linux 2023:
sed -i 's|^import versioneer$|# import versioneer|' generate_version.py
grep -q '^# import versioneer$' generate_version.py
%if 0%{?rhel} == 9
# RHEL 9 has numpy 1.24.4 for python3.12:
sed -i 's/numpy>=1.26.0,<2/numpy>=1.24.4,<2/g' pyproject.toml
if grep -q 'numpy>=1.26' pyproject.toml; then exit 1; fi
%endif

%build
%if 0%{?amzn} == 2023
# Cython is installed as cython%{python3_pkgversion} on Amazon Linux 2023:
export CYTHON=%{_bindir}/cython%{python3_pkgversion}
%endif
%if 0%{?rhel} == 9
export CYTHON=%{_bindir}/cython-%{python3_pkgversion}
%endif
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.md
%{python3_sitearch}/%{modname}/
%{python3_sitearch}/%{modname}-%{version}.dist-info/

%changelog
* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 2.3.3-2PGDG
- Add SLES 16 support, for pg_statviz: SLES 16 has no pandas. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Add RHEL 9 support (python3.12), with 2.1.4, for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249

* Tue Oct 06 2026 Devrim Gunduz <devrim@gunduz.org> - 2.3.3-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  pg_statviz dependency on Amazon Linux 2023.
