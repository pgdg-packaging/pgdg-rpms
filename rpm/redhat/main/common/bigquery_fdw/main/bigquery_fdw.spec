# Disable internal dependency generator.
# We will specify dependencies in the spec file.
%{?python_disable_dependency_generator}

%global debug_package %{nil}

%if 0%{?fedora} >= 40 || 0%{?rhel} >= 10
%{expand: %%global py3ver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global py3ver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif

Summary:	BigQuery Foreign Data Wrapper for PostgreSQL
Name:		bigquery_fdw
Version:	2.0
Release:	3PGDG%{?dist}
# The exceptions allow linking to OpenSSL and PostgreSQL's libpq
License:	LGPLv3+ with exceptions
Url:		https://github.com/gabfl/%{name}/
Source0:	https://github.com/gabfl/%{name}/archive/%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	python3-devel

Requires:	multicorn
Requires:	python3-google-auth = 1.14.3
Requires:	python3-google-oauthlib = 0.4.1
Requires:	python3-google-cloud-bigquery = 1.24

%description
%prep
%setup -q -n %{name}-%{version}

%build
# Change /usr/bin/python to /usr/bin/python2 in the scripts:
for i in `find . -iname "*.py"`; do sed -i "s/\/usr\/bin\/env python/\/usr\/bin\/env python3/g" $i; done

python3 setup.py build

%install
python3 setup.py install --no-compile --root %{buildroot}

%files
%defattr(-,root,root)
%doc docs/ README.md
%license LICENSE
%{_bindir}/bq_client_test
%{python3_sitelib}/%{name}/*.py
%if 0%{?rhel} || 0%{?fedora}
%{python3_sitelib}/%{name}/__pycache__/*.pyc
%endif
%dir %{python3_sitelib}/%{name}-%{version}-py%{py3ver}.egg-info
%{python3_sitelib}/%{name}-%{version}-py%{py3ver}.egg-info/*

%changelog
* Sun Sep 9 2025 Devrim Gündüz <devrim@gunduz.org> - 2.0-3PGDG
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
