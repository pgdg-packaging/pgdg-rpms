%pgdg_python3_setup

%global	modname tzdata

Name:		python%{python3_pkgversion}-%{modname}
Version:	2026.5
Release:	43PGDG%{?dist}
Summary:	Provider of IANA time zone data for Python

License:	Apache-2.0
URL:		https://github.com/python/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/t/%{modname}/%{modname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
%if ! 0%{?suse_version}
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

%description
This is a Python package containing zic-compiled binaries for the IANA time
zone database. It is intended to be a fallback for systems that do not have
system time zone data installed (or don't have it installed in a standard
location), as a part of PEP 615.

%prep
%autosetup -n %{modname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.rst NEWS.md
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}-%{version}.dist-info/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 2026.5-43PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 2026.5-42PGDG
- Add RHEL 10 support, for pandas, without EPEL. Start the release from 42,
  as for the other Python packages built for RHEL 10. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Tue Oct 06 2026 Devrim Gunduz <devrim@gunduz.org> - 2026.5-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  pandas dependency (for pg_statviz) on Amazon Linux 2023.
- Add RHEL 9 support (python3.12), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Add RHEL 8 support (python3.12), for dateutil 3.0.0. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/427
