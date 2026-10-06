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

%global	modname pillow

Name:		python%{python3_pkgversion}-%{modname}
Version:	11.1.0
Release:	1PGDG%{?dist}
Summary:	Python image processing library

License:	MIT-CMU
URL:		https://python-pillow.github.io/
Source0:	https://files.pythonhosted.org/packages/source/p/%{modname}/%{modname}-%{version}.tar.gz

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools >= 67.8
BuildRequires:	python%{python3_pkgversion}-wheel
BuildRequires:	gcc
BuildRequires:	freetype-devel lcms2-devel libimagequant-devel libjpeg-turbo-devel
BuildRequires:	libtiff-devel libwebp-devel libxcb-devel openjpeg2-devel zlib-devel

%description
Pillow is the friendly PIL fork. PIL is the Python Imaging Library. It adds
image processing capabilities to your Python interpreter, and supports many
file formats.

%prep
%autosetup -n %{modname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.md
%{python3_sitearch}/PIL/
%{python3_sitearch}/%{modname}-%{version}.dist-info/

%changelog
* Tue Oct 06 2026 Devrim Gunduz <devrim@gunduz.org> - 11.1.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  pg_statviz dependency on Amazon Linux 2023.
