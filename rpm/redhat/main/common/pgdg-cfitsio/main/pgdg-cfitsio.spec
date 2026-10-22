%global		sname cfitsio
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		cfitsioinstdir %{pgdg_cfitsioinstdir}

# The library is found through the rpath only (there is no ld.so.conf.d
# file), so it must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL cfitsio. Consumers require
# pgdg-cfitsio by name instead:
%global		__provides_exclude_from ^%{cfitsioinstdir}/
%global		__requires_exclude ^libcfitsio\\.so

%{!?runselftest:%global runselftest 0}

Name:		pgdg-%{sname}
Version:	4.7.0
Release:	1PGDG%{?dist}
Summary:	Library for manipulating FITS data files
License:	CFITSIO
URL:		https://heasarc.gsfc.nasa.gov/fitsio/
Source0:	https://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/%{sname}-%{version}.tar.gz

BuildRequires:	pgdg-srpm-macros >= 2.1.0
BuildRequires:	gcc gcc-gfortran make
BuildRequires:	bzip2-devel curl-devel zlib-devel

%description
CFITSIO is a library of C and FORTRAN subroutines for reading and writing
data files in FITS (Flexible Image Transport System) data format. CFITSIO
simplifies the task of writing software that deals with FITS files by
providing an easy to use set of high-level routines that insulate the
programmer from the internal complexities of the FITS file format. At the
same time, CFITSIO provides many advanced features that have made it the
most widely used FITS file programming interface in the astronomical
community.

This package installs CFITSIO under %{cfitsioinstdir}, for the packages
in the PostgreSQL RPM repository.

%package devel
Summary:	Headers required when building programs against cfitsio
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Headers required when building a program against the cfitsio library.

%package utils
Summary:	CFITSIO based utilities
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description utils
This package contains utility programs provided by CFITSIO.

%prep
%setup -q -n %{sname}-%{version}

%build
export LDFLAGS="%{build_ldflags} -Wl,-rpath,%{cfitsioinstdir}/lib64"
%configure --enable-reentrant --with-bzip2 \
	--prefix=%{cfitsioinstdir} --exec-prefix=%{cfitsioinstdir} \
	--bindir=%{cfitsioinstdir}/bin --libdir=%{cfitsioinstdir}/lib64 \
	--includedir=%{cfitsioinstdir}/include
%make_build

%install
%make_install
%{__rm} %{buildroot}%{cfitsioinstdir}/bin/cookbook
%{__rm} %{buildroot}%{cfitsioinstdir}/bin/smem
%{__rm} %{buildroot}%{cfitsioinstdir}/bin/speed
%{__rm} -f %{buildroot}%{cfitsioinstdir}/lib64/libcfitsio.a %{buildroot}%{cfitsioinstdir}/lib64/libcfitsio.la

%check
%if %runselftest
make testprog
LD_LIBRARY_PATH=. ./testprog > testprog.lis
cmp -s testprog.lis testprog.out
cmp -s testprog.fit testprog.std
%endif

%files
%doc README.md ChangeLog
%license licenses/License.txt
%dir %{cfitsioinstdir}
%dir %{cfitsioinstdir}/lib64
%{cfitsioinstdir}/lib64/libcfitsio.so.10*

%files devel
%doc utilities/cookbook.*
%{cfitsioinstdir}/include/
%{cfitsioinstdir}/lib64/libcfitsio.so
%{cfitsioinstdir}/lib64/pkgconfig/

%files utils
%license licenses/License.txt
%dir %{cfitsioinstdir}/bin
%{cfitsioinstdir}/bin/fitsverify
%{cfitsioinstdir}/bin/fitscopy
%{cfitsioinstdir}/bin/fpack
%{cfitsioinstdir}/bin/funpack
%{cfitsioinstdir}/bin/imcopy

%changelog
* Wed Oct 21 2026 Devrim Gunduz <devrim@gunduz.org> - 4.7.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-cfitsio, so that the GIS stack does not need the EPEL cfitsio
  package on RHEL. Based on the Fedora spec file. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
