%global sname gdal
%global gdalmajorversion 3.13

%if 0%{?fedora} >= 43 || 0%{?rhel} >= 9 || 0%{?suse_version} >= 1600 || 0%{?amzn} == 2023
%global gdal_python_enabled 1
%{!?gdaljava:%global gdaljava 1}
%else
%global gdal_python_enabled 0
%{!?gdaljava:%global gdaljava 0}
%endif

%if 0%{?fedora} && 0%{?fedora} == 45
%global __ospython %{_bindir}/python3.15
%global python3_pkgversion 3.15
%endif
%if 0%{?fedora} && 0%{?fedora} <= 44 && ! 0%{?amzn}
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?suse_version} == 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

%pgdg_set_gis_variables

%if %gdal_python_enabled
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%endif

%global bashcompletiondir %(pkg-config --variable=compatdir bash-completion)

%global geosfullversion %geos315fullversion
%global geosmajorversion %geos315majorversion
%global geosinstdir %geos315instdir

%global gdalinstdir /usr/%{name}
%global gdalsomajorversion	39
%global libspatialitemajorversion	50

%if 0%{?rhel} && 0%{?rhel} == 8
%global projmajorversion %proj96majorversion
%global projfullversion %proj96fullversion
%global projinstdir %proj96instdir
%else
%global projmajorversion %proj98majorversion
%global projfullversion %proj98fullversion
%global projinstdir %proj98instdir
%endif

%if 0%{?suse_version} <= 1600
%global	g2clib_enabled 0
%else
%global	g2clib_enabled 1
%endif

# Enable/disable generating refmans
# texlive currently broken deps and FTBFS in rawhide
%global build_refman 0
# https://bugzilla.redhat.com/show_bug.cgi?id=1490492

Name:		%{sname}313
Version:	%{gdalmajorversion}.3
Release:	9PGDG%{?dist}
Summary:	GIS file format library
License:	MIT
URL:		https://www.gdal.org
# Source0: https://download.osgeo.org/gdal/%%{version}/gdal-%%{version}.tar.xz
# See PROVENANCE.TXT-fedora and the cleaner script for details!

Source0:	https://download.postgresql.org/pub/repos/yum/sources/gdal/%{gdalmajorversion}/gdal-%{version}-fedora.tar.xz
Source4:	PROVENANCE.TXT-fedora

# Cleaner script for the tarball
Source5:	%{sname}-cleaner.sh

Source6:	%{name}-pgdg-libs.conf

Patch0:		%{name}-cleanup.patch

# lz4 and bash-completion dependencies
%if 0%{?suse_version} >= 1500
BuildRequires:	liblz4-devel bash-completion-devel
Requires:	liblz4-1
%endif
%if 0%{?rhel} || 0%{?fedora} || 0%{?amzn}
BuildRequires:	lz4-devel bash-completion
Requires:	lz4
%endif

BuildRequires:	ant cmake gcc-c++ bison pgdg-srpm-macros >= 1.0.52
%if 0%{?suse_version} == 1500
# %%build and %%install use GCC 13 there
BuildRequires:	gcc13 gcc13-c++
%endif

# Amazon Linux 2023 does not have armadillo, cfitsio, freexl, libarrow,
# libdeflate, libkml, netcdf, shapelib, SFCGAL and gpsbabel. GDAL builds
# without the drivers that need them there.
# RHEL: our pgdg-* packages under /usr/pgdg-*, instead of the EPEL ones:
%if 0%{?rhel}
BuildRequires:	pgdg-armadillo-devel pgdg-cfitsio-devel pgdg-freexl-devel
BuildRequires:	pgdg-hdf-devel pgdg-hdf5-devel pgdg-libdeflate-devel
BuildRequires:	pgdg-libgta-devel pgdg-libkml-devel pgdg-netcdf-devel
BuildRequires:	pgdg-xerces-c-devel
%ifnarch %{ppc64le}
BuildRequires:	pgdg-libarrow-devel
%endif
%if 0%{?rhel} >= 10
BuildRequires:	pgdg-qhull-devel
%endif
%endif
%if ! 0%{?amzn} && ! 0%{?rhel}
BuildRequires:	armadillo-devel
BuildRequires:	cfitsio-devel
%endif
BuildRequires:	chrpath
BuildRequires:	doxygen
BuildRequires:	fontconfig-devel
%if ! 0%{?amzn} && ! 0%{?rhel}
BuildRequires:	freexl-devel
%endif
%if 0%{?g2clib_enabled}
BuildRequires:	g2clib-devel
BuildRequires:	g2clib-static
%endif
BuildRequires:	geos%{geosmajorversion}-devel >= 3.13.3
BuildRequires:	ghostscript
BuildRequires:	jpackage-utils
%if 0%{?fedora} >= 42 || 0%{?rhel} >= 9 || 0%{?suse_version} >= 1499 || 0%{?amzn} == 2023
BuildRequires:	libarchive-devel >= 3.5.0
%endif
%ifnarch %{ppc64le}
%if ! 0%{?amzn} && ! 0%{?rhel}
%if 0%{?fedora}
BuildRequires:	libarrow-devel
%endif
BuildRequires:	libdeflate-devel
%endif
%endif
# For 'mvn_artifact' and 'mvn_install'
BuildRequires:	libgeotiff%{libgeotiffmajorversion}-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 1.6.0
%if 0%{?fedora} && ! 0%{?amzn}
BuildRequires:	libkml-devel
%endif
BuildRequires:	libspatialite%{libspatialitemajorversion}-devel >= 5.1.0-16

