# Disable internal dependency generator.
# We will specify dependencies in the spec file.
%{?python_disable_dependency_generator}

%if 0%{?fedora} && 0%{?fedora} == 44
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?fedora} && 0%{?fedora} == 43
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?fedora} && 0%{?fedora} <= 42
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?suse_version} == 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

%global debug_package %{nil}

%if 0%{?fedora} >= 42 || 0%{?rhel} >= 8 || 0%{?suse_version} == 1600
%{expand: %%global py3ver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global py3ver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif

Summary:	BigQuery Foreign Data Wrapper for PostgreSQL
Name:		bigquery_fdw
Version:	2.0
Release:	7PGDG%{?dist}
# The exceptions allow linking to OpenSSL and PostgreSQL's libpq
License:	LGPLv3+ with exceptions
Url:		https://github.com/gabfl/%{name}/
Source0:	https://github.com/gabfl/%{name}/archive/%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel python%{python3_pkgversion}-pip

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif

Requires:	multicorn2
Requires:	python3-google-auth = 1.14.3
Requires:	python3-google-oauthlib = 0.4.1
Requires:	python3-google-cloud-bigquery = 1.24

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
%if 0%{?rhel} || 0%{?fedora}
%{python3_sitelib}/%{name}/__pycache__/*.pyc
%endif
%{python3_sitelib}/%{name}-%{version}.dist-info

%changelog
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
