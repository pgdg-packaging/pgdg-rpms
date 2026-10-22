%global		sname qhull
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		qhullinstdir %{pgdg_qhullinstdir}

# The libraries are found through the rpath only (there is no ld.so.conf.d
# file), so they must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL qhull. Consumers require
# pgdg-qhull by name instead:
%global		__provides_exclude_from ^%{qhullinstdir}/
%global		__requires_exclude ^libqhull.*\\.so

%if 0%{?rhel} == 8
%undefine __cmake_in_source_build
%endif

Name:		pgdg-%{sname}
Version:	8.0.2
Release:	1PGDG%{?dist}
Summary:	General dimension convex hull programs
License:	Qhull
URL:		http://www.qhull.org
Source0:	https://github.com/qhull/qhull/archive/v%{version}.tar.gz#/%{sname}-%{version}.tar.gz
# From the Fedora package:
Patch0:		qhull-lib64.patch
Patch1:		qhull-install.patch
Patch2:		qhull-staticr-pic.patch

BuildRequires:	pgdg-srpm-macros >= 2.1.0
BuildRequires:	cmake gcc gcc-c++ make
%if 0%{?suse_version} >= 1500
BuildRequires:	cmake-full
%else
BuildRequires:	cmake-rpm-macros
%endif

%description
Qhull is a general dimension convex hull program that reads a set
of points from stdin, and outputs the smallest convex set that contains
the points to stdout.  It also generates Delaunay triangulations, Voronoi
diagrams, furthest-site Voronoi diagrams, and halfspace intersections
about a point.

This package installs Qhull, its programs and its libraries (libqhull,
libqhull_r and libqhull_p) under %{qhullinstdir}, for the packages in the
PostgreSQL RPM repository.

%package devel
Summary:	Development files for qhull
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for qhull.

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1
sed -i -e 's@cmake_minimum_required(VERSION 3.0)@cmake_minimum_required(VERSION 3.10)@' CMakeLists.txt

%build
%cmake \
	-DCMAKE_INSTALL_PREFIX:PATH=%{qhullinstdir} \
	-DLIB_INSTALL_DIR:PATH=%{qhullinstdir}/lib64 \
	-DBIN_INSTALL_DIR:PATH=%{qhullinstdir}/bin \
	-DINCLUDE_INSTALL_DIR:PATH=%{qhullinstdir}/include \
	-DMAN_INSTALL_DIR:PATH=%{qhullinstdir}/share/man/man1 \
	-DDOC_INSTALL_DIR:PATH=%{qhullinstdir}/share/doc/%{sname} \
	-DCMAKE_INSTALL_RPATH:PATH=%{qhullinstdir}/lib64 \
	-DLINK_APPS_SHARED:BOOL=ON
%cmake_build
%cmake_build -t libqhull qhull_p

%install
%cmake_install

%files
%license COPYING.txt
%doc README.txt REGISTER.txt Announce.txt
%dir %{qhullinstdir}
%dir %{qhullinstdir}/lib64
%{qhullinstdir}/bin/
%{qhullinstdir}/lib64/libqhull.so.*
%{qhullinstdir}/lib64/libqhull_r.so.*
%{qhullinstdir}/lib64/libqhull_p.so.*
%{qhullinstdir}/share/

%files devel
%{qhullinstdir}/include/
%{qhullinstdir}/lib64/*.so
%{qhullinstdir}/lib64/libqhullcpp.a
%{qhullinstdir}/lib64/libqhullstatic*.a
%{qhullinstdir}/lib64/cmake/
%{qhullinstdir}/lib64/pkgconfig/

%changelog
* Wed Oct 21 2026 Devrim Gunduz <devrim@gunduz.org> - 8.0.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-qhull, so that the GIS stack does not need the EPEL qhull
  packages on RHEL 10 (RHEL 8 and 9 ship it in CRB / PowerTools). Based on
  the Fedora spec file. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422
