%global _vpath_builddir .
%global sname	h3

Summary:	A Hexagonal Hierarchical Geospatial Indexing System
Name:		%{sname}
Version:	4.5.0
Release:	2PGDG%{dist}
License:	Apache
Source0:	https://github.com/uber/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/uber/%{sname}
BuildRequires:	gcc cmake libtool

%description
H3 is a geospatial indexing system using a hexagonal grid that can be
(approximately) subdivided into finer and finer hexagonal grids,
combining the benefits of a hexagonal grid with S2's hierarchical
subdivisions.

Documentation is available at https://h3geo.org

%package devel
Summary:	H3 development header files
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for h3.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__install} -d build
pushd build
%if 0%{?suse_version} >= 1315
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_BUILD_TYPE=Release \
	-DBUILD_SHARED_LIBS:BOOL=ON -DENABLE_LINTING=OFF ..
%else
%cmake -DCMAKE_BUILD_TYPE=Release -DENABLE_LINTING=OFF ..
%endif
%cmake_build
popd


%install
%{__rm} -rf %{buildroot}
pushd build
%cmake_install
popd
%{__mv} %{buildroot}/%{_includedir}/h3/h3api.h %{buildroot}/%{_includedir}/
%{__cp} src/h3lib/include/linkedGeo.h %{buildroot}/%{_includedir}/
%{__cp} src/h3lib/include/latLng.h %{buildroot}/%{_includedir}/
%{__cp} src/h3lib/include/bbox.h %{buildroot}/%{_includedir}/

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%license LICENSE
%doc README.md
%{_bindir}/cellToBoundary
%{_bindir}/cellToBoundaryHier
%{_bindir}/cellToLatLng
%{_bindir}/cellToLatLngHier
%{_bindir}/cellToLocalIj
%{_bindir}/gridDisk
%{_bindir}/gridDiskUnsafe
%{_bindir}/%{sname}
%{_bindir}/h3ToComponents
%{_bindir}/h3ToHier
%{_bindir}/latLngToCell
%{_bindir}/localIjToCell
%{_libdir}/libh3.so*

%files devel
%{_includedir}/bbox.h
%{_includedir}/h3api.h
%{_includedir}/latLng.h
%{_includedir}/linkedGeo.h
%{_libdir}/cmake/%{sname}/*.cmake
%{_libdir}/pkgconfig/%{sname}.pc

%changelog
* Sun Jun 7 2026 Devrim Gündüz <devrim@gunduz.org> - 4.5.0-2PGDG
- Add a few more header files to support h3-pg 4.5.0

* Sat May 23 2026 Devrim Gündüz <devrim@gunduz.org> - 4.5.0-1PGDG
- Update to 4.5.0 per changes described at:
  https://github.com/uber/h3/releases/tag/v4.5.0

* Thu Mar 19 2026 Devrim Gündüz <devrim@gunduz.org> - 4.4.1-2PGDG
- Fix builds with CMake 4. This also removed %%cmake3 macro which
  was a RHEL 7-era one.
- Disable linting (at least for now, which fails to run on Fedora 44).

* Thu Nov 13 2025 Devrim Gündüz <devrim@gunduz.org> - 4.4.1-1PGDG
- Update to 4.4.1 per changes described at:
  https://github.com/uber/h3/releases/tag/v4.4.1

* Fri Nov 7 2025 Devrim Gündüz <devrim@gunduz.org> - 4.4.0-1PGDG
- Update to 4.4.0 per changes described at:
  https://github.com/uber/h3/releases/tag/v4.4.0

* Wed Jun 18 2025 Devrim Gündüz <devrim@gunduz.org> - 4.3.0-1PGDG
- Update to 4.3.0 per changes described at:
  https://github.com/uber/h3/releases/tag/v4.3.0

* Wed Mar 12 2025 Devrim Gündüz <devrim@gunduz.org> - 4.2.1-1PGDG
- Update to 4.2.1 per changes described at:
  https://github.com/uber/h3/releases/tag/v4.2.1

* Tue Feb 11 2025 Devrim Gündüz <devrim@gunduz.org> - 4.2.0-3PGDG
- Revert the changes in 4.2.0-2 as new h3-pg does not need them.

* Wed Feb 5 2025 Devrim Gündüz <devrim@gunduz.org> - 4.2.0-2PGDG
- Install more header files along with -devel subpackage to build
  h3-pg
- Fix permissions of the binary files

* Fri Dec 6 2024 Devrim Gündüz <devrim@gunduz.org> - 4.2.0-1PGDG
- Update to 4.2.0 per changes described at:
  https://github.com/uber/h3/releases/tag/v4.2.0

* Sun Feb 18 2024 Devrim Gündüz <devrim@gunduz.org> - 4.1.0-2PGDG
- Fix SLES-15 builds

* Sat Nov 4 2023 Devrim Gündüz <devrim@gunduz.org> - 4.1.0-1PGDG
- Initial packaging of H3 to support h3-pg extension.
