# Disable internal dependency generator.
# We will specify dependencies in the spec file.
%{?python_disable_dependency_generator}

%if 0%{?fedora} && 0%{?fedora} == 45
%global __python3 %{_bindir}/python3.15
%global python3_pkgversion 3.15
%endif
%if 0%{?fedora} && 0%{?fedora} <= 44
%global __python3 %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__python3 %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?amzn} == 2023
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?suse_version} == 1500
%global	__python3 %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

# python3-google-auth and python3-google-oauthlib are retargeted to the
# python3.11 alt-stack on SLES 15 specifically (their own python_requires
# floors are newer than SLES 15's default python3.6), but keep their
# plain "python3-" naming everywhere else, including SLES 16 (whose
# default python3 is already new enough). This tracks their real
# package names independently of this spec's own %%python3_pkgversion
# above, which follows a different (Fedora dnf virtual-package) naming
# convention. python3-google-cloud-bigquery is never retargeted anywhere.
%global googauth_pkgversion 3
%if 0%{?suse_version} == 1500
%global googauth_pkgversion 311
%endif

%global debug_package %{nil}

Summary:	BigQuery Foreign Data Wrapper for PostgreSQL
Name:		bigquery_fdw
Version:	2.0
Release:	12PGDG%{?dist}
# The exceptions allow linking to OpenSSL and PostgreSQL's libpq
License:	LGPLv3+ with exceptions
Url:		https://github.com/gabfl/%{name}/
Source0:	https://github.com/gabfl/%{name}/archive/%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-packaging
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif

Requires:	multicorn2
Requires:	python%{googauth_pkgversion}-google-auth >= 2.48.0
Requires:	python%{googauth_pkgversion}-google-oauthlib >= 1.2.4
Requires:	python3-google-cloud-bigquery >= 1.24.0

%description
bigquery_fdw is a BigQuery foreign data wrapper for PostgreSQL using
Multicorn2.

It allows to write queries in PostgreSQL SQL syntax using a foreign table. It
supports most of BigQuery's data types and operators.

%prep
%setup -q -n %{name}-%{version}

%build
# Change /usr/bin/python to /usr/bin/python2 in the scripts:
for i in `find . -iname "*.py"`; do sed -i "s/\/usr\/bin\/env python/\/usr\/bin\/env python3/g" $i; done
%pyproject_wheel

%install
%pyproject_install

%files
%defattr(-,root,root)
%doc docs/ README.md
%license LICENSE
%{_bindir}/bq_client_test
%{python3_sitelib}/%{name}/*.py
%{python3_sitelib}/%{name}/__pycache__/*.pyc
%{python3_sitelib}/%{name}-%{version}.dist-info

%changelog
* Mon Sep 14 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0-12PGDG
- Refresh the stale, hardcoded exact-version Requires on
  python3-google-auth (was = 1.14.3), python3-google-oauthlib (was =
  0.4.1) and python3-google-cloud-bigquery (was = 1.24) 
- Switch to pyproject builds.
- Enable pycache everywhere
- Remove Fedora <= 42 support

* Thu Sep 10 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0-10PGDG
- Add missing BR

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0-9PGDG
- Also set __python3 (not just __ospython) for Amazon Linux 2023, so
  %pyproject_wheel/%pyproject_install actually build against python3.13
  instead of silently falling back to the system default python3
  (__ospython only affects this repo's own macro computations, not
  RPM's own pyproject/site-packages macros).

* Tue Aug 25 2026 Devrim Gündüz <devrim@gunduz.org> - 2.0-8PGDG
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Thu May 7 2026 Devrim Gündüz <devrim@gunduz.org> - 2.0-7PGDG
- Add missing BR

* Tue Apr 28 2026 Devrim Gündüz <devrim@gunduz.org> - 2.0-6PGDG
- Use Python 3.14 on Fedora 44. Many BRs and Requires are not ready
  for 3.15.

* Tue Apr 28 2026 Devrim Gündüz <devrim@gunduz.org> - 2.0-5PGDG
- Switch to pyproject builds
- Add Fedora 44 support

* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 2.0-4PGDG
- Use multicorn2 instead of deprecated multicorn package.
- Add SLES 16 support

* Sun Mar 9 2025 Devrim Gündüz <devrim@gunduz.org> - 2.0-3PGDG
- Add RHEL 10 dependency
- Remove redundant BR

* Fri Feb 16 2024 Devrim Gündüz <devrim@gunduz.org> - 2.0-2PGDG
- Fix SLES 15 builds
- Add PGDG branding
- Fix rpmlint warning

* Tue Dec 6 2022 Devrim Gündüz <devrim@gunduz.org> - 2.0-1
- Update to 2.0

* Tue Dec 6 2022 Devrim Gündüz <devrim@gunduz.org> - 1.6-3
- Remove Advance Toolchain support from RHEL 7 - ppc64le.

* Mon Mar 28 2022 Devrim Gündüz <devrim@gunduz.org> - 1.6-2
- Add Fedora 35+ support.

* Mon May 18 2020 Devrim Gündüz <devrim@gunduz.org> - 1.6-1
- Update to 1.6

* Mon May 4 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.2-1
- Initial packaging for PostgreSQL YUM repository
