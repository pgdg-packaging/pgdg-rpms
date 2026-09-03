%global modname requests

%if 0%{?fedora} && 0%{?fedora} == 45
%global __python3 %{_bindir}/python3.15
%global python3_pkgversion 3.15
%endif
%if 0%{?fedora} && 0%{?fedora} <= 43
%global __python3 %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__python3 %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?amzn} == 2023
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?suse_version} >= 1500
%global	__python3 %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif

Name:		python%{python3_pkgversion}-%{modname}
Version:	2.34.2
Release:	1PGDG%{?dist}
Summary:	HTTP library, written in Python, for human beings

License:	Apache-2.0
URL:		https://pypi.io/project/requests
Source0:	https://github.com/requests/requests/archive/v%{version}/requests-v%{version}.tar.gz

BuildRequires:	gcc python%{python3_pkgversion}-devel
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif

BuildArch:	noarch
Provides:	python%{python3_pkgversion}dist(%{modname})

%description
Most existing Python modules for sending HTTP requests are extremely verbose and
cumbersome. Python’s built-in urllib2 module provides most of the HTTP
capabilities you should need, but the API is thoroughly broken. This library is
designed to make HTTP requests easy for developers.

%prep
%autosetup -n requests-%{version}

%build
export HATCH_METADATA_CLASSIFIERS_NO_VERIFY=1
%pyproject_wheel

%install
%pyproject_install

%files
%{python3_sitelib}/%{modname}-%{version}.dist-info/
%{python3_sitelib}/%{modname}/*

%changelog
* Thu Sep 3 2026 Devrim Gunduz <devrim@gunduz.org> - 2.34.2-1PGDG
- Inıtial packaging for the PostgreSQL RPM repository to support Patroni
  on Amazon Linux 2023
