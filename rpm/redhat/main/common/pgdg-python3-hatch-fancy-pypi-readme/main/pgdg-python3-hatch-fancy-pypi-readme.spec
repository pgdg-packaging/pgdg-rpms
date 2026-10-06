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

%global	modname hatch-fancy-pypi-readme
%global	pymodname hatch_fancy_pypi_readme

Name:		python%{python3_pkgversion}-%{modname}
Version:	24.1.0
Release:	1PGDG%{?dist}
Summary:	Fancy PyPI READMEs with Hatch

License:	MIT
URL:		https://github.com/hynek/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/h/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-hatchling

Requires:	python%{python3_pkgversion}-hatchling

%description
hatch-fancy-pypi-readme is a Hatch metadata plugin for everyone who cares
about the first impression of their project's PyPI landing page.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
# Remove the command line tool, only the plugin is needed:
%{__rm} -rf %{buildroot}%{_bindir}

%files
%license LICENSE.txt
%doc README.md
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 24.1.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  the build of pydantic, httpx, httpcore and anthropic (for pg_statviz) on Amazon Linux 2023. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
