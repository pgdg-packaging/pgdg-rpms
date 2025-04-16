%if 0%{?fedora} >= 38 || 0%{?rhel} >= 8
%global debug_package %{nil}
%endif

%global sname libspatialite
%global libspatialiteinstdir	/usr/%{name}

%global	libspatialitemajorversion	50

%pgdg_set_gis_variables
# Override some variables.
%global geosfullversion %geos313fullversion
%global geosmajorversion %geos313majorversion
%global geosinstdir %geos313instdir

# Override PROJ:
%if 0%{?rhel} == 8
%global	projmajorversion %proj95majorversion
%global	projfullversion %proj95fullversion
%global	projinstdir %proj95instdir
%else
%global	projmajorversion %proj96majorversion
%global	projfullversion %proj96fullversion
%global	projinstdir %proj96instdir
%endif

Name:		%{sname}%{libspatialitemajorversion}
Version:	5.1.0
Release:	8PGDG%{?dist}
Summary:	Enables SQLite to support spatial data
License:	MPLv1.1 or GPLv2+ or LGPLv2+
URL:		https://www.gaia-gis.it/fossil/libspatialite
Source0:	http://www.gaia-gis.it/gaia-sins/%{sname}-sources/%{sname}-%{version}.tar.gz
Source1:	%{name}-pgdg-libs.conf

BuildRequires:	gcc librttopo-devel
BuildRequires:	minizip-devel pgdg-srpm-macros >= 1.0.36
BuildRequires:	geos%{geosmajorversion}-devel >= %{geosfullversion}
BuildRequires:	proj%{projmajorversion}-devel >= %{projfullversion}
BuildRequires:	sqlite-devel zlib-devel libxml2-devel

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

%build
CFLAGS="$CFLAGS -I%{projinstdir}/include"; export CFLAGS
CFLAGS="$CFLAGS -I%{geosinstdir}/include"; export CFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{geosinstdir}/lib64,%{projinstdir}/lib64" ; export SHLIB_LINK

# PROJ 9x uses lib64 as the library path.
LDFLAGS="$LDFLAGS -L%{geosinstdir}/lib64 -L%{projinstdir}/lib64"; export LDFLAGS
./configure \
	--prefix=%{libspatialiteinstdir} \
	--libdir=%{libspatialiteinstdir}/lib \
	--disable-static \
	--enable-freexl=no \
	--with-geosconfig=/%{geosinstdir}/bin/geos-config \
	--with-lwgeom \
%ifarch aarch64
	--build=aarch64-unknown-linux-gnu \
%endif
%ifarch ppc64 ppc64le
	--build=ppc64le-unknown-linux-gnu \
%endif
	--enable-libxml2 \
	--enable-geocallbacks

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

%post devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%files
%doc COPYING AUTHORS
%{libspatialiteinstdir}/lib/%{sname}.so.8*
%{libspatialiteinstdir}/lib/mod_spatialite.so.8*
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
* Wed Apr 16 2025 Devrim Gunduz <devrim@gunduz.org> - 5.1.0-8PGDG
- Rebuild against PROJ 9.6

* Thu Sep 26 2024 Devrim Gunduz <devrim@gunduz.org> - 5.1.0-7PGDG
- Rebuild due to issues with PROJ and GeOS dependency on the build instances

* Thu Sep 19 2024 Devrim Gunduz <devrim@gunduz.org> - 5.1.0-6PGDG
- Rebuild against PROJ 9.5 and GeOS 3.13

* Wed Apr 10 2024 Devrim Gunduz <devrim@gunduz.org> - 5.1.0-5PGDG
- Rebuild against PROJ 9.4

* Mon Apr 8 2024 Devrim Gunduz <devrim@gunduz.org> - 5.1.0-4PGDG
- Fix PROJ library path
- Enable debuginfo packages only on SLES until I can solve the issue.

* Mon Apr 1 2024 Devrim Gunduz <devrim@gunduz.org> - 5.1.0-3PGDG
- Rebuild properly against Proj 9.3

* Mon Jan 29 2024 Devrim Gunduz <devrim@gunduz.org> - 5.1.0-2PGDG
- Rebuild against Proj 9.3
- Spec file cleanup
- re-enable debug package

* Wed Aug 16 2023 Devrim Gunduz <devrim@gunduz.org> - 5.1.0-1PGDG
- Update to 5.1.0
- Build with GeOS 3.12 and Proj 9.0
- Add PGDG branding

* Thu Apr 20 2023 Devrim Gunduz <devrim@gunduz.org> - 5.0.1-6
- Use Proj 9.2.X on Fedora 38+

* Thu Mar 23 2023 Devrim Gunduz <devrim@gunduz.org> - 5.0.1-5
- Rebuild against GeOS 3.11.2

* Wed Oct 19 2022 Devrim Gunduz <devrim@gunduz.org> - 5.0.1-5
- Rebuild against GeOS 3.11.x

* Sat Jan 8 2022 Devrim Gunduz <devrim@gunduz.org> - 5.0.1-4
- Rebuild against Proj 8.2.x and GeOS 3.10.x

* Tue May 18 2021 Devrim Gunduz <devrim@gunduz.org> - 5.0.1-3
- Rebuild against Proj 8.0.1

* Fri Mar 12 2021 Devrim Gunduz <devrim@gunduz.org> - 5.0.1-2
- Rebuild against GeOS 3.9.1 and Proj 8.0.0.

* Mon Feb 15 2021 Devrim Gunduz <devrim@gunduz.org> - 5.0.1-1
- Update to 5.0.1
- Add librttopo dependency

* Sun Dec 20 2020 Devrim Gunduz <devrim@gunduz.org> - 5.0.0-4
- Rebuild against GeOS 3.9.0

* Fri Nov 27 2020 Devrim Gunduz <devrim@gunduz.org> - 5.0.0-3
- Rebuild against PROJ 7.2.0 and GeOS 3.8.0

* Tue Sep 8 2020 Devrim Gunduz <devrim@gunduz.org> - 5.0.0-2
- Add linker config file

* Wed Sep 2 2020 Devrim Gunduz <devrim@gunduz.org> - 5.0.0-1
- Update to 5.0.0

* Tue Aug 18 2020 Devrim Gunduz <devrim@gunduz.org> - 5.0.0RC1-1
- Update to 5.0.0-RC1
- Rebuild against Proj 7.1.0
- Remove patches, no longer needed.

* Mon May 4 2020 Devrim Gunduz <devrim@gunduz.org> - 5.0.0beta0-7
- Rebuild against Proj 7.0.1
- Add missing Requires.

* Wed Mar 11 2020 Devrim Gunduz <devrim@gunduz.org> - 5.0.0beta0-6
- Rebuild against GeOS 3.8.1 and Proj 7.0.0

* Tue Feb 25 2020 Devrim Gunduz <devrim@gunduz.org> - 5.0.0beta0-5
- Rebuild for Proj 6.3.1

* Wed Feb 5 2020 Devrim Gunduz <devrim@gunduz.org> - 5.0.0beta0-4
- Rebuild for Proj 6.3.0

* Fri Oct 11 2019 Devrim Gunduz <devrim@gunduz.org> - 5.0.0beta0-3
- Rebuild for GeOS 3.8.0

* Tue Sep 24 2019 Devrim Gunduz <devrim@gunduz.org> - 5.0.0beta0-2
- Rebuild for GeOS 3.7.2

* Sat Sep 21 2019 Devrim Gunduz <devrim@gunduz.org> - 5.0.0beta0-1
- Initial packaging for PostgreSQL RPM repository, based on Fedora spec file.
