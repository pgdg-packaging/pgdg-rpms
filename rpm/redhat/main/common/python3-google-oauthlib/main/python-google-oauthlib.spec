%global library google-oauthlib

# Upstream requires Python >= 3.7; SLES 15's default python3 is 3.6, so
# retarget to the python3.11 alt-stack there (matching python3-google
# -auth's own SLES 15 retarget, since this package depends on it and
# both need to be built against the same interpreter).
%if 0%{?suse_version} == 1500
%global __python3 %{_bindir}/python3.11
%global python3_pkgversion 311
%endif
%{!?python3_pkgversion: %global python3_pkgversion 3}

Name:		python%{python3_pkgversion}-%{library}
Version:	1.2.4
Release:	3PGDG%{?dist}
Epoch:		1
Summary:	oauthlib integration for Google Auth
License:	ASL 2.0
URL:		https://github.com/googleapis/google-auth-library-python-oauthlib

Source0:	https://github.com/googleapis/google-auth-library-python-oauthlib/archive/v%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-wheel
BuildRequires:	python%{python3_pkgversion}-setuptools
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif

Requires:	python%{python3_pkgversion}-google-auth >= 2.15.0

%description
oauthlib integration for Google Auth

%prep
%autosetup -n google-auth-library-python-oauthlib-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.rst
%{_bindir}/google-oauthlib-tool
%{python3_sitelib}/google_auth_oauthlib-%{version}.dist-info/
%{python3_sitelib}/google_auth_oauthlib/

%changelog
* Mon Sep 14 2026 Devrim Gunduz <devrim@gunduz.org> - 1.2.4-3PGDG
- Switch to pyproject builds
- Use Python 3.11 on SLES 15

* Mon Sep 14 2026 Devrim Gunduz <devrim@gunduz.org> - 1.2.4-2PGDG
- Fix the structural spec bug.
- Update to 1.2.4 per changes described at:
  https://github.com/googleapis/google-auth-library-python-oauthlib/releases/tag/v1.2.4

* Fri Aug 28 2026 Devrim Gündüz <devrim@gunduz.org> - 0.4.1-3PGDG
- Package the .egg-info directory itself instead of globbing only its
  contents (egg-info/*), so RHEL/Fedora's pythondist.attr generator
  (which is anchored on the .egg-info directory entry) actually fires
  and emits the correct runtime Requires. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226

* Sat Sep 21 2024 Devrim Gündüz <devrim@gunduz.org> - 0.4.1-2PGDG
- Remove comment
- Add PGDG branding

* Mon May 18 2020 Devrim Gündüz <devrim@gunduz.org> - 0.4.1-1
- Initial packaging for PostgreSQL RPM repository to satisfy
  bigquery_fdw dependency.
