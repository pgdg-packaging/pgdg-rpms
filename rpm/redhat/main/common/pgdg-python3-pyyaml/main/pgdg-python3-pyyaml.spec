%global modname PyYAML

%if 0%{?fedora} && 0%{?fedora} == 45
%global __python3 %{_bindir}/python3.15
%global python3_pkgversion 3.15
%endif
%if 0%{?fedora} && 0%{?fedora} <= 43
%global __python3 %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__python3 %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?amzn} == 2023
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?suse_version} >= 1500
%global	__python3 %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif

%{expand: %%global pybasever %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%{expand: %%global python3_sitearch %(echo `%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(2))"`)}

Name:		python%{python3_pkgversion}-%{modname}
Version:	6.0.3
Release:	1PGDG%{?dist}
Summary:	HTTP library with thread-safe connection pooling, file post, and more

License:	MIT
URL:		https://github.com/yaml/pyyaml
Source0:	https://github.com/yaml/pyyaml/archive/%{version}.tar.gz

BuildRequires:	gcc libyaml-devel python%{python3_pkgversion}-devel

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif

Provides:	python%{python3_pkgversion}pyyaml

%description
YAML is a data serialization format designed for human readability and\
interaction with scripting languages.  PyYAML is a YAML parser and\
emitter for Python.

PyYAML features a complete YAML 1.1 parser, Unicode support, pickle\
support, capable extension API, and sensible error messages.  PyYAML\
supports standard YAML tags and provides Python-specific tags that\
allow to represent an arbitrary Python object.

PyYAML is applicable for a broad range of tasks from complex\
configuration files to object serialization and persistence.

%prep
%autosetup -n pyyaml-%{version}

%build
export HATCH_METADATA_CLASSIFIERS_NO_VERIFY=1
%pyproject_wheel

%install
%pyproject_install

%files
%{python3_sitearch}/%{modname}-%{version}.dist-info/
%{python3_sitearch}/_yaml/*
%{python3_sitearch}/yaml/*

%changelog
* Thu Sep 3 2026 Devrim Gunduz <devrim@gunduz.org> - 6.0.3-1PGDG
- Inıtial packaging for the PostgreSQL RPM repository to support Patroni
  on Amazon Linux 2023
