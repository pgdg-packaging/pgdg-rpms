%global sname PyMySQL
%global pname pymysql

%if 0%{?fedora} && 0%{?fedora} == 44
%global __ospython %{_bindir}/python3.15
%global python3_pkgversion 3.15
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

%{expand: %%global py3ver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Name:		python%{python3_pkgversion}-%{sname}
Version:	1.1.2
Release:	42PGDG%{?dist}
Summary:	Pure-Python MySQL client library

License:	MIT
URL:		https://github.com/%{sname}/%{sname}
Source:		https://github.com/%{sname}/%{sname}/archive/refs/tags/v%{version}.tar.gz

Provides:	python3-%{sname}

BuildArch:	noarch

%description
This package contains a pure-Python MySQL client library. The goal of PyMySQL is
to be a drop-in replacement for MySQLdb and work on CPython, PyPy, IronPython
and Jython.

%prep
%autosetup -n %{sname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%doc README.md
%license LICENSE
%{python3_sitelib}/%{pname}-%{version}.dist-info/*
%{python3_sitelib}/%{pname}/*.py
%{python3_sitelib}/%{pname}/constants/*.py
%if 0%{?fedora} >= 41 || 0%{?rhel} >= 9 || 0%{?suse_version} == 1600
%{python3_sitelib}/%{pname}/__pycache__/*pyc
%{python3_sitelib}/%{pname}/constants/__pycache__/*.py*
%endif

%changelog
* Sat Mar 28 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support
  pg_chameleon on SLES-15
