%global sname gdal

%pgdg_set_gis_variables

%if 0%{?fedora} >= 35
%{expand: %%global pyver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global pyver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif

%global bashcompletiondir %(pkg-config --variable=compatdir bash-completion)

%global geosfullversion %geos312fullversion
%global geosmajorversion %geos312majorversion
%global geosinstdir %geos312instdir
%global projmajorversion %proj92majorversion
%global projfullversion %proj92fullversion
%global projinstdir %proj92instdir

%global gdalinstdir /usr/%{name}
%global gdalsomajorversion	30

%if 0%{?rhel} == 7 || 0%{?suse_version} >= 1315
%global libspatialitemajorversion	43
%else
%global libspatialitemajorversion	50
%endif

%if 0%{?rhel} && 0%{?rhel} == 7
%global sqlitepname	sqlite33
%global sqlitelibdir	/usr/sqlite330/lib
# Major digit of the proj so version
%global proj_somaj 19
%else
%global sqlitepname	sqlite
%global sqlitelibdir	%{_libdir}
# Major digit of the proj so version
%global proj_somaj 22
%endif

%if 0%{?rhel} == 8
# gdal-3.5 cmake build does not work in source directory
%undefine __cmake_in_source_build
%endif

# Override PROJ major version on RHEL 7.
# libspatialite 4.3 does not build against 8.0.0 as of March 2021.
%if 0%{?rhel} && 0%{?rhel} == 7
%global projmajorversion 72
%global projfullversion 7.2.1
%global projinstdir /usr/proj%{projmajorversion}
%endif

%if 0%{?fedora} >= 33 || 0%{?rhel} >= 7 || 0%{?suse_version} <= 1499
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

%if 0%{?rhel} >= 8 || 0%{?fedora} >= 35
%{!?with_python3:%global with_python3 1}
%else
%{!?with_python3:%global with_python3 0}
%endif

Name:		%{sname}35
Version:	3.5.3
Release:	7PGDG%{?pre:%pre}%{?dist}
Summary:	GIS file format library
License:	MIT
URL:		https://www.gdal.org
# Source0:   http://download.osgeo.org/gdal/%%{version}/gdal-%%{version}.tar.xz
# See PROVENANCE.TXT-fedora and the cleaner script for details!

Source0:	%{sname}-%{version}%{?pre:%pre}-fedora.tar.xz
Source4:	PROVENANCE.TXT-fedora

# Cleaner script for the tarball
Source5:	%{sname}-cleaner.sh

Source6:	%{name}-pgdg-libs.conf

%if 0%{?suse_version} >= 1315
Patch8:		%{sname}-3.2.1-java-sles.patch
%else
# Fedora uses Alternatives for Java
Patch8:		%{sname}-3.1.2-java.patch
%endif

# PGDG patches
Patch12:	%{name}-gdalconfig-pgdg-path.patch
Patch13:	gdal35-configure-ogdi%{ogdimajorversion}.patch

Patch16:	gdal-3.3.1-sfcgal-linker.patch

# lz4 dependency
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	liblz4-devel
Requires:	liblz4-1
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	lz4-devel
Requires:	lz4
%endif

BuildRequires:	cmake gcc-c++ pgdg-srpm-macros >= 1.0.31

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
BuildRequires:	geos%{geosmajorversion}-devel >= %{geosfullversion}
BuildRequires:	ghostscript
BuildRequires:	jpackage-utils
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
BuildRequires:	proj%{projmajorversion}-devel >= %{projfullversion}

%if 0%{?rhel} && 0%{?rhel} == 7
BuildRequires:	%{sqlitepname}-devel
%else
BuildRequires:	sqlite-devel
%endif
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

BuildRequires:	python3-devel

%if 0%{?rhel} && 0%{?rhel} == 7
BuildRequires:	python36-numpy
%else
BuildRequires:	python3-numpy
%endif
BuildRequires:	python3-setuptools

BuildRequires:	qhull-devel

# Run time dependency for gpsbabel driver
Requires:      gpsbabel
Requires:      %{name}-libs%{?_isa} = %{version}-%{release}


%description
Geospatial Data Abstraction Library (GDAL/OGR) is a cross platform
C++ translator library for raster and vector geospatial data formats.
As a library, it presents a single abstract data model to the calling
application for all supported formats. It also comes with a variety of
useful commandline utilities for data translation and processing.

It provides the primary data access engine for many applications.
GDAL/OGR is the most widely used geospatial data access library.


%package devel
Summary:       Development files for the GDAL file format library
Requires:      %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
This package contains development files for GDAL.


%package libs
Summary:       GDAL file format library
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
%if 0%{?fedora} >= 33 || 0%{?rhel} >= 7
Requires:	armadillo
%endif

%description libs
This package contains the GDAL file format library.

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

%if %{with_python3}
%package python3
%{?python_provide:%python_provide python3-gdal}
Summary:	Python modules for the GDAL file format library
Requires:	python3-numpy
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description python3
The GDAL Python 3 modules provide support to handle multiple GIS file formats.


%package python-tools
Summary:	Python tools for the GDAL file format library
Requires:	%{name}-python3%{?_isa} = %{version}-%{release}

%description python-tools
The GDAL Python package provides number of tools for programming and
manipulating GDAL file format library

# We don't want to provide private Python extension libs
%global __provides_exclude_from ^(%{python2_sitearch}|%{python3_sitearch})/.*\.so$
%global __provides_exclude_from ^%{python3_sitearch}/.*\.so$
%endif

%prep
%setup -q -n %{sname}-%{version}-fedora

# Delete bundled libraries
rm -rf frmts/zlib
rm -rf frmts/png/libpng
rm -rf frmts/gif/giflib
rm -rf frmts/jpeg/libjpeg
rm -rf frmts/jpeg/libjpeg12
#rm -rf frmts/gtiff/libgeotiff
rm -rf frmts/gtiff/libtiff
rm -rf mrf/LERCV1
#rm -rf third_party/LercLib

# For patch16:
autoreconf

%patch -P 8 -p0 -b .java~
%patch -P 12 -p0
%patch -P 13 -p0

%patch -P 16 -p0

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
%if %{with_python3}
 -DBUILD_PYTHON_BINDINGS=ON \
%else
 -DBUILD_PYTHON_BINDINGS=OFF \
 %endif
 -DGDAL_JAVA_INSTALL_DIR=%{_jnidir}/%{name} \
 -DCMAKE_PREFIX_PATH="%{geosinstdir};%{libgeotiffinstdir}" \
 -DGDAL_USE_JPEG12_INTERNAL=OFF

%cmake_build

%install
%cmake_install

%if %{with_python3}
# List of manpages for python scripts
for file in %{buildroot}%{gdalinstdir}/bin/*.py; do
  if [ -f %{buildroot}%{gdalinstdir}/share/man/man1/`basename ${file/.py/.1*}` ]; then
    echo "%{gdalinstdir}/share/man/man1/`basename ${file/.py/.1*}`" >> gdal_python_manpages.txt
    echo "%exclude %{gdalinstdir}/share/man/man1/`basename ${file/.py/.1*}`" >> gdal_python_manpages_excludes.txt
  fi
done

%{__mkdir} -p %{buildroot}/%{python3_sitearch}/
%{__mv} %{buildroot}/%{gdalinstdir}/lib64/python%{pyver}/site-packages/GDAL-%{version}-py*.egg-info/  %{buildroot}/%{python3_sitearch}/GDAL-%{version}-py*.egg-info/
%{__mv} %{buildroot}/%{gdalinstdir}/lib64/python%{pyver}/site-packages/osgeo %{buildroot}/%{python3_sitearch}/osgeo/
%{__mv} %{buildroot}/%{gdalinstdir}/lib64/python%{pyver}/site-packages/osgeo_utils %{buildroot}/%{python3_sitearch}/osgeo_utils
%endif

# Install linker config file:
%{__mkdir} -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%{__install} %{SOURCE6} %{buildroot}%{_sysconfdir}/ld.so.conf.d/


%if %{with_python3}
%files -f gdal_python_manpages_excludes.txt
%else
%files
%endif
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
%{gdalinstdir}/lib/libgdal.so.31
%{gdalinstdir}/lib/libgdal.so.31.*
%{gdalinstdir}/share/%{sname}/
%{gdalinstdir}/lib/gdalplugins/
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%files devel
%{gdalinstdir}/bin/%{sname}-config
%dir %{gdalinstdir}/include/
%{gdalinstdir}/include/*.h
%{gdalinstdir}/lib/*.so
%{gdalinstdir}/lib/pkgconfig/%{sname}.pc

%if %{with_python3}
%files python3
%doc swig/python/README.rst
%{python3_sitearch}/GDAL-%{version}-py*.egg-info/
%{python3_sitearch}/osgeo/
%{python3_sitearch}/osgeo_utils/

%files python-tools -f gdal_python_manpages.txt
%{gdalinstdir}/bin/gdal_calc.py
%{gdalinstdir}/bin/gdal_edit.py
%{gdalinstdir}/bin/gdal_fillnodata.py
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
%endif

%files java
%{gdalinstdir}/lib/cmake/%{sname}/GDAL*.cmake
%{_jnidir}/%{name}/gdal-%{version}-javadoc.jar
%{_jnidir}/%{name}/gdal-%{version}-sources.jar
%{_jnidir}/%{name}/gdal-%{version}.jar
%{_jnidir}/%{name}/gdal-%{version}.pom
%{_jnidir}/%{name}/libgdalalljni.so

%files javadoc
%{_jnidir}/%{name}/gdal-%{version}-javadoc.jar

%changelog
* Thu Sep 14 2023 Devrim Gunduz <devrim@gunduz.org> - 3.5.3-7PGDG
- Rebuild against GeOS 3.12 and Proj 9.2

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 3.5.3-6PGDG
- Properly build with GEOS and libgeotiff support, per report and
  patch from Andris Pavenis:
  https://redmine.postgresql.org/issues/7834
- Fix Python builds on RHEL 8. Reported by Mikko Partio, patch from
  Andris Pavenis https://redmine.postgresql.org/issues/7840
- Add PGDG branding

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 3.5.3-5.1
- Modernise %patch usage, which has been deprecated in Fedora 38

* Thu Apr 20 2023 Devrim Gunduz <devrim@gunduz.org> - 3.5.3-5
- Use latest versions of proj and libspatialite on Fedora 38+

* Thu Mar 23 2023 Devrim Gunduz <devrim@gunduz.org> - 3.5.3-4
- Rebuild against GDAL 3.11.2

* Wed Feb 1 2023 Devrim Gunduz <devrim@gunduz.org> - 3.5.3-3
- Copy/fix SLES dependencies from GDAL 3.4 spec file.
- Fix a bunch of rpmlint warnings.

* Sat Nov 12 2022 Devrim Gunduz <devrim@gunduz.org> - 3.5.3-2
- RHEL 8 includes poppler-devel, so no need for our version.

* Tue Nov 1 2022 Devrim Gunduz <devrim@gunduz.org> - 3.5.3-1
- Update to 3.5.3

* Mon Oct 17 2022 Devrim Gunduz <devrim@gunduz.org> - 3.5.2-3
- Install linker config file, per report from Daryl Herzmann.
  Fixes: https://redmine.postgresql.org/issues/7727

* Mon Sep 19 2022 Devrim Gunduz <devrim@gunduz.org> - 3.5.2-2
- Rebuild against GeOS 3.11.0, per report from Laurenz Albe .

* Fri Sep 16 2022 Devrim Gunduz <devrim@gunduz.org> - 3.5.2-1
- Update to 3.5.2

* Sun Aug 28 2022 Devrim Gunduz <devrim@gunduz.org> - 3.5.1-2
- Fix PROJ dependency on RHEL 7.

* Mon Aug 15 2022 Devrim Gunduz <devrim@gunduz.org> - 3.5.1-1
- Final version of the spec file for 3.5.1
