%pgdg_python3_setup

%global sname tornado

# For RHEL 8 and 9 only: RHEL 10 ships tornado, but RHEL 8 (and EPEL 8) and
# RHEL 9 only have it for the default python3 (3.6 and 3.9), and our Python
# packages use Python 3.12 there.

Name:		python%{python3_pkgversion}-%{sname}
Version:	6.6
Release:	2PGDG%{?dist}
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
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 6.6-2PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462
- Build on RHEL 9 too, for powa-web, which now runs with Python 3.12 there.

* Fri Oct 23 2026 Devrim Gunduz <devrim@gunduz.org> - 6.6-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for Python 3.12 on
  RHEL 8, where powa-web needs it. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
