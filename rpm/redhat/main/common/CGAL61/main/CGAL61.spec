%global		 _sourcename CGAL
# CGAL is header-only: there is nothing to put into a debuginfo package.
%global		debug_package %{nil}

Name:		CGAL
Version:	6.1.2
Release:	2PGDG%{?dist}
Summary:	Computational Geometry Algorithms Library
License:	GPL-3.0-or-later AND LGPL-3.0-or-later
URL:		https://www.cgal.org/
Source0:	https://github.com/CGAL/cgal/releases/download/v%{version}/CGAL-%{version}.tar.xz
Source1:	https://github.com/CGAL/cgal/releases/download/v%{version}/CGAL-%{version}-doc_html.tar.xz
BuildRequires:	blas-devel cmake >= 3.14 fdupes gmp-devel
BuildRequires:	lapack-devel mpfr-devel xz zlib-devel
%if 0%{?suse_version}
BuildRequires:	glu-devel libboost_atomic-devel >= 1.74
BuildRequires:	libboost_thread-devel >= 1.74
%endif
%if 0%{?amzn}
BuildRequires:	boost-devel >= 1.74 mesa-libGLU-devel
%endif
Requires:	libcgal-devel = %{version}
%if 0%{?suse_version} >= 150400 && 0%{?suse_version} < 160000 && 0%{?is_opensuse}
BuildRequires:	gcc13-c++
%else
BuildRequires:	gcc-c++
%endif

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
%if 0%{?suse_version}
Requires:	libboost_atomic-devel >= 1.72 libboost_thread-devel >= 1.72
%endif
%if 0%{?amzn}
Requires:	boost-devel >= 1.72
%endif
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
%if 0%{?suse_version} >= 150400 && 0%{?suse_version} < 160000 && 0%{?is_opensuse}
export CXX="g++-13"
%endif

%cmake -DCGAL_INSTALL_LIB_DIR=%{_lib} \
	 -DCGAL_INSTALL_DOC_DIR=%{_docdir}/%{name}-doc

%if 0%{?amzn}
%cmake_build
%else
%make_build
%endif

# Unfortunately take +6600sec locally.
# So we just deliver the source code in cgal package.
# -DWITH_examples=true \
# -DWITH_demos=true \

%install
%cmake_install

%{__install} -d %{buildroot}/%{_datadir}/CGAL/examples
%{__install} -d %{buildroot}/%{_datadir}/CGAL/demo
%{__cp} -a examples/* %{buildroot}/%{_datadir}/CGAL/examples
%{__cp} -a demo/* %{buildroot}/%{_datadir}/CGAL/demo

# installed as docs, but licenses are under %%{_datadir}/licenses/, remove duplicate
%{__rm} %{buildroot}%{_docdir}/%{name}-doc/LICENSE*

%{__cp} -a doc_html %{buildroot}/%{_docdir}/%{name}-doc/
%fdupes %{buildroot}%{_docdir}/%{name}-doc/

%fdupes %{buildroot}/%{_datadir}

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
* Wed Oct 21 2026 Devrim Gündüz <devrim@gunduz.org> - 6.1.2-2PGDG
- Add Amazon Linux 2023 support, to build SFCGAL there.

* Mon Aug 31 2026 Devrim Gündüz <devrim@gunduz.org> - 6.1.2-1PGDG
- Update to 6.1.2 per changes described at:
  https://github.com/CGAL/cgal/releases/tag/v6.1.2

* Fri Nov 7 2025 Devrim Gündüz <devrim@gunduz.org> - 6.1-420001PGDG
- Initial packaging for the PostgreSQL RPM repository to support SFCGAL on SLES 16.
  Took spec file from:
  https://download.opensuse.org/repositories/home:/Simmphonie:/blender/16.0/src/
