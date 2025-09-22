%global modname click

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
%if 0%{?suse_version} >= 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif

%{expand: %%global pybasever %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%global pgdg_python3_sitearch %(%{__ospython} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

Name:		python%{python3_pkgversion}-click
Version:	8.1.7
Release:	43PGDG%{?dist}.1
Summary:	Simple wrapper around optparse for powerful command line utilities

License:	BSD-3-Clause
URL:		https://github.com/pallets/%{modname}
Source0:	https://github.com/pallets/%{modname}/archive/%{version}/%{modname}-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python%{python3_pkgversion}-devel

Provides:	python%{python3_pkgversion}dist(click)

%description
click is a Python package for creating beautiful command line\
interfaces in a composable way with as little amount of code as necessary.\
It's the "Command Line Interface Creation Kit". It's highly configurable but\
comes with good defaults out of the box.

%prep
%autosetup -n click-%{version} -p1

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --no-compile --root %{buildroot}

%files
%license LICENSE.rst
%doc README.rst CHANGES.rst
%{pgdg_python3_sitearch}/%{modname}-%{version}-py%{pybasever}.egg-info/*
%{pgdg_python3_sitearch}/%{modname}/*.py*
%{pgdg_python3_sitearch}/%{modname}/__pycache__/*.py*
%{pgdg_python3_sitearch}/%{modname}/py.typed

%changelog
* Mon Sep 22 2025 Devrim Gunduz <devrim@gunduz.org> - 8.1.7-43PGDG.1
- Add Fedora 43 support

* Tue May 20 2025 Devrim Gunduz <devrim@gunduz.org> - 8.1.7-43PGDG
- Add Provides:

* Tue May 20 2025 Devrim Gunduz <devrim@gunduz.org> - 8.1.7-42PGDG
- Initial packaging for the PostgreSQL RPM repository to support Patroni
  on RHEL 9 and 8.
