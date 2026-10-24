# This spec builds two flavors, depending on the distribution:
#
# - On RHEL 8 and RHEL 9: the python3.12 alt-stack flavor
#   (python3.12-typing-extensions), for pg_statviz and grpcio (bigquery_fdw).
# - On RHEL 9 also the default python3 (3.9) flavor (python3-typing-extensions)
#   in the same build, for python3-psycopg3: RHEL 9 only has it in EPEL.
# - On SLES 16: the default python3 flavor (python3-typing-extensions), for
#   psycopg3. This used to be the separate python3-typing-extensions
#   directory, merged here per
#   https://github.com/pgdg-packaging/pgdg-rpms/issues/369
%global	pgdg_altstack 0
%if 0%{?rhel} && 0%{?rhel} <= 9
%global	pgdg_altstack 1
%endif
%global	with_os_python 0
%if 0%{?rhel} == 9
%global	with_os_python 1
%global	os_python %{_bindir}/python3
%global	os_sitelib %{_prefix}/lib/python3.9/site-packages
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
Release:	3PGDG%{?dist}
%else
Version:	4.16.0
Release:	3PGDG%{?dist}
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

%if %{with_os_python}
BuildRequires:	python3-devel
BuildRequires:	python3-pip
BuildRequires:	python3-flit-core
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

%if %{with_os_python}
%package -n python3-%{modname}
Summary:	Backported and experimental type hints for Python 3

%description -n python3-%{modname}
The typing_extensions module enables the use of new type system features on
older Python versions, and experimentation with new type system PEPs.

This is the flavor for the default python3 of RHEL 9, for python3-psycopg3.
%endif

%prep
%autosetup -n %{pymodname}-%{version}

%build
%if %{with_os_python}
%{os_python} -m pip wheel --no-deps --no-build-isolation --no-index \
	--disable-pip-version-check -w ../pgdg-os-dist .
%endif
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
%if %{with_os_python}
%{os_python} -m pip install --no-deps --no-index --no-compile \
	--disable-pip-version-check --ignore-installed \
	--root %{buildroot} --prefix %{_prefix} ../pgdg-os-dist/*.whl
# As %%pyproject_install does:
%{__rm} -f %{buildroot}%{os_sitelib}/*.dist-info/{direct_url.json,RECORD,REQUESTED}
echo rpm > $(echo %{buildroot}%{os_sitelib}/*.dist-info)/INSTALLER
%endif

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{python3_sitelib}/%{pymodname}.py
%{python3_sitelib}/__pycache__/%{pymodname}.*
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%if %{with_os_python}
%files -n python3-%{modname}
%license LICENSE
%doc README.md CHANGELOG.md
%{os_sitelib}/%{pymodname}.py
%{os_sitelib}/__pycache__/%{pymodname}.*
%{os_sitelib}/%{pymodname}-%{version}.dist-info/
%endif

%changelog
* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 4.12.2-3PGDG
- RHEL 9: Also build the default python3 (3.9) flavor, in the new
  python3-typing-extensions subpackage, which python3-psycopg3 needs:
  RHEL 9 only has it in EPEL. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 4.16.0-3PGDG
- Fix SLES 16 build: list the files explicitly, as the SUSE macros have
  no %%pyproject_files.
- Stop building on SLES 15: typing-extensions needs Python >= 3.9 and the
  python3 of SLES 15 is 3.6. grpcio uses python311-typing_extensions of
  SLES there.

* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 4.12.2-2PGDG
- Rebuild for the spec changes for SLES. No functional change on RHEL 8
  and RHEL 9.

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
