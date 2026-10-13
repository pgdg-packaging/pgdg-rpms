%global sname psycopg2
%global pname python39-%{sname}

%global __ospython %{_bindir}/python3.9

%{expand: %%global pybasever %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%{!?python39_sitearch: %global python39_sitearch %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(2))")}


Summary:	A PostgreSQL database adapter for Python 3.9
Name:		python39-%{sname}
Version:	2.9.6
Release:	1%{?dist}
# The exceptions allow linking to OpenSSL and PostgreSQL's libpq
License:	LGPLv3+ with exceptions
Url:		https://www.psycopg.org
Source0:	https://github.com/psycopg/psycopg2/archive/refs/tags/%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
BuildRequires:	python39-devel python39-setuptools

Requires:	libpq5 >= 10.0

%description
Psycopg is the most popular PostgreSQL adapter for the Python
programming language. At its core it fully implements the Python DB
API 2.0 specifications. Several extensions allow access to many of the
features offered by PostgreSQL.

%package -n python39-%{sname}-tests
Summary:	A testsuite for Python 3.9
Requires:	python39-%sname = %version-%release

%description -n python39-%{sname}-tests
This sub-package delivers set of tests for the adapter.

%prep
%setup -q -n %{sname}-%{version}

%build

export PATH=%{pginstdir}/bin:$PATH
%{__ospython} setup.py build

%install
export PATH=%{pginstdir}/bin:$PATH
%{__ospython} setup.py install --no-compile --root %{buildroot}

# Copy tests directory:
%{__mkdir} -p %{buildroot}%{python39_sitearch}/%{sname}/
%{__cp} -rp tests %{buildroot}%{python39_sitearch}/%{sname}/tests
# This test is skipped on 3.7 and has a syntax error so brp-python-bytecompile would choke on it
%{__rm} -f %{buildroot}%{python39_sitearch}/%{sname}/tests/test_async_keyword.py

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS LICENSE NEWS README.rst
%dir %{python39_sitearch}/%{sname}
%{python39_sitearch}/%{sname}/*.py
%if ! 0%{?suse_version}
%dir %{python39_sitearch}/%{sname}/__pycache__
%{python39_sitearch}/%{sname}/__pycache__/*.pyc
%endif
%{python39_sitearch}/%{sname}-%{version}-py%{pybasever}.egg-info
%{python39_sitearch}/%{sname}/_psycopg.cpython-3?*.so

%files -n python39-%{sname}-tests
%{python39_sitearch}/%{sname}/tests

%changelog
* Wed Apr 5 2023 Devrim Gündüz <devrim@gunduz.org> - 2.9.6-1
- Initial packaging for Python 3.9 to support pg_activity dependency
  on RHEL 8
