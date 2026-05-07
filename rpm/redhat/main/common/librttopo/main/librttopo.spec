%pgdg_set_gis_variables

# Override GeOS version:
%global geosfullversion %geos314fullversion
%global geosmajorversion %geos314majorversion
%global geosinstdir %geos314instdir

Name:		librttopo
Version:	1.1.0
Release:	43PGDG%{?dist}
Summary:	Create and manage SQL/MM topologies
License:	GPLv2+
URL:		https://git.osgeo.org/gitea/rttopo/%{name}
Source0:	https://git.osgeo.org/gitea/rttopo/%{name}/archive/%{name}-%{version}.tar.gz

BuildRequires:	autoconf automake gcc libtool make
BuildRequires:	pgdg-srpm-macros >= 1.0.24
BuildRequires:	geos%{geosmajorversion}-devel >= %{geosfullversion}

%description
The RT Topology Library exposes an API to create and manage standard
(ISO 13249 aka SQL/MM) topologies using user-provided data stores.

%package	devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1 -n %{name}

%build
CFLAGS="$CFLAGS -I%{geosinstdir}/include -g -fPIE"; export CFLAGS
autoreconf -ifv
export PATH=%{geosinstdir}/bin:$PATH
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{geosinstdir}/lib64" ; export SHLIB_LINK
%configure --disable-static
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%files
%license COPYING
%doc CREDITS NEWS.md README.md TODO
%{_libdir}/%{name}.so.*
%{_libdir}/%{name}.so

%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}_geom.h
%{_libdir}/pkgconfig/rttopo.pc

%changelog
* Thu May 7 2026 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-43PGDG
- Rebuild against GeOS 3.14

* Tue Dec 17 2024 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-42PGDG
- Beat EPEL package per report from Sagar Yedida.

* Sun Sep 22 2024 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-4PGDG
- Rebuild against GeOS 3.13

* Thu Jan 18 2024 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-3PGDG
- Rebuild against GeOS 3.12.x
- Add PGDG branding

* Wed Jul 13 2022 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-2
- Build with GeOS 3.11.x

* Mon Feb 15 2021 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1
- Initial packaging for PostgreSQL RPM repository to satisfy
  libspatialite50 packaging, per Fedora spec file written by
  Sandro Mani (ours is a bit different then that spec file).