BuildRequires:	libtiff-devel >= 4.1
BuildRequires:	libwebp-devel
BuildRequires:	libtool
BuildRequires:	giflib-devel
%if ! 0%{?amzn} && ! 0%{?rhel}
BuildRequires:	netcdf-devel >= 4.7
%endif
%if 0%{?rhel}
BuildRequires:	mariadb-devel
%endif
%if 0%{?fedora} || 0%{?amzn}
BuildRequires:	mariadb-connector-c-devel
%endif

# Enable muparser library for VRT expressions
%if 0%{?fedora} >= 42
BuildRequires:	muParser-devel
Requires:	muParser
%endif
%if 0%{?suse_version} == 1500
BuildRequires:	muparser-devel
Requires:	libmuparser2_3_3
%endif
%if 0%{?suse_version} == 1600
BuildRequires:	muparser-devel
Requires:	libmuparser2_3_4
%endif

BuildRequires:	libpq5-devel
BuildRequires:	pcre2-devel
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	%{_bindir}/pkg-config
%if 0%{?suse_version} >= 1500
BuildRequires:	libpoppler-devel >= 0.86
%else
BuildRequires:	poppler-devel >= 0.86
%endif
BuildRequires:	proj%{projmajorversion}-devel >= 9.4.1

BuildRequires:	sqlite-devel >= 3.31
BuildRequires:	swig
%if %{build_refman}
BuildRequires:	texlive-collection-fontsrecommended
%if 0%{?fedora}
BuildRequires:	texlive-collection-langcyrillic
BuildRequires:	texlive-collection-langportuguese
BuildRequires:	texlive-newunicodechar
%endif
BuildRequires:	texlive-epstopdf
BuildRequires:	tex(multirow.sty)
BuildRequires:	tex(sectsty.sty)
BuildRequires:	tex(tocloft.sty)
BuildRequires:	tex(xtab.sty)
%endif
BuildRequires:	unixODBC-devel

%if 0%{?suse_version} == 1500
BuildRequires:	hdf hdf-devel hdf-devel-static
BuildRequires:	hdf5 hdf5-devel hdf5-devel-static
BuildRequires:	libexpat-devel libjson-c-devel
BuildRequires:	libjasper-devel
BuildRequires:	libxerces-c-devel
BuildRequires:	python311-devel
BuildRequires:	libshp-devel libcurl-devel >= 7.68
BuildRequires:	java-11-openjdk-devel
%endif
%if 0%{?suse_version} == 1600
BuildRequires:	hdf5 hdf5-devel
BuildRequires:	libexpat-devel libjson-c-devel
BuildRequires:	libjasper-devel
BuildRequires:	libxerces-c-devel
BuildRequires:	java-21-openjdk-devel
%endif
%if 0%{?fedora} >= 42 || 0%{?rhel} >= 8
%if 0%{?fedora}
BuildRequires:	libdap-devel hdf-devel hdf-static hdf5-devel >= 1.10
%endif
BuildRequires:	expat-devel
BuildRequires:	jasper-devel
%if 0%{?rhel} == 8
BuildRequires:	java-11-openjdk-devel
%else
%if 0%{?rhel} == 9
BuildRequires:	java-17-openjdk-devel
%else
%if 0%{?rhel} == 10
BuildRequires:	java-21-openjdk-devel
%else
BuildRequires:	java-devel >= 1:1.6.0
%endif
%endif
%endif
BuildRequires:	json-c-devel
%if 0%{?fedora}
BuildRequires:	libdap-devel libgta-devel
%endif
BuildRequires:	perl-devel
BuildRequires:	perl-generators
BuildRequires:	python3-devel >= 3.8
%if 0%{?fedora}
BuildRequires:	xerces-c-devel
%endif
%endif
%if 0%{?amzn} == 2023
BuildRequires:	expat-devel jasper-devel json-c-devel
BuildRequires:	java-21-amazon-corretto-devel
BuildRequires:	perl-devel perl-generators
%endif
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
BuildRequires:	libtirpc-devel

