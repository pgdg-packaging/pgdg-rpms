%global sname consul

%if 0%{?fedora} && 0%{?fedora} == 43
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?fedora} && 0%{?fedora} <= 42
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?suse_version} == 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

%{expand: %%global pyver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:4])"`)}

Name:		python3-%{sname}
Version:	1.1.0
Release:	4PGDG%{?dist}
Summary:	Python client for Consul

License:	MIT
URL:		https://pypi.org/project/python-%{sname}/
Source0:	https://files.pythonhosted.org/packages/7f/06/c12ff73cb1059c453603ba5378521e079c3f0ab0f0660c410627daca64b7/python-%{sname}-%{version}.tar.gz

BuildArch:	noarch

Requires:	less python3
BuildRequires:	python3-six >= 1.4 python3-requests >= 2.0
BuildRequires:	python3-devel
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif

%description
Python client for Consul (http://www.consul.io/)

%prep
%setup -q -n python-%{sname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.rst
%{python3_sitelib}/consul/__pycache__/*
%{python3_sitelib}/consul/*.py
%{python3_sitelib}/python_%{sname}-%{version}.dist-info/*

%changelog
* Sat Nov 8 2025 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-4PGDG
- Add SLES 16 support
- Switch to pyproject build

* Tue Dec 17 2024 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-3PGDG
- Add RHEL 10 support
- Add PGDG branding
- Remove RHEL 7 support

* Mon Feb 28 2022 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-2
- Fix for Python 3.10

* Wed Aug 5 2020 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1
- Initial packaging for PostgreSQL RPM repository, to satisfy
patroni dependency.
