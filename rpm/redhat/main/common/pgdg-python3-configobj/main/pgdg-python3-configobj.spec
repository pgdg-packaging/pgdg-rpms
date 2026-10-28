%pgdg_python3_setup

%global	modname configobj
%global	pymodname configobj

Name:		python%{python3_pkgversion}-%{modname}
Version:	5.0.9
Release:	2PGDG%{?dist}
Summary:	Config file reading, writing, and validation

License:	BSD-3-Clause
URL:		https://github.com/DiffSK/configobj
Source0:	https://files.pythonhosted.org/packages/source/c/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

%description
ConfigObj is a simple but powerful config file reader and writer: an ini
file round tripper. Its main feature is that it is very easy to use, with a
straightforward programmer's interface and a simple syntax for config files.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/validate/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 5.0.9-2PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Fri Oct 23 2026 Devrim Gunduz <devrim@gunduz.org> - 5.0.9-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for cli-helpers
  and pgcli on RHEL 8 (python3.12), without EPEL. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
