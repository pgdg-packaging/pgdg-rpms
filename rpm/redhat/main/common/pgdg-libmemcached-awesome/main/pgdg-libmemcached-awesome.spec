%global		sname libmemcached-awesome
%global		libname libmemcached
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		libmemcachedinstdir %{pgdg_libmemcachedinstdir}

# The libraries are found through the rpath only (there is no ld.so.conf.d
# file), so they must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the EPEL libmemcached-awesome. Consumers
# require pgdg-libmemcached-awesome by name instead:
%global		__provides_exclude_from ^%{libmemcachedinstdir}/
%global		__requires_exclude ^lib(hashkit|memcached|memcachedprotocol|memcachedutil)\\.so

%global		gh_commit 92d18858b417309f6bdee6bce464a4f3d6a375fd
%global		gh_short %(c=%{gh_commit}; echo ${c:0:7})

%{!?runselftest:%global runselftest 0}

Name:		pgdg-%{sname}
Version:	1.1.4
Release:	1PGDG%{?dist}
Summary:	Client library for memcached server
License:	BSD-3-Clause
URL:		https://github.com/awesomized/%{libname}
Source0:	https://github.com/awesomized/%{libname}/archive/%{gh_commit}/%{libname}-%{version}-%{gh_short}.tar.gz
# Fix a test with memcached 1.6.40 (Fedora)
Patch0:		%{name}-memcached-1.6.40.patch

BuildRequires:	pgdg-srpm-macros >= 2.5.1
BuildRequires:	cmake >= 3.9
# Cannot use Ninja generator because of "multiple rules generate docs/man"
%global _cmake_generator "Unix Makefiles"
BuildRequires:	make gcc gcc-c++
BuildRequires:	bison flex
BuildRequires:	cyrus-sasl-devel
BuildRequires:	libevent-devel > 2
BuildRequires:	openssl-devel
BuildRequires:	systemtap-sdt-devel
%if %runselftest
BuildRequires:	memcached
%endif

Provides:	bundled(bobjenkins-hash)

%description
libmemcached-awesome is a C/C++ client library for the memcached server
(https://memcached.org/). It has been designed to be light on memory
usage, and provide full access to server side methods.

This package installs libmemcached-awesome under %{libmemcachedinstdir},
for the packages in the PostgreSQL RPM repository.

%package devel
Summary:	Header files and development libraries for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	cyrus-sasl-devel%{?_isa}

%description devel
This package contains the header files and development libraries
for %{sname}, installed under %{libmemcachedinstdir}.

%prep
%setup -q -n %{libname}-%{gh_commit}

# drop test hanging in mock
# and requiring some memcached build options
%{__rm} test/tests/memcached/sasl.cpp
%{__rm} test/tests/memcached/regression/lp_001-630-615.cpp
# temporarily ignore with erratic failure
%{__rm} test/tests/memcached/udp.cpp
%{__rm} test/tests/memcached/regression/lp_000-583-031.cpp
%{__rm} test/tests/memcached/regression/gh-php-memcached_0531.cpp

%patch -P 0 -p1

%build
# The command line tools are built (the test suite uses them), but not
# packaged:
%cmake \
	-DCMAKE_INSTALL_PREFIX:PATH=%{libmemcachedinstdir} \
	-DCMAKE_INSTALL_LIBDIR:PATH=lib64 \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=include \
	-DCMAKE_INSTALL_RPATH:PATH=%{libmemcachedinstdir}/lib64 \
%if %runselftest
	-DBUILD_TESTING:BOOL=ON \
%else
	-DBUILD_TESTING:BOOL=OFF \
%endif
	-DBUILD_DOCS:BOOL=OFF \
	-DENABLE_SASL:BOOL=ON \
	-DENABLE_DTRACE:BOOL=ON \
	-DENABLE_OPENSSL_CRYPTO:BOOL=ON \
	-DENABLE_HASH_HSIEH:BOOL=ON \
	-DENABLE_HASH_FNV64:BOOL=ON \
	-DENABLE_HASH_MURMUR:BOOL=ON \
	-DENABLE_MEMASLAP:BOOL=OFF
%cmake_build

%install
%cmake_install
%{__rm} -r %{buildroot}%{libmemcachedinstdir}/bin
%{__rm} -r %{buildroot}%{libmemcachedinstdir}/share
%{__rm} %{buildroot}%{libmemcachedinstdir}/lib64/libp9y.a
%{__rm} %{buildroot}%{libmemcachedinstdir}/lib64/cmake/%{sname}/p9y*

%check
%if %runselftest
%ctest
%endif

%files
%license LICENSE
%dir %{libmemcachedinstdir}
%dir %{libmemcachedinstdir}/lib64
%{libmemcachedinstdir}/lib64/libhashkit.so.2*
%{libmemcachedinstdir}/lib64/libmemcached.so.11*
%{libmemcachedinstdir}/lib64/libmemcachedprotocol.so.0*
%{libmemcachedinstdir}/lib64/libmemcachedutil.so.2*

%files devel
%doc *.md AUTHORS
%{libmemcachedinstdir}/include/
%{libmemcachedinstdir}/lib64/libhashkit.so
%{libmemcachedinstdir}/lib64/libmemcached.so
%{libmemcachedinstdir}/lib64/libmemcachedprotocol.so
%{libmemcachedinstdir}/lib64/libmemcachedutil.so
%{libmemcachedinstdir}/lib64/pkgconfig/
%{libmemcachedinstdir}/lib64/cmake/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1.4-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-libmemcached, so that pgpool-II and pgmemcache do not need the
  EPEL libmemcached-awesome package on RHEL 10. Based on the Fedora spec
  file. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422
