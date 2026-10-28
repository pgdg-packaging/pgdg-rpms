%pgdg_python3_setup

%global	modname anyio
%global	pymodname anyio

Name:		python%{python3_pkgversion}-%{modname}
Version:	4.9.0
Release:	44PGDG%{?dist}
Summary:	High level compatibility layer for multiple asynchronous event loop implementations

License:	MIT
URL:		https://github.com/agronholm/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/a/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
%if ! 0%{?suse_version}
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel
BuildRequires:	python%{python3_pkgversion}-setuptools_scm

Requires:	python%{python3_pkgversion}-idna >= 2.8
Requires:	python%{python3_pkgversion}-sniffio >= 1.1

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-anyio < %{version}-%{release}
%endif

%description
AnyIO is an asynchronous networking and concurrency library that works on top
of either asyncio or trio.

%if 0%{?rhel} == 10
# EPEL ships these extras metapackages, which require its own python3-anyio
# version, so they made dnf upgrade fail. Replace them with ours:
%package -n %{name}+trio
Summary:	Metapackage for %{name}: trio extras
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python3-anyio+trio = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	python3-anyio+trio < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{name}+trio
This is a metapackage bringing in trio extras requires for
%{name}. It makes sure the dependencies are installed.

%files -n %{name}+trio
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
%doc README.rst
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 4.9.0-44PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Mon Oct 26 2026 Devrim Gunduz <devrim@gunduz.org> - 4.9.0-43PGDG
- RHEL 10: Add the +trio extras metapackage, which replaces EPEL's.
  It requires EPEL's own python3-anyio version, so it made dnf
  upgrade fail. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 4.9.0-42PGDG
- Add RHEL 10 support, without EPEL, and obsolete the EPEL python3-anyio
  package there. Start the release from 42, so that our packages win over
  EPEL's. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 4.9.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  httpx and anthropic dependency (for pg_statviz) on Amazon Linux 2023. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Add RHEL 9 support (python3.12), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
