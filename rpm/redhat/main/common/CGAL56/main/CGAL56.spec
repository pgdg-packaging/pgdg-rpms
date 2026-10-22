%global		 _sourcename CGAL
# CGAL is header-only: there is nothing to put into a debuginfo package.
%global		debug_package %{nil}

%if 0%{?rhel} == 8
%undefine __cmake_in_source_build
%endif

# CGAL 5.6 is the last release series that works with Boost 1.66, which
# RHEL 8 ships (CGAL 6 needs Boost 1.72 or later). SFCGAL 2.x needs CGAL 5.6
# or later.
Name:		CGAL
Version:	5.6.3
Release:	1PGDG%{?dist}
Summary:	Computational Geometry Algorithms Library
License:	GPL-3.0-or-later AND LGPL-3.0-or-later
URL:		https://www.cgal.org/
Source0:	https://github.com/CGAL/cgal/releases/download/v%{version}/CGAL-%{version}.tar.xz
Source1:	https://github.com/CGAL/cgal/releases/download/v%{version}/CGAL-%{version}-doc_html.tar.xz
BuildRequires:	blas-devel cmake >= 3.14 gmp-devel
BuildRequires:	lapack-devel mpfr-devel xz zlib-devel
BuildRequires:	boost-devel >= 1.66 mesa-libGLU-devel
BuildRequires:	gcc-c++
Requires:	libcgal-devel = %{version}

%description
CGAL provides geometric algorithms in a C++ library.

The library offers data structures and algorithms like
triangulations, Voronoi diagrams, Boolean operations on polygons and
polyhedra, point set processing, arrangements of curves, surface and
volume mesh generation, geometry processing, alpha shapes, convex
hull algorithms, shape analysis, AABB and KD trees.

%package devel
Summary:	Development files and tools for CGAL applications
License:	BSL-1.0 AND GPL-3.0-or-later AND LGPL-3.0-or-later
Requires:	blas cmake gmp-devel lapack mpfr-devel zlib-devel
Requires:	boost-devel >= 1.66
#For compatibility with package looking for our old name
Provides:	libcgal-devel = %{version}

%description devel
This package provides the headers files and tools you may need to
develop applications using CGAL.

%package demo-examples-devel
Summary:	Example & demo files for CGAL library usage
License:	BSL-1.0 AND GPL-3.0-or-later AND LGPL-3.0-or-later AND MIT
Requires:	%{name}-devel = %{version}
BuildArch:	noarch

%description demo-examples-devel
This package provides the sources of examples and demos of
CGAL algorithms. You can study them, compile and test CGAL
library.

%package doc
Summary:	Documentation CGAL algorithms
License:	GPL-3.0-or-later AND LGPL-3.0-or-later
Group:		Documentation/HTML
BuildArch:	noarch

%description doc
This package provides the documentation for CGAL algorithms.

%prep
%setup -q -n CGAL-%{version} -a1

%build
%cmake -DCGAL_INSTALL_LIB_DIR=%{_lib} \
	 -DCGAL_INSTALL_DOC_DIR=%{_docdir}/%{name}-doc
%cmake_build

%install
%cmake_install
# Only useful on macOS:
%{__rm} -f %{buildroot}%{_bindir}/cgal_make_macosx_app

%{__install} -d %{buildroot}/%{_datadir}/CGAL/examples
%{__install} -d %{buildroot}/%{_datadir}/CGAL/demo
%{__cp} -a examples/* %{buildroot}/%{_datadir}/CGAL/examples
%{__cp} -a demo/* %{buildroot}/%{_datadir}/CGAL/demo

# installed as docs, but licenses are under %%{_datadir}/licenses/, remove duplicate
%{__rm} %{buildroot}%{_docdir}/%{name}-doc/LICENSE*

%{__cp} -a doc_html %{buildroot}/%{_docdir}/%{name}-doc/

%files devel
%license LICENSE*
%doc AUTHORS CHANGES.md
%{_includedir}/CGAL
%{_libdir}/cmake/CGAL
%{_bindir}/cgal_create_CMakeLists
%{_bindir}/cgal_create_cmake_script
%{_mandir}/man1/cgal_create_cmake_script.1*

%files demo-examples-devel
%license LICENSE*
%{_datadir}/CGAL

%files doc
%license LICENSE*
%doc %dir %{_docdir}/%{name}-doc
%doc %{_docdir}/%{name}-doc/doc_html
%doc %{_docdir}/%{name}-doc/AUTHORS
%doc %{_docdir}/%{name}-doc/CHANGES.md

%changelog
* Thu Oct 22 2026 Devrim Gunduz <devrim@gunduz.org> - 5.6.3-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for RHEL 8, so that
  SFCGAL does not need the EPEL CGAL package there. CGAL 6 needs Boost 1.72
  or later, and RHEL 8 ships Boost 1.66. Based on our CGAL61 spec file. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
