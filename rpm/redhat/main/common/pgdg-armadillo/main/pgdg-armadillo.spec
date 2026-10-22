%global		sname armadillo
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		armadilloinstdir %{pgdg_armadilloinstdir}

# The library is found through the rpath only (there is no ld.so.conf.d
# file), so it must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL libraries. Consumers require
# pgdg-armadillo by name instead:
%global		__provides_exclude_from ^%{armadilloinstdir}/
%global		__requires_exclude ^lib(armadillo|arpack|superlu)\\.so

%{!?runselftest:%global runselftest 0}

%if 0%{?rhel} == 8
%undefine __cmake_in_source_build
%endif

Name:		pgdg-%{sname}
Version:	15.6.2
Release:	1PGDG%{?dist}
Summary:	Fast C++ matrix library with syntax similar to MATLAB and Octave
License:	Apache-2.0
URL:		https://arma.sourceforge.net/
Source0:	https://sourceforge.net/projects/arma/files/%{sname}-%{version}.tar.xz

BuildRequires:	pgdg-srpm-macros >= 2.1.0
BuildRequires:	cmake gcc-c++ make
%if 0%{?suse_version} >= 1500
BuildRequires:	cmake-full
%else
BuildRequires:	cmake-rpm-macros
%endif
BuildRequires:	pgdg-arpack-devel pgdg-superlu-devel
Requires:	pgdg-arpack%{?_isa} pgdg-superlu%{?_isa}
# RHEL 8 does not have FlexiBLAS:
%if 0%{?rhel} == 8
BuildRequires:	openblas-devel lapack-devel
%else
BuildRequires:	flexiblas-devel
%endif

%description
Armadillo is a C++ linear algebra library (matrix maths)
aiming towards a good balance between speed and ease of use.
Integer, floating point and complex numbers are supported,
as well as a subset of trigonometric and statistics functions.
Various matrix decompositions are provided through optional
integration with LAPACK and ATLAS libraries.

This package installs Armadillo under %{armadilloinstdir}, for the
packages in the PostgreSQL RPM repository. It is built with ARPACK and
SuperLU support, from our pgdg-arpack and pgdg-superlu packages.

%package devel
Summary:	Development headers for the Armadillo C++ library
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	libstdc++-devel
Requires:	pgdg-arpack-devel%{?_isa} pgdg-superlu-devel%{?_isa}
%if 0%{?rhel} == 8
Requires:	openblas-devel lapack-devel
%else
Requires:	flexiblas-devel
%endif
# For ARMA_USE_HDF5:
Recommends:	pgdg-hdf5-devel

%description devel
This package contains files necessary for development using the
Armadillo C++ library.

%prep
%setup -q -n %{sname}-%{version}
sed -i 's/\r//' README.md

%build
# Use the same (serial) OpenBLAS library as pgdg-arpack and pgdg-superlu
# on RHEL 8, not the OpenMP one that armadillo would pick first:
%cmake \
	-DCMAKE_INSTALL_PREFIX:PATH=%{armadilloinstdir} \
	-DCMAKE_INSTALL_LIBDIR:PATH=lib64 \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=include \
	-DCMAKE_PREFIX_PATH:STRING="%{pgdg_arpackinstdir};%{pgdg_superluinstdir}" \
	-DCMAKE_INCLUDE_PATH:STRING="%{pgdg_superluinstdir}/include/SuperLU" \
	-DCMAKE_INSTALL_RPATH:STRING="%{armadilloinstdir}/lib64;%{pgdg_arpackinstdir}/lib64;%{pgdg_superluinstdir}/lib64" \
	-DCMAKE_INSTALL_RPATH_USE_LINK_PATH:BOOL=ON \
%if 0%{?rhel} == 8
	-DALLOW_FLEXIBLAS_LINUX:BOOL=OFF \
	-DOPENBLAS_PROVIDES_LAPACK:BOOL=ON \
	-Dopenblaso_LIBRARY:FILEPATH=%{_libdir}/libopenblas.so \
	-Dopenblasp_LIBRARY:FILEPATH=%{_libdir}/libopenblas.so \
%else
	-DALLOW_FLEXIBLAS_LINUX:BOOL=ON \
%endif
	-DBUILD_SMOKE_TEST:BOOL=OFF
%cmake_build

%install
%cmake_install

%files
%license LICENSE.txt NOTICE.txt
%doc README.md
%dir %{armadilloinstdir}
%dir %{armadilloinstdir}/lib64
%{armadilloinstdir}/lib64/libarmadillo.so.15*

%files devel
%{armadilloinstdir}/include/
%{armadilloinstdir}/lib64/libarmadillo.so
%{armadilloinstdir}/lib64/pkgconfig/
%{armadilloinstdir}/share/

%changelog
* Wed Oct 21 2026 Devrim Gunduz <devrim@gunduz.org> - 15.6.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-armadillo, so that the GIS stack does not need the EPEL
  armadillo package on RHEL. Built against our pgdg-arpack and pgdg-superlu
  packages. Based on the Fedora spec file. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
