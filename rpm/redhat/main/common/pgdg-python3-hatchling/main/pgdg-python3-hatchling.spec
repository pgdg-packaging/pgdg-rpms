%pgdg_python3_setup

%global	modname hatchling
%global	pymodname hatchling

Name:		python%{python3_pkgversion}-%{modname}
Version:	1.25.0
Release:	2PGDG%{?dist}
Summary:	Modern, extensible Python build backend

License:	MIT
URL:		https://hatch.pypa.io
Source0:	https://files.pythonhosted.org/packages/source/h/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-packaging >= 23.2
BuildRequires:	python%{python3_pkgversion}-pathspec >= 0.10.1
BuildRequires:	python%{python3_pkgversion}-pluggy >= 1.0.0
BuildRequires:	python%{python3_pkgversion}-trove-classifiers

Requires:	python%{python3_pkgversion}-packaging >= 23.2
Requires:	python%{python3_pkgversion}-pathspec >= 0.10.1
Requires:	python%{python3_pkgversion}-pluggy >= 1.0.0
Requires:	python%{python3_pkgversion}-trove-classifiers

%description
Hatchling is the extensible, standards compliant build backend used by Hatch.
It is only needed to build packages that use it.

This is 1.25.0: later releases need packaging 24.2, RHEL 9 has 23.2.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
# Remove the command line tool, only the build backend is needed:
%{__rm} -rf %{buildroot}%{_bindir}

%files
%license LICENSE.txt
%doc README.md
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 1.25.0-2PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 1.25.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to build the AI SDKs
  of pg_statviz on RHEL 9 (python3.12). Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
