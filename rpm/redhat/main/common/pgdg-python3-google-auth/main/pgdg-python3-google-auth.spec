# This spec builds the python3.12 / python3.13 alt-stack flavor
# (python3.12-google-auth, python3.13-google-auth) on RHEL 8, RHEL 9 and
# Amazon Linux 2023, for pg_statviz and bigquery_fdw.
#
# It is not built elsewhere: Fedora, RHEL 10 (EPEL) and SUSE ship
# python3-google-auth (python311-/python313-google-auth on SUSE) themselves,
# new enough for bigquery_fdw, together with its extras subpackages, which
# pin it to their own version. The default python3 flavor that this spec used
# to build there replaced the OS package and broke the updates of those
# extras.
%if 0%{?rhel}
%global	__ospython %{_bindir}/python3.12
%global	__python3 %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif

%global	modname google-auth
%global	pymodname google_auth

# The 2.47 series on RHEL 9 and Amazon Linux 2023 (see the description).
# RHEL 8 is only used by bigquery_fdw, and its python3.12-cryptography is
# new enough for the current release:
%if 0%{?rhel} != 8
%global	pgdg_gauth247 1
%else
%global	pgdg_gauth247 0
%endif

Name:		python%{python3_pkgversion}-%{modname}
%if %{pgdg_gauth247}
Version:	2.47.0
%else
Version:	2.62.0
%endif
Release:	42PGDG%{?dist}
Summary:	Google Authentication Library

License:	Apache-2.0
# The upstream repository moved into the google-cloud-python monorepo,
# which does not tag google-auth releases, so use the PyPI sdist:
URL:		https://github.com/googleapis/google-cloud-python/tree/main/packages/google-auth
Source0:	https://files.pythonhosted.org/packages/source/g/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel
%if 0%{?rhel} != 8
BuildRequires:	pyproject-rpm-macros
%endif

Requires:	python%{python3_pkgversion}-pyasn1-modules >= 0.2.1
%if %{pgdg_gauth247}
Requires:	python%{python3_pkgversion}-rsa >= 3.1.4
%else
Requires:	python%{python3_pkgversion}-cryptography >= 38.0.3
%endif

%if 0%{?rhel} == 8
# The RHEL 8 dependency generator may not create this for python3.12:
Provides:	python%{python3_pkgversion}dist(google-auth) = %{version}
%endif

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-google-auth < %{version}-%{release}
# Its google-auth[requests] metapackage requires that exact version.
# Our +requests subpackage replaces it (that macro takes no Obsoletes):
Obsoletes:	python3-google-auth+requests < %{version}-%{release}
%endif

%description
This library simplifies using Google's various server-to-server
authentication mechanisms to access Google APIs.

%if %{pgdg_gauth247}
This is the 2.47 series, the newest one that does not need cryptography >=
38 (Amazon Linux 2023 has 36 for python3.13).
%endif

# google-genai (pg_statviz) requires google-auth[requests]:
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
* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 2.62.0-42PGDG
- Add RHEL 10 support, without EPEL, and obsolete the EPEL
  python3-google-auth package there. Start the release from 42, so that our
  packages win over EPEL's. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Mon Oct 12 2026 Devrim Gunduz <devrim@gunduz.org> - 2.62.0-1PGDG
- Update to 2.62.0 per changes
  described at https://pypi.org/project/google-auth/2.62.0/ . Upstream
  moved to the google-cloud-python monorepo, so use the PyPI sdist.
  python3-rsa is no longer needed. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/364
- Drop RHEL 7, RHEL 8, RHEL 9, Amazon Linux 2023 and SLES 12 support. This
  package was built for the default python3 there, which bigquery_fdw (its
  only user) cannot use; bigquery_fdw now uses pgdg-python3-google-auth
  on those platforms. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/367

* Sun Oct 11 2026 Devrim Gunduz <devrim@gunduz.org> - 2.48.0-4PGDG
- Build the python311 flavor on SLES 15. The SUSE pyproject macros built
  for the default python3 (3.6), so the build failed there. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226
- Set python3_sitelib to the python3.11 one on SLES 15, too: the SUSE macro
  points to the default python3 (3.6).

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

* Mon Sep 14 2026 Devrim Gunduz <devrim@gunduz.org> - 2.48.0-3PGDG
- Use Python 3.11 on SLES 15
- Switch to pyproject builds

* Mon Sep 14 2026 Devrim Gunduz <devrim@gunduz.org> - 2.48.0-2
- Update to 2.48.0 per changes described at:
  https://github.com/googleapis/google-auth-library-python/releases/tag/v2.48.0
- Fix the structural spec bug
- Refresh the Requires to match upstream 2.48.0's actual install_requires
- Drop the google_auth-%%{version}*.pth glob from %%files

* Mon May 18 2020 Devrim Gündüz <devrim@gunduz.org> - 1.14.3-1
- Initial packaging for PostgreSQL RPM repository to satisfy
  bigquery_fdw dependency.
