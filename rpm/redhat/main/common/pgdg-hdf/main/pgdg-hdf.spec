%global		sname hdf
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		hdfinstdir %{pgdg_hdfinstdir}

# The libraries are found through the rpath only (there is no ld.so.conf.d
# file), so they must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL libraries. Consumers require
# pgdg-hdf by name instead:
%global		__provides_exclude_from ^%{hdfinstdir}/
%global		__requires_exclude ^lib(df|mfhdf|hdf4?[a-z_]*|xdr|sz|aec)\\.so

%{!?runselftest:%global runselftest 0}

%if 0%{?rhel} == 8
%undefine __cmake_in_source_build
%endif

Name:		pgdg-%{sname}
# HDF4 4.4 changed the Vgetclass() API, which GDAL 3.13 does not support yet:
Version:	4.3.1
Release:	1PGDG%{?dist}
Summary:	A general purpose library and file format for storing scientific data
License:	BSD-3-Clause-LBNL AND BSD-3-Clause AND libtiff
URL:		https://www.hdfgroup.org/
Source0:	https://github.com/HDFGroup/hdf4/archive/refs/tags/%{sname}%{version}.tar.gz

BuildRequires:	pgdg-srpm-macros >= 2.1.0
BuildRequires:	cmake >= 3.18 gcc gcc-c++
%if 0%{?suse_version} >= 1500
BuildRequires:	cmake-full
%else
BuildRequires:	cmake-rpm-macros
%endif
BuildRequires:	libjpeg-devel libtirpc-devel zlib-devel
# SZIP support:
BuildRequires:	pgdg-libaec-devel
Requires:	pgdg-libaec%{?_isa}

%description
HDF4 is a general purpose library and file format for storing scientific data.
HDF4 can store two primary objects: datasets and groups. A dataset is
essentially a multidimensional array of data elements, and a group is a
structure for organizing objects in an HDF4 file. Using these two basic
objects, one can create and store almost any kind of scientific data
structure, such as images, arrays of vectors, and structured and unstructured
grids. You can also mix and match them in HDF4 files according to your needs.

This package installs HDF4 under %{hdfinstdir}, for the packages in the
PostgreSQL RPM repository. It can be installed alongside the HDF4 packages
of EPEL.

%package devel
Summary:	HDF4 development files
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	libjpeg-devel%{?_isa} libtirpc-devel%{?_isa} zlib-devel%{?_isa}
Requires:	pgdg-libaec-devel%{?_isa}

%description devel
HDF4 development headers and libraries.

%prep
%setup -q -n hdf4-%{sname}%{version}

%build
%cmake \
	-DCMAKE_INSTALL_PREFIX:PATH=%{hdfinstdir} \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_INSTALL_RPATH:STRING="%{hdfinstdir}/lib64;%{pgdg_libaecinstdir}/lib64" \
	-DHDF4_ONLY_SHARED_LIBS:BOOL=ON \
	-DBUILD_STATIC_LIBS:BOOL=OFF \
	-DHDF4_BUILD_FORTRAN:BOOL=OFF \
	-DHDF4_BUILD_JAVA:BOOL=OFF \
	-DHDF4_BUILD_EXAMPLES:BOOL=OFF \
	-DHDF4_BUILD_TOOLS:BOOL=ON \
	-DHDF4_BUILD_UTILS:BOOL=ON \
	-DHDF4_ENABLE_NETCDF:BOOL=OFF \
	-DHDF4_BUILD_NETCDF_TOOLS:BOOL=OFF \
	-DHDF4_ENABLE_SZIP_SUPPORT:BOOL=ON \
	-DHDF4_ENABLE_SZIP_ENCODING:BOOL=ON \
	-Dlibaec_DIR:PATH=%{pgdg_libaecinstdir}/lib64/cmake/libaec \
%if %runselftest
	-DBUILD_TESTING:BOOL=ON \
%else
	-DBUILD_TESTING:BOOL=OFF \
%endif
	-DHDF4_INSTALL_BIN_DIR=bin \
	-DHDF4_INSTALL_LIB_DIR=lib64 \
	-DHDF4_INSTALL_INCLUDE_DIR=include \
	-DHDF4_INSTALL_CMAKE_DIR=lib64/cmake/%{sname} \
	-DHDF4_INSTALL_DATA_DIR=share/%{sname}
%cmake_build

%install
%cmake_install

%check
%if %runselftest
%ctest
%endif

%files
%license COPYING
%doc README.md
%dir %{hdfinstdir}
%dir %{hdfinstdir}/lib64
%{hdfinstdir}/bin/
%{hdfinstdir}/lib64/lib*.so.*
%{hdfinstdir}/share/

%files devel
%{hdfinstdir}/include/
%{hdfinstdir}/lib64/lib*.so
%{hdfinstdir}/lib64/*.settings
%{hdfinstdir}/lib64/cmake/
%{hdfinstdir}/lib64/pkgconfig/

%changelog
* Wed Oct 21 2026 Devrim Gunduz <devrim@gunduz.org> - 4.3.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-hdf, so that the GIS stack does not need the EPEL hdf package
  on RHEL. SZIP support comes from our pgdg-libaec package. Based on the
  Fedora spec file. 4.3.1, as GDAL 3.13 does not support the Vgetclass()
  API of HDF4 4.4. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422
