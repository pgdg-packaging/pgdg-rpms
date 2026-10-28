%pgdg_python3_setup

# Built for the python3.13 alt-stack of Amazon Linux 2023 only, for
# the Google Cloud storage backend of rohmu (pghoard).
# 0.22.0 is the newest version that works with the pyparsing 2.4.7 of
# Amazon Linux 2023 (0.23.0 and later need >= 3.1).

%global	modname httplib2
%global	pymodname httplib2

Name:		python%{python3_pkgversion}-%{modname}
Version:	0.22.0
Release:	2PGDG%{?dist}
Summary:	A comprehensive HTTP client library

License:	MIT
URL:		https://github.com/httplib2/httplib2
Source0:	https://files.pythonhosted.org/packages/source/h/httplib2/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

%description
A comprehensive HTTP client library that supports many features left
out of other HTTP libraries.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l httplib2

%files -f %{pyproject_files}
%doc README.md

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 0.22.0-2PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 0.22.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for
  the Google Cloud storage backend of rohmu (pghoard) on Amazon Linux 2023.
