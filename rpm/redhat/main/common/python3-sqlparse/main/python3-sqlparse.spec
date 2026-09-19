%global sname sqlparse

Name:		python3-%{sname}
Version:	0.5.5
Release:	1PGDG%{?dist}
Summary:	Non-validating SQL parser module for Python

License:	BSD-3-Clause
URL:		https://github.com/andialbrecht/%{sname}
Source0:	https://files.pythonhosted.org/packages/source/s/%{sname}/%{sname}-%{version}.tar.gz
BuildArch:	noarch

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python3-devel python3-hatchling python3-pip python3-wheel

%description
sqlparse is a non-validating SQL parser module for Python. It provides
support for parsing, splitting and formatting SQL statements.

%prep
%autosetup -n %{sname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc AUTHORS CHANGELOG README.rst
%{_bindir}/sqlformat
%{python3_sitelib}/%{sname}/
%{python3_sitelib}/%{sname}-%{version}.dist-info/

%changelog
* Sat Sep 19 2026 Devrim Gündüz <devrim@gunduz.org> - 0.5.5-1PGDG
- Add back to the repository, to satisfy the pgcli dependency on
  platforms where the OS does not ship it (e.g. RHEL 10).
