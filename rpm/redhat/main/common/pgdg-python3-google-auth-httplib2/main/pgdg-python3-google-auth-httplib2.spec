# Built for the python3.13 alt-stack of Amazon Linux 2023 only, for
# the Google Cloud storage backend of rohmu (pghoard).
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif

%global	modname google-auth-httplib2
%global	pymodname google_auth_httplib2

Name:		python%{python3_pkgversion}-%{modname}
Version:	0.4.4
Release:	1PGDG%{?dist}
Summary:	Google Authentication Library: httplib2 transport

License:	Apache-2.0
URL:		https://github.com/googleapis/google-cloud-python/tree/main/packages/google-auth-httplib2
Source0:	https://files.pythonhosted.org/packages/source/g/google-auth-httplib2/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

%description
This library provides an httplib2 transport for google-auth.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l google_auth_httplib2

%files -f %{pyproject_files}
%doc README.rst

%changelog
* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 0.4.4-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for
  the Google Cloud storage backend of rohmu (pghoard) on Amazon Linux 2023.
