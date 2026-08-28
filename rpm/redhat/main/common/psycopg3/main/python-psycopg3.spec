%global sname psycopg3
%global pname python-%{sname}

%{!?with_docs:%global with_docs 0}

%if 0%{?rhel} == 8
%global python3_runtimes python3.9
%global __ospython %{_bindir}/python3.9
%global python3_sitearch %(%{__ospython} -Ic "import sysconfig; print(sysconfig.get_path('platlib', vars={'platbase': '%{_prefix}', 'base': '%{_prefix}'}))")
%else
%if 0%{?amzn} == 2023
# AL2023's default python3 is 3.9, but psycopg requires >= 3.10, so build
# against the python3.13 alt-stack (also the only one with a Cython package).
%global __python3 %{_bindir}/python3.13
%global python3_runtimes python3.13
%global __ospython %{_bindir}/python3.13
%global python3_sitearch %(%{__ospython} -Ic "import sysconfig; print(sysconfig.get_path('platlib', vars={'platbase': '%{_prefix}', 'base': '%{_prefix}'}))")
%else
%global python3_runtimes python3
%global __ospython %{_bindir}/python3
%endif
%endif

%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

%if 0%{?fedora} >= 42 || 0%{?rhel} >= 10 || 0%{?suse_version} == 1600 || 0%{?amzn} == 2023
%{expand: %%global py3ver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global py3ver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif

Summary:	A PostgreSQL database adapter for Python 3
Name:		python3-%{sname}
Version:	3.3.4
Release:	3PGDG%{?dist}
# The exceptions allow linking to OpenSSL and PostgreSQL's libpq
License:	LGPLv3+ with exceptions
Url:		https://psycopg.org
Source0:	https://github.com/psycopg/psycopg/archive/refs/tags/%{version}.tar.gz
Patch0:		psycopg-3.3.3-pyproject-license.patch
Patch1:		psycopg-3.3.3-_c_pyproject-license.patch

BuildRequires:	postgresql%{pgmajorversion}-devel
%if 0%{?amzn} == 2023
BuildRequires:	python3.13-wheel
BuildRequires:	python3.13-devel python3.13-pip python3.13-setuptools
BuildRequires:	python3.13-cython
%else
BuildRequires:	python3-wheel
BuildRequires:	python3-devel python3-pip python3-setuptools
%if 0%{?suse_version} == 1600
BuildRequires:	python313-Cython
%else
BuildRequires:	python3-cython
%endif
%endif

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros pyproject-srpm-macros
%endif

Requires:	libpq5 >= 10.0
Requires:	python3-typing-extensions

BuildArch:	noarch

%description
Psycopg is the most popular PostgreSQL adapter for the Python
programming language. At its core it fully implements the Python DB
API 2.0 specifications. Several extensions allow access to many of the
features offered by PostgreSQL.

# Enable this package only on Fedora:
%if 0%{?fedora} >= 42
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

%package c
Summary:	C extensions for Psycopg 3
Requires:	libpq5

%description c
This package contains the C extensions for enhanced performance in Psycopg 3.

%prep
%setup -q -n psycopg-%{version}
%patch -P 0 -p0
%patch -P 1 -p0

%build
# Change Python path in the scripts:
find . -iname "*.py" -exec sed -i "s/\/usr\/bin\/env python/\/usr\/bin\/python3/g" {} \;

export PATH=%{pginstdir}/bin:$PATH
pushd psycopg
%pyproject_wheel
popd
pushd psycopg_c
%pyproject_wheel
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
%pyproject_install
popd
pushd psycopg_c
%pyproject_install
popd

%{__mkdir} -p %{buildroot}%{python3_sitearch}/%{sname}/

#Only on Fedora:
%if 0%{?fedora} >= 42
# Copy tests directory:
%{__cp} -rp tests %{buildroot}%{python3_sitearch}/%{sname}/tests
# This test is skipped on 3.7 and has a syntax error so brp-python-bytecompile would choke on it
%{__rm} -f %{buildroot}%{python3_sitearch}/%{sname}/tests/test_async_keyword.py
%endif

%pre
# Remove old psycopg3 directory on updates
if [ $1 -gt 1 ] ; then
%{__rm} -rf %{python3_sitelib}/psycopg-3*-py%{py3ver}.egg-info
fi

%files
%defattr(-,root,root)
%doc README.rst
%dir %{python3_sitearch}/%{sname}

%{python3_sitelib}/psycopg-%{version}.dist-info/
%{python3_sitelib}/psycopg/*.py
%{python3_sitelib}/psycopg/crdb/*.py*
%{python3_sitelib}/psycopg/pq/*.py*
%{python3_sitelib}/psycopg/types/*.py*
%{python3_sitelib}/psycopg/py.typed

%if 0%{?fedora} >= 42 || 0%{?rhel} >= 8 || 0%{?suse_version} == 1600 || 0%{?amzn} == 2023
%{python3_sitelib}/psycopg/__pycache__/*.pyc
%{python3_sitelib}/psycopg/crdb/__pycache__/*.py*
%{python3_sitelib}/psycopg/pq/__pycache__/*.py*
%{python3_sitelib}/psycopg/types/__pycache__/*.py*
%endif

# Only on Fedora:
%if 0%{?fedora} >= 42
%files -n python3-%{sname}-tests
%{python3_sitearch}/%{sname}/tests
%endif

%if %with_docs
%files doc
%defattr(-,root,root)
%doc doc
%endif

%files c
%{python3_sitelib}/psycopg_c-%{version}.dist-info/
%{python3_sitelib}/psycopg_c/*.py*
%{python3_sitelib}/psycopg_c/__pycache__/*py*
%{python3_sitelib}/psycopg_c/_psycopg/*
%{python3_sitelib}/psycopg_c/pq.pxd
%{python3_sitelib}/psycopg_c/pq/*
%{python3_sitelib}/psycopg_c/py.typed

%changelog
* Fri Aug 28 2026 Devrim Gündüz <devrim@gunduz.org> - 3.3.4-3PGDG
- Package the psycopg_c .dist-info directory itself instead of globbing
  only its contents (dist-info/*), so RHEL/Fedora's pythondist.attr
  generator (which is anchored on the .dist-info directory entry)
  actually fires and emits the correct runtime Requires for this
  subpackage too (the main psycopg package already packaged its own
  .dist-info directory correctly). Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226

* Tue Aug 25 2026 Devrim Gündüz <devrim@gunduz.org> - 3.3.4-2PGDG
- Build against the python3.13 alt-stack on Amazon Linux 2023, since the
  default python3 there is 3.9 and psycopg requires >= 3.10. It's also
  the only alt-Python version on AL2023 with a Cython package available.

* Sun May 3 2026 Devrim Gündüz <devrim@gunduz.org> - 3.3.4-1PGDG
- Update to 3.3.4 per changes described at:
  https://github.com/psycopg/psycopg/releases/tag/3.3.4

* Thu Feb 19 2026 Devrim Gündüz <devrim@gunduz.org> - 3.3.3-1PGDG
- Update to 3.3.3 per changes described at:
  https://github.com/psycopg/psycopg/releases/tag/3.3.3
- Add a patch that updates license field to compatible format for
  all supported Python versions.
- Add new subpackage: Optimization module written in C/Cython

* Sun Dec 7 2025 Devrim Gündüz <devrim@gunduz.org> - 3.3.2-1PGDG
- Update to 3.3.2 per changes described at:
  https://github.com/psycopg/psycopg/releases/tag/3.3.2

* Wed Dec 3 2025 Devrim Gündüz <devrim@gunduz.org> - 3.3.1-1PGDG
- Update to 3.3.1 per changes described at:
  https://github.com/psycopg/psycopg/releases/tag/3.3.1

* Tue Dec 2 2025 Devrim Gündüz <devrim@gunduz.org> - 3.3.0-1PGDG
- Update to 3.3.0 per changes described at:
  https://github.com/psycopg/psycopg/releases/tag/3.3.0

* Mon Nov 24 2025 Devrim Gündüz <devrim@gunduz.org> - 3.2.13-1PGDG
- Update to 3.2.13 per changes described at:
  https://github.com/psycopg/psycopg/releases/tag/3.2.13

* Fri Nov 7 2025 Devrim Gündüz <devrim@gunduz.org> - 3.2.12-2PGDG
- Add missing BRs. Spotted during mock builds.
- Install __pycache__ also on SLES 16.

* Mon Oct 27 2025 Devrim Gündüz <devrim@gunduz.org> - 3.2.12-1PGDG
- Update to 3.2.12 per changes described at:
  https://github.com/psycopg/psycopg/releases/tag/3.2.12

* Mon Oct 20 2025 Devrim Gündüz <devrim@gunduz.org> - 3.2.11-1PGDG
- Update to 3.2.11 per changes described at:
  https://github.com/psycopg/psycopg/releases/tag/3.2.11
- Switch to pyproject builds

* Sat Oct 4 2025 Devrim Gündüz <devrim@gunduz.org> - 3.2.10-2PGDG
- Add SLES 16 support

* Mon Sep 8 2025 Devrim Gündüz <devrim@gunduz.org> - 3.2.10-1PGDG
- Update to 3.2.10 per changes described at:
  https://github.com/psycopg/psycopg/releases/tag/3.2.10

* Mon Aug 25 2025 Devrim Gündüz <devrim@gunduz.org> - 3.2.9-2PGDG
- Forgot to bump up the version number in previous commit. Fixed.
- Fix logic in removing "old" psycopg egg directory. Improves the
  solution in https://github.com/pgdg-packaging/pgdg-rpms/issues/66

* Mon Aug 4 2025 Devrim Gündüz <devrim@gunduz.org> - 3.2.9-1PGDG
- Remove old psycopg3 directory on updates. Per report and patch from
  Alexandre Pereira: https://github.com/pgdg-packaging/pgdg-rpms/issues/66
- Update to 3.2.9 per changes described at:
  https://github.com/psycopg/psycopg/releases/tag/3.2.9

* Mon May 12 2025 Devrim Gündüz <devrim@gunduz.org> - 3.2.8-1PGDG
- Update to 3.2.8 per changes described at:
  https://github.com/psycopg/psycopg/releases/tag/3.2.8

* Mon May 5 2025 Devrim Gündüz <devrim@gunduz.org> - 3.2.7-1PGDG
- Update to 3.2.7 per changes described at:
  https://github.com/psycopg/psycopg/releases/tag/3.2.7

* Thu Mar 13 2025 Devrim Gündüz <devrim@gunduz.org> - 3.2.6-1PGDG
- Update to 3.2.6 per changes described at:
  https://github.com/psycopg/psycopg/releases/tag/3.2.6

* Mon Feb 24 2025 Devrim Gündüz <devrim@gunduz.org> - 3.2.5-1PGDG
- Update to 3.2.5 per changes described at:
  https://github.com/psycopg/psycopg/releases/tag/3.2.5

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
