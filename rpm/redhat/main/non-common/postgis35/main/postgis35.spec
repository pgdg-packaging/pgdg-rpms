%undefine _debugsource_packages
%global postgismajorversion 3.5
%global postgissomajorversion 3
%global postgiscurrmajorversion %(echo %{postgismajorversion}|tr -d '.')
%global sname	postgis

%pgdg_set_gis_variables

# Override some variables:
%global	geosfullversion %geos314fullversion
%global	geosmajorversion %geos314majorversion
%global	geosinstdir %geos314instdir
%global	projmajorversion %proj96majorversion
%global	projfullversion %proj96fullversion
%global	projinstdir %proj96instdir

%if 0%{?rhel} && 0%{?rhel} == 8
%global	gdalfullversion %gdal38fullversion
%global	gdalmajorversion %gdal38majorversion
%global	gdalinstdir %gdal38instdir
%else
%global	gdalfullversion %gdal311fullversion
%global	gdalmajorversion %gdal311majorversion
%global	gdalinstdir %gdal311instdir
%endif

%{!?llvm:%global llvm 1}

%{!?utils:%global	utils 1}
%{!?shp2pgsqlgui:%global	shp2pgsqlgui 1}
%{!?raster:%global	raster 1}

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
Version:	%{postgismajorversion}.3
Release:	5PGDG%{?dist}
License:	GPLv2+
Source0:	https://download.osgeo.org/postgis/source/postgis-%{version}.tar.gz
Source2:	https://download.osgeo.org/postgis/docs/postgis-%{version}-en.pdf
Source4:	%{sname}%{postgiscurrmajorversion}-filter-requires-perl-Pg.sh

URL:		https://www.postgis.net/

BuildRequires:	postgresql%{pgmajorversion}-devel geos%{geosmajorversion}-devel >= %{geosfullversion}
BuildRequires:	libgeotiff%{libgeotiffmajorversion}-devel libxml2 libxslt
BuildRequires:	pgdg-srpm-macros >= 1.0.50 gmp-devel
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
%if 0%{?fedora} >= 41 || 0%{?rhel} >= 9
BuildRequires:	SFCGAL SFCGAL-devel >= 2.1.0
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
Requires:	gdal%{gdalmajorversion}-libs >= %{gdalfullversion}
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
Summary:	Just-in-time compilation support for PostGIS 3.5
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
This package provides JIT support for PostGIS 3.5
%endif

%prep
%setup -q -n %{sname}-%{version}
# Copy .pdf file to top directory before installing.
%{__cp} -p %{SOURCE2} %{sname}-%{version}.pdf

%build
LDFLAGS="-Wl,-rpath,%{geosinstdir}/lib64 ${LDFLAGS}" ; export LDFLAGS
LDFLAGS="-Wl,-rpath,%{projinstdir}/lib64 ${LDFLAGS}" ; export LDFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{geosinstdir}/lib64" ; export SHLIB_LINK
SFCGAL_LDFLAGS="$SFCGAL_LDFLAGS -L/usr/lib64"; export SFCGAL_LDFLAGS

LDFLAGS="$LDFLAGS -L%{geosinstdir}/lib64 -lgeos_c -L%{projinstdir}/lib64 -L%{gdalinstdir}/lib -L%{libgeotiffinstdir}/lib -ltiff -L/usr/lib64"; export LDFLAGS
CFLAGS="$CFLAGS -I%{gdalinstdir}/include"; export CFLAGS
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:%{projinstdir}/lib64/pkgconfig

autoconf

