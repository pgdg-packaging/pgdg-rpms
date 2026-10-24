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

%global	modname poetry-core
%global	pymodname poetry_core

Name:		python%{python3_pkgversion}-%{modname}
Version:	2.1.3
Release:	42PGDG%{?dist}
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
