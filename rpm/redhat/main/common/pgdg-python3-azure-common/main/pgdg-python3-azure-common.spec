# Built for the python3.13 alt-stack of Amazon Linux 2023 only, for
# the Azure storage backend of rohmu (pghoard).
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif

%global	modname azure-common
%global	pymodname azure-common

Name:		python%{python3_pkgversion}-%{modname}
Version:	1.1.28
Release:	1PGDG%{?dist}
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
* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1.28-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for
  the Azure storage backend of rohmu (pghoard) on Amazon Linux 2023.