# RHEL 10 has no qhull; RHEL 8 and 9 ship it in CRB:
%if ! 0%{?rhel} || 0%{?rhel} < 10
BuildRequires:	qhull-devel
%endif
%if 0%{?fedora} >= 42 || 0%{?rhel} >= 9
BuildRequires:	SFCGAL-devel >= 2.0.0
%else
%if ! 0%{?amzn}
BuildRequires:	SFCGAL-devel
%endif
%endif
%if 0%{?suse_version} == 1500
%endif

%if ! 0%{?amzn} && ! 0%{?rhel}
BuildRequires:	shapelib-devel
%endif
BuildRequires:	curl-devel >= 7.68
%if 0%{?fedora} >= 42 || 0%{?rhel} >= 8 || 0%{?suse_version} >= 1600 || 0%{?amzn} == 2023
BuildRequires:	openjpeg2-devel >= 2.3.1
%endif

# Run time dependencies
%if 0%{?rhel}
Requires:	pgdg-gpsbabel
%endif
%if ! 0%{?amzn} && ! 0%{?rhel}
Requires:	gpsbabel
%endif
%if 0%{?fedora} >= 42 || 0%{?rhel} >= 9 || 0%{?amzn} == 2023
Requires:	libarchive >= 3.5.0
%endif
%if 0%{?suse_version} >= 1499
Requires: libarchive13 >= 3.5.0
%endif
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}


%description
Geospatial Data Abstraction Library (GDAL/OGR) is a cross platform
C++ translator library for raster and vector geospatial data formats.
As a library, it presents a single abstract data model to the calling
application for all supported formats. It also comes with a variety of
useful commandline utilities for data translation and processing.

It provides the primary data access engine for many applications.
GDAL/OGR is the most widely used geospatial data access library.


%package devel
Summary:	Development files for the GDAL file format library
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description devel
This package contains development files for GDAL.


%package libs
Summary:	GDAL file format library
# See frmts/grib/degrib/README.TXT
Provides:	bundled(g2lib) = 1.6.0
Provides:	bundled(degrib) = 2.14
Requires:	geos%{geosmajorversion} >= %{geosfullversion}
%if 0%{?rhel}
# These are found through the rpath, so require them by name (their sonames
# are filtered out below):
Requires:	pgdg-armadillo%{?_isa} pgdg-cfitsio%{?_isa} pgdg-freexl%{?_isa}
Requires:	pgdg-hdf%{?_isa} pgdg-hdf5%{?_isa} pgdg-libdeflate%{?_isa}
Requires:	pgdg-libgta%{?_isa} pgdg-libkml%{?_isa} pgdg-netcdf%{?_isa}
Requires:	pgdg-xerces-c%{?_isa} pgdg-gpsbabel
%ifnarch %{ppc64le}
Requires:	pgdg-libarrow%{?_isa}
%endif
%if 0%{?rhel} >= 10
Requires:	pgdg-qhull%{?_isa}
%endif
%endif
%if ! 0%{?amzn} && ! 0%{?rhel}
Requires:	netcdf >= 4.7 gpsbabel
%endif
Requires:	libgeotiff%{libgeotiffmajorversion}
Requires:	libspatialite%{libspatialitemajorversion} >= 5.1.0-16
# Require the libpq that we build against: libpq.so.5 is also provided
# by other packages (e.g. babelfish_postgresqlNN-libs), from directories
# that are not in the linker path.
Requires:	libpq5

%if 0%{?suse_version}
%if 0%{?suse_version} <= 1499
Requires:	libarmadillo10
%endif
%endif
%if 0%{?fedora} >= 42
Requires:	armadillo
%endif

