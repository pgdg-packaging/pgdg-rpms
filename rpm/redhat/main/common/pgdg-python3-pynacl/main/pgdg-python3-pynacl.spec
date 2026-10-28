%pgdg_python3_setup

# Built for the python3.13 alt-stack of Amazon Linux 2023, for the SFTP
# storage backend of rohmu (pghoard), and for RHEL 10, for paramiko.
# 1.5.0 is the newest release that works with the cffi 1.17 of Amazon
# Linux 2023 and the cffi 1.16 of RHEL 10 (1.6 needs cffi >= 2.0).

%global	modname pynacl
%global	pymodname PyNaCl

Name:		python%{python3_pkgversion}-%{modname}
Version:	1.5.0
Release:	43PGDG%{?dist}
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
# On RHEL, libsodium comes from pgdg-libsodium (EPEL is not needed), which
# is found through the rpath:
%if 0%{?rhel}
BuildRequires:	pgdg-srpm-macros >= 2.3.0 pgdg-libsodium-devel
Requires:	pgdg-libsodium%{?_isa}
%global __requires_exclude ^libsodium\\.so
%else
BuildRequires:	libsodium-devel
%endif
BuildRequires:	python%{python3_pkgversion}-cffi

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-pynacl < %{version}-%{release}
%endif

%description
PyNaCl is a Python binding to libsodium, a fork of the Networking and
Cryptography library.

%prep
%autosetup -n %{pymodname}-%{version}
# Use the system libsodium, not the bundled copy:
%{__rm} -rf src/libsodium

%build
export SODIUM_INSTALL=system
%if 0%{?rhel}
export CFLAGS="%{build_cflags} -I%{pgdg_libsodiuminstdir}/include"
export LDFLAGS="%{build_ldflags} -L%{pgdg_libsodiuminstdir}/lib64 -Wl,-rpath,%{pgdg_libsodiuminstdir}/lib64"
%endif
%pyproject_wheel

%install
export SODIUM_INSTALL=system
%pyproject_install
%pyproject_save_files -l nacl

%files -f %{pyproject_files}
%doc README.rst

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 1.5.0-43PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 1.5.0-42PGDG
- Add RHEL 10 support, for paramiko without EPEL: build against
  pgdg-libsodium, found through the rpath.
- RHEL 10: Obsolete the EPEL python3-pynacl package. Start the release from
  42, so that our packages win over EPEL's. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 1.5.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for
  the SFTP storage backend of rohmu (pghoard) on Amazon Linux 2023.
