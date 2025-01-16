%global sname psycopg3
%global pname python-%{sname}

%{!?with_docs:%global with_docs 0}

%if 0%{?rhel} == 8
%global python3_runtimes python3.9
%global __ospython %{_bindir}/python3.9
%global python3_sitearch %(%{__ospython} -Ic "import sysconfig; print(sysconfig.get_path('platlib', vars={'platbase': '%{_prefix}', 'base': '%{_prefix}'}))")
%else
%global python3_runtimes python3
%global __ospython %{_bindir}/python3
%endif

%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

%if 0%{?fedora} >= 40 || 0%{?rhel} >= 10
%{expand: %%global py3ver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global py3ver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif

Summary:	A PostgreSQL database adapter for Python 3
Name:		python3-%{sname}
Version:	3.2.4
Release:	1PGDG%{?dist}
# The exceptions allow linking to OpenSSL and PostgreSQL's libpq
License:	LGPLv3+ with exceptions
Url:		https://psycopg.org
Source0:	https://github.com/psycopg/psycopg/archive/refs/tags/%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	python3-devel

Requires:	libpq5 >= 10.0
Requires:	python3-typing-extensions

BuildArch:	noarch

%description
Psycopg is the most popular PostgreSQL adapter for the Python
programming language. At its core it fully implements the Python DB
API 2.0 specifications. Several extensions allow access to many of the
features offered by PostgreSQL.

# Enable this package only on Fedora, which has PY 3.9:
%if 0%{?fedora} >= 40
%package -n python3-%{sname}-tests
Summary:	A testsuite for Python 3
Requires:	python3-%sname = %version-%release

%description -n python3-%{sname}-tests
This sub-package delivers set of tests for the adapter.
%endif

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
%setup -q -n psycopg-%{version}

%build
# Change Python path in the scripts:
find . -iname "*.py" -exec sed -i "s/\/usr\/bin\/env python/\/usr\/bin\/python3/g" {} \;

export PATH=%{pginstdir}/bin:$PATH
pushd psycopg
%{__ospython} setup.py build
popd

%if %with_docs
# Fix for wrong-file-end-of-line-encoding problem; upstream also must fix this.
for i in `find doc -iname "*.html"`; do sed -i 's/\r//' $i; done
for i in `find doc -iname "*.css"`; do sed -i 's/\r//' $i; done

# Get rid of a "hidden" file that rpmlint complains about
%{__rm} -f doc/html/.buildinfo
%endif

%install
export PATH=%{pginstdir}/bin:$PATH
pushd psycopg
%{__ospython} setup.py install --no-compile --root %{buildroot}
popd

%{__mkdir} -p %{buildroot}%{python3_sitearch}/%{sname}/

#Only on Fedora:
%if 0%{?fedora} >= 40
# Copy tests directory:
%{__cp} -rp tests %{buildroot}%{python3_sitearch}/%{sname}/tests
# This test is skipped on 3.7 and has a syntax error so brp-python-bytecompile would choke on it
%{__rm} -f %{buildroot}%{python3_sitearch}/%{sname}/tests/test_async_keyword.py
%endif

%files
%defattr(-,root,root)
%doc README.rst
%dir %{python3_sitearch}/%{sname}

%{python3_sitelib}/psycopg-%{version}-py%{py3ver}.egg-info/*
%{python3_sitelib}/psycopg/*.py
%{python3_sitelib}/psycopg/crdb/*.py*
%{python3_sitelib}/psycopg/pq/*.py*
%{python3_sitelib}/psycopg/types/*.py*
%{python3_sitelib}/psycopg/py.typed

%if 0%{?fedora} >= 39 || 0%{?rhel} >= 7
%{python3_sitelib}/psycopg/__pycache__/*.pyc
%{python3_sitelib}/psycopg/crdb/__pycache__/*.py*
%{python3_sitelib}/psycopg/pq/__pycache__/*.py*
%{python3_sitelib}/psycopg/types/__pycache__/*.py*
%endif

# Only on Fedora:
%if 0%{?fedora} > 39
%files -n python3-%{sname}-tests
%{python3_sitearch}/%{sname}/tests
%endif

%if %with_docs
%files doc
%defattr(-,root,root)
%doc doc
%endif

%changelog
* Thu Jan 16 2025 Devrim Gündüz <devrim@gunduz.org> - 3.2.4-1PGDG
- Update to 3.2.4 per changes described at:
  https://github.com/psycopg/psycopg/releases/tag/3.2.4

* Tue Dec 17 2024 Devrim Gündüz <devrim@gunduz.org> - 3.2.3-2PGDG
- Add RHEL 10 support

* Wed Oct 2 2024 Devrim Gündüz <devrim@gunduz.org> - 3.2.3-1PGDG
- Update to 3.2.3 per changes described at:
  https://github.com/psycopg/psycopg/releases/tag/3.2.3

* Wed Sep 25 2024 Devrim Gündüz <devrim@gunduz.org> - 3.2.2-2PGDG
- Add python3-typing-extensions dependency per:
  https://redmine.postgresql.org/issues/7781

* Sun Sep 22 2024 Devrim Gündüz <devrim@gunduz.org> - 3.2.2-1PGDG
- Update to 3.2.2 per changes described at:
  https://github.com/psycopg/psycopg/releases/tag/3.2.2

* Tue Jul 2 2024 Devrim Gündüz <devrim@gunduz.org> - 3.2.1-1PGDG
- Update to 3.2.1

* Mon May 20 2024 Devrim Gündüz <devrim@gunduz.org> - 3.1.19-1PGDG
- Update to 3.1.19, per changes described at:
  https://github.com/psycopg/psycopg/releases/tag/3.1.19

* Tue Feb 6 2024 Devrim Gündüz <devrim@gunduz.org> - 3.1.18-1PGDG
- Update to 3.1.18, per changes described at:
  https://github.com/psycopg/psycopg/releases/tag/3.1.18

* Fri Jan 19 2024 Devrim Gündüz <devrim@gunduz.org> - 3.1.17-2PGDG
- Add RHEL 8 support

* Sun Jan 7 2024 Devrim Gündüz <devrim@gunduz.org> - 3.1.17-1PGDG
- Update to 3.1.17, per changes described at:
  https://github.com/psycopg/psycopg/releases/tag/3.1.17

* Wed Jan 3 2024 Devrim Gündüz <devrim@gunduz.org> - 3.1.16-1PGDG
- Update to 3.1.16, per changes described at:
  https://github.com/psycopg/psycopg/releases/tag/3.1.16
  https://github.com/psycopg/psycopg/releases/tag/3.1.15

* Mon Dec 11 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.14-1PGDG
- Update to 3.1.14, per changes described at:
  https://github.com/psycopg/psycopg/releases/tag/3.1.14

* Mon Oct 9 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.12-1PGDG
- Update to 3.1.12

* Thu Sep 14 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.10-1PGDG
- Update to 3.1.10
- Add PGDG branding

* Thu May 4 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.9-1
- Update to 3.1.9

* Tue Feb 21 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.8-1
- Update to 3.1.8

* Tue Jan 3 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.7-1
- Update to 3.1.7

* Tue Dec 6 2022 Devrim Gündüz <devrim@gunduz.org> - 3.1.4-2
- Remove Advance Toolchain support from RHEL 7 - ppc64le.

* Tue Nov 1 2022 Devrim Gündüz <devrim@gunduz.org> - 3.1.4-1
- Update to 3.1.4

* Fri Oct 7 2022 Devrim Gündüz <devrim@gunduz.org> - 3.1.3-1
- Update to 3.1.3

* Fri Sep 16 2022 Devrim Gündüz <devrim@gunduz.org> - 3.1.1-1
- Update to 3.1.1

* Sun Sep 4 2022 Devrim Gündüz <devrim@gunduz.org> - 3.1-1
- Update to 3.1

* Sun Jul 10 2022 Devrim Gündüz <devrim@gunduz.org> - 3.0.15-1
- Update to 3.0.15

* Mon Apr 18 2022 Devrim Gündüz <devrim@gunduz.org> - 3.0.11-1
- Update to 3.0.11

* Mon Mar 28 2022 Devrim Gündüz <devrim@gunduz.org> - 3.0.10-1
- Update to 3.0.10

* Mon Feb 28 2022 Devrim Gündüz <devrim@gunduz.org> - 3.0.9-1
- Update to 3.0.9

* Thu Jan 20 2022 Devrim Gündüz <devrim@gunduz.org> - 3.0.8-1
- Update to 3.0.8

* Wed Jan 5 2022 Devrim Gündüz <devrim@gunduz.org> - 3.0.7-1
- Update to 3.0.7

* Tue Nov 2 2021 Devrim Gündüz <devrim@gunduz.org> - 3.0-3
- Add Fedora 35 support.

* Wed Oct 13 2021 Devrim Gündüz <devrim@gunduz.org> - 3.0-2
- Disable unit tests on RHEL, because of Python version. Per tip from
  Daniele: https://github.com/psycopg/psycopg/issues/106

* Wed Oct 13 2021 Devrim Gündüz <devrim@gunduz.org> - 3.0-1
- Update to 3.0

* Wed Sep 8 2021 Devrim Gündüz <devrim@gunduz.org> - 3.0-beta1-1
- Initial packaging
