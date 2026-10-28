%pgdg_python3_setup

# This spec builds the python3.12 / python3.13 alt-stack flavor
# (python3.12-google-auth, python3.13-google-auth) on RHEL 8, 9 and 10 and
# Amazon Linux 2023, for pg_statviz and bigquery_fdw. On RHEL 10, where
# Python 3.12 is the default, it replaces EPEL's python3-google-auth and its
# extras subpackages.
#
# It is not built on Fedora and SUSE: they ship python3-google-auth
# (python311-/python313-google-auth on SUSE) themselves, new enough for
# bigquery_fdw, together with its extras subpackages, which pin it to their
# own version. The default python3 flavor that this spec used to build there
# replaced the OS package and broke the updates of those extras.

%global	modname google-auth
%global	pymodname google_auth

# The 2.47 series on RHEL 9 and Amazon Linux 2023 (see the description).
# RHEL 8 is only used by bigquery_fdw, and its python3.12-cryptography is
# new enough for the current release, as is the one of RHEL 10:
%if 0%{?rhel} == 9 || 0%{?amzn} == 2023
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
Release:	44PGDG%{?dist}
%if 0%{?rhel} == 10
# EPEL's python3-google-auth has Epoch 1, and obsoletes
# python3.12-google-auth < 1:<its version>, which matched ours, whatever our
# version was:
Epoch:		1
%endif
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
Obsoletes:	python3-google-auth < %{epoch}:%{version}-%{release}
%endif

%description
This library simplifies using Google's various server-to-server
authentication mechanisms to access Google APIs.

%if %{pgdg_gauth247}
This is the 2.47 series, the newest one that does not need cryptography >=
38 (Amazon Linux 2023 has 36 for python3.13).
%endif

# google-genai (pg_statviz) requires google-auth[requests]:
%if 0%{?rhel} == 9 || 0%{?amzn} == 2023
%pyproject_extras_subpkg -n python%{python3_pkgversion}-%{modname} requests
%endif

%if 0%{?rhel} == 10
# EPEL ships these extras metapackages, which require its own python3-google-auth
# version, so they made dnf upgrade fail. Replace them with ours:
%package -n %{name}+aiohttp
Summary:	Metapackage for %{name}: aiohttp extras
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python3-google-auth+aiohttp = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	python3-google-auth+aiohttp < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{name}+aiohttp
This is a metapackage bringing in aiohttp extras requires for
%{name}. It makes sure the dependencies are installed.

%files -n %{name}+aiohttp
%ghost %{python3_sitelib}/%{pymodname}-%{version}.dist-info

%package -n %{name}+enterprise_cert
Summary:	Metapackage for %{name}: enterprise_cert extras
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python3-google-auth+enterprise_cert = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	python3-google-auth+enterprise_cert < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{name}+enterprise_cert
This is a metapackage bringing in enterprise_cert extras requires for
%{name}. It makes sure the dependencies are installed.

%files -n %{name}+enterprise_cert
%ghost %{python3_sitelib}/%{pymodname}-%{version}.dist-info

%package -n %{name}+pyjwt
Summary:	Metapackage for %{name}: pyjwt extras
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python3-google-auth+pyjwt = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	python3-google-auth+pyjwt < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{name}+pyjwt
This is a metapackage bringing in pyjwt extras requires for
%{name}. It makes sure the dependencies are installed.

%files -n %{name}+pyjwt
%ghost %{python3_sitelib}/%{pymodname}-%{version}.dist-info

%package -n %{name}+pyopenssl
Summary:	Metapackage for %{name}: pyopenssl extras
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python3-google-auth+pyopenssl = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	python3-google-auth+pyopenssl < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{name}+pyopenssl
This is a metapackage bringing in pyopenssl extras requires for
%{name}. It makes sure the dependencies are installed.

%files -n %{name}+pyopenssl
%ghost %{python3_sitelib}/%{pymodname}-%{version}.dist-info

%package -n %{name}+requests
Summary:	Metapackage for %{name}: requests extras
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python3-google-auth+requests = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	python3-google-auth+requests < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{name}+requests
This is a metapackage bringing in requests extras requires for
%{name}. It makes sure the dependencies are installed.

%files -n %{name}+requests
%ghost %{python3_sitelib}/%{pymodname}-%{version}.dist-info

%package -n %{name}+urllib3
Summary:	Metapackage for %{name}: urllib3 extras
Requires:	%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	python3-google-auth+urllib3 = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	python3-google-auth+urllib3 < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{name}+urllib3
This is a metapackage bringing in urllib3 extras requires for
%{name}. It makes sure the dependencies are installed.

%files -n %{name}+urllib3
%ghost %{python3_sitelib}/%{pymodname}-%{version}.dist-info
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
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 1:2.62.0-44PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Mon Oct 26 2026 Devrim Gunduz <devrim@gunduz.org> - 1:2.62.0-43PGDG
- RHEL 10: Add Epoch 1, as EPEL's python3-google-auth has it, and obsoletes
  python3.12-google-auth < 1:<its version>, which matched our package, so
  EPEL's replaced ours on updates. Build 2.62.0 there, not the 2.47 series:
  RHEL 10 has a new enough cryptography.
- RHEL 10: Add the +aiohttp, +enterprise_cert, +pyjwt, +pyopenssl,
  +requests and +urllib3 extras metapackages, which replace EPEL's. They
  require EPEL's own python3-google-auth version, so they made dnf upgrade
  fail. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422

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
