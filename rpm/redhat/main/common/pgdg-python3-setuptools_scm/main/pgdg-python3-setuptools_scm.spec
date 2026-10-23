%if 0%{?fedora} && 0%{?fedora} == 45
%global __ospython %{_bindir}/python3.15
%global python3_pkgversion 3.15
%endif
%if 0%{?fedora} && 0%{?fedora} <= 44
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?rhel} == 9
%global	__python3 %{_bindir}/python3.12
%endif
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?suse_version} == 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

%global	modname setuptools_scm
%global	pymodname setuptools_scm

Name:		python%{python3_pkgversion}-%{modname}
Version:	9.2.2
Release:	1PGDG%{?dist}
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
* Fri Oct 23 2026 Devrim Gunduz <devrim@gunduz.org> - 9.2.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to build the
  packages that use it with python3.12 on RHEL 8 and 9 without EPEL. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
