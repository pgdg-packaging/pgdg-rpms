%global		sname libdeflate
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		libdeflateinstdir %{pgdg_libdeflateinstdir}

# The library is found through the rpath only (there is no ld.so.conf.d
# file), so it must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL libdeflate. Consumers
# require pgdg-libdeflate by name instead:
%global		__provides_exclude_from ^%{libdeflateinstdir}/
%global		__requires_exclude ^libdeflate\\.so

%{!?runselftest:%global runselftest 0}

%if 0%{?rhel} == 8
%undefine __cmake_in_source_build
# dwz on RHEL 8 fails on the hard linked libdeflate-gunzip:
%global _find_debuginfo_dwz_opts %{nil}
%endif

Name:		pgdg-%{sname}
Version:	1.26
Release:	1PGDG%{?dist}
Summary:	Fast implementation of DEFLATE, gzip, and zlib
License:	MIT
URL:		https://github.com/ebiggers/libdeflate
Source0:	%{url}/archive/v%{version}/%{sname}-%{version}.tar.gz

BuildRequires:	pgdg-srpm-macros >= 2.1.0
BuildRequires:	cmake gcc zlib-devel
%if 0%{?suse_version} >= 1500
BuildRequires:	cmake-full
%else
BuildRequires:	cmake-rpm-macros
%endif

%description
libdeflate is a library for fast, whole-buffer DEFLATE-based compression and
decompression, supporting DEFLATE, gzip, and zlib.

This package installs libdeflate under %{libdeflateinstdir}, for the
packages in the PostgreSQL RPM repository.

%package devel
Summary:	Development files for libdeflate
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for libdeflate.

%package utils
Summary:	Binaries from libdeflate
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description utils
Binaries from libdeflate.

%prep
%setup -q -n %{sname}-%{version}

%build
%cmake \
	-DCMAKE_INSTALL_PREFIX:PATH=%{libdeflateinstdir} \
	-DCMAKE_INSTALL_LIBDIR:PATH=lib64 \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=include \
	-DCMAKE_INSTALL_RPATH:PATH=%{libdeflateinstdir}/lib64 \
	-DLIBDEFLATE_BUILD_STATIC_LIB:BOOL=OFF \
	-DLIBDEFLATE_BUILD_SHARED_LIB:BOOL=ON \
	-DLIBDEFLATE_COMPRESSION_SUPPORT:BOOL=ON \
	-DLIBDEFLATE_DECOMPRESSION_SUPPORT:BOOL=ON \
	-DLIBDEFLATE_ZLIB_SUPPORT:BOOL=ON \
	-DLIBDEFLATE_GZIP_SUPPORT:BOOL=ON \
	-DLIBDEFLATE_FREESTANDING:BOOL=OFF \
	-DLIBDEFLATE_BUILD_GZIP:BOOL=ON \
	-DLIBDEFLATE_USE_SHARED_LIBS:BOOL=ON \
%if %runselftest
	-DLIBDEFLATE_BUILD_TESTS:BOOL=ON
%else
	-DLIBDEFLATE_BUILD_TESTS:BOOL=OFF
%endif
%cmake_build

%install
%cmake_install

%check
%if %runselftest
%ctest
%endif

%files
%doc NEWS.md README.md
%license COPYING
%dir %{libdeflateinstdir}
%dir %{libdeflateinstdir}/lib64
%{libdeflateinstdir}/lib64/libdeflate.so.0

%files devel
%{libdeflateinstdir}/include/
%{libdeflateinstdir}/lib64/libdeflate.so
%{libdeflateinstdir}/lib64/pkgconfig/
%{libdeflateinstdir}/lib64/cmake/

%files utils
%dir %{libdeflateinstdir}/bin
%{libdeflateinstdir}/bin/libdeflate-gzip
%{libdeflateinstdir}/bin/libdeflate-gunzip

%changelog
* Wed Oct 21 2026 Devrim Gunduz <devrim@gunduz.org> - 1.26-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-libdeflate, so that the GIS stack does not need the EPEL
  libdeflate package on RHEL. Based on the Fedora spec file. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
