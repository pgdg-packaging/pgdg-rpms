%global _vpath_builddir .
%global sname	h3

Summary:	A Hexagonal Hierarchical Geospatial Indexing System
Name:		%{sname}
Version:	4.2.1
Release:	1PGDG%{dist}
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
	-DBUILD_SHARED_LIBS:BOOL=ON ..
%else
%cmake3 -DCMAKE_BUILD_TYPE=Release ..
%endif

popd

%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} build

%install
%{__rm} -rf %{buildroot}
pushd build
%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} install \
	DESTDIR=%{buildroot}
popd
%{__mv} %{buildroot}/%{_includedir}/h3/h3api.h %{buildroot}/%{_includedir}/

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
%{_includedir}/h3api.h
%{_libdir}/cmake/%{sname}/*.cmake

%changelog
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
