# Built for the python3.13 alt-stack of Amazon Linux 2023 only, for
# the SFTP storage backend of rohmu (pghoard).
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif

%global	modname paramiko
%global	pymodname paramiko

Name:		python%{python3_pkgversion}-%{modname}
Version:	5.0.0
Release:	1PGDG%{?dist}
Summary:	SSH2 protocol library

License:	LGPL-2.1-or-later
URL:		https://www.paramiko.org
Source0:	https://files.pythonhosted.org/packages/source/p/paramiko/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

%description
Paramiko is a pure-Python implementation of the SSHv2 protocol,
providing both client and server functionality.

%prep
%autosetup -n %{pymodname}-%{version}
# PEP 639 license strings need setuptools >= 77, Amazon Linux 2023 has 69:
%{__sed} -i -e 's/^license = "\(.*\)"$/license = { text = "\1" }/' -e '/^license-files = /d' pyproject.toml

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l paramiko

%files -f %{pyproject_files}
%doc README.rst

%changelog
* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 5.0.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for
  the SFTP storage backend of rohmu (pghoard) on Amazon Linux 2023.
