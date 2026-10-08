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

%global	modname kiwisolver

Name:		python%{python3_pkgversion}-%{modname}
Version:	1.5.1
Release:	2PGDG%{?dist}
Summary:	A fast implementation of the Cassowary constraint solver

License:	BSD-3-Clause
URL:		https://github.com/nucleic/kiwi
Source0:	https://files.pythonhosted.org/packages/source/k/%{modname}/%{modname}-%{version}.tar.gz

BuildRequires:	python%{python3_pkgversion}-devel
%if ! 0%{?suse_version}
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-setuptools_scm
BuildRequires:	python%{python3_pkgversion}-wheel
BuildRequires:	python%{python3_pkgversion}-cppy >= 1.3.0
BuildRequires:	gcc-c++

%description
Kiwi is an efficient C++ implementation of the Cassowary constraint solving
algorithm, with Python bindings. It is used by the layout engine of
matplotlib.

%prep
%autosetup -n %{modname}-%{version}
# setuptools checks the classifiers against trove-classifiers when it is
# installed, and older releases of it do not know Python 3.15:
sed -i '/"Programming Language :: Python :: 3.15",/d' pyproject.toml

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.md
%{python3_sitearch}/%{modname}/
%{python3_sitearch}/%{modname}-%{version}.dist-info/

%changelog
* Thu Oct 08 2026 Devrim Gunduz <devrim@gunduz.org> - 1.5.1-2PGDG
- Remove the Python 3.15 classifier, which fails the build when an
  older trove-classifiers is installed.

* Tue Oct 06 2026 Devrim Gunduz <devrim@gunduz.org> - 1.5.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  pg_statviz dependency on Amazon Linux 2023.
- Add RHEL 9 support (python3.12), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
