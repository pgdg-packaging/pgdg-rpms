%global		sname mongo-c-driver
%global		libver 1.0
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		mongocinstdir %{pgdg_libmongocinstdir}

# The libraries are found through the rpath only (there is no ld.so.conf.d
# file), so they must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL mongo-c-driver. Consumers
# require pgdg-libmongoc-libs by name instead:
%global		__provides_exclude_from ^%{mongocinstdir}/
%global		__requires_exclude ^lib(mongoc|bson)-1\\.0\\.so

%if 0%{?rhel} == 8
%undefine __cmake_in_source_build
# No utf8proc on RHEL 8; use the bundled copy:
%global		with_libutf8proc 0
%else
%global		with_libutf8proc 1
%endif

Name:		pgdg-libmongoc
Version:	1.30.14
Release:	1PGDG%{?dist}
Summary:	Client library written in C for MongoDB
# See THIRD_PARTY_NOTICES
License:	Apache-2.0 AND ISC AND MIT AND Zlib
URL:		https://github.com/mongodb/%{sname}
Source0:	https://github.com/mongodb/%{sname}/archive/refs/tags/%{version}.tar.gz

BuildRequires:	pgdg-srpm-macros >= 2.3.0
BuildRequires:	cmake >= 3.15 gcc gcc-c++ make perl-interpreter
BuildRequires:	openssl-devel pkgconfig(libsasl2) pkgconfig(zlib)
BuildRequires:	pkgconfig(snappy) pkgconfig(libzstd) >= 0.8.0
%if %{with_libutf8proc}
BuildRequires:	pkgconfig(libutf8proc)
%endif
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description
mongo-c-driver is a library for building high-performance applications that
communicate with the MongoDB NoSQL database in the C language. It can also
be used to write fast client implementations in languages such as Python,
Ruby, or Perl. This package contains the mongoc-stat tool.

This package installs mongo-c-driver and libbson under %{mongocinstdir},
for the packages in the PostgreSQL RPM repository.

%package libs
Summary:	Shared libraries of mongo-c-driver and libbson
%if ! %{with_libutf8proc}
Provides:	bundled(libutf8proc) = 2.8.0
%endif
Provides:	bundled(uthash) = 2.3.0
Provides:	bundled(jsonsl)

%description libs
This package contains the shared libraries of mongo-c-driver, and of
libbson, which builds, parses and iterates BSON documents.

%package devel
Summary:	Development files for mongo-c-driver and libbson
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	pkgconfig(libzstd)

%description devel
The %{name}-devel package contains libraries and header files of
mongo-c-driver and libbson, for developing applications that use
them.

%prep
%setup -q -n %{sname}-%{version}

%build
# Client side field level encryption needs libmongocrypt, and the man pages
# a newer Sphinx than RHEL 8 and 9 have; both are disabled:
%cmake \
	-DCMAKE_INSTALL_PREFIX:PATH=%{mongocinstdir} \
	-DCMAKE_INSTALL_LIBDIR:PATH=lib64 \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=include \
	-DCMAKE_INSTALL_RPATH:PATH=%{mongocinstdir}/lib64 \
	-DBUILD_VERSION=%{version} \
	-DENABLE_MONGOC:BOOL=ON \
	-DENABLE_SHM_COUNTERS:BOOL=ON \
	-DENABLE_SSL:STRING=OPENSSL \
	-DENABLE_SASL:STRING=CYRUS \
	-DENABLE_MONGODB_AWS_AUTH:STRING=ON \
	-DENABLE_AUTOMATIC_INIT_AND_CLEANUP:BOOL=OFF \
	-DENABLE_CRYPTO_SYSTEM_PROFILE:BOOL=ON \
	-DENABLE_MAN_PAGES:BOOL=OFF \
	-DENABLE_HTML_DOCS:BOOL=OFF \
	-DENABLE_SHARED:BOOL=ON \
	-DENABLE_STATIC:STRING=OFF \
	-DENABLE_ZLIB:STRING=SYSTEM \
	-DENABLE_ZSTD:STRING=ON \
	-DENABLE_SNAPPY:STRING=ON \
	-DENABLE_TESTS:BOOL=OFF \
	-DENABLE_EXAMPLES:BOOL=OFF \
	-DENABLE_UNINSTALL:BOOL=OFF \
	-DENABLE_CLIENT_SIDE_ENCRYPTION:BOOL=OFF \
%if %{with_libutf8proc}
	-DUSE_BUNDLED_UTF8PROC:BOOL=OFF \
%else
	-DUSE_BUNDLED_UTF8PROC:BOOL=ON \
%endif
	-DENABLE_SRV:BOOL=ON
%cmake_build

%install
%cmake_install

# Static libraries and the documentation:
%{__rm} -f %{buildroot}%{mongocinstdir}/lib64/*.a
%{__rm} -rf %{buildroot}%{mongocinstdir}/lib64/cmake/*static*
%{__rm} -rf %{buildroot}%{mongocinstdir}/lib64/pkgconfig/*static*
%{__rm} -rf %{buildroot}%{mongocinstdir}/share

%files
%dir %{mongocinstdir}/bin
%{mongocinstdir}/bin/mongoc-stat

%files libs
%license COPYING THIRD_PARTY_NOTICES
%dir %{mongocinstdir}
%dir %{mongocinstdir}/lib64
%{mongocinstdir}/lib64/libmongoc-%{libver}.so.*
%{mongocinstdir}/lib64/libbson-%{libver}.so.*

%files devel
%doc NEWS
%{mongocinstdir}/include/
%{mongocinstdir}/lib64/libmongoc-%{libver}.so
%{mongocinstdir}/lib64/libbson-%{libver}.so
%{mongocinstdir}/lib64/pkgconfig/
%{mongocinstdir}/lib64/cmake/

%changelog
* Fri Oct 23 2026 Devrim Gunduz <devrim@gunduz.org> - 1.30.14-1PGDG
- Update to 1.30.14, the latest 1.x release (mongo_fdw does not support
  the 2.x API), and build it on RHEL 8, 9 and 10, installed under
  /usr/pgdg-libmongoc, so that mongo_fdw and postgresbson do not need the
  EPEL mongo-c-driver and libbson packages. Based on the Fedora spec file.
  The sonames are not provided anymore; consumers find the libraries
  through the rpath, and require pgdg-libmongoc-libs by name. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Sat Sep 12 2026 Devrim Gunduz <devrim@gunduz.org> - 1.17.3-2
- Fix build against CMake 4 on Fedora/RHEL/AL2023 (cmake3 no longer
  exists as a package; use cmake instead)
- Add -DCMAKE_POLICY_VERSION_MINIMUM=3.5: the bundled CMakeLists.txt's
  cmake_minimum_required is too old for CMake 4 ("Compatibility with
  CMake < 3.5 has been removed")

* Mon May 3 2021 Devrim Gündüz <devrim@gunduz.org> - 1.17.3-1
- Initial packaging for PostgreSQL RPM repository to fix
  mongo_fdw installations on RHEL 7, per:
  https://redmine.postgresql.org/issues/6424