%description libs
This package contains the GDAL file format library.

%if %gdaljava
%package java
Summary:	Java modules for the GDAL file format library
Requires:	jpackage-utils
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description java
The GDAL Java modules provide support to handle multiple GIS file formats.


%package javadoc
Summary:	Javadocs for %{name}
Requires:	jpackage-utils
BuildArch:	noarch

%description javadoc
This package contains the API documentation for %{name}.
%endif

%if %gdal_python_enabled
%package python3
%{?py_provide:%py_provide python3-gdal}
Summary:	Python modules for the GDAL file format library
BuildRequires:	python%{python3_pkgversion}-numpy
%if 0%{?suse_version}
# numpy/arrayobject.h
BuildRequires:	python%{python3_pkgversion}-numpy-devel
%endif
BuildRequires:	python%{python3_pkgversion}-devel python%{python3_pkgversion}-setuptools
Requires:	python%{python3_pkgversion}-numpy
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description python3
The GDAL Python 3 modules provide support to handle multiple GIS file formats.


%package python-tools
Summary:	Python tools for the GDAL file format library
Requires:	%{name}-python3

%description python-tools
The GDAL Python package provides number of tools for programming and
manipulating GDAL file format library
%endif

# We don't want to provide private Python extension libs
%global __provides_exclude_from ^(%{python2_sitearch}|%{python3_sitearch})/.*\.so$
%global __provides_exclude_from ^%{python3_sitearch}/.*\.so$

%if 0%{?rhel} >= 10
%global rhel_qhull_re |qhull[a-z_]*
%endif
# RHEL: do not require the sonames of the pgdg-* libraries, which are not
# provided (they are found through the rpath); see the Requires above:
%if 0%{?rhel}
%global __requires_exclude ^lib(armadillo|arrow[a-z_]*|parquet|cfitsio|freexl|hdf|mfhdf|hdf5[a-z_]*|sz|aec|deflate|gta|kml[a-z]*|minizip|netcdf|uriparser|xerces-c[-0-9.]*|blosc|arpack|superlu%{?rhel_qhull_re})\\.so
%endif

%prep
%setup -q -n %{sname}-%{version}-fedora

%patch -P 0 -p0

# Delete bundled libraries
rm -rf frmts/png/libpng
rm -rf frmts/gif/giflib
rm -rf frmts/jpeg/libjpeg
rm -rf frmts/jpeg/libjpeg12
rm -rf mrf/LERCV1

# Copy in PROVENANCE.TXT-fedora
cp -a %{SOURCE4} .

%build
# Use a newer GCC on SLES 15 to build this version of GDAL:
%if 0%{?suse_version} == 1500
export CC=/usr/bin/gcc-13
export CXX=/usr/bin/g++-13
%endif
%ifarch sparcv9 sparc64 s390 s390x
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpic"
%endif
export CXXFLAGS="$CFLAGS -I%{projinstdir}/include -I%{libgeotiffinstdir}/include -I%{geosinstdir}/include -I%{libspatialiteinstdir}/include"
export CPPFLAGS="$CPPFLAGS -I%{projinstdir}/include -I%{libgeotiffinstdir}/include -I%{geosinstdir}/include -I%{libspatialiteinstdir}/include"
# SLES 15 has -Itirpc on /usr/include, so use the following only on Fedora and RHEL:
%if 0%{?fedora} >= 30 || 0%{?rhel} >= 9 || 0%{?amzn}
export CXXFLAGS="$CFLAGS -I%{_includedir}/tirpc"
export CPPFLAGS="$CPPFLAGS -I%{_includedir}/tirpc"
%endif
# ant does not find the Corretto JDK on Amazon Linux 2023 by itself:
%if 0%{?amzn}
export JAVA_HOME=%{_jvmdir}/java-21-amazon-corretto
%endif
LDFLAGS="$LDFLAGS -L%{projinstdir}/lib64 -L%{libgeotiffinstdir}/lib -L%{geosinstdir}/lib64 -L%{libspatialiteinstdir}/lib -L%{_libdir} -Wl,-rpath,%{projinstdir}/lib64:%{libgeotiffinstdir}/lib:%{geosinstdir}/lib64:%{libspatialiteinstdir}/lib"; export LDFLAGS
# RHEL: our pgdg-* packages, instead of the EPEL ones:
%if 0%{?rhel}
for p in armadillo arpack arrow blosc cfitsio freexl hdf hdf5 libaec libdeflate libgta libkml minizip-ng netcdf qhull superlu uriparser xerces-c; do
	PGDGPREFIXES="${PGDGPREFIXES};/usr/pgdg-$p"
	PKG_CONFIG_PATH="${PKG_CONFIG_PATH:+$PKG_CONFIG_PATH:}/usr/pgdg-$p/lib64/pkgconfig"
	LDFLAGS="$LDFLAGS -Wl,-rpath,/usr/pgdg-$p/lib64"
