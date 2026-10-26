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

%global	modname httpx
%global	pymodname httpx

Name:		python%{python3_pkgversion}-%{modname}
Version:	0.28.1
Release:	43PGDG%{?dist}
Summary:	The next generation HTTP client

License:	BSD-3-Clause
URL:		https://github.com/encode/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/h/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
%if ! 0%{?suse_version}
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-hatchling
BuildRequires:	python%{python3_pkgversion}-hatch-fancy-pypi-readme

Requires:	python%{python3_pkgversion}-anyio
Requires:	python%{python3_pkgversion}-certifi
Requires:	python%{python3_pkgversion}-httpcore >= 1.0
Requires:	python%{python3_pkgversion}-idna

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-httpx < %{version}-%{release}
%endif

%description
HTTPX is a fully featured HTTP client library for Python 3, which provides
sync and async APIs, and support for both HTTP/1.1 and HTTP/2.

%if 0%{?rhel} == 10
# EPEL ships these extras metapackages, which require its own python3-httpx
# version, so they made dnf upgrade fail. Replace them with ours:
%package -n %{name}+brotli
Summary:	Metapackage for %{name}: brotli extras
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python3-httpx+brotli = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	python3-httpx+brotli < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{name}+brotli
This is a metapackage bringing in brotli extras requires for
%{name}. It makes sure the dependencies are installed.

%files -n %{name}+brotli
%ghost %{python3_sitelib}/%{pymodname}-%{version}.dist-info

%package -n %{name}+cli
Summary:	Metapackage for %{name}: cli extras
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python3-httpx+cli = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	python3-httpx+cli < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{name}+cli
This is a metapackage bringing in cli extras requires for
%{name}. It makes sure the dependencies are installed.

%files -n %{name}+cli
%ghost %{python3_sitelib}/%{pymodname}-%{version}.dist-info

%package -n %{name}+http2
Summary:	Metapackage for %{name}: http2 extras
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python3-httpx+http2 = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	python3-httpx+http2 < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{name}+http2
This is a metapackage bringing in http2 extras requires for
%{name}. It makes sure the dependencies are installed.

%files -n %{name}+http2
%ghost %{python3_sitelib}/%{pymodname}-%{version}.dist-info

%package -n %{name}+socks
Summary:	Metapackage for %{name}: socks extras
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python3-httpx+socks = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	python3-httpx+socks < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{name}+socks
This is a metapackage bringing in socks extras requires for
%{name}. It makes sure the dependencies are installed.

%files -n %{name}+socks
%ghost %{python3_sitelib}/%{pymodname}-%{version}.dist-info
%endif

%prep
%autosetup -n %{pymodname}-%{version}
%if 0%{?rhel} == 10
# The cli extra caps rich below 14, RHEL 10 (EPEL) has 14. The CLI works
# with it:
sed -i 's/"rich>=10,<14",/"rich>=10",/' pyproject.toml
grep -q '"rich>=10",' pyproject.toml
%endif

%build
%pyproject_wheel

%install
%pyproject_install
# Remove the command line tool, it needs the cli extra (click, rich):
%{__rm} -rf %{buildroot}%{_bindir}

%files
%license LICENSE.md
%doc README.md
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Mon Oct 26 2026 Devrim Gunduz <devrim@gunduz.org> - 0.28.1-43PGDG
- RHEL 10: Add the +brotli, +cli, +http2 and +socks extras metapackages,
  which replace EPEL's. Those require EPEL's own python3-httpx version, so
  they made dnf upgrade fail. Allow rich 14 (EPEL) for the +cli extra. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 0.28.1-42PGDG
- Add RHEL 10 support, without EPEL, and obsolete the EPEL python3-httpx
  package there. Start the release from 42, so that our packages win over
  EPEL's. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 0.28.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  anthropic and ollama dependency (for pg_statviz) on Amazon Linux 2023. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Add RHEL 9 support (python3.12), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