%configure --with-pgconfig=%{pginstdir}/bin/pg_config \
	--bindir=%{pginstdir}/bin/ \
	--datadir=%{pginstdir}/share/ \
	--mandir=%{_mandir}/%{name} \
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
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 8 || 0%{?suse_version} >= 1500
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
%{pginstdir}/bin/postgis
%{pginstdir}/bin/postgis_restore
%{pginstdir}/doc/extension/README.address_standardizer
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_comments.sql
%{pginstdir}/share/contrib/%{sname}-%{postgismajorversion}/postgis_upgrade*.sql
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
%{_mandir}/%{name}/man1/*

%files client
%defattr(644,root,root)
%attr(755,root,root) %{pginstdir}/bin/pgsql2shp
%if %{raster}
%attr(755,root,root) %{pginstdir}/bin/raster2pgsql
%endif
%attr(755,root,root) %{pginstdir}/bin/shp2pgsql
%attr(755,root,root) %{pginstdir}/bin/pgtopo_export
%attr(755,root,root) %{pginstdir}/bin/pgtopo_import
%{_mandir}/%{name}/man1/pgsql2shp*
%{_mandir}/%{name}/man1/pgtopo_*
%{_mandir}/%{name}/man1/shp2pgsql*

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
   %if %{raster}
     %{pginstdir}/lib/bitcode/postgis_raster-%{postgissomajorversion}*.bc
     %{pginstdir}/lib/bitcode/postgis_raster-%{postgissomajorversion}/*.bc
   %endif
   %if %{sfcgal}
   %{pginstdir}/lib/bitcode/postgis_sfcgal-%{postgissomajorversion}.index.bc
   %{pginstdir}/lib/bitcode/postgis_sfcgal-%{postgissomajorversion}/lwgeom_sfcgal.bc
   %{pginstdir}/lib/bitcode/postgis_sfcgal-%{postgissomajorversion}/postgis_sfcgal_legacy.bc
   %endif
%endif

%if %utils
%files utils
%defattr(-,root,root)
%doc utils/README
%attr(755,root,root) %{_datadir}/%{name}/*.pl
%endif

%changelog
* Wed Aug 27 2025 Devrim Gündüz <devrim@gunduz.org> - 3.5.3-5PGDG
- Rebuild against GeOS 3.14

* Thu Jul 31 2025 Devrim Gündüz <devrim@gunduz.org> - 3.5.3-4PGDG
- Rebuild against GDAL 3.11.3

* Thu Jul 17 2025 Devrim Gündüz <devrim@gunduz.org> - 3.5.3-3PGDG
- Use GDAL 3.11 and PROJ 9.6 on RHEL 8 and SLES 15 as well.

* Sun Jun 1 2025 Devrim Gündüz <devrim@gunduz.org> - 3.5.3-2PGDG
- Fix SLES 15 linker issue.

* Tue May 20 2025 Devrim Gündüz <devrim@gunduz.org> - 3.5.3-1PGDG
- Update to 3.5.3 per changes described at:
  https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.5.3/NEWS
- Keep using PROJ 9.5 and GDAL 3.10. Use GDAL 3.11 where available.

* Wed Apr 16 2025 Devrim Gündüz <devrim@gunduz.org> - 3.5.2-5PGDG
- Rebuild against PROJ 9.6

* Sat Mar 8 2025 Devrim Gündüz <devrim@gunduz.org> - 3.5.2-4PGDG
- Enable SFCGAL support on RHEL 9 - ppc64le

* Wed Feb 26 2025 Devrim Gündüz <devrim@gunduz.org> - 3.5.2-3PGDG
- Add missing BRs

* Thu Jan 30 2025 Devrim Gündüz <devrim@gunduz.org> - 3.5.2-2PGDG
- Add RHEL 10 support

* Thu Jan 23 2025 Devrim Gündüz <devrim@gunduz.org> - 3.5.2-1PGDG
- Update to 3.5.2 per changes described at:
  https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.5.2/NEWS

* Sat Dec 28 2024 Devrim Gündüz <devrim@gunduz.org> - 3.5.1-2PGDG
* Fix SLES 15 builds by adding --with-projdir option back. Also fix
  PROJ path.

* Tue Dec 24 2024 Devrim Gündüz <devrim@gunduz.org> - 3.5.1-1PGDG
- Update to 3.5.1 per changes described at:
  https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.5.1/NEWS
- Rebuild against GDAL 3.10 on Fedora, RHEL 9 and SLES 15.

* Wed Dec 18 2024 Devrim Gündüz <devrim@gunduz.org> - 3.5.0-4PGDG
- Fix changelog date

* Sun Nov 3 2024 Devrim Gündüz <devrim@gunduz.org> - 3.5.0-3PGDG
- Install man files to another location to avoid packaging conflict
  with other PostGIS RPMs.

* Sat Oct 12 2024 Devrim Gündüz <devrim@gunduz.org> - 3.5.0-2PGDG
- Rebuild against SFCGAL 2.0.0 on RHEL 9 and Fedora

* Thu Sep 26 2024 Devrim Gündüz <devrim@gunduz.org> - 3.5.0-1PGDG
- Update to 3.5.0 per changes described at:
  https://git.osgeo.org/gitea/postgis/postgis/raw/tag/3.5.0/NEWS

* Mon Sep 23 2024 Devrim Gündüz <devrim@gunduz.org> - 3.5.0rc1-1PGDG
- Update to 3.5.0 RC1

* Mon Sep 16 2024 Devrim Gündüz <devrim@gunduz.org> - 3.5.0beta1-1PGDG
- Update to 3.5.0 beta1
- Rebuild against PROJ 9.5, GeOS 3.13
- Rebuild against GDAL 3.9 on Fedora, RHEL 9 and SLES 15.

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 3.5.0alpha2-2PGDG
- Update LLVM dependencies

* Tue Jul 9 2024 Devrim Gunduz <devrim@gunduz.org> - 3.5.0alpha2-1PGDG
- Update to 3.5.0 Alpha2

* Fri Jul 5 2024 Devrim Gunduz <devrim@gunduz.org> - 3.5.0alpha1-1PGDG
- Initial cut for PostGIS 3.5.0 alpha1
