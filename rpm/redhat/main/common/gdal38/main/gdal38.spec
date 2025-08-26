%if 0%{?rhel} == 8
# gdal-3.8 cmake build does not work in source directory
%undefine __cmake_in_source_build
%endif

%global sname gdal

%if 0%{?fedora} == 40
%{!?gdaljava:%global gdaljava 0}
%else
%{!?gdaljava:%global gdaljava 1}
%endif

%pgdg_set_gis_variables

%if 0%{?fedora} >= 37
%{expand: %%global pyver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global pyver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif

%if 0%{?rhel} == 8
%global pyver 3.12
%endif

%global bashcompletiondir %(pkg-config --variable=compatdir bash-completion)

%global geosfullversion %geos314fullversion
%global geosmajorversion %geos314majorversion
%global geosinstdir %geos314instdir
%global	projmajorversion %proj96majorversion
%global	projfullversion %proj96fullversion
%global	projinstdir %proj96instdir

%global gdalinstdir /usr/%{name}
%global gdalsomajorversion	34
%global libspatialitemajorversion	50

%global sqlitepname	sqlite
%global sqlitelibdir	%{_libdir}

%if 0%{?fedora} >= 37 || 0%{?rhel} >= 8 || 0%{?suse_version} <= 1499
%global g2clib_enabled 1
%else
%global g2clib_enabled 0
%endif

# Enable/disable generating refmans
# texlive currently broken deps and FTBFS in rawhide
%global build_refman 0
# https://bugzilla.redhat.com/show_bug.cgi?id=1490492
%global mysql --with-mysql
# https://bugzilla.redhat.com/show_bug.cgi?id=1490492

%global poppler --with-poppler
%global spatialite "--with-spatialite=%{libspatialiteinstdir}"

Name:		%{sname}38
Version:	3.8.5
Release:	8PGDG%{?dist}
Summary:	GIS file format library
License:	MIT
URL:		https://www.gdal.org
# Source0: https://download.osgeo.org/gdal/%%{version}/gdal-%%{version}.tar.xz
# See PROVENANCE.TXT-fedora and the cleaner script for details!

Source0:	%{sname}-%{version}-fedora.tar.xz
Source4:	PROVENANCE.TXT-fedora

# Cleaner script for the tarball
Source5:	%{sname}-cleaner.sh

Source6:	%{name}-pgdg-libs.conf

# lz4 and bash-completion dependencies
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	liblz4-devel bash-completion-devel
Requires:	liblz4-1
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	lz4-devel bash-completion
Requires:	lz4
%endif

BuildRequires:	cmake gcc-c++ pgdg-srpm-macros >= 1.0.37

BuildRequires:	ant
BuildRequires:	armadillo-devel
BuildRequires:	cfitsio-devel
BuildRequires:	chrpath
BuildRequires:	curl-devel
BuildRequires:	doxygen
BuildRequires:	fontconfig-devel
BuildRequires:	freexl-devel
%if 0%{?g2clib_enabled}
BuildRequires:	g2clib-devel
%endif
BuildRequires:	geos%{geosmajorversion}-devel >= 3.9.0
BuildRequires:	ghostscript
BuildRequires:	jpackage-utils
%if 0%{?fedora} >= 38 || 0%{?rhel} >= 9 || 0%{?suse_version} >= 1499
BuildRequires:	libarchive-devel >= 3.5.0
%endif
%ifnarch %{ppc64le}
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	libarrow-devel
%endif
BuildRequires:	libdeflate-devel
%endif
# For 'mvn_artifact' and 'mvn_install'
BuildRequires:	libgeotiff%{libgeotiffmajorversion}-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
%if 0%{?fedora}
BuildRequires:	libkml-devel
%endif
BuildRequires:	libspatialite%{libspatialitemajorversion}-devel

BuildRequires:	libtiff-devel
BuildRequires:	libwebp-devel
BuildRequires:	libtool
BuildRequires:	giflib-devel
BuildRequires:	netcdf-devel
%if 0%{?rhel}
BuildRequires:	mariadb-devel
%endif
%if 0%{?fedora}
BuildRequires:	mariadb-connector-c-devel
%endif
BuildRequires:	libpq5-devel
BuildRequires:	pcre2-devel
BuildRequires:	ogdi%{ogdimajorversion}-devel
BuildRequires:	openjpeg2-devel
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	%{_bindir}/pkg-config
%if 0%{?suse_version} >= 1500
BuildRequires:	libpoppler-devel
%else
BuildRequires:	poppler-devel
%endif
BuildRequires:	proj%{projmajorversion}-devel >= 7.1.0

BuildRequires:	sqlite-devel
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

%if 0%{?suse_version}
%if 0%{?suse_version} <= 1315
BuildRequires:	java-1_8_0-openjdk-devel
%else
BuildRequires:	java-11-openjdk-devel
%endif
%endif

%if 0%{?suse_version} >= 1315
BuildRequires:	hdf hdf-devel hdf-devel-static
BuildRequires:	hdf5 hdf5-devel hdf5-devel-static
BuildRequires:	libexpat-devel libjson-c-devel
BuildRequires:	libjasper-devel
BuildRequires:	libxerces-c-devel
BuildRequires:	python3-numpy-devel
%else
BuildRequires:	g2clib-static
BuildRequires:	libdap-devel
BuildRequires:	expat-devel
BuildRequires:	hdf-devel hdf-static hdf5-devel
BuildRequires:	jasper-devel
BuildRequires:	java-devel >= 1:1.6.0
BuildRequires:	json-c-devel
BuildRequires:	libdap-devel libgta-devel
BuildRequires:	librx-devel
BuildRequires:	perl-devel
BuildRequires:	perl-generators
BuildRequires:	xerces-c-devel
%endif
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
BuildRequires:	libtirpc-devel
%if 0%{?fedora} >= 39 || 0%{?rhel} >= 9 || 0%{?suse_version} <= 1499
BuildRequires:	python3-devel
%endif
%if 0%{?rhel} == 8
BuildRequires:	python3.12-devel
%endif
BuildRequires:	python3-numpy
BuildRequires:	python3-setuptools

BuildRequires:	qhull-devel

# Run time dependencies
Requires:	gpsbabel
%if 0%{?fedora} >= 38 || 0%{?rhel} >= 9
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
Requires:	geos%{geosmajorversion} ogdi%{ogdimajorversion}
Requires:	netcdf gpsbabel
Requires:	libgeotiff%{libgeotiffmajorversion}-devel
Requires:	libspatialite%{libspatialitemajorversion}-devel

%if 0%{?suse_version}
%if 0%{?suse_version} <= 1499
Requires:	libarmadillo10
%endif
%endif
%if 0%{?fedora} >= 37 || 0%{?rhel} >= 7
Requires:	armadillo
%endif

%description libs
This package contains the GDAL file format library.

%if %gdaljava
# No complete java yet in EL8
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

%package python3
%{?py_provide:%py_provide python3-gdal}
Summary:	Python modules for the GDAL file format library
Requires:	python3-numpy
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description python3
The GDAL Python 3 modules provide support to handle multiple GIS file formats.


%package python-tools
Summary:	Python tools for the GDAL file format library
Requires:	gdal38-python3

%description python-tools
The GDAL Python package provides number of tools for programming and
manipulating GDAL file format library

# We don't want to provide private Python extension libs
%global __provides_exclude_from ^(%{python2_sitearch}|%{python3_sitearch})/.*\.so$
%global __provides_exclude_from ^%{python3_sitearch}/.*\.so$

%prep
%setup -q -n %{sname}-%{version}-fedora

# Delete bundled libraries
rm -rf frmts/png/libpng
rm -rf frmts/gif/giflib
rm -rf frmts/jpeg/libjpeg
rm -rf frmts/jpeg/libjpeg12
rm -rf frmts/gtiff/libtiff
rm -rf mrf/LERCV1

# Copy in PROVENANCE.TXT-fedora
cp -a %{SOURCE4} .


%build
%ifarch sparcv9 sparc64 s390 s390x
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpic"
%endif
export CXXFLAGS="$CFLAGS -I%{projinstdir}/include -I%{libgeotiffinstdir}/include -I%{geosinstdir}/include -I%{ogdiinstdir}/include -I%{libspatialiteinstdir}/include -I%{_includedir}/tirpc"
export CPPFLAGS="$CPPFLAGS -I%{projinstdir}/include -I%{libgeotiffinstdir}/include -I%{geosinstdir}/include -I%{ogdiinstdir}/include -I%{libspatialiteinstdir}/include -I%{_includedir}/tirpc"
LDFLAGS="$LDFLAGS -L%{projinstdir}/lib64 -L%{ogdiinstdir}/lib -L%{libgeotiffinstdir}/lib -L%{geosinstdir}/lib64 -L%{libspatialiteinstdir}/lib -L%{sqlitelibdir}"; export LDFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{projinstdir}/lib64,%{ogdiinstdir}/lib,%{libgeotiffinstdir}/lib,%{geosinstdir}/lib64,%{libspatialiteinstdir}/lib" ; export SHLIB_LINK
export OGDI_CFLAGS='-I%{ogdiinstdir}/include/ogdi'
export OGDI_INCLUDE='-I%{ogdiinstdir}/include/ogdi'
export OGDI_LIBS='-L%{ogdiinstdir}/lib'

%if 0%{?rhel} == 8
export PYTHON=/usr/bin/python3.12
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
 %{__install} -d build
 pushd build
 cmake .. -DCMAKE_INSTALL_PREFIX:PATH=%{gdalinstdir} \
%endif
%else
 %cmake3 -DCMAKE_INSTALL_PREFIX:PATH=%{gdalinstdir} \
%endif
 -DCMAKE_INSTALL_INCLUDEDIR=include \
 -DCMAKE_INSTALL_LIBDIR=lib \
 -DBUILD_PYTHON_BINDINGS=ON \
 -DPython_ROOT=/usr \
 -DPython_LOOKUP_VERSION=%{pyver} \
 -DSPATIALITE_INCLUDE_DIR=%{libspatialiteinstdir}/include \
 -DSPATIALITE_LIBRARY=%{libspatialiteinstdir}/lib/libspatialite.so \
 -DGDAL_JAVA_INSTALL_DIR=%{_jnidir}/%{name} \
 -DCMAKE_PREFIX_PATH="%{geosinstdir};%{libgeotiffinstdir}" \
 -DGDAL_USE_JPEG12_INTERNAL=OFF \
%if 0%{?rhel} == 8
 -DGDAL_USE_ARCHIVE=OFF \
%endif
%if %gdaljava
 -DBUILD_JAVA_BINDINGS=ON \
%else
 -DBUILD_JAVA_BINDINGS=OFF \
%endif
 -DSWIG_REGENERATE_PYTHON=OFF

%cmake_build

%install
%cmake_install

# List of manpages for python scripts
for file in %{buildroot}%{gdalinstdir}/bin/*.py; do
  if [ -f %{buildroot}%{gdalinstdir}/share/man/man1/`basename ${file/.py/.1*}` ]; then
    echo "%{gdalinstdir}/share/man/man1/`basename ${file/.py/.1*}`" >> gdal_python_manpages.txt
    echo "%exclude %{gdalinstdir}/share/man/man1/`basename ${file/.py/.1*}`" >> gdal_python_manpages_excludes.txt
  fi
done

%{__mkdir} -p %{buildroot}/%{python3_sitearch}/
%{__mv} %{buildroot}/%{gdalinstdir}/lib64/python%{pyver}/site-packages/GDAL-%{version}-py*.egg-info/ %{buildroot}/%{python3_sitearch}/GDAL-%{version}-py*.egg-info/
%{__mv} %{buildroot}/%{gdalinstdir}/lib64/python%{pyver}/site-packages/osgeo %{buildroot}/%{python3_sitearch}/osgeo/
%{__mv} %{buildroot}/%{gdalinstdir}/lib64/python%{pyver}/site-packages/osgeo_utils %{buildroot}/%{python3_sitearch}/osgeo_utils

# Install linker config file:
%{__mkdir} -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%{__install} %{SOURCE6} %{buildroot}%{_sysconfdir}/ld.so.conf.d/


%files -f gdal_python_manpages_excludes.txt
%{gdalinstdir}/bin/gdal_contour
%{gdalinstdir}/bin/gdal_create
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
%{gdalinstdir}/bin/ogr_layer_algebra.py
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
%{gdalinstdir}/lib/cmake/%{sname}/GDAL*.cmake
%{gdalinstdir}/lib/*.so
%{gdalinstdir}/lib/pkgconfig/%{sname}.pc

%files python3
%doc swig/python/README.rst
%{python3_sitearch}/GDAL-%{version}-py*.egg-info/
%{python3_sitearch}/osgeo/
%{python3_sitearch}/osgeo_utils/

%files python-tools -f gdal_python_manpages.txt
%{gdalinstdir}/bin/gdal_calc.py
%{gdalinstdir}/bin/gdal_edit.py
%{gdalinstdir}/bin/gdal_fillnodata.py
%{gdalinstdir}/bin/gdal_footprint
%{gdalinstdir}/bin/gdal_merge.py
%{gdalinstdir}/bin/gdal_pansharpen.py
%{gdalinstdir}/bin/gdal_polygonize.py
%{gdalinstdir}/bin/gdal_proximity.py
%{gdalinstdir}/bin/gdal_retile.py
%{gdalinstdir}/bin/gdal_sieve.py
%{gdalinstdir}/bin/gdal2tiles.py
%{gdalinstdir}/bin/gdal2xyz.py
%{gdalinstdir}/bin/gdalattachpct.py
%{gdalinstdir}/bin/gdalcompare.py
%{gdalinstdir}/bin/gdalmove.py
%{gdalinstdir}/bin/ogrmerge.py
%{gdalinstdir}/bin/pct2rgb.py
%{gdalinstdir}/bin/rgb2pct.py
%{gdalinstdir}/share/bash-completion/completions/*.py

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
* Tue Aug 26 2025 Devrim Gunduz <devrim@gunduz.org> - 3.8.5-8PGDG
- Rebuild against PROJ 9.6 and GeOS 3.14
- Use Python 3.12 on RHEL 8 to match Patroni and other packages.

* Fri Jan 24 2025 Devrim Gunduz <devrim@gunduz.org> - 3.8.5-7PGDG
- Fix long standing python3-tools subpackage bug:
  https://redmine.postgresql.org/issues/7931

* Wed Oct 30 2024 Devrim Gunduz <devrim@gunduz.org> - 3.8.5-6PGDG
- Rebuild against libarrow 16 on Fedora 41

* Thu Sep 26 2024 Devrim Gunduz <devrim@gunduz.org> - 3.8.5-5PGDG
- Rebuild against PROJ 9.5 and GeOS 3.13
- Disable libarchive support properly on RHEL 8
- Fix RHEL 8 Python builds.

* Tue Apr 23 2024 Devrim Gunduz <devrim@gunduz.org> - 3.8.5-4PGDG
- Disable JAVA bindings on Fedora 40 until the build issue is resolved.

* Wed Apr 10 2024 Devrim Gunduz <devrim@gunduz.org> - 3.8.5-2PGDG
- Build against PROJ 9.4.0

* Mon Apr 8 2024 Devrim Gunduz <devrim@gunduz.org> - 3.8.5-2PGDG
- Disable libarchive support RHEL 8 as GDAL now requires at least 3.5.0

* Mon Apr 8 2024 Devrim Gunduz <devrim@gunduz.org> - 3.8.5-1PGDG
- Update to 3.8.5 per changes described at
  https://github.com/OSGeo/gdal/blob/v3.8.5/NEWS.md

* Tue Feb 27 2024 Devrim Gunduz <devrim@gunduz.org> - 3.8.4-2PGDG
- Build with libarchive to enable direct reading of files within
  rar and 7z archives.

* Sun Feb 18 2024 Devrim Gunduz <devrim@gunduz.org> - 3.8.4-1PGDG
- Update to 3.8.4 per changes described at
  https://github.com/OSGeo/gdal/blob/v3.8.4/NEWS.md

* Sat Feb 17 2024 Devrim Gunduz <devrim@gunduz.org> - 3.8.3-3PGDG
- Add missing BR

* Mon Jan 29 2024 Devrim Gunduz <devrim@gunduz.org> - 3.8.3-2PGDG
- Build against Proj 9.3.X

* Mon Jan 15 2024 Devrim Gunduz <devrim@gunduz.org> - 3.8.3-1PGDG
- Update to 3.8.3

* Tue Jan 2 2024 Devrim Gunduz <devrim@gunduz.org> - 3.8.2-1PGDG
- Update to 3.8.2

* Mon Dec 4 2023 Devrim Gunduz <devrim@gunduz.org> - 3.8.1-1PGDG
- Initial 3.8.x packaging.
