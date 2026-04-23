%global sname python-systemd

%if 0%{?fedora} && 0%{?fedora} == 44
%global __python3 %{_bindir}/python3.15
%global python3_pkgversion 3.15
%endif
%if 0%{?fedora} && 0%{?fedora} == 43
%global __python3 %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?fedora} && 0%{?fedora} <= 42
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__python3 %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?suse_version} == 1500
%global	__python3 %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

Name:		python%{python3_pkgversion}-systemd
Version:	235
Release:	42PGDG%{?dist}
Summary:	Python module wrapping libsystemd functionality

License:	LGPL-2.1-or-later
URL:		https://github.com/systemd/%{sname}
Source0:	https://github.com/systemd/%{sname}/archive/v%{version}.tar.gz#/%{sname}-%{version}.tar.gz

Patch0:		https://github.com/systemd/%{sname}/pull/140.patch

BuildRequires:	make gcc systemd-devel
BuildRequires:	python%{python3_pkgversion}-devel

Provides:	python3-%{sname}%{?_isa} = %{version}-%{release}
Provides:	python%{python3_pkgversion}dist(%{name}) = %{version}-%{release}

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif

%description
Python module for native access to the libsystemd facilities. Functionality
includes sending of structured messages to the journal and reading journal
files, querying machine and boot identifiers and a lists of message identifiers
provided by systemd. Other functionality provided the library is also wrapped

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p1
sed -i 's/py\.test/pytest/' Makefile

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE.txt
%doc README.md NEWS
%{python3_sitearch}/systemd/
%{python3_sitearch}/systemd_python-%{version}.dist-info

%changelog
* Thu Apr 23 2026 Devrim Gunduz <devrim@gunduz.org> - 235-42PGDG
- Initial packaging for the PostgreSQL RPM repository to support
  patroni.
