%undefine _debugsource_packages
%global postgismajorversion 3.3
%global postgissomajorversion 3
%global postgiscurrmajorversion %(echo %{postgismajorversion}|tr -d '.')
%global sname	postgis

%pgdg_set_gis_variables

# Override some variables. PostGIS 3.3 is best served with GeOS 3.13,
# PROJ 9.5 and GDAL 3.10 (except on RHEL 8 where GDAL 3.8 is available):
%global	geosfullversion %geos313fullversion
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

%global	libspatialitemajorversion      50

%{!?llvm:%global llvm 1}

%{!?utils:%global	utils 1}
%{!?shp2pgsqlgui:%global	shp2pgsqlgui 1}
%{!?raster:%global     raster 1}

%if 0%{?fedora} >= 40 || 0%{?rhel} >= 9 || 0%{?suse_version} >= 1500
%{!?sfcgal:%global	sfcgal 1}
%endif
%if 0%{?rhel} == 8
%ifarch ppc64 ppc64le
%{!?sfcgal:%global	sfcgal 0}
%else
%{!?sfcgal:%global	sfcgal 1}
%endif
%endif

Summary:	Geographic Information Systems Extensions to PostgreSQL
Name:		%{sname}%{postgiscurrmajorversion}_%{pgmajorversion}
Version:	%{postgismajorversion}.8
Release:	5PGDG%{?dist}
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
%if 0%{?fedora} >= 39 || 0%{?rhel} >= 9
BuildRequires:	SFCGAL SFCGAL-devel >= 2.0.0
%endif
%if 0%{?rhel} == 8 || 0%{?suse_version} >= 1500
BuildRequires:	SFCGAL SFCGAL-devel
%endif
%endif
%if %{raster}
BuildRequires:	gdal%{gdalmajorversion}-devel >= %{gdalfullversion}
Requires:	gdal%{gdalmajorversion}-libs >= %{gdalfullversion}
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
BuildRequires:	libxerces-c-devel
%else
Requires:	json-c xerces-c
BuildRequires:	xerces-c-devel
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
Summary:	Just-in-time compilation support for PostGIS 3.3
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 17.0 clang-devel >= 17.0
Requires:	llvm => 17.0
%endif

%description llvmjit
This packages provides JIT support for PostGIS 3.3
%endif

%prep
%setup -q -n %{sname}-%{version}
# Copy .pdf file to top directory before installing.
%{__cp} -p %{SOURCE2} .
%patch -P 0 -p0

%build
LDFLAGS="-Wl,-rpath,%{geosinstdir}/lib64 ${LDFLAGS}" ; export LDFLAGS
LDFLAGS="-Wl,-rpath,%{projinstdir}/lib64 ${LDFLAGS}" ; export LDFLAGS
LDFLAGS="-Wl,-rpath,%{libspatialiteinstdir}/lib ${LDFLAGS}" ; export LDFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{geosinstdir}/lib64" ; export SHLIB_LINK
SFCGAL_LDFLAGS="$SFCGAL_LDFLAGS -L/usr/lib64"; export SFCGAL_LDFLAGS

LDFLAGS="$LDFLAGS -L%{geosinstdir}/lib64 -lgeos_c -L%{projinstdir}/lib64 -L%{gdalinstdir}/lib -L%{libgeotiffinstdir}/lib -ltiff -L/usr/lib64"; export LDFLAGS
CFLAGS="$CFLAGS -I%{gdalinstdir}/include"; export CFLAGS
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:%{projinstdir}/lib64/pkgconfig

autoconf

%configure --with-pgconfig=%{pginstdir}/bin/pg_config \
	--enable-lto \
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
%if 0%{?fedora} >= 39 || 0%{?rhel} >= 8 || 0%{?suse_version} >= 1500
	--with-protobuf \
%else
	--without-protobuf \
%endif
	--enable-rpath --libdir=%{pginstdir}/lib \
	--with-geosconfig=%{geosinstdir}/bin/geos-config \
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
%attr(755,root,root) %{pginstdir}/bin/pgtopo_export
%attr(755,root,root) %{pginstdir}/bin/pgtopo_import

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
* Sat Mar 8 2025 Devrim Gündüz <devrim@gunduz.org> - 3.3.8-5PGDG
- Enable SFCGAL support on RHEL 9 - ppc64le

* Wed Feb 26 2025 Devrim Gündüz <devrim@gunduz.org> - 3.3.8-4PGDG
- Add missing BRs

* Thu Jan 30 2025 Devrim Gündüz <devrim@gunduz.org> - 3.3.8-3PGDG
- Add RHEL 10 support

* Sat Dec 28 2024 Devrim Gündüz <devrim@gunduz.org> - 3.3.8-2PGDG
- Fix SLES 15 builds by adding --with-projdir option back. Also fix
  PROJ path.

