%pgdg_python3_setup

# Built for the python3.13 alt-stack of Amazon Linux 2023 only, for
# the Azure storage backend of rohmu (pghoard).
# azure-storage-blob needs it.

%global	modname isodate
%global	pymodname isodate

Name:		python%{python3_pkgversion}-%{modname}
Version:	0.7.2
Release:	2PGDG%{?dist}
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
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 0.7.2-2PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 0.7.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for
  the Azure storage backend of rohmu (pghoard) on Amazon Linux 2023.
