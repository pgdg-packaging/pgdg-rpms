%pgdg_python3_setup

%global	modname poetry-core
%global	pymodname poetry_core

Name:		python%{python3_pkgversion}-%{modname}
Version:	2.1.3
Release:	43PGDG%{?dist}
Summary:	Poetry PEP 517 build backend

License:	MIT
URL:		https://github.com/python-poetry/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/p/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
%if ! 0%{?suse_version}
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-pip

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-poetry-core < %{version}-%{release}
%endif

%description
poetry-core is the PEP 517 build backend of Poetry. It is only needed to
build packages that use it, such as rsa.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/poetry/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 2.1.3-43PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 2.1.3-42PGDG
- Add RHEL 10 support, without EPEL, and obsolete the EPEL
  python3-poetry-core package there. Start the release from 42, so that our
  packages win over EPEL's. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 2.1.3-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  the build of rsa (for pg_statviz) on Amazon Linux 2023. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Add RHEL 9 support (python3.12), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