done
export PKG_CONFIG_PATH LDFLAGS
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1500
 %{__install} -d build
 pushd build
 cmake .. -DCMAKE_INSTALL_PREFIX:PATH=%{gdalinstdir} \
%endif
%else
 %cmake -DCMAKE_INSTALL_PREFIX:PATH=%{gdalinstdir} \
%endif
 -DCMAKE_INSTALL_INCLUDEDIR=include \
 -DCMAKE_INSTALL_LIBDIR=lib \
 -DHAVE_SPATIALITE=ON \
 -DSPATIALITE_INCLUDE_DIR=%{libspatialiteinstdir}/include \
 -DSPATIALITE_LIBRARY=%{libspatialiteinstdir}/lib/libspatialite.so \
 -DCMAKE_PREFIX_PATH="%{geosinstdir};%{libgeotiffinstdir}${PGDGPREFIXES}" \
 -DGDAL_USE_JPEG12_INTERNAL=OFF \
%if 0%{?rhel} >= 9
 -DCMAKE_CXX_STANDARD=20 \
%endif
%if %gdal_python_enabled
  -DBUILD_PYTHON_BINDINGS:BOOL=ON \
  -DPython_ROOT=/usr \
  -DPython_LOOKUP_VERSION=%{pyver} \
%else
 -DBUILD_PYTHON_BINDINGS:BOOL=OFF \
%endif
 -DGDAL_USE_SHAPELIB=OFF \
%if %gdaljava
 -DBUILD_JAVA_BINDINGS=ON \
 -DGDAL_JAVA_INSTALL_DIR=%{_jnidir}/%{name} \
%else
 -DBUILD_JAVA_BINDINGS=OFF \
%endif
 -DSWIG_REGENERATE_PYTHON=OFF \
 -DBUILD_CSHARP_BINDINGS=OFF

%cmake_build

%install
# Use a newer GCC on SLES 15 to install this version of GDAL:
%if 0%{?suse_version} == 1500
export CC=/usr/bin/gcc-13
export CXX=/usr/bin/g++-13
%endif

%cmake_install

