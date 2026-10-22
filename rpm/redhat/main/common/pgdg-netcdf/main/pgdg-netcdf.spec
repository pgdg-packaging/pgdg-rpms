%global		sname netcdf
%global		sover 22
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		netcdfinstdir %{pgdg_netcdfinstdir}
# The HDF5 filter plugins go to the default plugin directory of pgdg-hdf5:
%global		plugin_dir %{pgdg_hdf5instdir}/lib64/plugin

# The libraries are found through the rpath only (there is no ld.so.conf.d
# file), so they must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL libraries. Consumers require
# pgdg-netcdf by name instead:
%global		__provides_exclude_from ^(%{netcdfinstdir}|%{plugin_dir})/
%global		__requires_exclude ^lib(netcdf|hdf5.*|hdf|mfhdf|sz|aec|blosc|_+nc[a-z0-9]*)\\.so

%{!?runselftest:%global runselftest 0}

%if 0%{?rhel} == 8
%undefine __cmake_in_source_build
%endif

Name:		pgdg-%{sname}
Version:	4.10.1
Release:	1PGDG%{?dist}
Summary:	Libraries for the Unidata network Common Data Form
License:	BSD-3-Clause
URL:		https://www.unidata.ucar.edu/software/netcdf/
Source0:	https://github.com/Unidata/netcdf-c/archive/v%{version}/%{sname}-%{version}.tar.gz

BuildRequires:	pgdg-srpm-macros >= 2.1.0
BuildRequires:	cmake gcc-c++ gawk m4
%if 0%{?suse_version} >= 1500
BuildRequires:	cmake-full
%else
BuildRequires:	cmake-rpm-macros
%endif
BuildRequires:	bzip2-devel libcurl-devel libxml2-devel libzstd-devel zlib-devel
# Internal S3 support:
BuildRequires:	openssl-devel
# NCZarr zip file storage; RHEL 8 has no libzip:
%if 0%{?rhel} >= 9 || 0%{?fedora}
BuildRequires:	libzip-devel
%endif
BuildRequires:	pgdg-blosc-devel pgdg-hdf-devel pgdg-hdf5-devel pgdg-libaec-devel
Requires:	pgdg-blosc%{?_isa} pgdg-hdf%{?_isa} pgdg-hdf5%{?_isa} pgdg-libaec%{?_isa}

%description
NetCDF (network Common Data Form) is an interface for array-oriented
data access and a freely-distributed collection of software libraries
for C, Fortran, C++, and perl that provides an implementation of the
interface.  The NetCDF library also defines a machine-independent
format for representing scientific data.  Together, the interface,
library, and format support the creation, access, and sharing of
scientific data. The NetCDF software was developed at the Unidata
Program Center in Boulder, Colorado.

This package installs netCDF under %{netcdfinstdir}, for the packages in
the PostgreSQL RPM repository. It is built against our pgdg-hdf5 and
pgdg-hdf packages, with HDF4 support.

%package devel
Summary:	Development files for netcdf
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	libcurl-devel%{?_isa}
Requires:	pgdg-hdf5-devel%{?_isa}

%description devel
This package contains the netCDF C header files, shared devel libs, and
man pages.

%prep
%setup -q -n %{sname}-c-%{version}
# ncgen links libhdf5 directly; keep the library directories in its rpath,
# like for the other tools:
sed -i '/^SET(CMAKE_INSTALL_RPATH_USE_LINK_PATH FALSE)/d' ncgen/CMakeLists.txt

%build
export PKG_CONFIG_PATH=%{pgdg_bloscinstdir}/lib64/pkgconfig
%cmake \
	-DCMAKE_INSTALL_PREFIX:PATH=%{netcdfinstdir} \
	-DCMAKE_INSTALL_LIBDIR:PATH=lib64 \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=include \
	-DCMAKE_PREFIX_PATH:STRING="%{pgdg_hdf5instdir};%{pgdg_hdfinstdir};%{pgdg_libaecinstdir};%{pgdg_bloscinstdir}" \
	-DHDF5_ROOT:PATH=%{pgdg_hdf5instdir} \
	-DMFHDF_H_INCLUDE_DIR:PATH=%{pgdg_hdfinstdir}/include \
	-DCMAKE_INSTALL_RPATH:STRING="%{netcdfinstdir}/lib64;%{pgdg_hdf5instdir}/lib64;%{pgdg_hdfinstdir}/lib64;%{pgdg_libaecinstdir}/lib64;%{pgdg_bloscinstdir}/lib64" \
	-DCMAKE_INSTALL_RPATH_USE_LINK_PATH:BOOL=ON \
	-DNETCDF_ENABLE_DAP_REMOTE_TESTS:BOOL=OFF \
	-DNETCDF_ENABLE_HDF4:BOOL=ON \
	-DNETCDF_ENABLE_S3_INTERNAL:BOOL=ON \
	-DNETCDF_PLUGIN_INSTALL:BOOL=ON \
	-DNETCDF_WITH_PLUGIN_DIR:PATH=%{plugin_dir} \
	-DNETCDF_ENABLE_DOXYGEN:BOOL=OFF \
%if %runselftest
	-DNETCDF_ENABLE_TESTS:BOOL=ON
%else
	-DNETCDF_ENABLE_TESTS:BOOL=OFF
%endif
%cmake_build

%install
%cmake_install

%check
%if %runselftest
%ctest --verbose -E "hdf4_test_run_get_hdf4_files|nczarr_test_run_(external|s3_credentials)"
%endif

%files
%license COPYRIGHT
%doc README.md RELEASE_NOTES.md
%dir %{netcdfinstdir}
%dir %{netcdfinstdir}/bin
%dir %{netcdfinstdir}/lib64
%{netcdfinstdir}/bin/nccopy
%{netcdfinstdir}/bin/ncdump
%{netcdfinstdir}/bin/ncgen
%{netcdfinstdir}/bin/ncgen3
%{plugin_dir}/lib__nc*.so
%{netcdfinstdir}/lib64/*.so.%{sover}*
%{netcdfinstdir}/share/man/man1/*

%files devel
%{netcdfinstdir}/bin/nc-config
%{netcdfinstdir}/include/
%{netcdfinstdir}/lib64/libnetcdf.settings
%{netcdfinstdir}/lib64/*.so
%{netcdfinstdir}/lib64/cmake/
%{netcdfinstdir}/lib64/pkgconfig/
%{netcdfinstdir}/share/man/man3/*

%changelog
* Wed Oct 21 2026 Devrim Gunduz <devrim@gunduz.org> - 4.10.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-netcdf, so that the GIS stack does not need the EPEL netcdf
  package on RHEL. Built against our pgdg-hdf5, pgdg-hdf, pgdg-libaec and
  pgdg-blosc packages. Based on the Fedora spec file. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
