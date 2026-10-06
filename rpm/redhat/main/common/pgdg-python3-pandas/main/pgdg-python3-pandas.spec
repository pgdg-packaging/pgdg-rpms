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

%global	modname pandas

Name:		python%{python3_pkgversion}-%{modname}
Version:	2.3.3
Release:	1PGDG%{?dist}
Summary:	Python library providing high-performance data analysis tools

License:	BSD-3-Clause
URL:		https://pandas.pydata.org/
Source0:	https://files.pythonhosted.org/packages/source/p/%{modname}/%{modname}-%{version}.tar.gz

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-cython >= 3.0
BuildRequires:	python%{python3_pkgversion}-meson-python >= 0.13.1
BuildRequires:	python%{python3_pkgversion}-numpy >= 2.0
BuildRequires:	gcc gcc-c++ ninja-build

Requires:	python%{python3_pkgversion}-dateutil >= 2.8.2
Requires:	python%{python3_pkgversion}-numpy >= 1.26.0
Requires:	python%{python3_pkgversion}-pytz >= 2020.1

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

%build
# Cython is installed as cython%{python3_pkgversion} on Amazon Linux 2023:
export CYTHON=%{_bindir}/cython%{python3_pkgversion}
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.md
%{python3_sitearch}/%{modname}/
%{python3_sitearch}/%{modname}-%{version}.dist-info/

%changelog
* Tue Oct 06 2026 Devrim Gunduz <devrim@gunduz.org> - 2.3.3-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  pg_statviz dependency on Amazon Linux 2023.
