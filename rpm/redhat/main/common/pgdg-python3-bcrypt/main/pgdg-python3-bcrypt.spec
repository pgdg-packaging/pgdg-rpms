# Built for the python3.13 alt-stack of Amazon Linux 2023 only, for
# the SFTP storage backend of rohmu (pghoard).
# 3.2.2 is the last release without Rust; paramiko needs >= 3.2.
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif

%global	modname bcrypt
%global	pymodname bcrypt

Name:		python%{python3_pkgversion}-%{modname}
Version:	3.2.2
Release:	1PGDG%{?dist}
Summary:	Modern password hashing for your software and your servers

License:	Apache-2.0
URL:		https://github.com/pyca/bcrypt
Source0:	https://files.pythonhosted.org/packages/source/b/bcrypt/%{pymodname}-%{version}.tar.gz

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel
BuildRequires:	gcc
BuildRequires:	python%{python3_pkgversion}-cffi

%description
Good password hashing for your software and your servers.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l bcrypt

%files -f %{pyproject_files}
%doc README.rst

%changelog
* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 3.2.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for
  the SFTP storage backend of rohmu (pghoard) on Amazon Linux 2023.
