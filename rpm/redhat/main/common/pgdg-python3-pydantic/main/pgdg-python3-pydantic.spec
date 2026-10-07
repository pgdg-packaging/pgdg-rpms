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

%global	modname pydantic
%global	pymodname pydantic

Name:		python%{python3_pkgversion}-%{modname}
Version:	2.11.10
Release:	1PGDG%{?dist}
Summary:	Data validation using Python type hints

License:	MIT
URL:		https://github.com/pydantic/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/p/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
%if ! 0%{?suse_version}
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-hatchling
BuildRequires:	python%{python3_pkgversion}-hatch-fancy-pypi-readme

Requires:	python%{python3_pkgversion}-annotated-types >= 0.6.0
Requires:	python%{python3_pkgversion}-pydantic-core = 2.33.2
Requires:	python%{python3_pkgversion}-typing-extensions >= 4.12.2
Requires:	python%{python3_pkgversion}-typing-inspection >= 0.4.0

%description
Data validation using Python type hints. Fast and extensible, Pydantic plays
nicely with your linters/IDE/brain. Define how data should be in pure,
canonical Python; validate it with Pydantic.

This is the 2.11 series, the newest one that works with typing-extensions
4.12.2 of Amazon Linux 2023.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.md HISTORY.md
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 2.11.10-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  anthropic and ollama dependency (for pg_statviz) on Amazon Linux 2023. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Add RHEL 9 support (python3.12), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
