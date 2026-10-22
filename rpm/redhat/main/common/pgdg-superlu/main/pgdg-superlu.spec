%global		sname superlu
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		superluinstdir %{pgdg_superluinstdir}

# The library is found through the rpath only (there is no ld.so.conf.d
# file), so it must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL SuperLU. Consumers require
# pgdg-superlu by name instead:
%global		__provides_exclude_from ^%{superluinstdir}/
%global		__requires_exclude ^libsuperlu\\.so

%{!?runselftest:%global runselftest 0}

%if 0%{?rhel} == 8
%undefine __cmake_in_source_build
%endif

Name:		pgdg-%{sname}
Version:	7.0.1
Release:	1PGDG%{?dist}
Summary:	Subroutines to solve sparse linear systems
License:	BSD-3-Clause-LBNL
URL:		https://portal.nersc.gov/project/sparse/superlu/
Source0:	https://github.com/xiaoyeli/superlu/archive/v%{version}/%{sname}-%{version}.tar.gz
# From the Fedora package. Remove mc64ad.c, which is not free software:
Patch0:		superlu-removemc64.patch

BuildRequires:	pgdg-srpm-macros >= 2.1.0
BuildRequires:	cmake gcc gcc-gfortran make
%if 0%{?suse_version} >= 1500
BuildRequires:	cmake-full
%else
BuildRequires:	cmake-rpm-macros
%endif
%if 0%{?rhel} == 8
BuildRequires:	openblas-devel
%else
BuildRequires:	flexiblas-devel
%endif

%description
SuperLU contains a set of subroutines to solve a sparse linear system
A*X=B. It uses Gaussian elimination with partial pivoting (GEPP).
The columns of A may be preordered before factorization; the
preordering for sparsity is completely separate from the factorization.

This package installs SuperLU under %{superluinstdir}, for the packages in
the PostgreSQL RPM repository. It is built without the optional METIS
ordering; the built in orderings (COLAMD, MMD) are available.

%package devel
Summary:	Header files and libraries for SuperLU development
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains the header files and libraries for use
with SuperLU.

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p1
%{__rm} -rf CBLAS
sed -e 's|-O0|-O2|g' -i SRC/CMakeLists.txt

%build
%if 0%{?rhel} == 8
%global		blaslibs -lopenblas
%else
%global		blaslibs -lflexiblas
%endif
%cmake \
	-DCMAKE_INSTALL_PREFIX:PATH=%{superluinstdir} \
	-DCMAKE_INSTALL_LIBDIR:PATH=lib64 \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=include/SuperLU \
	-DCMAKE_INSTALL_RPATH:PATH=%{superluinstdir}/lib64 \
	-Denable_internal_blaslib:BOOL=NO \
	-DXSDK_ENABLE_Fortran:BOOL=OFF \
	-DTPL_BLAS_LIBRARIES="%{blaslibs}" \
	-DTPL_ENABLE_METISLIB:BOOL=OFF \
	-Denable_examples:BOOL=OFF \
%if %runselftest
	-Denable_tests:BOOL=ON \
%else
	-Denable_tests:BOOL=OFF \
%endif
	-DCMAKE_BUILD_TYPE:STRING=Release
%cmake_build

%install
%cmake_install

%check
%if %runselftest
%ctest
%endif

%files
%license License.txt
%dir %{superluinstdir}
%dir %{superluinstdir}/lib64
%{superluinstdir}/lib64/libsuperlu.so.7
%{superluinstdir}/lib64/libsuperlu.so.%{version}

%files devel
%{superluinstdir}/include/
%{superluinstdir}/lib64/libsuperlu.so
%{superluinstdir}/lib64/cmake/
%{superluinstdir}/lib64/pkgconfig/

%changelog
* Wed Oct 21 2026 Devrim Gunduz <devrim@gunduz.org> - 7.0.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-superlu, so that the GIS stack does not need the EPEL SuperLU
  package on RHEL. Based on the Fedora spec file. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
