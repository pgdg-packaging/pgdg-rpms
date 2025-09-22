%global sname psycopg2

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
%if 0%{?suse_version} >= 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif

%{expand: %%global pybasever %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%{expand: %%global pgdg_python3_sitearch %(echo `%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(2))"`)}

Summary:	A PostgreSQL database adapter for Python %{python3_pkgversion}
Name:		python%{python3_pkgversion}-%{sname}
Version:	2.9.10
Release:	1PGDG%{?dist}.1
# The exceptions allow linking to OpenSSL and PostgreSQL's libpq
License:	LGPLv3+ with exceptions
Url:		https://www.psycopg.org
Source0:	https://github.com/psycopg/psycopg2/archive/refs/tags/%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	python%{python3_pkgversion}-devel python%{python3_pkgversion}-setuptools

Requires:	libpq5 >= 10.0

%description
Psycopg is the most popular PostgreSQL adapter for the Python
programming language. At its core it fully implements the Python DB
API 2.0 specifications. Several extensions allow access to many of the
features offered by PostgreSQL.

%prep
%setup -q -n %{sname}-%{version}

%build

export PATH=%{pginstdir}/bin:$PATH
%{__ospython} setup.py build

%install
export PATH=%{pginstdir}/bin:$PATH
%{__ospython} setup.py install --no-compile --root %{buildroot}


%files
%defattr(-,root,root)
%doc AUTHORS LICENSE NEWS README.rst
%dir %{pgdg_python3_sitearch}/%{sname}
%{pgdg_python3_sitearch}/%{sname}/*.py
%if ! 0%{?suse_version}
%dir %{pgdg_python3_sitearch}/%{sname}/__pycache__
%{pgdg_python3_sitearch}/%{sname}/__pycache__/*.pyc
%endif
%{pgdg_python3_sitearch}/%{sname}-%{version}-py%{pybasever}.egg-info
%{pgdg_python3_sitearch}/%{sname}/_psycopg.cpython-3?*.so


%changelog
* Mon Sep 22 2025 Devrim Gunduz <devrim@gunduz.org> - 2.9.10-1PGDG.1
- Add Fedora 43 support

* Fri May 16 2025 Devrim Gündüz <devrim@gunduz.org> - 2.9.10-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support
  Patroni and Barman packages on RHEL 8 and 9.
