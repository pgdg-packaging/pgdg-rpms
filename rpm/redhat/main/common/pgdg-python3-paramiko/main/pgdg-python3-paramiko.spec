%pgdg_python3_setup

# Built for the python3.13 alt-stack of Amazon Linux 2023, for the SFTP
# storage backend of rohmu (pghoard), and for RHEL 10 (the OS Python there),
# for sshtunnel.

%global	modname paramiko
%global	pymodname paramiko

Name:		python%{python3_pkgversion}-%{modname}
Version:	5.0.0
Release:	44PGDG%{?dist}
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

%if 0%{?rhel} == 10
# EPEL's python-paramiko-doc requires EPEL's own paramiko version, so it
# made dnf upgrade fail. We do not build the documentation:
Obsoletes:	python-paramiko-doc < %{version}-%{release}
%endif

%if 0%{?rhel} == 10
# %%pgdg_python3_setup renamed python3-paramiko to python%%{python3_pkgversion}-paramiko:
Provides:	python3-%{modname} = %{version}-%{release}
Obsoletes:	python3-%{modname} < %{version}-%{release}
%endif

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
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 5.0.0-44PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462
- On RHEL 10, the package is now python3.12-paramiko, which provides
  and obsoletes python3-paramiko.

* Mon Oct 26 2026 Devrim Gunduz <devrim@gunduz.org> - 5.0.0-43PGDG
- RHEL 10: Obsolete EPEL's python-paramiko-doc, which requires EPEL's own
  paramiko version, so it made dnf upgrade fail. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 5.0.0-42PGDG
- Add RHEL 10 support, without EPEL. Start the release from 42, so that our
  packages win over EPEL's. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 5.0.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for
  the SFTP storage backend of rohmu (pghoard) on Amazon Linux 2023.
