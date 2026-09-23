%global debug_package		%{nil}
%global sname libspatialite
%global libspatialiteinstdir	/usr/%{name}

%global	libspatialitemajorversion	43

%global sqlitepname		sqlite33
%global sqlite33dir		/usr/sqlite330

%pgdg_set_gis_variables

# Override PROJ major version on RHEL 7.
# libspatialite 4.3 does not build against 8.0.0 as of March 2021.
%if 0%{?rhel} && 0%{?rhel} == 7
%global projmajorversion 72
%global projfullversion 7.2.1
%global projinstdir /usr/proj%{projmajorversion}
%endif

# A new feature available in PostGIS 2.0
#%%global _lwgeom "--enable-lwgeom=yes"
# Disabled due to a circular dependency issue with PostGIS
# https://bugzilla.redhat.com/show_bug.cgi?id=979179
%global _lwgeom "--disable-lwgeom"

# Geocallbacks work with SQLite 3.7.3 and up, available in Fedora and EL 7
%if (0%{?fedora} || 0%{?rhel} > 6)
  %global _geocallback "--enable-geocallbacks"
%endif

# check_bufovflw test fails on gcc 4.9
# https://groups.google.com/forum/#!msg/spatialite-users/zkGP-gPByXk/EAZ-schWn1MJ
%if (0%{?fedora} >= 21 || 0%{?rhel} > 7)
  %global _no_checks 1
%endif

Name:		%{sname}%{libspatialitemajorversion}
Version:	4.3.0a
Release:	17%{?dist}.1
Summary:	Enables SQLite to support spatial data
License:	MPLv1.1 or GPLv2+ or LGPLv2+
URL:		https://www.gaia-gis.it/fossil/%{sname}
Source0:	http://www.gaia-gis.it/gaia-sins/%{sname}-sources/%{sname}-%{version}.tar.gz
Source1:	%{name}-pgdg-libs.conf

Patch0:		%{name}-proj_api.h-configure.patch
Patch1:		%{name}-proj_api.h-c.patch
BuildRequires:	gcc autoconf
BuildRequires:	freexl-devel pgdg-srpm-macros >= 1.0.9
BuildRequires:	geos%{geosmajorversion}-devel >= %{geosfullversion}
BuildRequires:	proj%{projmajorversion}-devel >= %{projfullversion}
BuildRequires:	sqlite33-devel zlib-devel libxml2-devel
Requires:	geos%{geosmajorversion} >= %{geosfullversion}
Requires:	proj%{projmajorversion} >= %{projfullversion}


%description
SpatiaLite is a a library extending the basic SQLite core in order to
get a full fledged Spatial DBMS, really simple and lightweight, but
mostly OGC-SFS compliant.

%package devel
Summary:	Development libraries and headers for SpatiaLite
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p0
%patch -P 1 -p0
autoconf

%build
CFLAGS="$CFLAGS -I%{projinstdir}/include -I%{geosinstdir}/include -I%{sqlite33dir}/include"; export CFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{geosinstdir}/lib64,%{projinstdir}/lib" ; export SHLIB_LINK
LDFLAGS="$LDFLAGS -L%{geosinstdir}/lib64 -L%{projinstdir}/lib -L%{sqlite33dir}/lib"; export LDFLAGS
./configure \
	--prefix=%{libspatialiteinstdir} \
	--libdir=%{libspatialiteinstdir}/lib \
	--disable-static \
	--with-geosconfig=%{geosinstdir}/bin/geos-config \
	--with-lwgeom \
%ifarch aarch64
	--build=aarch64-unknown-linux-gnu \
%endif
%ifarch ppc64 ppc64le
	--build=ppc64le-unknown-linux-gnu \
%endif
	--enable-libxml2 \
	%{?_geocallback}

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__make} install DESTDIR=%{buildroot}

