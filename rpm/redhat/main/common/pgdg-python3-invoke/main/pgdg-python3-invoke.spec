# Built for the python3.13 alt-stack of Amazon Linux 2023 only, for
# the SFTP storage backend of rohmu (pghoard).
# paramiko needs it.
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif

%global	modname invoke
%global	pymodname invoke

Name:		python%{python3_pkgversion}-%{modname}
Version:	3.0.3
Release:	1PGDG%{?dist}
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
* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 3.0.3-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for
  the SFTP storage backend of rohmu (pghoard) on Amazon Linux 2023.
