# This spec builds two flavors, depending on the distribution:
#
# - On RHEL 8 and RHEL 9: the python3.12 alt-stack flavor
#   (python3.12-typing-extensions), for pg_statviz and grpcio (bigquery_fdw).
# - On SLES: the default python3 flavor (python3-typing-extensions), for
#   psycopg3. This used to be the separate python3-typing-extensions
#   directory, merged here per
#   https://github.com/pgdg-packaging/pgdg-rpms/issues/369
%global	pgdg_altstack 0
%if 0%{?rhel} && 0%{?rhel} <= 9
%global	pgdg_altstack 1
%endif

%if %{pgdg_altstack}
%global	__ospython %{_bindir}/python3.12
%global	__python3 %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%else
%{!?python3_pkgversion: %global python3_pkgversion 3}
%endif

%global	modname typing-extensions
%global	pymodname typing_extensions

Name:		python%{python3_pkgversion}-%{modname}
%if %{pgdg_altstack}
Version:	4.12.2
Release:	1PGDG%{?dist}
%else
Version:	4.16.0
Release:	2PGDG%{?dist}
%endif
Summary:	Backported and experimental type hints for Python

License:	PSF-2.0
URL:		https://github.com/python/typing_extensions
Source0:	https://files.pythonhosted.org/packages/source/t/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-flit-core
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%endif
%if ! 0%{?suse_version} && 0%{?rhel} != 8
BuildRequires:	pyproject-rpm-macros
%endif
%if 0%{?rhel} == 8
# The RHEL 8 %%python3_sitelib macro needs distutils, which python3.12 only
# has through setuptools:
BuildRequires:	python%{python3_pkgversion}-setuptools
%endif

%if 0%{?rhel} == 8
# The RHEL 8 dependency generator may not create this for python3.12:
Provides:	python%{python3_pkgversion}dist(typing-extensions) = %{version}
%endif

%description
The typing_extensions module enables the use of new type system features on
older Python versions, and experimentation with new type system PEPs.

%if %{pgdg_altstack}
This is 4.12.2, the newest release that builds with flit-core 3.9 of RHEL 9.
%endif

%prep
%autosetup -n %{pymodname}-%{version}

%build
%if 0%{?rhel} == 8
# There are no pyproject-rpm-macros on RHEL 8:
%{__python3} -m pip wheel --no-deps --no-build-isolation --no-index \
	--disable-pip-version-check -w pgdg-dist .
%else
%pyproject_wheel
%endif

%install
%if 0%{?rhel} == 8
%{__python3} -m pip install --no-deps --no-index --no-compile \
	--disable-pip-version-check --ignore-installed \
	--root %{buildroot} --prefix %{_prefix} pgdg-dist/*.whl
%{__rm} -f %{buildroot}%{python3_sitelib}/*.dist-info/direct_url.json
echo rpm > $(echo %{buildroot}%{python3_sitelib}/*.dist-info)/INSTALLER
%else
%pyproject_install
%endif

%if %{pgdg_altstack}
%files
%else
%files -f %{pyproject_files}
%endif
%license LICENSE
%doc README.md CHANGELOG.md
%if %{pgdg_altstack}
%{python3_sitelib}/%{pymodname}.py
%{python3_sitelib}/__pycache__/%{pymodname}.*
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/
%endif

%changelog
* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 4.12.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  psycopg dependency (for pg_statviz) on RHEL 9 (python3.12). Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Add RHEL 8 support (python3.12), for grpcio, for bigquery_fdw. Build with pip there,
  as RHEL 8 has no pyproject-rpm-macros. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/367

* Thu Sep 10 2026 Devrim Gündüz <devrim@gunduz.org> - 4.16.0-2PGDG
- Add missing BR

* Mon Aug 31 2026 Devrim Gündüz <devrim@gunduz.org> - 4.16.0-1PGDG
- Update to 4.16.0 per changes described at:
  https://pypi.org/project/typing-extensions/4.16.0/

* Sat Nov 8 2025 Devrim Gündüz <devrim@gunduz.org> - 4.7.0-2PGDG
- Fix builds on SLES
- Add missing BRs

* Fri Jun 30 2023 Devrim Gündüz <devrim@gunduz.org> - 3.9.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support psycopg3
  RPM on RHEL 8 and SLES 15. RHEL 9 and Fedora already has this package.
