%global		sname opencv
%global		abiver 414
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		opencvinstdir %{pgdg_opencvinstdir}

# The libraries are found through the rpath only (there is no ld.so.conf.d
# file), so they must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL OpenCV. Consumers require
# pgdg-opencv by name instead:
%global		__provides_exclude_from ^%{opencvinstdir}/
%global		__requires_exclude ^libopencv_.*\\.so

%if 0%{?rhel} == 8
%undefine __cmake_in_source_build
%endif

Name:		pgdg-%{sname}
Version:	4.14.0
Release:	1PGDG%{?dist}
Summary:	Collection of algorithms for computer vision (core, imgproc, imgcodecs)
License:	Apache-2.0
URL:		https://opencv.org
# The upstream tarball without the "Lena" image, made with opencv-clean.sh,
# as in the Fedora package:
Source0:	https://download.postgresql.org/pub/repos/yum/sources/opencv/%{sname}-clean-%{version}.tar.gz

BuildRequires:	pgdg-srpm-macros >= 2.1.0
BuildRequires:	cmake gcc-c++ ninja-build
%if 0%{?suse_version} >= 1500
BuildRequires:	cmake-full
%else
BuildRequires:	cmake-rpm-macros
%endif
BuildRequires:	eigen3-devel libjpeg-devel libpng-devel libtiff-devel
BuildRequires:	libwebp-devel openjpeg2-devel zlib-devel

%description
OpenCV means Intel(R) Open Source Computer Vision Library. It is a collection
of C functions and a few C++ classes that implement many popular Image
Processing and Computer Vision algorithms.

This package installs the core, imgproc and imgcodecs modules of OpenCV
under %{opencvinstdir}, for the packages in the PostgreSQL RPM repository
(osm2pgsql-gen).

%package devel
Summary:	Development files for using the OpenCV library
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the OpenCV C/C++ library and header files, as well as
documentation. It should be installed if you want to develop programs that
will use the OpenCV library.

%prep
%setup -q -n %{sname}-%{version}
# Use the libraries of the OS, not the bundled ones:
%{__rm} -r 3rdparty/libjpeg 3rdparty/libjpeg-turbo 3rdparty/libpng \
	3rdparty/libtiff 3rdparty/libwebp 3rdparty/openjpeg 3rdparty/zlib

%build
%cmake -GNinja \
	-DCMAKE_INSTALL_PREFIX:PATH=%{opencvinstdir} \
	-DCMAKE_INSTALL_LIBDIR:PATH=lib64 \
	-DCMAKE_INSTALL_RPATH:PATH=%{opencvinstdir}/lib64 \
	-DCMAKE_BUILD_TYPE=Release \
	-DBUILD_LIST=core,imgproc,imgcodecs \
	-DOPENCV_GENERATE_PKGCONFIG:BOOL=ON \
	-DOPENCV_CONFIG_INSTALL_PATH=lib64/cmake/opencv4 \
	-DOPENCV_LICENSES_INSTALL_PATH=share/licenses/%{name} \
	-DBUILD_SHARED_LIBS:BOOL=ON \
	-DBUILD_TESTS:BOOL=OFF -DBUILD_PERF_TESTS:BOOL=OFF \
	-DBUILD_EXAMPLES:BOOL=OFF -DBUILD_DOCS:BOOL=OFF \
	-DBUILD_JAVA:BOOL=OFF -DBUILD_opencv_python3:BOOL=OFF \
	-DBUILD_opencv_apps:BOOL=OFF \
	-DBUILD_ZLIB:BOOL=OFF -DBUILD_JPEG:BOOL=OFF -DBUILD_PNG:BOOL=OFF \
	-DBUILD_TIFF:BOOL=OFF -DBUILD_WEBP:BOOL=OFF -DBUILD_OPENJPEG:BOOL=OFF \
	-DWITH_JPEG:BOOL=ON -DWITH_PNG:BOOL=ON -DWITH_TIFF:BOOL=ON \
	-DWITH_WEBP:BOOL=ON -DWITH_OPENJPEG:BOOL=ON -DWITH_JASPER:BOOL=OFF \
	-DWITH_EIGEN:BOOL=ON \
	-DWITH_GDAL:BOOL=OFF -DWITH_GDCM:BOOL=OFF -DWITH_OPENEXR:BOOL=OFF \
	-DWITH_IMGCODEC_HDR:BOOL=ON -DWITH_IMGCODEC_SUNRASTER:BOOL=ON \
	-DWITH_IMGCODEC_PXM:BOOL=ON -DWITH_IMGCODEC_PFM:BOOL=ON \
	-DWITH_FFMPEG:BOOL=OFF -DWITH_GSTREAMER:BOOL=OFF -DWITH_V4L:BOOL=OFF \
	-DWITH_GTK:BOOL=OFF -DWITH_QT:BOOL=OFF -DWITH_VTK:BOOL=OFF \
	-DWITH_IPP:BOOL=OFF -DWITH_ITT:BOOL=OFF -DWITH_ADE:BOOL=OFF \
	-DWITH_PROTOBUF:BOOL=OFF -DWITH_OPENCL:BOOL=OFF -DWITH_LAPACK:BOOL=OFF \
	-DWITH_CAROTENE:BOOL=OFF -DWITH_KLEIDICV:BOOL=OFF \
	-DOPENCV_DOWNLOAD_TRIES_LIST=0 \
	-DCPU_BASELINE_DISABLE=SSE3 -DCPU_BASELINE_REQUIRE=SSE2
%cmake_build

%install
%cmake_install
%{__rm} -rf %{buildroot}%{opencvinstdir}/share/opencv4/valgrind* %{buildroot}%{opencvinstdir}/bin/setup_vars_opencv4.sh

%files
%license LICENSE
%dir %{opencvinstdir}
%dir %{opencvinstdir}/lib64
%{opencvinstdir}/lib64/libopencv_core.so.%{abiver}*
%{opencvinstdir}/lib64/libopencv_core.so.%{version}
%{opencvinstdir}/lib64/libopencv_imgproc.so.%{abiver}*
%{opencvinstdir}/lib64/libopencv_imgproc.so.%{version}
%{opencvinstdir}/lib64/libopencv_imgcodecs.so.%{abiver}*
%{opencvinstdir}/lib64/libopencv_imgcodecs.so.%{version}
%{opencvinstdir}/share/

%files devel
%{opencvinstdir}/include/
%{opencvinstdir}/lib64/libopencv_*.so
%{opencvinstdir}/lib64/cmake/
%{opencvinstdir}/lib64/pkgconfig/

%changelog
* Wed Oct 21 2026 Devrim Gunduz <devrim@gunduz.org> - 4.14.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-opencv, so that osm2pgsql-gen does not need the EPEL opencv
  packages on RHEL 10. Only the core, imgproc and imgcodecs modules that
  osm2pgsql uses are built. Based on the Fedora spec file. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
