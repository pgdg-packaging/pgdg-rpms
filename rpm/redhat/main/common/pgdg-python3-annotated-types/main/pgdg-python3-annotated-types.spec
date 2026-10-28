%pgdg_python3_setup

%global	modname annotated-types
%global	pymodname annotated_types

Name:		python%{python3_pkgversion}-%{modname}
Version:	0.7.0
Release:	43PGDG%{?dist}
Summary:	Reusable constraint types to use with typing.Annotated

License:	MIT
URL:		https://github.com/annotated-types/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/a/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
%if ! 0%{?suse_version}
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-hatchling

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-annotated-types < %{version}-%{release}
%endif

%description
This package provides metadata objects which can be used to represent common
constraints such as upper and lower bounds on scalar values and collection
sizes, a Predicate marker for runtime checks, and descriptions of how we
intend these metadata to be interpreted.

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
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 0.7.0-43PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 0.7.0-42PGDG
- Add RHEL 10 support, without EPEL, and obsolete the EPEL
  python3-annotated-types package there. Start the release from 42, so that
  our packages win over EPEL's. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 0.7.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  pydantic dependency (for pg_statviz) on Amazon Linux 2023. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Add RHEL 9 support (python3.12), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
