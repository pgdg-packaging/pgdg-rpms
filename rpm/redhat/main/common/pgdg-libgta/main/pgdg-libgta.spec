%global		sname libgta
%global		so_version 1
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		libgtainstdir %{pgdg_libgtainstdir}

# The library is found through the rpath only (there is no ld.so.conf.d
# file), so it must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL libgta. Consumers require
# pgdg-libgta by name instead:
%global		__provides_exclude_from ^%{libgtainstdir}/
%global		__requires_exclude ^libgta\\.so

%{!?runselftest:%global runselftest 0}

%if 0%{?rhel} == 8
%undefine __cmake_in_source_build
%endif

Name:		pgdg-%{sname}
Version:	1.2.1
Release:	1PGDG%{?dist}
Summary:	Library that implements the Generic Tagged Arrays file format
License:	LGPL-2.1-or-later
URL:		https://marlam.de/gta/
Source0:	https://marlam.de/gta/releases/%{sname}-%{version}.tar.xz

BuildRequires:	pgdg-srpm-macros >= 2.1.0
BuildRequires:	cmake gcc
%if 0%{?suse_version} >= 1500
BuildRequires:	cmake-full
%else
BuildRequires:	cmake-rpm-macros
%endif

%description
Libgta is a portable library that implements the GTA (Generic Tagged Arrays)
file format. It provides interfaces for C and C++.

This package installs libgta under %{libgtainstdir}, for the packages in
the PostgreSQL RPM repository.

%package devel
Summary:	Development Libraries for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{sname}.

%prep
%setup -q -n %{sname}-%{version}

%build
%cmake \
	-DCMAKE_INSTALL_PREFIX:PATH=%{libgtainstdir} \
	-DCMAKE_INSTALL_LIBDIR:PATH=lib64 \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=include \
	-DCMAKE_INSTALL_RPATH:PATH=%{libgtainstdir}/lib64 \
	-DGTA_BUILD_STATIC_LIB:BOOL=FALSE \
	-DGTA_BUILD_DOCUMENTATION:BOOL=FALSE
%cmake_build

%install
%cmake_install
%{__rm} -rf %{buildroot}%{libgtainstdir}/share/doc

%check
%if %runselftest
%ctest
%endif

%files
%doc COPYING AUTHORS README
%dir %{libgtainstdir}
%dir %{libgtainstdir}/lib64
%{libgtainstdir}/lib64/%{sname}.so.%{so_version}
%{libgtainstdir}/lib64/%{sname}.so.%{so_version}.*

%files devel
%doc doc/example*
%{libgtainstdir}/lib64/cmake/
%{libgtainstdir}/lib64/pkgconfig/
%{libgtainstdir}/include/
%{libgtainstdir}/lib64/%{sname}.so

%changelog
* Wed Oct 21 2026 Devrim Gunduz <devrim@gunduz.org> - 1.2.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-libgta, so that the GIS stack does not need the EPEL libgta
  package on RHEL. Based on the Fedora spec file. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
