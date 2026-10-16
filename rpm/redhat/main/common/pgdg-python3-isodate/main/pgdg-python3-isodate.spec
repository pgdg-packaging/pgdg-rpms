# Built for the python3.13 alt-stack of Amazon Linux 2023 only, for
# the Azure storage backend of rohmu (pghoard).
# azure-storage-blob needs it.
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif

%global	modname isodate
%global	pymodname isodate

Name:		python%{python3_pkgversion}-%{modname}
Version:	0.7.2
Release:	1PGDG%{?dist}
Summary:	An ISO 8601 date/time/duration parser and formatter

License:	BSD-3-Clause
URL:		https://github.com/gweis/isodate
Source0:	https://files.pythonhosted.org/packages/source/i/isodate/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel
BuildRequires:	python%{python3_pkgversion}-setuptools_scm

%description
This module implements ISO 8601 date, time and duration parsing.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l isodate

%files -f %{pyproject_files}
%doc README.rst

%changelog
* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 0.7.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for
  the Azure storage backend of rohmu (pghoard) on Amazon Linux 2023.
