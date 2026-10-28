%pgdg_python3_setup

# Built for the python3.13 alt-stack of Amazon Linux 2023 only, for
# the Azure storage backend of rohmu (pghoard).

%global	modname azure-common
%global	pymodname azure-common

Name:		python%{python3_pkgversion}-%{modname}
Version:	1.1.28
Release:	2PGDG%{?dist}
Summary:	Microsoft Azure client library common code

License:	MIT
URL:		https://github.com/Azure/azure-sdk-for-python
Source0:	https://files.pythonhosted.org/packages/source/a/azure-common/%{pymodname}-%{version}.zip
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

%description
Microsoft Azure client library code shared by the Azure SDK packages.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l azure

%files -f %{pyproject_files}
%doc README.md

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1.28-2PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1.28-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for
  the Azure storage backend of rohmu (pghoard) on Amazon Linux 2023.
