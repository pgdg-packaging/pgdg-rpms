%global sname PyMySQL
%global pname pymysql

%if 0%{?suse_version} == 1500
%global	__python3 %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

%global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

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
%{python3_sitelib}/%{sname}-%{version}.dist-info/*
%{python3_sitelib}/%{pname}/*.py
%{python3_sitelib}/%{pname}/constants/*.py
%{python3_sitelib}/%{pname}/__pycache__/*pyc
%{python3_sitelib}/%{pname}/constants/__pycache__/*.py*

%changelog
* Sat Mar 28 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support
  pg_chameleon on SLES-15
