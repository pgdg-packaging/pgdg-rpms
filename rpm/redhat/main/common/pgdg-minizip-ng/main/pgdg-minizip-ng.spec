%global		sname minizip-ng
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		minizipnginstdir %{pgdg_minizipnginstdir}

# The library is found through the rpath only (there is no ld.so.conf.d
# file), so it must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL minizip. Consumers require
# pgdg-minizip-ng by name instead:
%global		__provides_exclude_from ^%{minizipnginstdir}/
%global		__requires_exclude ^libminizip.*\\.so

%if 0%{?rhel} == 8
%undefine __cmake_in_source_build
%endif

Name:		pgdg-%{sname}
Version:	4.2.2
Release:	1PGDG%{?dist}
Summary:	Zip manipulation library, with the minizip compatible API
License:	Zlib
URL:		https://github.com/nmoinvaz/%{sname}
Source0:	https://github.com/nmoinvaz/%{sname}/archive/%{version}/%{sname}-%{version}.tar.gz
# PPMd support: minizip-ng uses the PPMd code of 7-Zip, which it otherwise
# fetches with git during the build:
%global		ppmdversion 26.00
Source1:	https://github.com/ip7z/7zip/archive/%{ppmdversion}/7zip-%{ppmdversion}.tar.gz
# From the Fedora package:
Patch0:		minizip-ng-openssl_no_engine.patch

BuildRequires:	pgdg-srpm-macros >= 2.1.0
BuildRequires:	cmake gcc-c++
%if 0%{?suse_version} >= 1500
BuildRequires:	cmake-full
%else
BuildRequires:	cmake-rpm-macros
%endif
BuildRequires:	bzip2-devel libzstd-devel openssl-devel xz-devel zlib-devel
Provides:	bundled(7zip-ppmd) = %{ppmdversion}

%description
minizip-ng is a zip manipulation library written in C, with AES encryption,
I/O buffering, PKWARE disk splitting and support for the BZIP2, LZMA, XZ
and ZSTD compression methods.

This package is built with the compatibility layer, so it provides the
API of the classic minizip library (unzip.h, zip.h), and installs under
%{minizipnginstdir}, for the packages in the PostgreSQL RPM repository.

%package devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	zlib-devel

%description devel
Development files for %{name}, with the minizip compatible API.

%prep
%setup -q -n %{sname}-%{version} -a 1
%patch -P 0 -p1

%build
# RHEL does not ship libbsd: minizip-ng uses OpenSSL for random numbers then.
%cmake \
	-DCMAKE_INSTALL_PREFIX:PATH=%{minizipnginstdir} \
	-DCMAKE_INSTALL_LIBDIR:PATH=lib64 \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=include \
	-DCMAKE_INSTALL_RPATH:PATH=%{minizipnginstdir}/lib64 \
	-DMZ_COMPAT:BOOL=ON \
	-DMZ_LIBBSD:BOOL=OFF \
	-DMZ_FETCH_LIBS:BOOL=OFF \
	-DMZ_FORCE_FETCH_LIBS:BOOL=OFF \
	-DFETCHCONTENT_SOURCE_DIR_PPMD:PATH=$PWD/7zip-%{ppmdversion} \
	-DFETCHCONTENT_FULLY_DISCONNECTED:BOOL=ON \
	-DMZ_BUILD_TESTS:BOOL=OFF \
	-DSKIP_INSTALL_BINARIES:BOOL=ON
%cmake_build

%install
%cmake_install

%files
%license LICENSE 7zip-%{ppmdversion}/DOC/License.txt
%doc README.md
%dir %{minizipnginstdir}
%dir %{minizipnginstdir}/lib64
%{minizipnginstdir}/lib64/libminizip.so.*

%files devel
%{minizipnginstdir}/include/
%{minizipnginstdir}/lib64/libminizip.so
# The bundled PPMd, linked into libminizip:
%{minizipnginstdir}/lib64/libppmd.a
%{minizipnginstdir}/lib64/pkgconfig/
%{minizipnginstdir}/lib64/cmake/

%changelog
* Wed Oct 21 2026 Devrim Gunduz <devrim@gunduz.org> - 4.2.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-minizip-ng, so that the GIS stack does not need the EPEL
  minizip packages on RHEL. Built with the minizip compatible API only.
  Based on the Fedora spec file. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
