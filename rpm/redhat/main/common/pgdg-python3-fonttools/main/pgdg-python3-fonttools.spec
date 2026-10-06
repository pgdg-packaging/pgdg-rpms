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

%global	modname fonttools
%global	pymodname fontTools

Name:		python%{python3_pkgversion}-%{modname}
Version:	4.66.1
Release:	1PGDG%{?dist}
Summary:	Tools to manipulate font files

License:	MIT
URL:		https://github.com/%{modname}/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/f/%{modname}/%{modname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

%description
fontTools is a library for manipulating fonts, written in Python. The project
includes the TTX tool, that can convert TrueType and OpenType fonts to and
from an XML text format, which is also called TTX. It supports TrueType,
OpenType, AFM and to an extent Type 1 and some Mac-specific formats.

This package is built without the optional Cython extensions.

%prep
%autosetup -n %{modname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
# Remove the scripts and the man page, they conflict with the
# python3-fonttools package of the OS:
%{__rm} -rf %{buildroot}%{_bindir} %{buildroot}%{_mandir}

%files
%license LICENSE LICENSE.external
%doc README.rst
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{modname}-%{version}.dist-info/

%changelog
* Tue Oct 06 2026 Devrim Gunduz <devrim@gunduz.org> - 4.66.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  pg_statviz dependency on Amazon Linux 2023.
