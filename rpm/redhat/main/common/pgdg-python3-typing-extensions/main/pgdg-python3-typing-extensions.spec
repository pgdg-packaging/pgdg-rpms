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
%if 0%{?rhel} && 0%{?rhel} <= 9
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

%global	modname typing-extensions
%global	pymodname typing_extensions

Name:		python%{python3_pkgversion}-%{modname}
Version:	4.12.2
Release:	1PGDG%{?dist}
Summary:	Backported and experimental type hints for Python

License:	PSF-2.0
URL:		https://github.com/python/typing_extensions
Source0:	https://files.pythonhosted.org/packages/source/t/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
%if 0%{?rhel} != 8
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-flit-core
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

This is 4.12.2, the newest release that builds with flit-core 3.9 of RHEL 9.

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

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{python3_sitelib}/%{pymodname}.py
%{python3_sitelib}/__pycache__/%{pymodname}.*
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 4.12.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  psycopg dependency (for pg_statviz) on RHEL 9 (python3.12). Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Add RHEL 8 support (python3.12), for grpcio, for bigquery_fdw. Build with pip there,
  as RHEL 8 has no pyproject-rpm-macros. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/367
