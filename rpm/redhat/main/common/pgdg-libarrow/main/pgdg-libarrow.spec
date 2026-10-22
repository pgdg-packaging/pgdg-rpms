%global		sname libarrow
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		arrowinstdir %{pgdg_libarrowinstdir}

# The libraries are found through the rpath only (there is no ld.so.conf.d
# file), so they must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL libraries. Consumers require
# pgdg-libarrow by name instead:
%global		__provides_exclude_from ^%{arrowinstdir}/
%global		__requires_exclude ^lib(arrow[a-z_]*|parquet|uriparser)\\.so

# RHEL 8 uses Arrow 15, which GDAL 3.8 (gdal38) builds with; Arrow 26
# needs C++20 and removed APIs that GDAL 3.8 uses:
%if 0%{?rhel} == 8
%global		arrowversion 15.0.2
%else
%global		arrowversion 26.0.0
%endif

# Dependencies that RHEL does not ship are built into the Arrow libraries
# from their source tarballs, with the mechanism Arrow provides for that.
# These are the versions Arrow is tested with (cpp/thirdparty/versions.txt):
%global		rapidjsoncommit 232389d4f1012dddec4ef84861face2d2ba85709
%if 0%{?rhel} == 8
%global		re2version 2022-06-01
%global		thriftversion 0.16.0
%global		utf8procversion 2.7.0
%global		xsimdversion 9.0.1
%else
%global		re2version 2023-03-01
%global		simdjsonversion 4.6.4
%global		thriftversion 0.22.0
%global		utf8procversion 2.10.0
%global		xsimdversion 14.2.0
%endif

%if 0%{?rhel} == 8
%undefine __cmake_in_source_build
%endif

Name:		pgdg-%{sname}
Version:	%{arrowversion}
Release:	1PGDG%{?dist}
Summary:	A toolbox for accelerated data interchange and in-memory processing
License:	Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND MIT AND BSL-1.0 AND Unicode-3.0
URL:		https://arrow.apache.org/
Source0:	https://downloads.apache.org/arrow/arrow-%{version}/apache-arrow-%{version}.tar.gz
Source1:	https://github.com/google/re2/archive/%{re2version}.tar.gz#/re2-%{re2version}.tar.gz
Source2:	https://github.com/miloyip/rapidjson/archive/%{rapidjsoncommit}.tar.gz#/rapidjson-%{rapidjsoncommit}.tar.gz
%if 0%{?rhel} != 8
Source3:	https://github.com/simdjson/simdjson/archive/refs/tags/v%{simdjsonversion}.tar.gz#/simdjson-%{simdjsonversion}.tar.gz
%endif
Source4:	https://archive.apache.org/dist/thrift/%{thriftversion}/thrift-%{thriftversion}.tar.gz
Source5:	https://github.com/JuliaStrings/utf8proc/archive/v%{utf8procversion}.tar.gz#/utf8proc-%{utf8procversion}.tar.gz
Source6:	https://github.com/xtensor-stack/xsimd/archive/%{xsimdversion}.tar.gz#/xsimd-%{xsimdversion}.tar.gz

ExcludeArch:	ppc64le

BuildRequires:	pgdg-srpm-macros >= 2.1.0
BuildRequires:	cmake >= 3.16 ninja-build
%if 0%{?suse_version} >= 1500
BuildRequires:	cmake-full
%else
BuildRequires:	cmake-rpm-macros
%endif
BuildRequires:	boost-devel gcc-c++
BuildRequires:	brotli-devel bzip2-devel libzstd-devel lz4-devel
BuildRequires:	openssl-devel snappy-devel zlib-devel
BuildRequires:	pgdg-uriparser-devel
Requires:	pgdg-uriparser%{?_isa}
Provides:	bundled(re2) = %(echo %{re2version} | tr - .)
Provides:	bundled(rapidjson) = %{rapidjsoncommit}
%if 0%{?rhel} != 8
Provides:	bundled(simdjson) = %{simdjsonversion}
%endif
Provides:	bundled(thrift) = %{thriftversion}
Provides:	bundled(utf8proc) = %{utf8procversion}
Provides:	bundled(xsimd) = %{xsimdversion}

%description
Apache Arrow is a cross-language development platform for in-memory data.
It specifies a standardized language-independent columnar memory format for
flat and hierarchical data, organized for efficient analytic operations on
modern hardware. It also provides computational libraries and zero-copy
streaming messaging and inter-process communication.

This package installs the Arrow C++ libraries (Arrow with Acero, Compute,
CSV, JSON, IPC and filesystems, Dataset and Parquet) under %{arrowinstdir},
for the packages in the PostgreSQL RPM repository.

%package devel
Summary:	Libraries and header files for Apache Arrow C++
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	brotli-devel bzip2-devel libzstd-devel lz4-devel
Requires:	openssl-devel snappy-devel zlib-devel
Requires:	pgdg-uriparser-devel%{?_isa}

