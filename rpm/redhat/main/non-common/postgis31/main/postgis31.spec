%undefine _debugsource_packages
%global postgismajorversion 3.1
%global postgissomajorversion 3
%global postgiscurrmajorversion %(echo %{postgismajorversion}|tr -d '.')
%global sname	postgis

%pgdg_set_gis_variables

# Override some variables. PostGIS 3.2 is best served with GeOS 3.13,
# PROJ 9.5 and GDAL 3.10 (except on RHEL 8 where GDAL 3.8 is available):
%global	geosfullversion	%geos313fullversion
%global	geosmajorversion %geos313majorversion
%global	geosinstdir %geos313instdir
%if 0%{?rhel} == 8
%global	gdalfullversion %gdal38fullversion
%global	gdalmajorversion %gdal38majorversion
%global	gdalinstdir %gdal38instdir
%else
%global	gdalfullversion %gdal310fullversion
%global	gdalmajorversion %gdal310majorversion
%global	gdalinstdir %gdal310instdir
%endif
%global	projmajorversion %proj95majorversion
%global	projfullversion %proj95fullversion
%global	projinstdir %proj95instdir

%global	libgeotiffmajorversion 17
%global	libgeotiffinstdir %libgeotiff17instdir

%global	libspatialitemajorversion	50

%{!?llvm:%global llvm 1}

%{!?utils:%global	utils 1}
%{!?shp2pgsqlgui:%global	shp2pgsqlgui 1}
%{!?raster:%global	raster 1}

%if 0%{?fedora} >= 39 || 0%{?rhel} >= 8 || 0%{?suse_version} >= 1500
%ifnarch ppc64 ppc64le
# TODO
%{!?sfcgal:%global	sfcgal 1}
%else
%{!?sfcgal:%global	sfcgal 0}
%endif
%else
%{!?sfcgal:%global	sfcgal 0}
%endif

Summary:	Geographic Information Systems Extensions to PostgreSQL
Name:		%{sname}%{postgiscurrmajorversion}_%{pgmajorversion}
Version:	%{postgismajorversion}.12
Release:	4PGDG%{?dist}
License:	GPLv2+
Source0:	https://download.osgeo.org/postgis/source/postgis-%{version}.tar.gz
Source2:	https://download.osgeo.org/postgis/docs/postgis-%{version}.pdf
Source4:	%{sname}%{postgiscurrmajorversion}-filter-requires-perl-Pg.sh
Patch0:		%{sname}%{postgiscurrmajorversion}-%{postgismajorversion}.0-gdalfpic.patch

URL:		https://www.postgis.net/

BuildRequires:	postgresql%{pgmajorversion}-devel geos%{geosmajorversion}-devel >= %{geosfullversion}
BuildRequires:	libgeotiff%{libgeotiffmajorversion}-devel libxml2 libxslt autoconf
BuildRequires:	pgdg-srpm-macros >= 1.0.45 gmp-devel
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 10
BuildRequires:	pcre2-devel
Requires:	pcre2
%else
BuildRequires:	pcre-devel
Requires:	pcre
%endif
%if 0%{?suse_version} >= 1500
Requires:	libgmp10
%else
Requires:	gmp
%endif
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1500
BuildRequires:	libjson-c-devel proj%{projmajorversion}-devel >= %{projfullversion}
%endif
%else
BuildRequires:	proj%{projmajorversion}-devel >= %{projfullversion} flex json-c-devel
%endif
BuildRequires:	libxml2-devel
%if %{shp2pgsqlgui}
BuildRequires:	gtk2-devel > 2.8.0
%endif
%if %{sfcgal}
BuildRequires:	SFCGAL-devel SFCGAL
Requires:	SFCGAL
%endif
%if %{raster}
BuildRequires:	gdal%{gdalmajorversion}-devel >= %{gdalfullversion}
%endif

%if 0%{?suse_version} >= 1500
Requires:	libprotobuf-c1
BuildRequires:	libprotobuf-c-devel
%else
# Fedora/RHEL:
Requires:	protobuf-c >= 1.1.0
BuildRequires:	protobuf-c-devel >= 1.1.0
%endif

Requires:	postgresql%{pgmajorversion} geos%{geosmajorversion} >= %{geosfullversion}
Requires:	postgresql%{pgmajorversion}-contrib proj%{projmajorversion} >= %{projfullversion}
Requires:	libgeotiff%{libgeotiffmajorversion}
Requires:	hdf5

