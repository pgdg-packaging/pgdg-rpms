%pgdg_python3_setup

# Built for the python3.13 alt-stack of Amazon Linux 2023, for the SFTP
# storage backend of rohmu (pghoard), and for RHEL 10 (the OS Python there).
# paramiko needs it.

%global	modname invoke
%global	pymodname invoke

Name:		python%{python3_pkgversion}-%{modname}
Version:	3.0.3
Release:	43PGDG%{?dist}
Summary:	Pythonic task execution

License:	BSD-2-Clause
URL:		https://www.pyinvoke.org
Source0:	https://files.pythonhosted.org/packages/source/i/invoke/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

%if 0%{?rhel} == 10
# %%pgdg_python3_setup renamed python3-invoke to python%%{python3_pkgversion}-invoke:
Provides:	python3-%{modname} = %{version}-%{release}
Obsoletes:	python3-%{modname} < %{version}-%{release}
%endif

%description
Invoke is a Python task execution tool and library. paramiko uses it.

%prep
%autosetup -n %{pymodname}-%{version}
# PEP 639 license strings need setuptools >= 77, Amazon Linux 2023 has 69:
%{__sed} -i -e 's/^license = "\(.*\)"$/license = { text = "\1" }/' -e '/^license-files = /d' pyproject.toml

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l invoke
# Only the library is needed (by paramiko); do not ship the invoke and
# inv commands:
%{__rm} -f %{buildroot}%{_bindir}/invoke %{buildroot}%{_bindir}/inv

%files -f %{pyproject_files}
%doc README.rst

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 3.0.3-43PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462
- On RHEL 10, the package is now python3.12-invoke, which provides
  and obsoletes python3-invoke.

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 3.0.3-42PGDG
- Add RHEL 10 support, without EPEL. Start the release from 42, so that our
  packages win over EPEL's. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 3.0.3-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for
  the SFTP storage backend of rohmu (pghoard) on Amazon Linux 2023.
