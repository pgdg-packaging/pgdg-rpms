%global pypi_name zstandard

%if 0%{?fedora} && 0%{?fedora} == 43
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?fedora} && 0%{?fedora} <= 42
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?suse_version} >= 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif

%{expand: %%global pybasever %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%{expand: %%global python3_sitearch %(echo `%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(2))"`)}

Name:		python%{python3_pkgversion}-%{pypi_name}
Version:	0.25.0
Release:	1PGDG%{?dist}.1
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
%if 0%{?amzn} == 2023
# AL2023's brp-python-bytecompile doesn't auto-discover the python3.13
# alt-stack site-packages dir the way Fedora/RHEL's does, so __pycache__
# never gets populated. Bytecompile explicitly instead.
%py_byte_compile %{__ospython} %{buildroot}%{python3_sitearch}/%{pypi_name}
%endif

%files
%license LICENSE zstd/COPYING
%doc README.rst
%{python3_sitearch}/%{pypi_name}-%{version}-py%{pybasever}.egg-info/
%{python3_sitearch}/%{pypi_name}/*.py*
%{python3_sitearch}/%{pypi_name}/py.typed
%{python3_sitearch}/%{pypi_name}/*.so
%if 0%{?rhel} || 0%{?fedora}
%{python3_sitearch}/%{pypi_name}/__pycache__/*.py*
%endif

%changelog
* Mon Aug 31 2026 Devrim Gunduz <devrim@gunduz.org> - 0.25.0-1PGDG.1
- Update to 0.25.0 per changes described at:
  https://pypi.org/project/zstandard/0.25.0/

* Fri Aug 28 2026 Devrim Gunduz <devrim@gunduz.org> - 0.23.0-46PGDG.1
- Package the .egg-info directory itself instead of globbing only its
  contents (egg-info/*), so RHEL/Fedora's pythondist.attr generator
  (which is anchored on the .egg-info directory entry) actually fires
  and emits the correct runtime Requires. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 0.23.0-45PGDG.1
- Explicitly bytecompile with %%py_byte_compile on Amazon Linux 2023.
  AL2023's brp-python-bytecompile doesn't auto-discover the python3.13
  alt-stack site-packages dir, so __pycache__ was never populated and
  the build failed with a missing-file error.

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 0.23.0-44PGDG.1
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Mon Sep 22 2025 Devrim Gunduz <devrim@gunduz.org> - 0.23.0-43PGDG.1
- Add Fedora 43 support

* Fri Jun 13 2025 Devrim Gunduz <devrim@gunduz.org> - 0.23.0-43PGDG
- Add SLES 15 support

* Tue May 27 2025 Devrim Gunduz <devrim@gunduz.org> - 0.23.0-42PGDG
- Initial packaging for the PostgreSQL RPM repository to support Barman
  on RHEL 9 and RHEL 8.
