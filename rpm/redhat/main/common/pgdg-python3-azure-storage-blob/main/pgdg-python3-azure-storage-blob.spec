%pgdg_python3_setup

# Built for the python3.13 alt-stack of Amazon Linux 2023 only, for
# the Azure storage backend of rohmu (pghoard).

%global	modname azure-storage-blob
%global	pymodname azure_storage_blob

Name:		python%{python3_pkgversion}-%{modname}
Version:	12.31.1
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
* Fri Oct 30 2026 Devrim Gunduz <devrim@gunduz.org> - 12.31.1-1PGDG
- Update to 12.31.1 per changes described at:
  https://pypi.org/project/azure-storage-blob/12.31.1/

* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 12.31.0-2PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 12.31.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for
  the Azure storage backend of rohmu (pghoard) on Amazon Linux 2023.
