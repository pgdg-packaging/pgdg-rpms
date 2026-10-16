# Built for the python3.13 alt-stack of Amazon Linux 2023 only, for
# the Azure storage backend of rohmu (pghoard).
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif

%global	modname azure-storage-blob
%global	pymodname azure_storage_blob

Name:		python%{python3_pkgversion}-%{modname}
Version:	12.31.0
Release:	1PGDG%{?dist}
Summary:	Microsoft Azure Blob Storage client library for Python

License:	MIT
URL:		https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/storage/azure-storage-blob
Source0:	https://files.pythonhosted.org/packages/source/a/azure-storage-blob/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

%description
Azure Blob storage is Microsoft's object storage solution for the cloud.
This is its Python client library.

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
* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 12.31.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for
  the Azure storage backend of rohmu (pghoard) on Amazon Linux 2023.
