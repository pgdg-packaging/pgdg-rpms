%global mongocinstdir	/usr/%{name}
%global sname		mongo-c-driver
%global pname		pgdg-libmongoc
%global BsonName	pgdg-libbson

Name:		%{pname}
Version:	1.17.3
Release:	2%{?dist}
Summary:	MongoDB C Driver
License:	Apache-2.0
URL:		https://github.com/mongodb/%{sname}
Source0:	https://github.com/mongodb/%{sname}/releases/download/%{version}/%{sname}-%{version}.tar.gz
BuildRequires:	make cyrus-sasl-devel libtool cmake
BuildRequires:	openssl-devel pkgconfig snappy-devel
Provides:	%{sname} = %{version}
Provides:	libmongoc-1.0 = %{version}

%description
mongo-c-driver is a library for building high-performance applications that
communicate with the MongoDB NoSQL database in the C language. It can also
be used to write fast client implementations in languages such as Python,
Ruby, or Perl.

%package -n %{pname}-devel
Summary:	Development files for mongo-c-driver
Obsoletes:	%{name} <= 1.9.5

%description -n %{pname}-devel
The %{pname}-devel package contains libraries and header files of mongoc driver and bbson for
developing applications that use %{sname}.

%package -n %{pname}-libs
Summary:	Library files for mongo-c-driver
Obsoletes:	%{name} <= 1.9.5

%description -n %{pname}-libs
The %{pname} package contains libraries for mongoc driver and bbson for
developing applications that use %{sname}.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__install} -d build
pushd build
cmake -DENABLE_AUTOMATIC_INIT_AND_CLEANUP=OFF -DENABLE_SSL=AUTO \
	-DENABLE_STATIC=OFF -DENABLE_TESTS=OFF -DENABLE_MAN_PAGES=OFF \
	-DCMAKE_INSTALL_PREFIX=%{mongocinstdir} ..
%{__make} %{?_smp_mflags} build
popd

%install
%{__rm} -rf %{buildroot}
pushd build
%{__make} prefix=%{_prefix} %{?_smp_mflags} install DESTDIR=%{buildroot}
popd

%{__rm} -rf %{buildroot}/%{mongocinstdir}/share
%{__rm} -f %{buildroot}/%{mongocinstdir}/lib/*.la

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -n %{pname}
%{mongocinstdir}/bin/mongoc-stat

%files -n %{pname}-devel
%dir %{mongocinstdir}/include/libmongoc-1.0*
%{mongocinstdir}/include/libmongoc-1.0/mongoc*
%{mongocinstdir}/%{_lib}/pkgconfig/libmongoc-1.0.pc
%{mongocinstdir}/%{_lib}/pkgconfig/libmongoc-ssl-1.0.pc
%{mongocinstdir}/%{_lib}/cmake/libmongoc-1.0
%{mongocinstdir}/%{_lib}/cmake/mongoc-1.0/*.cmake
%{mongocinstdir}/bin/mongoc-stat
%dir %{mongocinstdir}/include/libbson-1.0*
%dir %{mongocinstdir}/include/libbson-1.0/bson
%{mongocinstdir}/include/libbson-1.0/bson*
%{mongocinstdir}/%{_lib}/pkgconfig/libbson-1.0.pc
%{mongocinstdir}/%{_lib}/cmake/bson-1.0/*.cmake
%{mongocinstdir}/%{_lib}/cmake/libbson-1.0/*.cmake

%files -n %{pname}-libs
%{mongocinstdir}/%{_lib}/libmongoc-1.0.so*
%{mongocinstdir}/%{_lib}/libbson-1.0.so*

%changelog
* Sat Sep 12 2026 Devrim Gunduz <devrim@gunduz.org> - 1.17.3-2
- Fix build against CMake 4 on Fedora/RHEL/AL2023 (cmake3 no longer
  exists as a package; use cmake instead)

* Mon May 3 2021 Devrim Gündüz <devrim@gunduz.org> - 1.17.3-1
- Initial packaging for PostgreSQL RPM repository to fix
  mongo_fdw installations on RHEL 7, per:
  https://redmine.postgresql.org/issues/6424
