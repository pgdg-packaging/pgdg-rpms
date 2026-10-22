%global		sname shapelib
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		shapelibinstdir %{pgdg_shapelibinstdir}

# The library is found through the rpath only (there is no ld.so.conf.d
# file), so it must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL shapelib. Consumers require
# pgdg-shapelib by name instead:
%global		__provides_exclude_from ^%{shapelibinstdir}/
%global		__requires_exclude ^libshp\\.so

%if 0%{?rhel} == 8
%undefine __cmake_in_source_build
%endif

Name:		pgdg-%{sname}
Version:	1.6.3
Release:	1PGDG%{?dist}
Summary:	C library for handling ESRI Shapefiles
License:	(LGPL-2.0-or-later OR MIT) AND GPL-2.0-or-later AND LicenseRef-Fedora-Public-Domain
URL:		http://shapelib.maptools.org/
Source0:	https://download.osgeo.org/%{sname}/%{sname}-%{version}.tar.gz

BuildRequires:	pgdg-srpm-macros >= 2.1.0
BuildRequires:	cmake gcc-c++
%if 0%{?suse_version} >= 1500
BuildRequires:	cmake-full
%else
BuildRequires:	cmake-rpm-macros
%endif

%description
The Shapefile C Library provides the ability to write
simple C programs for reading, writing and updating (to a
limited extent) ESRI Shapefiles, and the associated
attribute file (.dbf).

This package installs shapelib under %{shapelibinstdir}, for the packages
in the PostgreSQL RPM repository.

%package devel
Summary:	Development files for shapelib
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains libshp and the appropriate header files.

%package tools
Summary:	shapelib utility programs
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description tools
This package contains various utility programs distributed with shapelib.

%prep
%setup -q -n %{sname}-%{version}

%build
%cmake \
	-DCMAKE_INSTALL_PREFIX:PATH=%{shapelibinstdir} \
	-DCMAKE_INSTALL_LIBDIR:PATH=lib64 \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=include \
	-DCMAKE_INSTALL_CMAKEDIR:PATH=lib64/cmake/%{sname} \
	-DUSE_RPATH:BOOL=ON \
	-DBUILD_TESTING:BOOL=OFF
%cmake_build

%install
%cmake_install
%{__rm} -rf %{buildroot}%{shapelibinstdir}/share/doc

%files
%doc README README.tree ChangeLog web/*.html
%license LICENSE*
%dir %{shapelibinstdir}
%dir %{shapelibinstdir}/lib64
%{shapelibinstdir}/lib64/libshp.so.%{version}
%{shapelibinstdir}/lib64/libshp.so.4*

%files devel
%{shapelibinstdir}/include/
%{shapelibinstdir}/lib64/libshp.so
%{shapelibinstdir}/lib64/pkgconfig/
%{shapelibinstdir}/lib64/cmake/

%files tools
%doc contrib/doc/
%{shapelibinstdir}/bin/

%changelog
* Wed Oct 21 2026 Devrim Gunduz <devrim@gunduz.org> - 1.6.3-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-shapelib, so that the GIS stack does not need the EPEL
  shapelib package on RHEL. Based on the Fedora spec file. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
