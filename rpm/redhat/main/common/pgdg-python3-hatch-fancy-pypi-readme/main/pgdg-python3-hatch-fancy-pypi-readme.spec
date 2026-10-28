%pgdg_python3_setup

%global	modname hatch-fancy-pypi-readme
%global	pymodname hatch_fancy_pypi_readme

Name:		python%{python3_pkgversion}-%{modname}
Version:	24.1.0
Release:	43PGDG%{?dist}
Summary:	Fancy PyPI READMEs with Hatch

License:	MIT
URL:		https://github.com/hynek/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/h/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
%if ! 0%{?suse_version}
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-hatchling

Requires:	python%{python3_pkgversion}-hatchling

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-hatch-fancy-pypi-readme < %{version}-%{release}
%endif

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
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 24.1.0-43PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 24.1.0-42PGDG
- Add RHEL 10 support, without EPEL, and obsolete the EPEL
  python3-hatch-fancy-pypi-readme package there. Start the release from 42,
  so that our packages win over EPEL's. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 24.1.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  the build of pydantic, httpx, httpcore and anthropic (for pg_statviz) on Amazon Linux 2023. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Add RHEL 9 support (python3.12), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