%if %{raster}
Requires:	gdal%{gdalmajorversion}-libs >= %{gdalfullversion}
%endif

%if 0%{?suse_version} >= 1500
Requires:	libjson-c5
Requires:	libxerces-c-3_2
%endif
%if 0%{?rhel} || 0%{?fedora}
Requires:	json-c xerces-c
%endif
Requires(post):	%{_sbindir}/update-alternatives

Provides:	%{sname} = %{version}-%{release}
Obsoletes:	%{sname}3_%{pgmajorversion} <= %{postgismajorversion}.0-1
Provides:	%{sname}3_%{pgmajorversion} => %{postgismajorversion}.0

%description
PostGIS adds support for geographic objects to the PostgreSQL object-relational
database. In effect, PostGIS "spatially enables" the PostgreSQL server,
allowing it to be used as a backend spatial database for geographic information
systems (GIS), much like ESRI's SDE or Oracle's Spatial extension. PostGIS
follows the OpenGIS "Simple Features Specification for SQL" and has been
certified as compliant with the "Types and Functions" profile.

%package client
Summary:	Client tools and their libraries of PostGIS
Requires:	%{name}%{?_isa} = %{version}-%{release}
Provides:	%{sname}-client = %{version}-%{release}
Obsoletes:	%{sname}2_%{pgmajorversion}-client <= %{postgismajorversion}.2-1
Provides:	%{sname}2_%{pgmajorversion}-client => %{postgismajorversion}.0

%description client
The %{name}-client package contains the client tools and their libraries
of PostGIS.

%package devel
Summary:	Development headers and libraries for PostGIS
Requires:	%{name}%{?_isa} = %{version}-%{release}
Provides:	%{sname}-devel = %{version}-%{release}
Obsoletes:	%{sname}2_%{pgmajorversion}-devel <= %{postgismajorversion}.2-1
Provides:	%{sname}2_%{pgmajorversion}-devel => %{postgismajorversion}.0

%description devel
The %{name}-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with PostGIS.

%package docs
Summary:	Extra documentation for PostGIS
Obsoletes:	%{sname}2_%{pgmajorversion}-docs <= %{postgismajorversion}.2-1
Provides:	%{sname}2_%{pgmajorversion}-docs => %{postgismajorversion}.0

%description docs
The %{name}-docs package includes PDF documentation of PostGIS.

%if %{shp2pgsqlgui}
%package	gui
Summary:	GUI for PostGIS
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	gui
The %{name}-gui package provides a gui for PostGIS.
%endif

%if %utils
%package utils
Summary:	The utils for PostGIS
Requires:	%{name} = %{version}-%{release} perl-DBD-Pg
Provides:	%{sname}-utils = %{version}-%{release}
Obsoletes:	%{sname}2_%{pgmajorversion}-utils <= %{postgismajorversion}.2-1
Provides:	%{sname}2_%{pgmajorversion}-utils => %{postgismajorversion}.0

%description utils
The %{name}-utils package provides the utilities for PostGIS.
%endif

%global __perl_requires %{SOURCE4}

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for postgis31
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 13.0 clang-devel >= 13.0
Requires:	llvm => 13.0
%endif

%description llvmjit
This packages provides JIT support for postgis31
%endif

%prep
%setup -q -n %{sname}-%{version}
# Copy .pdf file to top directory before installing.
%{__cp} -p %{SOURCE2} .
%patch -P 0 -p0

%build
LDFLAGS="-Wl,-rpath,%{geosinstdir}/lib64 ${LDFLAGS}" ; export LDFLAGS
# PROJ 9x uses lib64 as the library path.
LDFLAGS="$LDFLAGS -L%{geosinstdir}/lib64 -L%{projinstdir}/lib64"; export LDFLAGS
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:%{projinstdir}/lib64/pkgconfig
LDFLAGS="-Wl,-rpath,%{libspatialiteinstdir}/lib ${LDFLAGS}" ; export LDFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{geosinstdir}/lib64" ; export SHLIB_LINK
SFCGAL_LDFLAGS="$SFCGAL_LDFLAGS -L/usr/lib64"; export SFCGAL_LDFLAGS

LDFLAGS="$LDFLAGS -L%{geosinstdir}/lib64 -lgeos_c -L%{projinstdir}/lib64 -L%{gdalinstdir}/lib -L%{libgeotiffinstdir}/lib -ltiff -L/usr/lib64"; export LDFLAGS
CFLAGS="$CFLAGS -I%{gdalinstdir}/include"; export CFLAGS

autoconf

