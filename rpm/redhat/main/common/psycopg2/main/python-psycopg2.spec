%global sname psycopg2
%global pname python-%{sname}

%global ppg2majver 2
%if 0%{?rhel} == 8
# DO NOT BUMP UP THESE VALUES FOR RHEL 8 #
%global ppg2midver 9
%global ppg2minver 6
%else
%global ppg2midver 9
%global ppg2minver 10
%endif
%{!?with_docs:%global with_docs 0}

%global __ospython %{_bindir}/python3
%global python3_runtimes python3

%if 0%{?fedora} >= 40 || 0%{?rhel} >= 10
%{expand: %%global py3ver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global py3ver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif

Summary:	A PostgreSQL database adapter for Python 3
Name:		python3-%{sname}
Version:	%{ppg2majver}.%{ppg2midver}.%{ppg2minver}
Release:	4PGDG%{?dist}
# The exceptions allow linking to OpenSSL and PostgreSQL's libpq
License:	LGPLv3+ with exceptions
Url:		https://www.psycopg.org
Source0:	https://github.com/psycopg/psycopg2/archive/refs/tags/%{ppg2majver}.%{ppg2midver}.%{ppg2minver}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	python3-devel

Requires:	libpq5 >= 10.0

Conflicts:	python-%{sname}-zope < %{version}

%description
Psycopg is the most popular PostgreSQL adapter for the Python
programming language. At its core it fully implements the Python DB
API 2.0 specifications. Several extensions allow access to many of the
features offered by PostgreSQL.

%package -n python3-%{sname}-tests
Summary:	A testsuite for Python 3
Requires:	python3-%sname = %version-%release

%description -n python3-%{sname}-tests
This sub-package delivers set of tests for the adapter.

%if %with_docs
%package doc
Summary:	Documentation for psycopg python PostgreSQL database adapter
Requires:	%{name} = %{version}-%{release}
Obsoletes:	python-%{sname}-doc >= 2.0.0
Provides:	python-%{sname}-doc = %{version}-%{release}

%description doc
Documentation and example files for the psycopg python PostgreSQL
database adapter.
%endif

%prep
%setup -q -n %{sname}-%{version}

%build

export PATH=%{pginstdir}/bin:$PATH

for python in %{python3_runtimes} ; do
  $python setup.py build

done

%if %with_docs
# Fix for wrong-file-end-of-line-encoding problem; upstream also must fix this.
for i in `find doc -iname "*.html"`; do sed -i 's/\r//' $i; done
for i in `find doc -iname "*.css"`; do sed -i 's/\r//' $i; done

# Get rid of a "hidden" file that rpmlint complains about
%{__rm} -f doc/html/.buildinfo
%endif

%install
export PATH=%{pginstdir}/bin:$PATH
for python in %{python3_runtimes} ; do
  $python setup.py install --no-compile --root %{buildroot}
done

# Copy tests directory:
%{__mkdir} -p %{buildroot}%{python3_sitearch}/%{sname}/
%{__cp} -rp tests %{buildroot}%{python3_sitearch}/%{sname}/tests
# This test is skipped on 3.7 and has a syntax error so brp-python-bytecompile would choke on it
%{__rm} -f %{buildroot}%{python3_sitearch}/%{sname}/tests/test_async_keyword.py

%files
%defattr(-,root,root)
%doc AUTHORS LICENSE NEWS README.rst
%dir %{python3_sitearch}/%{sname}
%{python3_sitearch}/%{sname}/*.py
%if ! 0%{?suse_version}
%dir %{python3_sitearch}/%{sname}/__pycache__
%{python3_sitearch}/%{sname}/__pycache__/*.pyc
%endif
%{python3_sitearch}/%{sname}-%{version}-py%{py3ver}.egg-info
%{python3_sitearch}/%{sname}/_psycopg.cpython-3?*.so

%files -n python3-%{sname}-tests
%{python3_sitearch}/%{sname}/tests

%if %with_docs
%files doc
%defattr(-,root,root)
%doc doc
%endif

%changelog
* Sat Mar 8 2025 Devrim Gündüz <devrim@gunduz.org> - 2.9.10-4PGDG
- Remove redundant BR

* Tue Dec 17 2024 Devrim Gündüz <devrim@gunduz.org> - 2.9.10-3PGDG
- psycopg2 > 2.9.6 does not build on RHEL 8. So add a permanent guard
  against accidental builds on RHEL 8 to prevent breakage.

* Tue Dec 17 2024 Devrim Gündüz <devrim@gunduz.org> - 2.9.10-2PGDG
- Add RHEL 10 support

* Wed Nov 20 2024 Devrim Gündüz <devrim@gunduz.org> - 2.9.10-1PGDG
- Update to 2.9.10 per changes descrihed at:
  https://github.com/psycopg/psycopg2/releases/tag/2.9.10

* Tue Jan 16 2024 Devrim Gündüz <devrim@gunduz.org> - 2.9.9-2PGDG
- Fix builds on RHEL 8 by exporting Python version manually

* Mon Oct 9 2023 Devrim Gündüz <devrim@gunduz.org> - 2.9.9-1PGDG
- Update to 2.9.9
- Add PGDG branding

* Fri Jun 2 2023 Devrim Gündüz <devrim@gunduz.org> - 2.9.6-1
- Update to 2.9.6

* Fri Mar 24 2023 Devrim Gündüz <devrim@gunduz.org> - 2.9.5-3
- Remove Python2 portions of the spec file. Psycopg2 dropped
  support for Python 2.7 (and 3.4 and 3.5) as of 2.9.

* Tue Dec 6 2022 Devrim Gündüz <devrim@gunduz.org> - 2.9.5-2
- Remove Advance Toolchain support from RHEL 7 - ppc64le.

* Tue Nov 1 2022 Devrim Gündüz <devrim@gunduz.org> - 2.9.5-1
- Update to 2.9.5

* Fri Oct 7 2022 Devrim Gündüz <devrim@gunduz.org> - 2.9.4-1
- Update to 2.9.4

* Wed Jan 5 2022 Devrim Gündüz <devrim@gunduz.org> - 2.9.3-1
- Update to 2.9.3

* Mon Jun 21 2021 Devrim Gündüz <devrim@gunduz.org> - 2.9-1
- Update to 2.9

* Mon Sep 7 2020 Devrim Gündüz <devrim@gunduz.org> - 2.8.6-1
- Update to 2.8.6

* Thu Aug 13 2020 Devrim Gündüz <devrim@gunduz.org> - 2.8.5-4
- Use the path provided by the "common" makefile. This package
  now goes to common directory.

* Wed May 13 2020 Devrim Gündüz <devrim@gunduz.org> - 2.8.5-3
- Depend on "libpq5", which is now provided by the latest
  PostgreSQL 10+ minor update set.

* Mon May 11 2020 Devrim Gündüz <devrim@gunduz.org> - 2.8.5-2
- Let python2-psycopg2 provide python-psycopg2. Per
  https://redmine.postgresql.org/issues/5491

* Mon Apr 6 2020 Devrim Gündüz <devrim@gunduz.org> - 2.8.5-1
- Update to 2.8.5

* Mon Oct 28 2019 Devrim Gündüz <devrim@gunduz.org> - 2.8.3-5
- Fix SLES 12 builds. Patch from Talha Bin Rizwan.

* Mon Oct 28 2019 Devrim Gündüz <devrim@gunduz.org> - 2.8.3-4
- Make PY3 package the default one, so that we can build this
  package easier on Fedora 31+ (and RHEL 9+)
- Remove SLES bits

* Wed Oct 16 2019 Devrim Gündüz <devrim@gunduz.org> - 2.8.3-3
- Add PY3 support to RHEL 7 package
- Get rid of -debug subpackage

* Tue Oct 1 2019 Devrim Gündüz <devrim@gunduz.org> - 2.8.3-2
- Rebuilt
- Require versionless -libs subpackage. Fixes
  https://redmine.postgresql.org/issues/4798
  https://redmine.postgresql.org/issues/4799

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 2.8.3-1.1
- Rebuild for PostgreSQL 12

* Fri Jun 28 2019 Devrim Gündüz <devrim@gunduz.org> - 2.8.3-1
- Update to 2.8.3

* Fri May 24 2019 Devrim Gündüz <devrim@gunduz.org> - 2.8.2-2
- Fix conflict with existing packages, per
  https://redmine.postgresql.org/issues/4287

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.8.2-1
- Update to 2.8.2
- Disable -doc subpackage for now. We need sphinx to build the docs,
  and I will defer it until 2.8.2 is out.
- Change main package name from python-psycopg2 to python2-psycopg2,
  in order to distinguish py2 and py3 packages. Also provide old package
  name in order not to break upgrades. Also invent pname macro, which
  stands for "provides name" (I was lazy to rename patches)
- Switch to python2_sitearch macro.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.7.5-1.1
- Rebuild against PostgreSQL 11.0

* Mon Jun 18 2018 Devrim Gündüz <devrim@gunduz.org> 2.7.5-1
- Update to 2.7.5 per
  http://www.psycopg.org/psycopg/articles/2018/06/17/psycopg-275-released/
- Change python to python2, to supress warning on Fedora 28+.

* Fri Feb 9 2018 Devrim Gündüz <devrim@gunduz.org> 2.7.4-1
- Update to 2.7.4 per
  http://www.psycopg.org/psycopg/articles/2018/02/08/psycopg-274-released/

* Sun Dec 10 2017 Devrim Gündüz <devrim@gunduz.org> 2.7.3.2-1
- Update to 2.7.3.2, per
  http://initd.org/psycopg/articles/2017/10/24/psycopg-2732-released/
- Add -tests subpackages.

* Mon Jul 24 2017 Devrim Gündüz <devrim@gunduz.org> 2.7.3-1
- Update to 2.7.3

* Tue Mar 14 2017 Devrim Gündüz <devrim@gunduz.org> 2.7.1-1
- Update to 2.7.1

* Sun Mar 05 2017 Devrim Gündüz <devrim@gunduz.org> 2.7-1
- Update to 2.7, per #2223.

* Fri Feb 24 2017 Devrim Gündüz <devrim@gunduz.org> 2.7b2-1
- Update to 2.7 beta 2

* Fri Oct 7 2016 Devrim Gündüz <devrim@gunduz.org> 2.6.2-3
- Move one .so file into python3-psycopg2 subpackage, per report
  from Oskari Saarenmaa.
- Fix RHEL 6 builds, with custom conditionals.
- Add BR for Python 2.7 environments.

* Tue Sep 13 2016 Devrim Gündüz <devrim@gunduz.org> 2.6.2-2
- Move python-debug (PY2 version) package into non-py3 builds.
  We need this at least for pgadmin4.

* Thu Jul 7 2016 Devrim Gündüz <devrim@gunduz.org> 2.6.2-1
- Update to 2.6.2, per changes described at:
  http://www.psycopg.org/psycopg/articles/2016/07/07/psycopg-262-released/

* Thu Jan 21 2016 Devrim Gündüz <devrim@gunduz.org> 2.6.1-1
- Update to 2.6.1
- Create unified spec file for all distros.
- Remove Zope subpackage.
- Minor spec file cleanups

* Mon Feb 9 2015 Devrim Gündüz <devrim@gunduz.org> 2.6-1
- Update to 2.6, per changes described at:
  http://www.psycopg.org/psycopg/articles/2015/02/09/psycopg-26-and-255-released/
- Trim changelog
- Merge some changes from Fedora spec file.
