%pgdg_python3_setup

%global	modname pytz

Name:		python%{python3_pkgversion}-%{modname}
Version:	2026.6
Release:	42PGDG%{?dist}
Summary:	World timezone definitions for Python

License:	MIT
URL:		https://pythonhosted.org/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/p/%{modname}/%{modname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-pytz < %{version}-%{release}
%endif

%description
pytz brings the Olson tz database into Python. This library allows accurate
and cross platform timezone calculations.

%prep
%autosetup -n %{modname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE.txt
%doc README.rst
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}-%{version}.dist-info/

%changelog
* Thu Oct 29 2026 Devrim Gunduz <devrim@gunduz.org> - 2026.6-42PGDG
- Update to 2026.6, per changes described at:
  https://github.com/stub42/pytz/releases/tag/release_2026.6
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/484

* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 2025.2-43PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 2025.2-42PGDG
- Add RHEL 10 support, without EPEL, and obsolete the EPEL python3-pytz
  package there. Start the release from 42, so that our packages win over
  EPEL's. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 2025.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  pandas dependency (for pg_statviz) on RHEL 9 (python3.12). Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
