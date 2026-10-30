%pgdg_python3_setup

%global	modname pyasn1
%global	pymodname pyasn1

Name:		python%{python3_pkgversion}-%{modname}
Version:	0.6.5
Release:	1PGDG%{?dist}
Summary:	ASN.1 types and codecs

License:	BSD-2-Clause
URL:		https://github.com/pyasn1/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/p/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
%if ! 0%{?suse_version} && 0%{?rhel} != 8
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

%if 0%{?rhel} == 8
# The RHEL 8 dependency generator may not create this for python3.12:
Provides:	python%{python3_pkgversion}dist(pyasn1) = %{version}
%endif

%description
This is a pure-Python implementation of ASN.1 types and DER/BER/CER codecs
(X.208).

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
%license LICENSE.rst
%doc README.md
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Fri Oct 30 2026 Devrim Gunduz <devrim@gunduz.org> - 0.6.5-1PGDG
- Update to 0.6.5 per changes described at
  https://github.com/pyasn1/pyasn1/releases/tag/v0.6.5 . Fixes
  GHSA-mm57-4v3p-rchx, GHSA-2qm8-x737-gmw5, GHSA-9m75-vc3g-4x39 and
  GHSA-fm9c-5rcf-2q5p. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/460

* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 0.6.1-2PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 0.6.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  google-auth dependency (for pg_statviz) on Amazon Linux 2023. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Add RHEL 9 support (python3.12), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Add RHEL 8 support (python3.12), for google-auth, for bigquery_fdw. Build with pip there,
  as RHEL 8 has no pyproject-rpm-macros. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/367