%configure --with-pgconfig=%{pginstdir}/bin/pg_config \
	--with-projdir=%{projinstdir} \
%if !%raster
	--without-raster \
%endif
%if %{sfcgal}
	--with-sfcgal=%{_bindir}/sfcgal-config \
%endif
%if %{shp2pgsqlgui}
	--with-gui \
%endif
%if 0%{?fedora} >= 38 || 0%{?rhel} >= 8 || 0%{?suse_version} >= 1500
	--with-protobuf \
%else
	--without-protobuf \
%endif
	--with-projdir=%{projinstdir} \
	--enable-rpath --libdir=%{pginstdir}/lib \
	--with-geosconfig=/%{geosinstdir}/bin/geos-config \
	--with-gdalconfig=%{gdalinstdir}/bin/gdal-config

SHLIB_LINK="$SHLIB_LINK" %{__make} LPATH=`%{pginstdir}/bin/pg_config --pkglibdir` shlib="%{sname}-%{postgissomajorversion}.so"

%{__make} %{?_smp_mflags} -C extensions

%if %utils
 SHLIB_LINK="$SHLIB_LINK" %{__make} %{?_smp_mflags} -C utils
%endif

%install
%{__rm} -rf %{buildroot}
SHLIB_LINK="$SHLIB_LINK" %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%if %utils
%{__install} -d %{buildroot}%{_datadir}/%{name}
%{__install} -m 644 utils/*.pl %{buildroot}%{_datadir}/%{name}
%endif

# Create alternatives entries for common binaries
%post client
%{_sbindir}/update-alternatives --install %{_bindir}/pgsql2shp postgis-pgsql2shp %{pginstdir}/bin/pgsql2shp %{pgmajorversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/shp2pgsql postgis-shp2pgsql %{pginstdir}/bin/shp2pgsql %{pgmajorversion}0

# Drop alternatives entries for common binaries and man files
%postun client
if [ "$1" -eq 0 ]
  then
	# Only remove these links if the package is completely removed from the system (vs.just being upgraded)
	%{_sbindir}/update-alternatives --remove postgis-pgsql2shp	%{_bindir}/bin/pgsql2shp
	%{_sbindir}/update-alternatives --remove postgis-shp2pgsql	%{_bindir}/bin/shp2pgsql
fi

%files
%defattr(-,root,root)
%doc COPYING CREDITS NEWS TODO README.%{sname} doc/html loader/README.* doc/%{sname}.xml doc/ZMSgeoms.txt
%license LICENSE.TXT
%{pginstdir}/doc/extension/README.address_standardizer
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_comments.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_upgrade*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_restore.pl
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/uninstall_postgis.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/legacy*.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/*topology*.sql
%{pginstdir}/lib/%{sname}-%{postgissomajorversion}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%if %{sfcgal}
%{pginstdir}/lib/%{sname}_sfcgal-%{postgissomajorversion}.so
%{pginstdir}/share/extension/%{sname}_sfcgal*.sql
%{pginstdir}/share/extension/%{sname}_sfcgal.control
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/sfcgal.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/sfcgal_upgrade.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/uninstall_sfcgal.sql
%endif
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/lib/%{sname}_topology-%{postgissomajorversion}.so
%{pginstdir}/lib/address_standardizer-3.so
%{pginstdir}/share/extension/address_standardizer*.sql
%{pginstdir}/share/extension/address_standardizer*.control
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/sfcgal_comments.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/raster_comments.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/spatial*.sql
%{pginstdir}/share/extension/%{sname}_tiger_geocoder*.sql
%{pginstdir}/share/extension/%{sname}_tiger_geocoder.control
%{pginstdir}/share/extension/%{sname}_topology-*.sql
%{pginstdir}/share/extension/%{sname}_topology.control
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/uninstall_legacy.sql
%if %{raster}
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/rtpostgis.sql
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/rtpostgis_legacy.sql
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/rtpostgis_upgrade.sql
%{pginstdir}/share/contrib/postgis-%{postgismajorversion}/uninstall_rtpostgis.sql
%{pginstdir}/share/extension/postgis_raster*.sql
%{pginstdir}/lib/postgis_raster-%{postgissomajorversion}.so
%{pginstdir}/share/extension/%{sname}_raster.control
%endif

%files client
%defattr(644,root,root)
%attr(755,root,root) %{pginstdir}/bin/pgsql2shp
%if %{raster}
%attr(755,root,root) %{pginstdir}/bin/raster2pgsql
%endif
%attr(755,root,root) %{pginstdir}/bin/shp2pgsql

%files devel
%defattr(644,root,root)

%files docs
%defattr(-,root,root)
%doc %{sname}-%{version}.pdf

%if %shp2pgsqlgui
%files gui
%defattr(-,root,root)
%{pginstdir}/bin/shp2pgsql-gui
%{pginstdir}/share/applications/shp2pgsql-gui.desktop
%{pginstdir}/share/icons/hicolor/*/apps/shp2pgsql-gui.png
%endif

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/address_standardizer*.bc
   %{pginstdir}/lib/bitcode/address_standardizer-3/*.bc
   %{pginstdir}/lib/bitcode/postgis-%{postgissomajorversion}*.bc
   %{pginstdir}/lib/bitcode/postgis_topology-%{postgissomajorversion}/*.bc
   %{pginstdir}/lib/bitcode/postgis_topology-%{postgissomajorversion}*.bc
   %{pginstdir}/lib/bitcode/postgis-%{postgissomajorversion}/*.bc
   %if %raster
    %{pginstdir}/lib/bitcode/postgis_raster-%{postgissomajorversion}*.bc
    %{pginstdir}/lib/bitcode/postgis_raster-%{postgissomajorversion}/*.bc
   %endif
   %if %{sfcgal}
   %{pginstdir}/lib/bitcode/postgis_sfcgal-%{postgissomajorversion}.index.bc
   %{pginstdir}/lib/bitcode/postgis_sfcgal-%{postgissomajorversion}/lwgeom_sfcgal.bc
   %endif
%endif

%if %utils
%files utils
%defattr(-,root,root)
%doc utils/README
%attr(755,root,root) %{_datadir}/%{name}/*.pl
%endif

%changelog
* Wed Feb 26 2025 Devrim Gündüz <devrim@gunduz.org> - 3.1.12-4PGDG
- Add missing BR

* Thu Jan 30 2025 Devrim Gündüz <devrim@gunduz.org> - 3.1.12-3PGDG
- Add RHEL 10 support

* Sat Dec 28 2024 Devrim Gunduz <devrim@gunduz.org> - 3.1.12-2PGDG
- Fix SLES 15 builds by adding --with-projdir option back. Also fix
  PROJ path.

* Tue Dec 24 2024 Devrim Gunduz <devrim@gunduz.org> - 3.1.12-1PGDG
- Update to 3.1.12, per changes described at:
  https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.1.12/NEWS
- Rebuild against GDAL 3.10 on Fedora, RHEL 9 and SLES 15.

* Mon Dec 9 2024 Devrim Gündüz <devrim@gunduz.org> - 3.1.11-6PGDG
- Rebuild against SFCGAL 2.0 on RHEL 9 and Fedora
- Rebuild against PROJ 9.5, GeOS 3.13
- Rebuild against GDAL 3.9 on Fedora, RHEL 9 and SLES 15.

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 3.1.11-4PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Wed Apr 10 2024 Devrim Gunduz <devrim@gunduz.org> - 3.1.11-3PGDG
- Rebuild against PROJ 9.4
- Rebuild against GDAL 3.8 on SLES 15 as well.

* Mon Feb 26 2024 Devrim Gunduz <devrim@gunduz.org> - 3.11-2PGDG
- Rebuild against PROJ 9.3
- Rebuild against GDAL 3.8 (except SLES 15, use 3.6 there)

* Fri Feb 9 2024 Devrim Gunduz <devrim@gunduz.org> - 3.1.11-1PGDG
- Update to 3.1.11, per changes described at:
  https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.1.11/NEWS
- Add protobuf support to SLES 15

* Mon Nov 20 2023 Devrim Gunduz <devrim@gunduz.org> - 3.1.10-1PGDG
- Update to 3.1.10, per changes described at:
  https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.1.10/NEWS

* Sun Oct 22 2023 Devrim Gunduz <devrim@gunduz.org> - 3.1.9-3PGDG
- Do not override dependencies on Fedora 38+.

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 3.1.9-2PGDG
- Rebuild against GeOS 3.12, Proj 9.2, and libgeotiff 1.7
- Add PGDG branding
- Cleanup rpmlint warnings

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 3.1.9-1.1
- Rebuild against LLVM 15 on SLES 15

* Tue May 30 2023 Devrim Gunduz <devrim@gunduz.org> - 3.1.9-1
- Update to 3.1.9, per changes described at:
  https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.1.9/NEWS

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 3.1.8-6.1
- Modernise %%patch usage, which has been deprecated in Fedora 38

* Fri Apr 21 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.8-6
- Use Proj 9.2.X, GeOS 3.11, GDAL 3.6 and libgeotiff 1.7 on Fedora 38+

* Thu Mar 23 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.8-5
- Rebuild against GeOS 3.11.2

* Tue Jan 10 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.8-4
- Match libspatialite dependency with GDAL34 package on SLES 15.

* Fri Jan 6 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.8-3
- Fix SLES 15 dependency, per report from Muralikrishna Bandaru.

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 3.1.8-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Sun Nov 13 2022 Devrim Gunduz <devrim@gunduz.org> - 3.1.8-1
- Update to 3.1.8, per changes described at:
  https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.1.8/NEWS

* Thu Oct 20 2022 Devrim Gunduz <devrim@gunduz.org> - 3.1.7-2
- Switch to GDAL 3.4 and GeOS 3.10

* Fri Aug 19 2022 Devrim Gunduz <devrim@gunduz.org> - 3.1.7-1
- Update to 3.1.7, per changes described at:
  https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.1.7/NEWS

* Thu Jul 21 2022 Devrim Gunduz <devrim@gunduz.org> - 3.1.6-1
- Update to 3.1.6, per changes described at:
  https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.1.6/NEWS

* Mon Feb 7 2022 Devrim Gunduz <devrim@gunduz.org> - 3.1.5-1
- Update to 3.1.5, per changes described at:
  https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.1.5/NEWS

* Thu Dec 9 2021 Devrim Gunduz <devrim@gunduz.org> - 3.1.4-3
- Enable raster support on SLES 15. We now have all dependencies
  in the repo.

* Wed Oct 6 2021 Devrim Gunduz <devrim@gunduz.org> - 3.1.4-2
- Add SLES 12 support.

* Wed Sep 8 2021 Devrim Gunduz <devrim@gunduz.org> - 3.1.4-1
- Update to 3.1.4, per changes described at:
  https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.1.4/NEWS

* Thu Aug 26 2021 Devrim Gunduz <devrim@gunduz.org> - 3.1.3-2
- Rebuild against Proj 8.1.0 and GDAL 3.3.1

* Sun Jul 4 2021 Devrim Gunduz <devrim@gunduz.org> - 3.1.3-1
- Update to 3.1.3

* Thu Jun 10 2021 Devrim Gunduz <devrim@gunduz.org> - 3.1.2-2
- Fix builds on RHEL 8 - ppc64le

* Wed May 26 2021 Devrim Gunduz <devrim@gunduz.org> - 3.1.2-1
- Update to 3.1.2, per changes described at:
  https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.1.2/NEWS
- Remove PROJ 8.0 patch, now in 3.1.2.

* Tue May 18 2021 Devrim Gunduz <devrim@gunduz.org> - 3.1.1-5
- Rebuild against Proj 8.0.1 and GDAL 3.2.3

* Sun Mar 28 2021 Devrim Gunduz <devrim@gunduz.org> - 3.1.1-4
- Add a patch to support PROJ 8.0, too. Could be removed in
  next minor version.

* Mon Mar 22 2021 Devrim Gunduz <devrim@gunduz.org> - 3.1.1-3
- Emergency RHEL 7 patches

* Sun Mar 21 2021 Devrim Gunduz <devrim@gunduz.org> - 3.1.1-2
- Rebuild against Proj 8.0.0 (except on RHEL 7) and GeOS 3.9.1
- Override PROJ major version on RHEL 7. libspatialite 4.3
  does not build against 8.0.0 as of March 2021.

* Sun Jan 31 2021 Devrim Gunduz <devrim@gunduz.org> - 3.1.1-1
- Update to 3.1.1

* Wed Jan 27 2021 Devrim Gunduz <devrim@gunduz.org> - 3.1.0-2
- Disable raster support on SLES (15), because of missing
  build dependencies for GDAL.

* Sun Dec 20 2020 Devrim Gunduz <devrim@gunduz.org> - 3.1.0-1
- Update to 3.1.0
- Final fix for the rpath issues, where OS supplied GEOS and Proj
  packages are installed alongside ours.
- Disable MVT and Geobuf support on RHEL 7 (min 1.1.0 is required)

* Wed Nov 25 2020 Devrim Gunduz <devrim@gunduz.org> - 3.1.0-alpha2_4
- Update to 3.1.0-alpha3

* Fri Oct 30 2020 Devrim Gunduz <devrim@gunduz.org> - 3.1.0-alpha2_4
- Rebuild against new GDAL and new PROJ.

* Fri Oct 30 2020 Devrim Gunduz <devrim@gunduz.org> - 3.1.0-alpha2_3
- Fix various rpath issues, per Sandeep Thakkar.

* Tue Sep 29 2020 Devrim Gunduz <devrim@gunduz.org> - 3.1.0-alpha2_2
- Rebuild against GDAL and libgeotiff 1.6

* Tue Jul 28 2020 Devrim Gunduz <devrim@gunduz.org> - 3.1.0-alpha2_1
- Update to 3.1 alpha2

* Sun May 24 2020 Devrim Gunduz <devrim@gunduz.org> - 3.1.0-alpha1_1
- Initial cut for PostGIS 3.1.0 Alpha 1

* Tue May 5 2020 Devrim Gunduz <devrim@gunduz.org> - 3.0.1-5
- Rebuild against Proj 7.0.1

* Thu Mar 12 2020 Devrim Gunduz <devrim@gunduz.org> - 3.0.1-4
- Rebuild against Proj 7.0.0 and GeOS 3.8.1
- Make sure that the package requires exact versions of Proj and GeOS.

* Thu Mar 12 2020 Devrim Gunduz <devrim@gunduz.org> - 3.0.1-3
- Fix alternatives error

* Tue Feb 25 2020 Devrim Gunduz <devrim@gunduz.org> - 3.0.1-2
- Use pkgconfig for Proj support, per warnings.

* Tue Feb 25 2020 Devrim Gunduz <devrim@gunduz.org> - 3.0.1-1
- Update to 3.0.1

* Wed Feb 5 2020 Devrim Gunduz <devrim@gunduz.org> - 3.0.0-2
- Rebuild for Proj 6.3.0 and GDAL 3.0.4

* Fri Oct 25 2019 Devrim Gunduz <devrim@gunduz.org> - 3.0.0-1
- Update to 3.0.0

* Wed Oct 16 2019 Devrim Gunduz <devrim@gunduz.org> - 3.0.0rc2
- Update to 3.0.0rc2

* Fri Oct 11 2019 Devrim Gunduz <devrim@gunduz.org> - 3.0.0rc1
- Update to rc1

* Fri Oct 4 2019 Devrim Gunduz <devrim@gunduz.org> - 3.0.0beta1
- Update to beta1
- Use Geos 3.8

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Tue Sep 24 2019 Devrim Gunduz <devrim@gunduz.org> - 3.0.0alpha4-6
- Fix broken symlink, per report from Paul Ramsey:
  https://redmine.postgresql.org/issues/4776

* Tue Sep 24 2019 Devrim Gunduz <devrim@gunduz.org> - 3.0.0alpha4-5
- Rebuild for GeOS 3.7.2

* Tue Sep 17 2019 Devrim Gündüz <devrim@gunduz.org> - 3.0.0alpha4-4
- Update GDAL dependency to 3.0.1
- Use a few more macros for easier maintenance.

* Tue Sep 3 2019 Devrim Gündüz <devrim@gunduz.org> - 3.0.0alpha4-3
- Update Proj to 6.2

* Thu Aug 29 2019 Devrim Gündüz <devrim@gunduz.org> - 3.0.0alpha4-2
- PostGIS 30: Use a few more macros, and also update Proj dependency to 6.1
- Add xerces-c dependency, per https://redmine.postgresql.org/issues/4672

* Sun Aug 11 2019 Devrim Gündüz <devrim@gunduz.org> - 3.0.0alpha4-1
- Update to 3.0.0 Alpha 4

* Thu Jun 27 2019 Devrim Gündüz <devrim@gunduz.org> - 3.0.0alpha2-4
- Add protobuf dependency only for RHEL 8 and Fedora, per
  https://redmine.postgresql.org/issues/4390#note-3

* Thu Jun 27 2019 Devrim Gündüz <devrim@gunduz.org> - 3.0.0alpha2-3
- Obsolete correct version. Patch from Alan Ivey

* Thu Jun 27 2019 Devrim Gündüz <devrim@gunduz.org> - 3.0.0alpha2-2
- Add protobuf-c dependency, so that related functions can be used.
  Per https://redmine.postgresql.org/issues/4390

* Wed Jun 5 2019 Devrim Gündüz <devrim@gunduz.org> - 3.0.0alpha2-1
- Initial cut for PostGIS 3.0.0 Alpha 2
