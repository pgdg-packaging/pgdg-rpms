%pgdg_python3_setup

%global	modname pyproject-metadata
%global	pymodname pyproject_metadata

Name:		python%{python3_pkgversion}-%{modname}
Version:	0.9.1
Release:	43PGDG%{?dist}
Summary:	PEP 621 metadata parsing

License:	MIT
URL:		https://github.com/pypa/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/p/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
%if ! 0%{?suse_version}
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-flit-core

Requires:	python%{python3_pkgversion}-packaging

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-pyproject-metadata < %{version}-%{release}
%endif

%description
Dataclass for PEP 621 metadata with support for core metadata generation.

This project does not implement the parsing of pyproject.toml containing
PEP 621 metadata. Instead, given a Python data structure representing PEP
621 metadata (already parsed), it will validate this input and generate a
PEP 643-compliant metadata file (e.g. PKG-INFO).

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 0.9.1-43PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 0.9.1-42PGDG
- Add RHEL 10 support, without EPEL, and obsolete the EPEL
  python3-pyproject-metadata package there. Start the release from 42, so
  that our packages win over EPEL's. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Tue Oct 06 2026 Devrim Gunduz <devrim@gunduz.org> - 0.9.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  pg_statviz dependency on Amazon Linux 2023.
- Add RHEL 9 support (python3.12), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
