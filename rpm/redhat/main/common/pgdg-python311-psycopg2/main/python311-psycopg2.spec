%global sname psycopg2
%global pname python311-%{sname}

%global __ospython %{_bindir}/python3.11

%{expand: %%global pybasever %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%{!?python311_sitearch: %global python311_sitearch %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(2))")}

Summary:	A PostgreSQL database adapter for Python 3.11
Name:		python311-%{sname}
Version:	2.9.9
Release:	1PGDG%{?dist}
# The exceptions allow linking to OpenSSL and PostgreSQL's libpq
License:	LGPLv3+ with exceptions
Url:		https://www.psycopg.org
Source0:	https://github.com/psycopg/psycopg2/archive/refs/tags/%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	python311-devel python311-setuptools

Requires:	libpq5 >= 10.0

%description
Psycopg is the most popular PostgreSQL adapter for the Python
programming language. At its core it fully implements the Python DB
API 2.0 specifications. Several extensions allow access to many of the
features offered by PostgreSQL.

%package -n python311-%{sname}-tests
Summary:	A testsuite for Python 3.11
Requires:	python311-%sname = %version-%release

%description -n python311-%{sname}-tests
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
%{__mkdir} -p %{buildroot}%{python311_sitearch}/%{sname}/
%{__cp} -rp tests %{buildroot}%{python311_sitearch}/%{sname}/tests
# This test is skipped on 3.7 and has a syntax error so brp-python-bytecompile would choke on it
%{__rm} -f %{buildroot}%{python311_sitearch}/%{sname}/tests/test_async_keyword.py

%files
%defattr(-,root,root)
%doc AUTHORS LICENSE NEWS README.rst
%dir %{python311_sitearch}/%{sname}
%{python311_sitearch}/%{sname}/*.py
%if ! 0%{?suse_version}
%dir %{python311_sitearch}/%{sname}/__pycache__
%{python311_sitearch}/%{sname}/__pycache__/*.pyc
%endif
%{python311_sitearch}/%{sname}-%{version}-py%{pybasever}.egg-info
%{python311_sitearch}/%{sname}/_psycopg.cpython-3?*.so

%files -n python311-%{sname}-tests
%{python311_sitearch}/%{sname}/tests

%changelog
* Mon Feb 19 2024 Devrim Gündüz <devrim@gunduz.org> - 2.9.9-1PGDG
- Initial packaging for Python 3.11 to support pg_activity dependencies
  on SLES 15.
