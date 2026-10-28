%pgdg_python3_setup

%global	modname prompt-toolkit
%global	pymodname prompt_toolkit

Name:		python%{python3_pkgversion}-%{modname}
Version:	3.0.53
Release:	2PGDG%{?dist}
Summary:	Library for building powerful interactive command lines in Python

License:	BSD-3-Clause
URL:		https://github.com/prompt-toolkit/python-prompt-toolkit
Source0:	https://files.pythonhosted.org/packages/source/p/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-setuptools >= 68
BuildRequires:	python%{python3_pkgversion}-wheel

# RHEL 8 has no automatic python3.12dist() requires:
Requires:	python%{python3_pkgversion}-wcwidth >= 0.1.4

%description
prompt_toolkit is a library for building powerful interactive command lines
and terminal applications in Python.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.rst AUTHORS.rst CHANGELOG
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 3.0.53-2PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Fri Oct 23 2026 Devrim Gunduz <devrim@gunduz.org> - 3.0.53-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for pgcli on
  RHEL 8 (python3.12), without EPEL. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
