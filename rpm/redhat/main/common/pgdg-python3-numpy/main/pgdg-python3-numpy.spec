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

%global	modname numpy

Name:		python%{python3_pkgversion}-%{modname}
Version:	2.2.6
Release:	1PGDG%{?dist}
Summary:	A fast multidimensional array facility for Python

License:	BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0
URL:		https://numpy.org/
Source0:	https://files.pythonhosted.org/packages/source/n/%{modname}/%{modname}-%{version}.tar.gz

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-cython >= 3.0.6
BuildRequires:	python%{python3_pkgversion}-meson-python >= 0.15.0
BuildRequires:	gcc gcc-c++ ninja-build pkgconfig
BuildRequires:	openblas-devel

%description
NumPy is a general-purpose array-processing package designed to
efficiently manipulate large multi-dimensional arrays of arbitrary
records without sacrificing too much speed for small multi-dimensional
arrays.

%prep
%autosetup -n %{modname}-%{version}

%build
# Cython is installed as cython%{python3_pkgversion} on Amazon Linux 2023:
export CYTHON=%{_bindir}/cython%{python3_pkgversion}
# numpy builds with its own vendored copy of meson:
%pyproject_wheel -C setup-args=-Dblas=openblas -C setup-args=-Dlapack=openblas -C setup-args=-Dallow-noblas=false

%install
%pyproject_install
# Rename the scripts, they conflict with the python3-numpy package of the OS:
for f in f2py numpy-config; do
	%{__mv} %{buildroot}%{_bindir}/$f %{buildroot}%{_bindir}/$f-%{python3_pkgversion}
done

%files
%license LICENSE.txt LICENSES_bundled.txt
%doc README.md
%{_bindir}/f2py-%{python3_pkgversion}
%{_bindir}/numpy-config-%{python3_pkgversion}
%{python3_sitearch}/%{modname}/
%{python3_sitearch}/%{modname}-%{version}.dist-info/

%changelog
* Tue Oct 06 2026 Devrim Gunduz <devrim@gunduz.org> - 2.2.6-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  pg_statviz dependency on Amazon Linux 2023.
