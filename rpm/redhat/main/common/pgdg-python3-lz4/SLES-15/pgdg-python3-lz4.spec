%global srcname lz4

%if 0%{?fedora} && 0%{?fedora} >= 41
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?suse_version} >= 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif

%{expand: %%global pybasever %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}

Name:		python%{python3_pkgversion}-%{srcname}
Version:	4.3.3
Release:	42PGDG%{?dist}
URL:		https://github.com/python-%{srcname}/python-%{srcname}
Summary:	LZ4 Bindings for Python
# Automatically converted from old format: BSD - review is highly recommended.
License:	LicenseRef-Callaway-BSD
Source:		https://files.pythonhosted.org/packages/source/l/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRequires:	gcc lz4-devel
BuildRequires:	python%{python3_pkgversion}-devel

%description
Python 3 bindings for the lz4 compression library.

%prep
%setup -q -n %{srcname}-%{version}

#rm lz4libs/lz4*.[ch]

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --no-compile --root %{buildroot}

find %{buildroot}%{python3_sitearch} -name 'lz4*.so' \
	-exec chmod 0755 {} \;

%files
%license LICENSE
%doc README.rst
%{python3_sitearch}/%{srcname}-%{version}-py%{pybasever}.egg-info/*
%{python3_sitearch}/%{srcname}/*.py*
%{python3_sitearch}/%{srcname}/*.so
%{python3_sitearch}/%{srcname}/__pycache__/*.py*
%{python3_sitearch}/%{srcname}/block/*.py*
%{python3_sitearch}/%{srcname}/block/*.so
%{python3_sitearch}/%{srcname}/block/__pycache__/*.py*
%{python3_sitearch}/%{srcname}/frame/*.py*
%{python3_sitearch}/%{srcname}/frame/*.so
%{python3_sitearch}/%{srcname}/frame/__pycache__/*.py*

%changelog
* Tue May 27 2025 Devrim Gunduz <devrim@gunduz.org> - 4.3.3-42PGDG
- Initial packaging for the PostgreSQL RPM repository to support Barman
  on RHEL 9 and RHEL 8.
