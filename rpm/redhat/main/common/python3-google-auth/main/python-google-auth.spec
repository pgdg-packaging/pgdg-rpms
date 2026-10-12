%{?python_enable_dependency_generator}

%global library google-auth

# Upstream requires Python >= 3.8; SLES 15's default python3 is 3.6, so
# retarget to the python3.11 alt-stack there (matching the convention
# used elsewhere in this repo, e.g. PyMySQL/argcomplete on SLES 15).
%if 0%{?suse_version} == 1500
%global __python3 %{_bindir}/python3.11
%global python3_pkgversion 311
# Build the python311 flavor with the SUSE pyproject macros, instead of
# the default python3 (3.6):
%global	pythons python311
%global	python3_sitelib %{_prefix}/lib/python3.11/site-packages
%endif
%{!?python3_pkgversion: %global python3_pkgversion 3}

# google-auth 2.51.0 and later need Python >= 3.10 and cryptography >=
# 38.0.3. The default python3 on RHEL 8 (3.6), RHEL 9 and Amazon Linux
# 2023 (3.9, with cryptography 36) is too old for that, so stay at 2.48.0
# there:
%global	gauth_legacy 0
%if ( 0%{?rhel} && 0%{?rhel} <= 9 ) || 0%{?amzn} == 2023 || 0%{?suse_version} == 1315
%global	gauth_legacy 1
%endif

Name:		python%{python3_pkgversion}-%{library}
%if %{gauth_legacy}
Version:	2.48.0
Release:	4PGDG%{?dist}
%else
Version:	2.62.0
Release:	1PGDG%{?dist}
%endif
Epoch:		1
Summary:	Google Auth Python Library
License:	ASL 2.0
%if %{gauth_legacy}
URL:		https://github.com/googleapis/google-auth-library-python
Source0:	https://github.com/googleapis/google-auth-library-python/archive/v%{version}.tar.gz
%else
# The upstream repository moved into the google-cloud-python monorepo,
# which does not tag google-auth releases, so use the PyPI sdist:
URL:		https://github.com/googleapis/google-cloud-python/tree/main/packages/google-auth
Source0:	https://files.pythonhosted.org/packages/source/g/google_auth/google_auth-%{version}.tar.gz
%endif

BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-pip python%{python3_pkgversion}-wheel
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif
Requires:	python%{python3_pkgversion}-pyasn1-modules
%if %{gauth_legacy}
Requires:	python%{python3_pkgversion}-cryptography
Requires:	python%{python3_pkgversion}-rsa
%else
Requires:	python%{python3_pkgversion}-cryptography >= 38.0.3
%endif

%description
Google Auth Python Library

%prep
%if %{gauth_legacy}
%autosetup -n google-auth-library-python-%{version}
%else
%autosetup -n google_auth-%{version}
%endif

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%{python3_sitelib}/google/auth
%{python3_sitelib}/google/oauth2
%{python3_sitelib}/google_auth-%{version}.dist-info/

%changelog
* Mon Oct 12 2026 Devrim Gunduz <devrim@gunduz.org> - 2.62.0-1PGDG
- Update to 2.62.0 on Fedora, RHEL 10 and SLES 15/16, per changes
  described at https://pypi.org/project/google-auth/2.62.0/ . Upstream
  moved to the google-cloud-python monorepo, so use the PyPI sdist.
  python3-rsa is no longer needed.
- Stay at 2.48.0 on RHEL 8, RHEL 9 and Amazon Linux 2023: 2.51.0 and
  later need Python >= 3.10 and cryptography >= 38.0.3.
- Per https://github.com/pgdg-packaging/pgdg-rpms/issues/364

* Sun Oct 11 2026 Devrim Gunduz <devrim@gunduz.org> - 2.48.0-4PGDG
- Build the python311 flavor on SLES 15. The SUSE pyproject macros built
  for the default python3 (3.6), so the build failed there. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226
- Set python3_sitelib to the python3.11 one on SLES 15, too: the SUSE macro
  points to the default python3 (3.6).

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
