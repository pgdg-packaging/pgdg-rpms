%pgdg_python3_setup

# Built for the python3.13 alt-stack of Amazon Linux 2023, for the S3
# storage backend of rohmu (pghoard), and for the python3.12 stack of
# RHEL 8 and 9, where the OS package is built for the default Python.
# botocore needs it.

%global	modname jmespath
%global	pymodname jmespath

Name:		python%{python3_pkgversion}-%{modname}
Version:	1.1.0
Release:	3PGDG%{?dist}
Summary:	JSON Matching Expressions

License:	MIT
URL:		https://github.com/jmespath/jmespath.py
Source0:	https://files.pythonhosted.org/packages/source/j/jmespath/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

%description
JMESPath allows you to declaratively specify how to extract elements
from a JSON document.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l jmespath
# Do not ship the jp.py example script, it would conflict with the
# python3-jmespath package of the OS:
%{__rm} -f %{buildroot}%{_bindir}/jp.py

%files -f %{pyproject_files}
%doc README.rst

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1.0-3PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Tue Oct 20 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1.0-2PGDG
- Build for the python3.12 stack on RHEL 9 and 8, too. botocore needs it.

* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for
  the S3 storage backend of rohmu (pghoard) on Amazon Linux 2023.
