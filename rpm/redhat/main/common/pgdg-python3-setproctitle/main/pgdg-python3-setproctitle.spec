%pgdg_python3_setup

%global	modname setproctitle
%global	pymodname setproctitle

Name:		python%{python3_pkgversion}-%{modname}
Version:	1.3.8
Release:	43PGDG%{?dist}
Summary:	Python module to customize a process title

License:	BSD-3-Clause
URL:		https://github.com/dvarrazzo/py-setproctitle
Source0:	https://files.pythonhosted.org/packages/source/s/%{pymodname}/%{pymodname}-%{version}.tar.gz

BuildRequires:	gcc
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-setproctitle < %{version}-%{release}
%endif

%description
The setproctitle module allows a process to change its title (as displayed
by system tools such as ps and top).

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.rst
%{python3_sitearch}/%{pymodname}/
%{python3_sitearch}/%{pymodname}-%{version}.dist-info/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 1.3.8-43PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 1.3.8-42PGDG
- Add RHEL 10 support, without EPEL, and obsolete the EPEL
  python3-setproctitle package there. Start the release from 42, so that our
  packages win over EPEL's. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Fri Oct 23 2026 Devrim Gunduz <devrim@gunduz.org> - 1.3.8-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for pgcli on
  RHEL 8 (python3.12), without EPEL. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
