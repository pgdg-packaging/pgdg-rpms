%pgdg_python3_setup

%global	modname trove-classifiers
%global	pymodname trove_classifiers

Name:		python%{python3_pkgversion}-%{modname}
Version:	2025.9.11.17
Release:	2PGDG%{?dist}
Summary:	Canonical source for classifiers on PyPI

License:	Apache-2.0
URL:		https://github.com/pypa/trove-classifiers
Source0:	https://files.pythonhosted.org/packages/source/t/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel
BuildRequires:	python%{python3_pkgversion}-calver

%description
The canonical source for classifiers on PyPI. It is a dependency of hatchling.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
# Remove the command line tool, only the classifier list is needed:
%{__rm} -rf %{buildroot}%{_bindir}

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 2025.9.11.17-2PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 2025.9.11.17-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to build the AI SDKs
  of pg_statviz on RHEL 9 (python3.12). Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
