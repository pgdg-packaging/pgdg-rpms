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

%global	modname google-auth
%global	pymodname google_auth

Name:		python%{python3_pkgversion}-%{modname}
# RHEL 8 is only used by bigquery_fdw, and its python3.12-cryptography is
# new enough for the current release, which also does not need rsa:
%if 0%{?rhel} == 8
Version:	2.62.0
%else
Version:	2.47.0
%endif
Release:	1PGDG%{?dist}
Summary:	Google Authentication Library

License:	Apache-2.0
URL:		https://github.com/googleapis/google-auth-library-python
Source0:	https://files.pythonhosted.org/packages/source/g/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
%if ! 0%{?suse_version} && 0%{?rhel} != 8
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

Requires:	python%{python3_pkgversion}-pyasn1-modules >= 0.2.1
%if 0%{?rhel} == 8
Requires:	python%{python3_pkgversion}-cryptography >= 38.0.3
%else
Requires:	python%{python3_pkgversion}-rsa >= 3.1.4
%endif

%if 0%{?rhel} == 8
# The RHEL 8 dependency generator may not create this for python3.12:
Provides:	python%{python3_pkgversion}dist(google-auth) = %{version}
%endif

%description
This library simplifies using Google's various server-to-server
authentication mechanisms to access Google APIs.

%if 0%{?rhel} != 8
This is the 2.47 series, the newest one that does not need cryptography >=
38 (Amazon Linux 2023 has 36 for python3.13).
%endif

# google-genai requires google-auth[requests]:
%if 0%{?rhel} != 8
%pyproject_extras_subpkg -n python%{python3_pkgversion}-%{modname} requests
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

%files
%license LICENSE
%doc README.rst
%{python3_sitelib}/google/auth/
%{python3_sitelib}/google/oauth2/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 2.47.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  google-genai dependency (for pg_statviz) on Amazon Linux 2023. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Add RHEL 9 support (python3.12), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Add RHEL 8 support (python3.12), for bigquery_fdw. Use 2.62.0 there,
  which does not need python3-rsa, and build with pip, as RHEL 8 has no
  pyproject-rpm-macros. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/367
