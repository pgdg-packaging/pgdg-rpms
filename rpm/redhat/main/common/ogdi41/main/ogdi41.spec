%global		sname	ogdi
%global		gittag	4_1_1
%global		ogdimajorver 41
%global		ogdi41instdir /usr/ogdi%{ogdimajorver}

Name:		ogdi%{ogdimajorver}
Version:	4.1.1
Release:	2PGDG%{?dist}
Summary:	Open Geographic Datastore Interface
License:	BSD
URL:		https://github.com/libogdi/ogdi
Source0:	https://github.com/libogdi/ogdi/releases/download/ogdi_%{gittag}/ogdi-%{version}.tar.gz
Source1:	http://ogdi.sourceforge.net/ogdi.pdf
Source2:	%{name}-pgdg-libs.conf
# https://bugzilla.redhat.com/show_bug.cgi?id=1470896
Patch0:		%{name}-4.1.0-sailer.patch
Patch1:		%{name}-4.1.0-mkinstalldirs.patch

BuildRequires:	gcc
%if 0%{?suse_version} >= 1315
BuildRequires:	libexpat-devel
%else
BuildRequires:	expat-devel
%endif
BuildRequires:	libtirpc-devel
BuildRequires:	zlib-devel

# ODBC driver has been removed in 4.1.1 without replacement
Obsoletes:	%{name}-odbc < 4.1.1

%description
OGDI is the Open Geographic Datastore Interface. OGDI is an
application programming interface (API) that uses a standardized
access methods to work in conjunction with GIS software packages (the
application) and various geospatial data products. OGDI uses a
client/server architecture to facilitate the dissemination of
geospatial data products over any TCP/IP network, and a
driver-oriented approach to facilitate access to several geospatial
data products/formats.


%package devel
Summary:	OGDI header files and documentation
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
Requires:	zlib-devel
%if 0%{?suse_version} >= 1315
BuildRequires:	libexpat-devel
%else
BuildRequires:	expat-devel
%endif

%description devel
OGDI header files and developer's documentation.


%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p1
%patch -P 1 -p0

# include documentation
%{__cp} -p %{SOURCE1} .

%build
TOPDIR=`pwd`; TARGET=Linux; export TOPDIR TARGET
INST_LIB=%{ogdi41instdir}/lib/;export INST_LIB
export CFG=debug # for -g

# removal of -D_FORTIFY_SOURCE from preprocessor flags seems not needed any more
# ogdits-3.1 test suite produces same result with and without the flag
export CFLAGS="$RPM_OPT_FLAGS -DDONT_TD_VOID -DUSE_TERMIO -ltirpc -std=gnu17"
./configure \
	--prefix=%{ogdi41instdir} \
	--with-binconfigs \
	--with-expat \
	--with-zlib

# WARNING !!!
# using %{?_smp_mflags} may break build
%{__make}

# build contributions
%{__make} -C contrib/gdal

%install
# export env
TOPDIR=`pwd`; TARGET=Linux; export TOPDIR TARGET
export DESTDIR=%{buildroot}
%{__make} install \
	INST_INCLUDE=%{buildroot}%{ogdi41instdir}/include/ \
	INST_LIB=%{buildroot}%{ogdi41instdir}/lib \
	INST_BIN=%{buildroot}%{ogdi41instdir}/bin

# install plugins olso
%{__make} install -C contrib/gdal \
	INST_LIB=%{buildroot}%{ogdi41instdir}/lib

# remove example binary
%{__rm} %{buildroot}%{ogdi41instdir}/bin/example?

# we have multilib ogdi-config
%if "%{_lib}" == "lib"
%global cpuarch 32
%else
%global cpuarch 64
%endif

# fix file(s) for multilib issue
touch -r ogdi-config.in ogdi-config

# install pkgconfig file and ogdi-config
%{__mkdir} -p %{buildroot}%{ogdi41instdir}/lib/pkgconfig
%{__install} -p -m 644 ogdi.pc %{buildroot}%{ogdi41instdir}/lib/pkgconfig/
%{__install} -p -m 755 ogdi-config %{buildroot}%{ogdi41instdir}/bin/ogdi-config-%{cpuarch}
# ogdi-config wrapper for multiarch
cat > %{buildroot}%{ogdi41instdir}/bin/%{sname}-config <<EOF
#!/bin/bash

ARCH=\$(uname -m)
case \$ARCH in
x86_64 | ppc64 | ppc64le | ia64 | s390x | sparc64 | alpha | alphaev6 | aarch64 )
ogdi-config-64 \${*}
;;
*)
ogdi-config-32 \${*}
;;
esac
EOF
chmod 755 %{buildroot}%{ogdi41instdir}/bin/%{sname}-config
touch -r ogdi-config.in %{buildroot}%{ogdi41instdir}/bin/%{sname}-config

# Install linker config file:
%{__mkdir} -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%{__install} %{SOURCE2} %{buildroot}%{_sysconfdir}/ld.so.conf.d/

%files
%doc ogdi.pdf
%doc LICENSE NEWS ChangeLog README
%{ogdi41instdir}/bin/gltpd
%{ogdi41instdir}/bin/ogdi_*
%{ogdi41instdir}/lib/libogdi.so*
%dir %{ogdi41instdir}/lib/ogdi
%{ogdi41instdir}/lib/%{sname}/lib*.so
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%files devel
%doc ogdi/examples/example1/example1.c
%doc ogdi/examples/example2/example2.c
%{ogdi41instdir}/bin/%{sname}-config
%{ogdi41instdir}/bin/%{sname}-config-%{cpuarch}
%{ogdi41instdir}/lib/pkgconfig/%{sname}.pc
%dir %{ogdi41instdir}/include/
%{ogdi41instdir}/include/*.h

%changelog
* Mon Mar 24 2025 Devrim Gunduz <devrim@gunduz.org> - 4.1.1-2PGDG
- Fix/surpress build errors against GCC 15. GDAL will drop OGDI
  support along with 3.11, so don't bother to fix more.
- Retire tcl subpackage. Cannot be built against GCC 15.

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 4.1.1-1PGDG
- Update to 4.1.1 per changes described at:
  https://github.com/libogdi/ogdi/releases/tag/ogdi_4_1_1
- Remove ODBC package per upstream.
- Add PGDG branding

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 4.1.0-3.1
- Modernise %patch usage, which has been deprecated in Fedora 38

* Sat Feb 15 2020 Devrim Gündüz <devrim@gunduz.org> - 4.1.0-3
* Remove tcl subpackage We don't need it (and also SLES is throwing build
  errors)

* Mon Sep 16 2019 Devrim Gündüz <devrim@gunduz.org> - 4.1.0-2
* Initial ogdi41 packaging for PostgreSQL RPM repository
