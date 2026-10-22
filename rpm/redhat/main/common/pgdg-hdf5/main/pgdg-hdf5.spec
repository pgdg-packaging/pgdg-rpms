%global		sname hdf5
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		hdf5instdir %{pgdg_hdf5instdir}
%global		_hdf5libdir lib64
# Soname major: LT_VERS_INTERFACE - LT_VERS_AGE in config/lt_vers.am
%global		so_version 320
%global		plugin_dir %{hdf5instdir}/%{_hdf5libdir}/plugin

# The libraries are found through the rpath only (there is no ld.so.conf.d
# file), so they must not satisfy the libhdf5 dependencies of OS or EPEL
# packages, and our packages must not pick the OS or EPEL HDF5 libraries.
# Consumers require pgdg-hdf5 by name instead:
%global		__provides_exclude_from ^%{hdf5instdir}/
%global		__requires_exclude ^lib(hdf5.*|sz|aec)\\.so

%{!?runselftest:%global runselftest 0}

# HDF5 refuses in-source builds, which is the %%cmake default on RHEL 8:
%if 0%{?rhel} == 8
%undefine __cmake_in_source_build
%endif

Name:		pgdg-%{sname}
Version:	2.2.0
Release:	1PGDG%{?dist}
Summary:	A general purpose library and file format for storing scientific data
License:	BSD-3-Clause
URL:		https://www.hdfgroup.org/solutions/hdf5/
Source0:	https://github.com/HDFGroup/%{sname}/archive/%{version}/%{sname}-%{version}.tar.gz

BuildRequires:	pgdg-srpm-macros >= 2.1.0
BuildRequires:	cmake >= 3.26
%if 0%{?suse_version} >= 1500
BuildRequires:	cmake-full
%else
BuildRequires:	cmake-rpm-macros
%endif
BuildRequires:	gcc gcc-c++ gcc-gfortran
BuildRequires:	zlib-devel
# SZIP support:
BuildRequires:	pgdg-libaec-devel
Requires:	pgdg-libaec%{?_isa}
%if %runselftest
BuildRequires:	hostname perl-interpreter time
%endif

%description
HDF5 is a general purpose library and file format for storing scientific data.
HDF5 can store two primary objects: datasets and groups. A dataset is
essentially a multidimensional array of data elements, and a group is a
structure for organizing objects in an HDF5 file. Using these two basic
objects, one can create and store almost any kind of scientific data
structure, such as images, arrays of vectors, and structured and unstructured
grids. You can also mix and match them in HDF5 files according to your needs.

This package installs HDF5 under %{hdf5instdir}, for the packages in the
PostgreSQL RPM repository. It can be installed alongside the HDF5 packages
of the OS and EPEL.

%package devel
Summary:	HDF5 development files
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	zlib-devel%{?_isa}
Requires:	pgdg-libaec-devel%{?_isa}
Requires:	gcc-gfortran%{?_isa}

%description devel
HDF5 development headers and libraries. Programs that link against them
need an rpath to %{hdf5instdir}/%{_hdf5libdir}; the h5cc, h5c++ and h5fc
wrappers add it.

%prep
%setup -q -n %{sname}-%{version}

