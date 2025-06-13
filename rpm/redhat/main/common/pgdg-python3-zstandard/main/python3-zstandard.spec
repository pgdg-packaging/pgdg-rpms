%global pypi_name zstandard

%if 0%{?fedora} && 0%{?fedora} <= 42
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?suse_version} >= 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif

%{expand: %%global pybasever %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%{expand: %%global python3_sitearch %(echo `%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(2))"`)}

Name:		python%{python3_pkgversion}-%{pypi_name}
Version:	0.23.0
Release:	43PGDG%{?dist}
Summary:	Zstandard bindings for Python
License:	(BSD-3-Clause OR GPL-2.0-only) AND MIT
URL:		https://github.com/indygreg/python-%{pypi_name}
Source0:	https://files.pythonhosted.org/packages/source/z/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# relax dependencies
Patch1:		python-%{pypi_name}-deps.patch
BuildRequires:	gcc
BuildRequires:	libzstd-devel
BuildRequires:	python%{python3_pkgversion}-devel

# https://github.com/indygreg/python-zstandard/issues/48
Provides:	bundled(zstd) = 1.5.6

%description
This project provides Python bindings for interfacing with the Zstandard\
compression library. A C extension and CFFI interface are provided.


%prep
%autosetup -p1 -n %{pypi_name}-%{version}
%{__rm} -rf %{pypi_name}.egg-info

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --no-compile --root %{buildroot}

%files
%license LICENSE zstd/COPYING
%doc README.rst
%{python3_sitearch}/%{pypi_name}-%{version}-py%{pybasever}.egg-info/*
%{python3_sitearch}/%{pypi_name}/*.py*
%{python3_sitearch}/%{pypi_name}/py.typed
%{python3_sitearch}/%{pypi_name}/*.so
%if 0%{?rhel} || 0%{?fedora}
%{python3_sitearch}/%{pypi_name}/__pycache__/*.py*
%endif

%changelog
* Fri Jun 13 2025 Devrim Gunduz <devrim@gunduz.org> - 0.23.0-43PGDG
- Add SLES 15 support

* Tue May 27 2025 Devrim Gunduz <devrim@gunduz.org> - 0.23.0-42PGDG
- Initial packaging for the PostgreSQL RPM repository to support Barman
  on RHEL 9 and RHEL 8.
