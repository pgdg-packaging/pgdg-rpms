# Built for the python3.13 alt-stack of Amazon Linux 2023 only, for
# the SFTP storage backend of rohmu (pghoard).
# 1.5.0 is the newest release that works with the cffi 1.17 of Amazon
# Linux 2023 (1.6 needs cffi >= 2.0).
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif

%global	modname pynacl
%global	pymodname PyNaCl

Name:		python%{python3_pkgversion}-%{modname}
Version:	1.5.0
Release:	1PGDG%{?dist}
Summary:	Python binding to the Networking and Cryptography (NaCl) library

License:	Apache-2.0
URL:		https://github.com/pyca/pynacl
Source0:	https://files.pythonhosted.org/packages/source/P/PyNaCl/%{pymodname}-%{version}.tar.gz

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel
BuildRequires:	gcc
BuildRequires:	libsodium-devel
BuildRequires:	python%{python3_pkgversion}-cffi

%description
PyNaCl is a Python binding to libsodium, a fork of the Networking and
Cryptography library.

%prep
%autosetup -n %{pymodname}-%{version}
# Use the system libsodium, not the bundled copy:
%{__rm} -rf src/libsodium

%build
export SODIUM_INSTALL=system
%pyproject_wheel

%install
export SODIUM_INSTALL=system
%pyproject_install
%pyproject_save_files -l nacl

%files -f %{pyproject_files}
%doc README.rst

%changelog
* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 1.5.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for
  the SFTP storage backend of rohmu (pghoard) on Amazon Linux 2023.
