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
# RHEL 10: 2.10 and later need typing-extensions >= 4.12.2, RHEL 10 has
# 4.9.0 (in BaseOS, for python3.12 itself). 2.9.2 needs >= 4.6.1.
%if 0%{?rhel} == 10
Version:	2.9.2
%global	coreversion 2.23.4
%else
Version:	2.11.10
%global	coreversion 2.33.2
%endif
Release:	43PGDG%{?dist}
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
Requires:	python%{python3_pkgversion}-pydantic-core = %{coreversion}
%if 0%{?rhel} == 10
Requires:	python%{python3_pkgversion}-typing-extensions >= 4.6.1
%else
Requires:	python%{python3_pkgversion}-typing-extensions >= 4.12.2
Requires:	python%{python3_pkgversion}-typing-inspection >= 0.4.0
%endif
%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-%{modname} < %{version}-%{release}
%endif

%description
Data validation using Python type hints. Fast and extensible, Pydantic plays
nicely with your linters/IDE/brain. Define how data should be in pure,
canonical Python; validate it with Pydantic.

This is the 2.11 series, the newest one that works with typing-extensions
4.12.2 of Amazon Linux 2023 (2.9 on RHEL 10).

%if 0%{?rhel} == 10
# EPEL ships these extras metapackages, which require its own python3-pydantic
# version, so they made dnf upgrade fail. Replace them with ours:
%package -n %{name}+email
Summary:	Metapackage for %{name}: email extras
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python3-pydantic+email = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	python3-pydantic+email < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{name}+email
This is a metapackage bringing in email extras requires for
%{name}. It makes sure the dependencies are installed.

%files -n %{name}+email
%ghost %{python3_sitelib}/%{pymodname}-%{version}.dist-info

%package -n %{name}+timezone
Summary:	Metapackage for %{name}: timezone extras
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python3-pydantic+timezone = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	python3-pydantic+timezone < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{name}+timezone
This is a metapackage bringing in timezone extras requires for
%{name}. It makes sure the dependencies are installed.

%files -n %{name}+timezone
%ghost %{python3_sitelib}/%{pymodname}-%{version}.dist-info
%endif

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
* Mon Oct 26 2026 Devrim Gunduz <devrim@gunduz.org> - 2.11.10-43PGDG
- RHEL 10: Add the +email, +timezone extras metapackages, which replace EPEL's.
  They require EPEL's own python3-pydantic version, so they made dnf
  upgrade fail. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 2.11.10-42PGDG
- Add RHEL 10 support, without EPEL: use 2.9.2 there, the newest release
  that works with the typing-extensions 4.9.0 of RHEL 10, and obsolete the
  EPEL python3-pydantic package. Start the release from 42, so that our
  packages win over EPEL's. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 2.11.10-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  anthropic and ollama dependency (for pg_statviz) on Amazon Linux 2023. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Add RHEL 9 support (python3.12), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
