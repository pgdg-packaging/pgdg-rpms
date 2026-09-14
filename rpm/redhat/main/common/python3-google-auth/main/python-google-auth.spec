%{?python_enable_dependency_generator}

%global library google-auth

# Upstream requires Python >= 3.8; SLES 15's default python3 is 3.6, so
# retarget to the python3.11 alt-stack there (matching the convention
# used elsewhere in this repo, e.g. PyMySQL/argcomplete on SLES 15).
%if 0%{?suse_version} == 1500
%global __python3 %{_bindir}/python3.11
%global python3_pkgversion 311
%endif
%{!?python3_pkgversion: %global python3_pkgversion 3}

Name:		python%{python3_pkgversion}-%{library}
Version:	2.48.0
Release:	3%{?dist}
Epoch:		1
Summary:	Google Auth Python Library
License:	ASL 2.0
URL:		https://github.com/googleapis/google-auth-library-python

Source0:	https://github.com/googleapis/google-auth-library-python/archive/v%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-pip python%{python3_pkgversion}-wheel
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif
Requires:	python%{python3_pkgversion}-cryptography
Requires:	python%{python3_pkgversion}-pyasn1-modules
Requires:	python%{python3_pkgversion}-rsa

%description
Google Auth Python Library

%prep
%autosetup -n google-auth-library-python-%{version}

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
