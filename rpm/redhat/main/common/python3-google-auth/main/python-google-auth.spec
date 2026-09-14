%{?python_enable_dependency_generator}

%global library google-auth

Name:		python3-%{library}
Version:	2.48.0
Release:	2%{?dist}
Epoch:		1
Summary:	Google Auth Python Library
License:	ASL 2.0
URL:		https://github.com/googleapis/google-auth-library-python

Source0:	https://github.com/googleapis/google-auth-library-python/archive/v%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	python3-devel python3-setuptools
Requires:	python3-cryptography
Requires:	python3-pyasn1-modules
Requires:	python3-rsa

%description
Google Auth Python Library

%prep
%autosetup -n google-auth-library-python-%{version}

%build
%py3_build

%install
%py3_install

%check

%files
%license LICENSE
%{python3_sitelib}/google/auth
%{python3_sitelib}/google/oauth2
%{python3_sitelib}/google_auth-%{version}*.egg-info

%changelog
* Mon Sep 14 2026 Devrim Gunduz <devrim@gunduz.org> - 2.48.0-2
- Update to 2.48.0 per changes described at:
  https://github.com/googleapis/google-auth-library-python/releases/tag/v2.48.0
- Fix the structural spec bug
- Refresh the Requires to match upstream 2.48.0's actual install_requires
- Drop the google_auth-%%{version}*.pth glob from %%files

* Mon May 18 2020 Devrim Gündüz <devrim@gunduz.org> - 1.14.3-1
- Initial packaging for PostgreSQL RPM repository to satisfy
  bigquery_fdw dependency.
