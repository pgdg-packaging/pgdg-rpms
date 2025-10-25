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

Name:		python3-snappy
Version:	0.6.1
Release:	42PGDG%{dist}
Summary:	Python library for the snappy compression library
License:	BSD-3-Clause
URL:		https://github.com/andrix/python-snappy
Source:		https://files.pythonhosted.org/packages/source/p/python-snappy/python-snappy-%{version}.tar.gz

BuildRequires:	gcc-c++ pkgconfig snappy-devel
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif

Provides:	python3-%{sname}%{?_isa} = %{version}-%{release}
Provides:	python%{python3_pkgversion}dist(%{name}) = %{version}-%{release}

%description
Python library for the snappy compression library from Google.

%prep
%setup -q -n python-snappy-%{version}
sed -i -e '/^#!\//, 1d' src/snappy/snappy.py

%build
%pyproject_wheel

%install
%pyproject_install

%files
%doc AUTHORS README.rst
%license LICENSE
%{python3_sitearch}/*

%changelog
* Sat Oct 25 2025 Devrim Gündüz <devrim@gunduz.org> - 0.6.1-42PGDG
- Add SLES 16 support
- Switch to pyproject build

* Tue Feb 20 2024 Devrim Gündüz <devrim@gunduz.org> - 0.6.1-3PGDG
- Initial packaging for the PostgreSQL RPM repository to support
  pghoard on SLES 15.