touch gdal_python_manpages.txt gdal_python_manpages_excludes.txt
# List of manpages for python scripts
for file in %{buildroot}%{gdalinstdir}/bin/*.py; do
  if [ -f %{buildroot}%{gdalinstdir}/share/man/man1/`basename ${file/.py/.1*}` ]; then
    echo "%{gdalinstdir}/share/man/man1/`basename ${file/.py/.1*}`" >> gdal_python_manpages.txt
    echo "%exclude %{gdalinstdir}/share/man/man1/`basename ${file/.py/.1*}`" >> gdal_python_manpages_excludes.txt
  fi
done

%if %gdal_python_enabled
%{__mkdir} -p %{buildroot}/%{python3_sitearch}/
%{__mv} %{buildroot}/%{gdalinstdir}/lib64/python%{pyver}/site-packages/GDAL-%{version}-py*.egg-info/ %{buildroot}/%{python3_sitearch}/GDAL-%{version}-py*.egg-info/
%{__mv} %{buildroot}/%{gdalinstdir}/lib64/python%{pyver}/site-packages/osgeo %{buildroot}/%{python3_sitearch}/osgeo/
%{__mv} %{buildroot}/%{gdalinstdir}/lib64/python%{pyver}/site-packages/osgeo_utils %{buildroot}/%{python3_sitearch}/osgeo_utils
%endif

# Install linker config file:
%{__mkdir} -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%{__install} %{SOURCE6} %{buildroot}%{_sysconfdir}/ld.so.conf.d/

%files -f gdal_python_manpages_excludes.txt
%{gdalinstdir}/bin/gdal
%{gdalinstdir}/bin/gdal_contour
%{gdalinstdir}/bin/gdal_create
%{gdalinstdir}/bin/gdal_footprint
%{gdalinstdir}/bin/gdal_grid
%{gdalinstdir}/bin/gdal_rasterize
%{gdalinstdir}/bin/gdal_translate
%{gdalinstdir}/bin/gdal_viewshed
%{gdalinstdir}/bin/gdaladdo
%{gdalinstdir}/bin/gdalbuildvrt
%{gdalinstdir}/bin/gdaldem
%{gdalinstdir}/bin/gdalenhance
%{gdalinstdir}/bin/gdalinfo
%{gdalinstdir}/bin/gdallocationinfo
%{gdalinstdir}/bin/gdalmanage
%{gdalinstdir}/bin/gdalmdiminfo
%{gdalinstdir}/bin/gdalmdimtranslate
%{gdalinstdir}/bin/gdalsrsinfo
%{gdalinstdir}/bin/gdaltindex
%{gdalinstdir}/bin/gdaltransform
%{gdalinstdir}/bin/gdalwarp
%{gdalinstdir}/bin/gnmanalyse
%{gdalinstdir}/bin/gnmmanage
%{gdalinstdir}/bin/nearblack
%{gdalinstdir}/bin/sozip
%if %gdal_python_enabled
%{gdalinstdir}/bin/ogr_layer_algebra*
%endif
%{gdalinstdir}/bin/ogr2ogr
%{gdalinstdir}/bin/ogrinfo
%{gdalinstdir}/bin/ogrlineref
%{gdalinstdir}/bin/ogrtindex
%{gdalinstdir}/share/bash-completion/completions/*
%exclude %{gdalinstdir}/share/bash-completion/completions/*.py
%{gdalinstdir}/share/man/man1/*
%exclude %{gdalinstdir}/share/man/man1/gdal-config.1*
# Python manpages excluded in -f gdal_python_manpages_excludes.txt

%files libs
%license LICENSE.TXT
%doc NEWS.md PROVENANCE.TXT COMMITTERS PROVENANCE.TXT-fedora
%{gdalinstdir}/lib/libgdal.so.%{gdalsomajorversion}
%{gdalinstdir}/lib/libgdal.so.%{gdalsomajorversion}.*
%{gdalinstdir}/share/%{sname}/
%{gdalinstdir}/lib/gdalplugins/
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%files devel
%{gdalinstdir}/bin/%{sname}-config
%dir %{gdalinstdir}/include/
%{gdalinstdir}/include/*.h
%{gdalinstdir}/include/*.hpp
%{gdalinstdir}/lib/cmake/%{sname}/GDAL*.cmake
%{gdalinstdir}/lib/*.so
%{gdalinstdir}/lib/pkgconfig/%{sname}.pc

%if %gdal_python_enabled
%files python3
%doc swig/python/README.rst
%{python3_sitearch}/GDAL-%{version}-py*.egg-info/
%{python3_sitearch}/osgeo/
%{python3_sitearch}/osgeo_utils/

%files python-tools -f gdal_python_manpages.txt
%{gdalinstdir}/bin/gdal_calc*
%{gdalinstdir}/bin/gdal_edit*
%{gdalinstdir}/bin/gdal_fillnodata*
%{gdalinstdir}/bin/gdal_merge*
%{gdalinstdir}/bin/gdal_pansharpen*
%{gdalinstdir}/bin/gdal_polygonize*
%{gdalinstdir}/bin/gdal_proximity*
%{gdalinstdir}/bin/gdal_retile*
%{gdalinstdir}/bin/gdal_sieve*
%{gdalinstdir}/bin/gdal2tiles*
%{gdalinstdir}/bin/gdal2xyz*
%{gdalinstdir}/bin/gdalattachpct*
%{gdalinstdir}/bin/gdalcompare*
%{gdalinstdir}/bin/gdalmove*
%{gdalinstdir}/bin/ogrmerge*
%{gdalinstdir}/bin/pct2rgb*
%{gdalinstdir}/bin/rgb2pct*
%{gdalinstdir}/share/bash-completion/completions/*.py
%endif

%if %gdaljava
%files java
%{_jnidir}/%{name}/gdal-%{version}-javadoc.jar
%{_jnidir}/%{name}/gdal-%{version}-sources.jar
%{_jnidir}/%{name}/gdal-%{version}.jar
%{_jnidir}/%{name}/gdal-%{version}.pom
%{gdalinstdir}/lib/jni/libgdalalljni.so

%files javadoc
%{_jnidir}/%{name}/gdal-%{version}-javadoc.jar
%endif

%changelog
* Fri Oct 23 2026 Devrim Gunduz <devrim@gunduz.org> - 3.13.3-9PGDG
- Build with C++20 on RHEL 9 and 10: the headers of Arrow 26
  (pgdg-libarrow) need it, and GDAL defaults to C++17, which broke
  the Arrow and Parquet drivers. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Wed Oct 21 2026 Devrim Gunduz <devrim@gunduz.org> - 3.13.3-8PGDG
- RHEL: build against our pgdg-* packages (armadillo, cfitsio, freexl,
  hdf, hdf5, libarrow, libdeflate, libgta, libkml, netcdf, qhull on RHEL 10,
  xerces-c) instead of the EPEL ones, and require pgdg-gpsbabel. Do not
  BuildRequire libdap and shapelib there, which this build does not use.
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Tue Oct 20 2026 Devrim Gunduz <devrim@gunduz.org> - 3.13.3-7PGDG
- Add Amazon Linux 2023 support: skip the BuildRequires and Requires
  that are not available there (armadillo, cfitsio, freexl, libarrow,
  libdeflate, libkml, netcdf, shapelib, SFCGAL and gpsbabel), add the
  ones that the Fedora/RHEL conditionals miss there (AL2023 defines
  %%fedora as 34), and enable the Python and Java bindings, building
  the latter with the Corretto 21 JDK.
- Require libpq5 in the -libs subpackage: libpq.so.5 is also provided by
  babelfish_postgresqlNN-libs, which dnf may pick instead, and whose
  libpq is not in the linker path.

* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 3.13.3-6PGDG
- Update download URL

* Mon Oct 12 2026 Devrim Gunduz <devrim@gunduz.org> - 3.13.3-5PGDG
- Rebuild against GEOS 3.15. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/359

* Mon Oct 5 2026 Devrim Gunduz <devrim@gunduz.org> - 3.13.3-4PGDG
- Embed the PROJ, GeOS, libgeotiff and SpatiaLite library paths as
  rpaths, so that GDAL uses GeOS 3.14 also when other GeOS versions are
  installed: they were passed in SHLIB_LINK, which CMake ignores.
- Require the GeOS package that we build against.
- Build against and require libspatialite50 5.1.0-16 or later, which
  uses GeOS 3.14 also when other GeOS versions are installed.
- Add the numpy-devel BuildRequires on SUSE, which has the numpy headers
  that the Python bindings need.
- Add the gcc13 BuildRequires on SLES 15, where the package is built
  with GCC 13.

* Mon Aug 31 2026 Devrim Gunduz <devrim@gunduz.org> - 3.13.3-3PGDG
- Pin java-11/17/21-openjdk-devel BuildRequires on RHEL 8/9/10
  respectively, instead of the unversioned java-devel, which resolves
  to the outdated default JDK 8 on RHEL 8. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/110

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 3.13.3-2PGDG
- Set python3_pkgversion/__ospython for Amazon Linux 2023 (python3.13),
  to keep the Python stack consistent across all packages in the repo.
  Note: gdal_python_enabled still doesn't cover amzn, so this has no
  effect until that's revisited separately.

* Tue Aug 18 2026 Devrim Gunduz <devrim@gunduz.org> - 3.13.3-1PGDG
- Update to 3.13.3 per changes described at:
  https://github.com/OSGeo/gdal/releases/tag/v3.13.3

* Wed Jul 22 2026 Devrim Gunduz <devrim@gunduz.org> - 3.13.2-1PGDG
- Update to 3.13.2 per changes described at:
  https://github.com/OSGeo/gdal/releases/tag/v3.13.2

* Sat Jun 6 2026 Devrim Gunduz <devrim@gunduz.org> - 3.13.1-1PGDG
- Update to 3.13.1 per changes described at:
  https://github.com/OSGeo/gdal/releases/tag/v3.13.1

* Wed May 13 2026 Devrim Gunduz <devrim@gunduz.org> - 3.13.0-1PGDG
- Initial 3.13.0 packaging per changes described at:
  https://github.com/OSGeo/gdal/releases/tag/v3.13.0
  Check the migration guide:
  https://gdal.org/en/latest/user/migration_guide.html#from-gdal-3-12-to-gdal-3-13