%description devel
Libraries and header files for Apache Arrow C++, Dataset and Parquet.

%prep
%setup -q -n apache-arrow-%{version}

%build
export ARROW_RE2_URL=%{SOURCE1}
export ARROW_RAPIDJSON_URL=%{SOURCE2}
%if 0%{?rhel} != 8
export ARROW_SIMDJSON_URL=%{SOURCE3}
%endif
export ARROW_THRIFT_URL=%{SOURCE4}
export ARROW_UTF8PROC_URL=%{SOURCE5}
export ARROW_XSIMD_URL=%{SOURCE6}
cd cpp
%cmake -GNinja \
	-DCMAKE_INSTALL_PREFIX:PATH=%{arrowinstdir} \
	-DCMAKE_INSTALL_LIBDIR:PATH=lib64 \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=include \
	-DCMAKE_PREFIX_PATH:PATH=%{pgdg_uriparserinstdir} \
	-DCMAKE_INSTALL_RPATH:STRING="%{arrowinstdir}/lib64;%{pgdg_uriparserinstdir}/lib64" \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DARROW_DEPENDENCY_SOURCE=AUTO \
	-Dre2_SOURCE=BUNDLED \
	-DRapidJSON_SOURCE=BUNDLED \
%if 0%{?rhel} != 8
	-Dsimdjson_SOURCE=BUNDLED \
%endif
	-DThrift_SOURCE=BUNDLED \
	-Dutf8proc_SOURCE=BUNDLED \
	-Dxsimd_SOURCE=BUNDLED \
	-Duriparser_SOURCE=SYSTEM \
	-DARROW_ACERO:BOOL=ON \
	-DARROW_COMPUTE:BOOL=ON \
	-DARROW_CSV:BOOL=ON \
	-DARROW_DATASET:BOOL=ON \
	-DARROW_FILESYSTEM:BOOL=ON \
	-DARROW_IPC:BOOL=ON \
	-DARROW_JSON:BOOL=ON \
	-DARROW_PARQUET:BOOL=ON \
	-DPARQUET_REQUIRE_ENCRYPTION:BOOL=ON \
	-DARROW_FLIGHT:BOOL=OFF \
	-DARROW_GANDIVA:BOOL=OFF \
	-DARROW_ORC:BOOL=OFF \
	-DARROW_S3:BOOL=OFF \
	-DARROW_GCS:BOOL=OFF \
	-DARROW_AZURE:BOOL=OFF \
	-DARROW_JEMALLOC:BOOL=OFF \
	-DARROW_MIMALLOC:BOOL=OFF \
	-DARROW_SIMD_LEVEL:STRING=NONE \
	-DARROW_RUNTIME_SIMD_LEVEL:STRING=NONE \
	-DARROW_WITH_BROTLI:BOOL=ON \
	-DARROW_WITH_BZ2:BOOL=ON \
	-DARROW_WITH_LZ4:BOOL=ON \
	-DARROW_WITH_SNAPPY:BOOL=ON \
	-DARROW_WITH_ZLIB:BOOL=ON \
	-DARROW_WITH_ZSTD:BOOL=ON \
	-DARROW_BUILD_STATIC:BOOL=OFF \
	-DARROW_BUILD_TESTS:BOOL=OFF \
	-DARROW_BUILD_UTILITIES:BOOL=OFF \
	-DARROW_USE_CCACHE:BOOL=OFF \
	-DCMAKE_UNITY_BUILD:BOOL=ON
%cmake_build

%install
cd cpp
%cmake_install
# GDB pretty printers, not useful under this prefix:
%{__rm} -rf %{buildroot}%{arrowinstdir}/share/gdb %{buildroot}%{arrowinstdir}/share/arrow/gdb
%{__rm} -f %{buildroot}%{arrowinstdir}/lib64/*-gdb.py

%files
%license LICENSE.txt NOTICE.txt
%doc README.md
%dir %{arrowinstdir}
%dir %{arrowinstdir}/lib64
%{arrowinstdir}/lib64/lib*.so.*

%files devel
%{arrowinstdir}/include/
%{arrowinstdir}/lib64/lib*.so
%{arrowinstdir}/lib64/cmake/
%{arrowinstdir}/lib64/pkgconfig/
%{arrowinstdir}/share/

%changelog
* Wed Oct 21 2026 Devrim Gunduz <devrim@gunduz.org> - 26.0.0-1PGDG
- Arrow 15.0.2 on RHEL 8, for GDAL 3.8 (gdal38).
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-arrow, so that the GIS stack does not need the EPEL libarrow
  packages on RHEL. The dependencies that RHEL does not ship (re2,
  RapidJSON, simdjson, Thrift, utf8proc and xsimd) are built in, from the
  versions Arrow is tested with. Based on the Fedora spec file. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
