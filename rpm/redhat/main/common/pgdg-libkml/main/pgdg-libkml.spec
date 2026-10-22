%global		sname libkml
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		libkmlinstdir %{pgdg_libkmlinstdir}

# The libraries are found through the rpath only (there is no ld.so.conf.d
# file), so they must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL libraries. Consumers require
# pgdg-libkml by name instead:
%global		__provides_exclude_from ^%{libkmlinstdir}/
%global		__requires_exclude ^lib(kml[a-z]*|minizip|uriparser)\\.so

# As in the Fedora package:
%global		_smp_mflags -j1

%if 0%{?rhel} == 8
%undefine __cmake_in_source_build
%endif

Name:		pgdg-%{sname}
Version:	1.3.0
Release:	1PGDG%{?dist}
Summary:	Reference implementation of OGC KML 2.2
License:	BSD-3-Clause
URL:		https://github.com/libkml/libkml
Source0:	https://github.com/libkml/libkml/archive/%{version}/%{sname}-%{version}.tar.gz
# From the Fedora package:
Patch0:		0001-Fix-build-failure-due-to-failure-to-convert-pointer-.patch
Patch1:		0002-Fix-mistaken-use-of-std-cerr-instead-of-std-endl.patch
Patch2:		libkml_crypth.patch
Patch3:		libkml_cmakever.patch
Patch4:		libkml_boost.patch

BuildRequires:	pgdg-srpm-macros >= 2.1.0
BuildRequires:	cmake gcc-c++ make
%if 0%{?suse_version} >= 1500
BuildRequires:	cmake-full
%else
BuildRequires:	cmake-rpm-macros
%endif
BuildRequires:	boost-devel curl-devel expat-devel zlib-devel
BuildRequires:	pgdg-minizip-ng-devel pgdg-uriparser-devel
Requires:	pgdg-minizip-ng%{?_isa} pgdg-uriparser%{?_isa}

%description
Reference implementation of OGC KML 2.2.
It also includes implementations of Google's gx: extensions used by Google
Earth, as well as several utility libraries for working with other formats.

This package installs libkml under %{libkmlinstdir}, for the packages in
the PostgreSQL RPM repository.

%package devel
Summary:	Development files for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	boost-devel expat-devel
Requires:	pgdg-minizip-ng-devel%{?_isa} pgdg-uriparser-devel%{?_isa}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{sname}.

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1
%patch -P 3 -p1
%patch -P 4 -p1

%build
%cmake \
	-DCMAKE_INSTALL_PREFIX:PATH=%{libkmlinstdir} \
	-DCMAKE_INSTALL_DIR:PATH=%{libkmlinstdir}/lib64/cmake/%{sname} \
	-DINCLUDE_INSTALL_DIR:PATH=%{libkmlinstdir}/include/kml \
	-DLIB_INSTALL_DIR:PATH=%{libkmlinstdir}/lib64 \
	-DCMAKE_INSTALL_RPATH:STRING="%{libkmlinstdir}/lib64;%{pgdg_minizipnginstdir}/lib64;%{pgdg_uriparserinstdir}/lib64" \
	-DMINIZIP_INCLUDE_DIR:PATH=%{pgdg_minizipnginstdir}/include \
	-DMINIZIP_LIBRARY:FILEPATH=%{pgdg_minizipnginstdir}/lib64/libminizip.so \
	-DURIPARSER_INCLUDE_DIR:PATH=%{pgdg_uriparserinstdir}/include \
	-DURIPARSER_LIBRARY:FILEPATH=%{pgdg_uriparserinstdir}/lib64/liburiparser.so \
	-DWITH_SWIG:BOOL=OFF -DWITH_PYTHON:BOOL=OFF -DWITH_JAVA:BOOL=OFF \
	-DBUILD_TESTING:BOOL=OFF -DBUILD_EXAMPLES:BOOL=OFF
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc AUTHORS README.md
%dir %{libkmlinstdir}
%dir %{libkmlinstdir}/lib64
%{libkmlinstdir}/lib64/libkml*.so.*

%files devel
%{libkmlinstdir}/include/
%{libkmlinstdir}/lib64/libkml*.so
%{libkmlinstdir}/lib64/cmake/
%{libkmlinstdir}/lib64/pkgconfig/

%changelog
* Wed Oct 21 2026 Devrim Gunduz <devrim@gunduz.org> - 1.3.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-libkml, so that the GIS stack does not need the EPEL libkml
  package on RHEL. Built against our pgdg-minizip-ng and pgdg-uriparser
  packages, instead of the bundled minizip of the Fedora package. Based on
  the Fedora spec file. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422