* Tue Dec 24 2024 Devrim Gündüz <devrim@gunduz.org> - 3.3.8-1PGDG
- Update to 3.3.8 per changes described at:
  https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.3.8/NEWS
- Rebuild against GDAL 3.10 on Fedora, RHEL 9 and SLES 15.

* Sat Oct 12 2024 Devrim Gündüz <devrim@gunduz.org> - 3.3.7-3PGDG
- Rebuild against SFCGAL 2.0 on RHEL 9 and Fedora

* Sun Sep 22 2024 Devrim Gündüz <devrim@gunduz.org> - 3.3.7-2PGDG
- Rebuild against PROJ 9.5, GeOS 3.13
- Rebuild against GDAL 3.9 on Fedora, RHEL 9 and SLES 15.

* Fri Sep 6 2024 Devrim Gunduz <devrim@gunduz.org> - 3.3.7-1PGDG
- Update to 3.3.7 per changes described at:
  https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.3.7/NEWS

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 3.3.6-4PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Wed Apr 10 2024 Devrim Gunduz <devrim@gunduz.org> - 3.3.6-3PGDG
- Rebuild against PROJ 9.4
- Rebuild against GDAL 3.8 on SLES 15 as well.

* Mon Feb 26 2024 Devrim Gunduz <devrim@gunduz.org> - 3.3.6-2PGDG
- Rebuild against PROJ 9.3
- Rebuild against GDAL 3.8 (except SLES 15, use 3.6 there)

* Fri Feb 9 2024 Devrim Gunduz <devrim@gunduz.org> - 3.3.6-1PGDG
- Update to 3.3.6, per changes described at:
  https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.3.6/NEWS
- Add protobuf support to SLES 15.
- Remove conditionals around raster macro. Already enabled everywhere.

* Mon Nov 20 2023 Devrim Gunduz <devrim@gunduz.org> - 3.3.5-1PGDG
- Update to 3.3.5, per changes described at:
  https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.3.5/NEWS

* Thu Sep 14 2023 Devrim Gunduz <devrim@gunduz.org> - 3.3.4-2PGDG
- Rebuild against GeOS 3.12, Proj 9.2, and libgeotiff 1.7

* Sat Jul 29 2023 Devrim Gunduz <devrim@gunduz.org> - 3.3.4-1PGDG
- Update to 3.3.4, per changes described at:
  https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.3.4/NEWS
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 3.3.3-1.1
- Rebuild against LLVM 15 on SLES 15

* Tue May 30 2023 Devrim Gunduz <devrim@gunduz.org> - 3.3.3-1
- Update to 3.3.3, per changes described at:
  https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.3.3/NEWS

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 3.3.2-5.1
- Modernise %%patch usage, which has been deprecated in Fedora 38

* Thu Apr 6 2023 Devrim Gündüz <devrim@gunduz.org> - 3.3.2-5
- Use Proj 9.2.X, GDAL 3.6 and libgeotiff 1.7 on Fedora 38+

* Thu Mar 23 2023 Devrim Gündüz <devrim@gunduz.org> - 3.3.2-4
- Rebuild against GeOS 3.11.2

* Wed Feb 1 2023 Devrim Gündüz <devrim@gunduz.org>-  3.3.2-3
- Enable raster on SLES 15. We now have all BR and Requires on
  this platform.

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org>-  3.3.2-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Sun Nov 13 2022 Devrim Gunduz <devrim@gunduz.org> - 3.3.2-1
- Update to 3.3.2, per changes described at:
  https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.3.2/NEWS

* Fri Oct 14 2022 Devrim Gunduz <devrim@gunduz.org> - 3.3.1-2
- Use GDAL 3.4 on RHEL 7

* Sat Sep 10 2022 Devrim Gunduz <devrim@gunduz.org> - 3.3.1-1
- Update to 3.3.1 (needed only for PostgreSQL 15 beta 4)

* Sun Aug 28 2022 Devrim Gunduz <devrim@gunduz.org> - 3.3.0-1
- Update to 3.3.0

* Tue Aug 23 2022 Devrim Gunduz <devrim@gunduz.org> - 3.3.0rc2-1
- Update to 3.3.0 rc2

* Fri Aug 19 2022 Devrim Gunduz <devrim@gunduz.org> - 3.3.0rc1-1
- Update to 3.3.0 rc1
- Use PROJ 9.0.X

* Thu Jul 14 2022 Devrim Gunduz <devrim@gunduz.org> - 3.3.0beta2-1
- Update to 3.3.0 beta2

* Wed Jul 13 2022 Devrim Gunduz <devrim@gunduz.org> - 3.3.0beta1-1
- Initial cut for PostGIS 3.3.0 beta 1