# Install linker config file:
%{__mkdir} -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%{__install} %{SOURCE1} %{buildroot}%{_sysconfdir}/ld.so.conf.d/

# Delete undesired libtool archives
find %{buildroot} -type f -name "*.la" -delete

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

%files
%doc COPYING AUTHORS
%{libspatialiteinstdir}/lib/%{sname}.so.7*
%{libspatialiteinstdir}/lib/mod_spatialite.so.7*
# The symlink must be present to allow loading the extension
# https://groups.google.com/forum/#!topic/spatialite-users/zkGP-gPByXk
%{libspatialiteinstdir}/lib/mod_spatialite.so
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%files devel
%doc examples/*.c
%{libspatialiteinstdir}/include/spatialite.h
%{libspatialiteinstdir}/include/spatialite
%{libspatialiteinstdir}/lib/%{sname}.so
%{libspatialiteinstdir}/lib/pkgconfig/spatialite.pc


%changelog
* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 4.3.0a-17.1
- Modernise %patch usage, which has been deprecated in Fedora 38

* Mon Nov 14 2022 Devrim Gunduz <devrim@gunduz.org> - 4.3.0a-17
- Use PROJ 7.2 on RHEL 7.

* Fri Mar 12 2021 Devrim Gunduz <devrim@gunduz.org> - 4.3.0a-16
- Rebuild against GeOS 3.9.1 and Proj 8.0.0.

* Wed Jan 6 2021 Devrim Gunduz <devrim@gunduz.org> - 4.3.0a-15
- Fix installation path of -devel package, per
  https://redmine.postgresql.org/issues/6126

* Sun Dec 20 2020 Devrim Gunduz <devrim@gunduz.org> - 4.3.0a-14
- Rebuild against GeOS 3.9.0

* Fri Nov 27 2020 Devrim Gunduz <devrim@gunduz.org> - 4.3.0a-13
- Rebuild against PROJ 7.2.0 and GeOS 3.8.0

* Tue Sep 8 2020 Devrim Gunduz <devrim@gunduz.org> - 4.3.0a-12
- Add linker config file

* Tue Aug 18 2020 Devrim Gunduz <devrim@gunduz.org> - 4.3.0a-11
- Rebuild against Proj 7.1.0

* Thu Jul 9 2020 Devrim Gunduz <devrim@gunduz.org> - 4.3.0a-10
- Fix intermittent build failure. Patch by Varsha Mehtre.

* Mon May 4 2020 Devrim Gunduz <devrim@gunduz.org> - 4.3.0a-9
- Rebuild against Proj 7.0.1
- Add missing Requires.

* Wed Mar 11 2020 Devrim Gunduz <devrim@gunduz.org> - 4.3.0a-8
- Rebuild against GeOS 3.8.1 and Proj 7.0.0

* Tue Feb 25 2020 Devrim Gunduz <devrim@gunduz.org> - 4.3.0a-7
- Rebuild for Proj 6.3.1

* Wed Feb 5 2020 Devrim Gunduz <devrim@gunduz.org> - 4.3.0a-6
- Rebuild for Proj 6.3.0

* Thu Nov 21 2019 Devrim Gunduz <devrim@gunduz.org> - 4.3.0a-5
- Use our own sqlite33 package on RHEL 7 to fix performance issues.

* Mon Nov 4 2019 Devrim Gunduz <devrim@gunduz.org> - 4.3.0a-4
- Rebuild for Proj 6.2.1

* Fri Oct 11 2019 Devrim Gunduz <devrim@gunduz.org> - 4.3.0a-3
- Rebuild for GeOS 3.8.0

* Tue Sep 24 2019 Devrim Gunduz <devrim@gunduz.org> - 4.3.0a-2
- Rebuild for GeOS 3.7.2

* Sat Sep 21 2019 Devrim Gunduz <devrim@gunduz.org> - 4.3.0a-1
- Initial packaging for PostgreSQL RPM repository for RHEL 7.
