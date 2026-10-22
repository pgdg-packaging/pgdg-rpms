%global		sname freexl
%global		so_version 1
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		freexlinstdir %{pgdg_freexlinstdir}

# The library is found through the rpath only (there is no ld.so.conf.d
# file), so it must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL libraries. Consumers require
# pgdg-freexl by name instead:
%global		__provides_exclude_from ^%{freexlinstdir}/
%global		__requires_exclude ^lib(freexl|minizip)\\.so

%{!?runselftest:%global runselftest 0}

Name:		pgdg-%{sname}
Version:	2.0.0
Release:	1PGDG%{?dist}
Summary:	Library to extract data from within an Excel spreadsheet
License:	MPL-1.1 OR GPL-2.0-or-later OR LGPL-2.1-or-later
URL:		https://www.gaia-gis.it/fossil/freexl/index
Source0:	https://www.gaia-gis.it/gaia-sins/%{sname}-%{version}.tar.gz

BuildRequires:	pgdg-srpm-macros >= 2.1.0
BuildRequires:	autoconf automake libtool gcc make
BuildRequires:	expat-devel
BuildRequires:	pgdg-minizip-ng-devel
Requires:	pgdg-minizip-ng%{?_isa}

%description
FreeXL is a library to extract valid data from within spreadsheets.

Design goals:
  * to be simple and lightweight
  * to be stable, robust and efficient
  * to be easily and universally portable
  * completely ignoring any GUI-related oddity

This package installs FreeXL under %{freexlinstdir}, for the packages in
the PostgreSQL RPM repository.

%package devel
Summary:	Development Libraries for FreeXL
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use FreeXL.

%prep
%setup -q -n %{sname}-%{version}

%build
autoreconf --force --install
export CPPFLAGS="-I%{pgdg_minizipnginstdir}/include"
export LDFLAGS="%{build_ldflags} -L%{pgdg_minizipnginstdir}/lib64 -Wl,-rpath,%{freexlinstdir}/lib64:%{pgdg_minizipnginstdir}/lib64"
%configure --disable-static \
	--prefix=%{freexlinstdir} --exec-prefix=%{freexlinstdir} \
	--libdir=%{freexlinstdir}/lib64 --includedir=%{freexlinstdir}/include
%make_build

%install
%make_install
%{__rm} -f %{buildroot}%{freexlinstdir}/lib64/*.la

%check
%if %runselftest
%make_build check
%endif

%files
%license COPYING
%doc AUTHORS README
%dir %{freexlinstdir}
%dir %{freexlinstdir}/lib64
%{freexlinstdir}/lib64/libfreexl.so.%{so_version}{,.*}

%files devel
%{freexlinstdir}/include/
%{freexlinstdir}/lib64/libfreexl.so
%{freexlinstdir}/lib64/pkgconfig/

%changelog
* Wed Oct 21 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-freexl, so that the GIS stack does not need the EPEL freexl
  package on RHEL. Built against our pgdg-minizip-ng package. Based on the
  Fedora spec file. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422
