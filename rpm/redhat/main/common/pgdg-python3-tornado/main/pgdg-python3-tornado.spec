%global sname tornado

# For RHEL 8 only: RHEL 9 and 10 ship tornado, but RHEL 8 (and EPEL 8) only
# have it for the default python3 (3.6), and our Python packages use Python
# 3.12 there.
%if 0%{?rhel} == 8
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif

Name:		python%{python3_pkgversion}-%{sname}
Version:	6.6
Release:	1PGDG%{?dist}
Summary:	Scalable, non-blocking web server and tools

License:	Apache-2.0
URL:		https://www.tornadoweb.org
Source0:	https://files.pythonhosted.org/packages/source/t/%{sname}/%{sname}-%{version}.tar.gz

BuildRequires:	gcc
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel
BuildRequires:	pyproject-rpm-macros

# The python3.12 packages of RHEL 8 get no automatic python3.12dist()
# provides:
Provides:	python%{python3_pkgversion}dist(%{sname}) = %{version}

%description
Tornado is an open source version of the scalable, non-blocking web
server and tools.

The framework is distinct from most mainstream web server frameworks
(and certainly most Python frameworks) because it is non-blocking and
reasonably fast. Because it is non-blocking and uses epoll, it can
handle thousands of simultaneous standing connections, which means it is
ideal for real-time web services.

%prep
%setup -q -n %{sname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.rst
%{python3_sitearch}/%{sname}/
%{python3_sitearch}/%{sname}-%{version}.dist-info/

%changelog
* Fri Oct 23 2026 Devrim Gunduz <devrim@gunduz.org> - 6.6-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for Python 3.12 on
  RHEL 8, where powa-web needs it. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
