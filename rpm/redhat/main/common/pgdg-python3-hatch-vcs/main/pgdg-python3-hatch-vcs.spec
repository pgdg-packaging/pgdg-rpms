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

%global	modname hatch-vcs
%global	pymodname hatch_vcs

Name:		python%{python3_pkgversion}-%{modname}
Version:	0.4.0
Release:	1PGDG%{?dist}
Summary:	Hatch plugin for versioning with your preferred VCS

License:	MIT
URL:		https://github.com/ofek/hatch-vcs
Source0:	https://files.pythonhosted.org/packages/source/h/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-hatchling

Requires:	python%{python3_pkgversion}-hatchling >= 1.1.0
Requires:	python%{python3_pkgversion}-setuptools_scm >= 6.4.0

%description
This provides a plugin for Hatch that uses your preferred version control
system (like Git) to determine project versions. It is a build dependency
of ollama.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE.txt
%doc README.md
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 0.4.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to build the AI SDKs
  of pg_statviz on RHEL 9 (python3.12). Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
