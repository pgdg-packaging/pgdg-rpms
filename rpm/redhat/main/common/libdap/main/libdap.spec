Name:		libdap
Summary:	The C++ DAP2 library from OPeNDAP
Version:	3.20.11
Release:	1%{?dist}

License:	LGPLv2+
URL:		 http://www.opendap.org/
Source0:	http://www.opendap.org/pub/source/libdap-%{version}.tar.gz
#Don't run HTTP tests - builders don't have network connections
Patch0:		libdap-offline.patch

BuildRequires:	gcc-c++
# For autoreconf
BuildRequires:	libtool
BuildRequires:	bison
BuildRequires:	cppunit-devel
BuildRequires:	curl-devel
BuildRequires:	doxygen
BuildRequires:	flex
BuildRequires:	graphviz
BuildRequires:	libtirpc-devel
BuildRequires:	libuuid-devel
BuildRequires:	libxml2-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
%ifnarch s390 %{mips}
BuildRequires:	valgrind
%endif

Provides:	bundled(gnulib)


%description
The libdap++ library contains an implementation of DAP2. This package
contains the library, dap-config, and getdap. The script dap-config
simplifies using the library in other projects. The getdap utility is a
simple command-line tool to read from DAP2 servers. It is built using the
library and demonstrates simple uses of it.


%package devel
Summary:	Development and header files from libdap
Requires:	%{name} = %{version}-%{release}
Requires:	curl-devel
Requires:	libxml2-devel
Requires:	pkgconfig
# for the /usr/share/aclocal directory ownership
Requires:	automake

%description devel
This package contains all the files needed to develop applications that
will use libdap.


%package doc
Summary:	Documentation of the libdap library

%description doc
Documentation of the libdap library.


%prep
%setup -qn %{name}-%{version}
iconv -f latin1 -t utf8 < COPYRIGHT_W3C > COPYRIGHT_W3C.utf8
touch -r COPYRIGHT_W3C COPYRIGHT_W3C.utf8
mv COPYRIGHT_W3C.utf8 COPYRIGHT_W3C

%build
# To fix rpath
autoreconf -f -i
%configure --disable-static --disable-dependency-tracking
# --enable-valgrind - missing valgrind exclusions file
%{__make} %{?_smp_mflags}

%{__make} %{?_smp_mflags} docs


%install
%{__make} %{?_smp_mflags} install INSTALL="%{__install} -p"
%{__mkdir} -p %{buildroot}%{_libdir}/libdap
%{__mv} %{buildroot}%{_libdir}/libtest-types.a %{buildroot}%{_libdir}/libdap/
%{__rm} %{buildroot}%{_libdir}/*.la
%{__mv} %{buildroot}%{_bindir}/dap-config-pkgconfig %{buildroot}%{_bindir}/dap-config

%{__rm} -rf __dist_docs
%{__cp} -pr html __dist_docs
# those .map and .md5 are of dubious use, remove them
%{__rm} -f __dist_docs/*.map __dist_docs/*.md5
# use the ChangeLog timestamp to have the same timestamps for the doc files 
# for all arches
touch -r ChangeLog __dist_docs/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYRIGHT_W3C COPYING COPYRIGHT_URI
%doc README NEWS README.dodsrc
%{_bindir}/getdap
%{_bindir}/getdap4
%{_libdir}/libdap.so.25*
%{_libdir}/libdapclient.so.6*
%{_libdir}/libdapserver.so.7*
%{_mandir}/man1/getdap.1*
%{_mandir}/man1/getdap4.1*

%files devel
%{_libdir}/libdap.so
%{_libdir}/libdapclient.so
%{_libdir}/libdapserver.so
%{_libdir}/libdap/
%{_libdir}/pkgconfig/libdap*.pc
%{_bindir}/dap-config
%{_includedir}/libdap/
%{_datadir}/aclocal/*
%{_mandir}/man1/dap-config.1*

%files doc
%license COPYING COPYRIGHT_URI COPYRIGHT_W3C
%doc __dist_docs/


%changelog
* Mon Aug 31 2026 Devrim Gündüz <devrim@gunduz.org> - 3.20.11-1
- Update to 3.20.11 per changes described at:
  https://github.com/OPENDAP/libdap4/releases/tag/3.20.11

* Sat Feb 15 2020 Devrim Gündüz <devrim@gunduz.org> - 3.20.5-1
- Initial packaging for PostgreSQL RPM repository, to satisfy
  gdal30 dependency on SLES 12.
