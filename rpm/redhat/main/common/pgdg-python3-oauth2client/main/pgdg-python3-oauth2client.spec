# Built for the python3.13 alt-stack of Amazon Linux 2023 only, for
# the Google Cloud storage backend of rohmu (pghoard).
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif

%global	modname oauth2client
%global	pymodname oauth2client

Name:		python%{python3_pkgversion}-%{modname}
Version:	4.1.3
Release:	1PGDG%{?dist}
Summary:	OAuth 2.0 client library

License:	Apache-2.0
URL:		https://github.com/googleapis/oauth2client
Source0:	https://files.pythonhosted.org/packages/source/o/oauth2client/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

%description
oauth2client is a client library for OAuth 2.0. It is deprecated
upstream, but rohmu still uses it.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l oauth2client

%files -f %{pyproject_files}
%doc README.md

%changelog
* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 4.1.3-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for
  the Google Cloud storage backend of rohmu (pghoard) on Amazon Linux 2023.
