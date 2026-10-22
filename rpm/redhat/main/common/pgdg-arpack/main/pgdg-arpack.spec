%global		sname arpack
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		arpackinstdir %{pgdg_arpackinstdir}

# The library is found through the rpath only (there is no ld.so.conf.d
# file), so it must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL arpack. Consumers require
# pgdg-arpack by name instead:
%global		__provides_exclude_from ^%{arpackinstdir}/
%global		__requires_exclude ^libarpack\\.so

%undefine	_ld_as_needed
%{!?runselftest:%global runselftest 0}

# RHEL 8 does not have FlexiBLAS:
%if 0%{?rhel} == 8
%global		blaslib -lopenblas
%else
%global		blaslib -lflexiblas
%endif

Name:		pgdg-%{sname}
Version:	3.9.1
Release:	1PGDG%{?dist}
Summary:	Fortran 77 subroutines for solving large scale eigenvalue problems
License:	BSD-3-Clause
URL:		https://github.com/opencollab/arpack-ng
Source0:	https://github.com/opencollab/arpack-ng/archive/%{version}/arpack-ng-%{version}.tar.gz

BuildRequires:	pgdg-srpm-macros >= 2.1.0
BuildRequires:	gcc-c++ gcc-gfortran make libtool >= 2.4.2
BuildRequires:	eigen3-devel
%if 0%{?rhel} == 8
BuildRequires:	openblas-devel
%else
BuildRequires:	flexiblas-devel
%endif

%description
ARPACK is a collection of Fortran 77 subroutines designed to solve large
scale eigenvalue problems.

The package is designed to compute a few eigenvalues and corresponding
eigenvectors of a general n by n matrix A. It is most appropriate for
large sparse or structured matrices A where structured means that a
matrix-vector product w <- Av requires order n rather than the usual
order n**2 floating point operations. This software is based upon an
algorithmic variant of the Arnoldi process called the Implicitly
Restarted Arnoldi Method (IRAM).

This package installs ARPACK under %{arpackinstdir}, for the packages in
the PostgreSQL RPM repository.

%package devel
Summary:	Files needed for developing arpack based applications
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the so library links used for building arpack
based applications.

%prep
%setup -q -n arpack-ng-%{version}
autoreconf -vif

%build
export LDFLAGS="%{build_ldflags} -Wl,-rpath,%{arpackinstdir}/lib64"
%configure --enable-shared --disable-static \
	--prefix=%{arpackinstdir} --exec-prefix=%{arpackinstdir} \
	--libdir=%{arpackinstdir}/lib64 --includedir=%{arpackinstdir}/include \
	--with-blas=%{blaslib} --with-lapack=%{blaslib} \
	--enable-eigen --enable-icb
%make_build

%install
%make_install
%{__rm} -f %{buildroot}%{arpackinstdir}/lib64/*.la

%check
%if %runselftest
make check
%endif

%files
%doc CHANGES README.md
%license COPYING
%dir %{arpackinstdir}
%dir %{arpackinstdir}/lib64
%{arpackinstdir}/lib64/libarpack.so.2{,.*}

%files devel
%{arpackinstdir}/include/
%{arpackinstdir}/lib64/libarpack.so
%{arpackinstdir}/lib64/pkgconfig/

%changelog
* Wed Oct 21 2026 Devrim Gunduz <devrim@gunduz.org> - 3.9.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-arpack, so that the GIS stack does not need the EPEL arpack
  package on RHEL. Based on the Fedora spec file. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
