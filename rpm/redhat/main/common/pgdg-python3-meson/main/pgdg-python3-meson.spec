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

%global	modname meson

Name:		python%{python3_pkgversion}-%{modname}
Version:	1.12.1
Release:	1PGDG%{?dist}
Summary:	High productivity build system

License:	Apache-2.0
URL:		https://mesonbuild.com/
Source0:	https://github.com/mesonbuild/%{modname}/releases/download/%{version}/%{modname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

Requires:	ninja-build

%description
Meson is a build system designed to optimize programmer productivity. It
aims to do this by providing simple, out-of-the-box support for modern
software development tools and practices, such as unit tests, coverage
reports, Valgrind, Ccache and the like.

This package installs Meson for Python %{python3_pkgversion} as
%{_bindir}/meson-%{python3_pkgversion}, so that it does not conflict with
the meson package of the OS. It is used to build the meson-python based
packages in the PostgreSQL RPM repository.

%prep
%autosetup -n %{modname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%{__mv} %{buildroot}%{_bindir}/%{modname} %{buildroot}%{_bindir}/%{modname}-%{python3_pkgversion}
# Remove the man page and the polkit policy, they conflict with the
# meson package of the OS:
%{__rm} -rf %{buildroot}%{_datadir}

%files
%license COPYING
%doc README.md
%{_bindir}/%{modname}-%{python3_pkgversion}
%{python3_sitelib}/mesonbuild/
%{python3_sitelib}/%{modname}-%{version}.dist-info/

%changelog
* Tue Oct 06 2026 Devrim Gunduz <devrim@gunduz.org> - 1.12.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  pg_statviz dependency on Amazon Linux 2023.
