%global		sname blosc
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		bloscinstdir %{pgdg_bloscinstdir}

# The library is found through the rpath only (there is no ld.so.conf.d
# file), so it must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL blosc. Consumers require
# pgdg-blosc by name instead:
%global		__provides_exclude_from ^%{bloscinstdir}/
%global		__requires_exclude ^libblosc\\.so

%{!?runselftest:%global runselftest 0}

%if 0%{?rhel} == 8
%undefine __cmake_in_source_build
%endif

Name:		pgdg-%{sname}
Version:	1.21.6
Release:	1PGDG%{?dist}
Summary:	High performance compressor optimized for binary data
License:	BSD-3-Clause
URL:		https://github.com/Blosc/c-blosc
Source0:	https://github.com/Blosc/c-blosc/archive/v%{version}/%{sname}-%{version}.tar.gz
# From the Fedora package:
Source2:	c-blosc-config.cmake
Patch0:		blosc-gcc11.patch
Patch1:		blosc-gcc23.patch
Patch2:		blosc-CMake4.0.patch

BuildRequires:	pgdg-srpm-macros >= 2.1.0
BuildRequires:	cmake gcc gcc-c++
%if 0%{?suse_version} >= 1500
BuildRequires:	cmake-full
%else
BuildRequires:	cmake-rpm-macros
%endif
BuildRequires:	libzstd-devel lz4-devel snappy-devel zlib-devel

%description
Blosc is a compression library designed to transmit data to the processor
cache faster than the traditional non-compressed memory fetch.
Compression ratios are not very high, but the decompression is very fast.
Blosc is meant not only to reduce the size of large datasets on-disk or
in-memory, but also to accelerate memory-bound computations.

This package installs Blosc under %{bloscinstdir}, for the packages in the
PostgreSQL RPM repository.

%package devel
Summary:	Header files and libraries for Blosc development
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains the header files and libraries needed
to develop programs that use the blosc meta-compressor.

%prep
%setup -q -n c-%{sname}-%{version}
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1
# Use the OS lz4 and zstd:
%{__rm} -r internal-complibs/lz4* internal-complibs/zstd*
sed -i '1i  set\(CMAKE_POSITION_INDEPENDENT_CODE TRUE\)' CMakeLists.txt
sed -i 's|lib/pkgconfig|lib64/pkgconfig|' CMakeLists.txt

%build
%cmake \
	-DCMAKE_INSTALL_PREFIX:PATH=%{bloscinstdir} \
	-DCMAKE_INSTALL_LIBDIR:PATH=lib64 \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=include \
	-DCMAKE_INSTALL_RPATH:PATH=%{bloscinstdir}/lib64 \
	-DBUILD_STATIC:BOOL=OFF \
	-DBUILD_BENCHMARKS:BOOL=OFF \
	-DBUILD_FUZZERS:BOOL=OFF \
%if %runselftest
	-DBUILD_TESTS:BOOL=ON \
%else
	-DBUILD_TESTS:BOOL=OFF \
%endif
	-DPREFER_EXTERNAL_LZ4:BOOL=ON \
	-DTEST_INCLUDE_BENCH_SUITE:BOOL=OFF \
	-DDEACTIVATE_SNAPPY:BOOL=OFF \
	-DPREFER_EXTERNAL_ZLIB:BOOL=ON \
	-DPREFER_EXTERNAL_ZSTD:BOOL=ON
%cmake_build

%install
%cmake_install
%{__install} -d %{buildroot}%{bloscinstdir}/lib64/cmake/c-blosc
%{__install} -p -m 0644 %{SOURCE2} %{buildroot}%{bloscinstdir}/lib64/cmake/c-blosc

%check
%if %runselftest
%ctest
%endif

%files
%license LICENSES/*
%doc README.md ANNOUNCE.rst RELEASE_NOTES.rst
%dir %{bloscinstdir}
%dir %{bloscinstdir}/lib64
%{bloscinstdir}/lib64/libblosc.so.1*

%files devel
%{bloscinstdir}/include/
%{bloscinstdir}/lib64/libblosc.so
%{bloscinstdir}/lib64/pkgconfig/
%{bloscinstdir}/lib64/cmake/

%changelog
* Wed Oct 21 2026 Devrim Gunduz <devrim@gunduz.org> - 1.21.6-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-blosc, so that the GIS stack does not need the EPEL blosc
  package on RHEL. Based on the Fedora spec file. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
