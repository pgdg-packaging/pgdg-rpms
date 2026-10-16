# Built for the python3.13 alt-stack of Amazon Linux 2023 only, for
# the S3 storage backend of rohmu (pghoard).
# botocore needs it.
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif

%global	modname jmespath
%global	pymodname jmespath

Name:		python%{python3_pkgversion}-%{modname}
Version:	1.1.0
Release:	1PGDG%{?dist}
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
# python3-jmespath package of Amazon Linux 2023:
%{__rm} -f %{buildroot}%{_bindir}/jp.py

%files -f %{pyproject_files}
%doc README.rst

%changelog
* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for
  the S3 storage backend of rohmu (pghoard) on Amazon Linux 2023.
