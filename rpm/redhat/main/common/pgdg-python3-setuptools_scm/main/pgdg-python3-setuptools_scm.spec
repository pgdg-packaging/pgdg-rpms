%pgdg_python3_setup

%global	modname setuptools_scm
%global	pymodname setuptools_scm

Name:		python%{python3_pkgversion}-%{modname}
Version:	9.2.2
Release:	2PGDG%{?dist}
Summary:	Blessed package to manage your versions by SCM tags

License:	MIT
URL:		https://github.com/pypa/setuptools-scm
Source0:	https://files.pythonhosted.org/packages/source/s/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-packaging >= 20
BuildRequires:	python%{python3_pkgversion}-setuptools >= 61
BuildRequires:	python%{python3_pkgversion}-wheel

Requires:	python%{python3_pkgversion}-packaging >= 20
Requires:	python%{python3_pkgversion}-setuptools

%description
setuptools_scm extracts Python package versions from git or hg metadata
instead of declaring them as the version argument or in a SCM managed file.
It is only needed to build packages that use it.

This is 9.2.2: setuptools_scm 10 needs vcs-versioning, which needs
packaging 26.2; RHEL 8 and 9 have 23.2.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
# Remove the command line tool, only the module is needed:
%{__rm} -rf %{buildroot}%{_bindir}

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 9.2.2-2PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Fri Oct 23 2026 Devrim Gunduz <devrim@gunduz.org> - 9.2.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to build the
  packages that use it with python3.12 on RHEL 8 and 9 without EPEL. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
