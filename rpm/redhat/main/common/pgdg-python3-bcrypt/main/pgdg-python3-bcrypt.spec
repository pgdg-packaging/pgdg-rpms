%pgdg_python3_setup

# Built for the python3.13 alt-stack of Amazon Linux 2023, for the SFTP
# storage backend of rohmu (pghoard), and for RHEL 10 (the OS Python there),
# for paramiko.
# 3.2.2 is the last release without Rust; paramiko needs >= 3.2.

%global	modname bcrypt
%global	pymodname bcrypt

Name:		python%{python3_pkgversion}-%{modname}
Version:	3.2.2
Release:	43PGDG%{?dist}
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

%if 0%{?rhel} == 10
# %%pgdg_python3_setup renamed python3-bcrypt to python%%{python3_pkgversion}-bcrypt:
Provides:	python3-%{modname} = %{version}-%{release}
Provides:	python3-%{modname}%{?_isa} = %{version}-%{release}
Obsoletes:	python3-%{modname} < %{version}-%{release}
%endif

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
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 3.2.2-43PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462
- On RHEL 10, the package is now python3.12-bcrypt, which provides
  and obsoletes python3-bcrypt.

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 3.2.2-42PGDG
- Add RHEL 10 support, without EPEL. Start the release from 42, so that our
  packages win over EPEL's. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 3.2.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for
  the SFTP storage backend of rohmu (pghoard) on Amazon Linux 2023.
