%{?python_enable_dependency_generator}

%global library google-auth

Name:		python3-%{library}
Version:	2.48.0
Release:	1%{?dist}
Epoch:		1
Summary:	Google Auth Python Library
License:	ASL 2.0
URL:		https://github.com/googleapis/google-auth-library-python

Source0:	https://github.com/googleapis/google-auth-library-python/archive/v%{version}.tar.gz

BuildArch:	noarch

%description
Google Auth Python Library

BuildRequires:	python3-devel python3-setuptools
Requires:	python3-pyasn1 python3-pyasn1-modules
Requires:	python3-rsa python3-six
Requires:	python3-cachetools

%prep
%autosetup -n google-auth-library-python-%{version}

#Allow newer cachetools
sed -i 's/<3\.2/<5.0/g' setup.py

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
%{python3_sitelib}/google_auth-%{version}*.pth

%changelog
* Mon Aug 31 2026 Devrim Gündüz <devrim@gunduz.org> - 2.48.0-1
- Update to 2.48.0 per changes described at:
  https://github.com/googleapis/google-auth-library-python/releases/tag/v2.48.0

* Mon May 18 2020 Devrim Gündüz <devrim@gunduz.org> - 1.14.3-1
- Initial packaging for PostgreSQL RPM repository to satisfy
  bigquery_fdw dependency.
