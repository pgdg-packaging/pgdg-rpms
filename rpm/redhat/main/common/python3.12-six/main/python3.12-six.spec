%if 0%{?fedora} <= 42
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.12
%endif
%if 0%{?suse_version} >= 1500
%global __python3 %{_bindir}/python3.12
%global	python3_pkgversion 312
%endif
%if 0%{?rhel} && 0%{?rhel} < 10
%global	__python3 %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif

%global python_wheelname six-%{version}-py2.py3-none-any.whl

Name:		python%{python3_pkgversion}-six
Version:	1.16.0
Release:	1PGDG%{?dist}
Summary:	Python 2 and 3 compatibility utilities

License:	MIT
URL:		https://github.com/benjaminp/six
Source0:	https://files.pythonhosted.org/packages/source/s/six/six-%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-rpm-macros
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-wheel

Obsoletes:	python3.12-six <= 1.16.0

%description
Six is a Python 2 and 3 compatibility library. It provides utility functions
for smoothing over the differences between the Python versions with the goal
of writing Python code that is compatible on both Python versions.}

%prep
%autosetup -p1 -n six-%{version}

%build
%py3_build_wheel

%install
%py3_install_wheel %{python_wheelname}

%files
%license LICENSE
%doc README.rst documentation/index.rst
%{python3_sitelib}/six-*.dist-info/
%pycached %{python3_sitelib}/six.py

%changelog
* Mon May 19 2025 Devrim Gunduz <devrim@gunduz.org> - 1.16.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support
  Barman on RHEL 9.