# Force shared by default for compiler wrappers (Fedora bug #1266645)
sed -i -e '/^STATIC_AVAILABLE=/s/=.*/=no/' */*/h5[cf]*.in

%build
%cmake \
	-DCMAKE_INSTALL_PREFIX:PATH=%{hdf5instdir} \
	-DCMAKE_BUILD_TYPE=Release \
	-DBUILD_STATIC_LIBS:BOOL=OFF \
	-DCMAKE_INSTALL_RPATH:STRING="%{hdf5instdir}/%{_hdf5libdir};%{pgdg_libaecinstdir}/lib64" \
	-DH5_DEFAULT_PLUGINDIR=%{plugin_dir} \
	-DHDF5_BUILD_CPP_LIB:BOOL=ON \
	-DHDF5_BUILD_EXAMPLES:BOOL=OFF \
	-DHDF5_BUILD_FORTRAN:BOOL=ON \
	-DHDF5_BUILD_HL_LIB:BOOL=ON \
	-DHDF5_BUILD_JAVA:BOOL=OFF \
	-DHDF5_BUILD_TOOLS:BOOL=ON \
	-DHDF5_ENABLE_ZLIB_SUPPORT:BOOL=ON \
	-DHDF5_ENABLE_SZIP_SUPPORT:BOOL=ON \
	-DHDF5_ENABLE_SZIP_ENCODING:BOOL=ON \
	-DSZIP_USE_EXTERNAL:BOOL=OFF \
	-DHDF5_USE_LIBAEC_STATIC:BOOL=OFF \
	-Dlibaec_DIR:PATH=%{pgdg_libaecinstdir}/lib64/cmake/libaec \
%if %runselftest
	-DBUILD_TESTING:BOOL=ON \
%else
	-DBUILD_TESTING:BOOL=OFF \
%endif
	-DHDF5_INSTALL_BIN_DIR=bin \
	-DHDF5_INSTALL_LIB_DIR=%{_hdf5libdir} \
	-DHDF5_INSTALL_INCLUDE_DIR=include \
	-DHDF5_INSTALL_MODULE_DIR=include \
	-DHDF5_INSTALL_CMAKE_DIR=%{_hdf5libdir}/cmake/%{sname} \
	-DHDF5_INSTALL_DATA_DIR=share/%{sname}

%cmake_build

%install
%cmake_install

# Plugin directory:
%{__mkdir} -p %{buildroot}%{plugin_dir}

# Let CMake consumers find our libaec without setting libaec_DIR:
sed -i 's|^\(\s*\)find_dependency (libaec |\1if (NOT DEFINED libaec_DIR)\n\1  set (libaec_DIR "%{pgdg_libaecinstdir}/lib64/cmake/libaec")\n\1endif ()\n\1find_dependency (libaec |' \
	%{buildroot}%{hdf5instdir}/%{_hdf5libdir}/cmake/%{sname}/hdf5-config.cmake
grep -q 'pgdg-libaec\|%{pgdg_libaecinstdir}' %{buildroot}%{hdf5instdir}/%{_hdf5libdir}/cmake/%{sname}/hdf5-config.cmake

%check
%if %runselftest
%ctest
%endif

%files
%license LICENSE
%doc ACKNOWLEDGMENTS README.md
%dir %{hdf5instdir}
%dir %{hdf5instdir}/bin
%{hdf5instdir}/bin/h5clear
%{hdf5instdir}/bin/h5copy
%{hdf5instdir}/bin/h5debug
%{hdf5instdir}/bin/h5delete
%{hdf5instdir}/bin/h5diff
%{hdf5instdir}/bin/h5dump
%{hdf5instdir}/bin/h5format_convert
%{hdf5instdir}/bin/h5import
%{hdf5instdir}/bin/h5jam
%{hdf5instdir}/bin/h5ls
%{hdf5instdir}/bin/h5mkgrp
%{hdf5instdir}/bin/h5perf_serial
%{hdf5instdir}/bin/h5repack
%{hdf5instdir}/bin/h5repart
%{hdf5instdir}/bin/h5stat
%{hdf5instdir}/bin/h5unjam
%{hdf5instdir}/bin/h5watch
%dir %{hdf5instdir}/%{_hdf5libdir}
%{plugin_dir}/
%{hdf5instdir}/%{_hdf5libdir}/libhdf5.so.%{so_version}*
%{hdf5instdir}/%{_hdf5libdir}/libhdf5_cpp.so.%{so_version}*
%{hdf5instdir}/%{_hdf5libdir}/libhdf5_fortran.so.%{so_version}*
%{hdf5instdir}/%{_hdf5libdir}/libhdf5_f90cstub.so.%{so_version}*
%{hdf5instdir}/%{_hdf5libdir}/libhdf5_hl.so.%{so_version}*
%{hdf5instdir}/%{_hdf5libdir}/libhdf5_hl_cpp.so.%{so_version}*
%{hdf5instdir}/%{_hdf5libdir}/libhdf5_hl_f90cstub.so.%{so_version}*
%{hdf5instdir}/%{_hdf5libdir}/libhdf5_hl_fortran.so.%{so_version}*
%{hdf5instdir}/%{_hdf5libdir}/libhdf5_tools.so.%{so_version}*
%{hdf5instdir}/share/

%files devel
%{hdf5instdir}/bin/h5c++
%{hdf5instdir}/bin/h5cc
%{hdf5instdir}/bin/h5fc
%{hdf5instdir}/include/
%{hdf5instdir}/%{_hdf5libdir}/lib*.so
%{hdf5instdir}/%{_hdf5libdir}/lib*.settings
%{hdf5instdir}/%{_hdf5libdir}/cmake/
%{hdf5instdir}/%{_hdf5libdir}/pkgconfig/

%changelog
* Wed Oct 21 2026 Devrim Gunduz <devrim@gunduz.org> - 2.2.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-hdf5, so that the GIS stack does not need the EPEL HDF5
  package on RHEL. Based on the Fedora spec file. SZIP support comes from
  our pgdg-libaec package. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
