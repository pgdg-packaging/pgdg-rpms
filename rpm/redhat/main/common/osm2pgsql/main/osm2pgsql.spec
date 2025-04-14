%global sname osm2pgsql

%pgdg_set_gis_variables

%global projmajorversion %proj95majorversion
%global projfullversion %proj95fullversion
%global projinstdir %proj95instdir

Summary:	Import map data from OpenStreetMap to a PostgreSQL database
Name:		%{sname}
Version:	2.1.1
Release:	1PGDG%{?dist}
License:	GPLv2
Source0:	https://github.com/%{sname}-dev/%{sname}/archive/refs/tags/%{version}.tar.gz
URL:		https://github.com/%{sname}-dev/%{sname}

BuildRequires:	make gcc-c++ cmake libtool libpq5-devel
BuildRequires:	libxml2-devel proj%{projmajorversion}-devel >= %{projfullversion}
BuildRequires:	python3-psycopg2 python3-devel
BuildRequires:	zlib-devel

# These packages are have been deprecated as of RHEL 8.7,
# so enable these features on Fedora and RHEL 8:
# https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html/8.7_release_notes/deprecated_functionality#deprecated-packages
%if 0%{?fedora} >= 40 || 0%{?rhel} == 8
BuildRequires:	protozero-devel libosmium-devel
%endif

%if 0%{?suse_version} >= 1500
BuildRequires:	libboost_headers1_66_0-devel libbz2-devel
BuildRequires:	Catch2-2-devel clang-tools
BuildRequires:	libexpat-devel nlohmann_json-devel
BuildRequires:	lua54-devel
%else
BuildRequires:	boost-devel bzip2-devel
BuildRequires:	catch2-devel clang-tools-extra
BuildRequires:	expat-devel json-devel
BuildRequires:	lua-devel
%endif

Requires:	libpq5

%description
osm2pgsql is a tool for loading OpenStreetMap data into a PostgreSQL /
PostGIS database suitable for applications like rendering into a map,
geocoding with Nominatim, or general analysis.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__install} -d build
pushd build
%cmake .. \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_BUILD_TYPE=Release \
	-DPROJ_LIBRARY=%{projinstdir}/lib64/libproj.so \
	-DPROJ6_INCLUDE_DIR=%{projinstdir}/include \
	-DEXTERNAL_FMT=OFF \
%if 0%{?fedora} >= 40 || 0%{?rhel} == 8
	-DEXTERNAL_LIBOSMIUM=ON \
	-DEXTERNAL_PROTOZERO=ON \
%else
	-DEXTERNAL_LIBOSMIUM=OFF \
	-DEXTERNAL_PROTOZERO=OFF \
%endif
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64
%endif

popd

%{__make} -C "build/%{_vpath_builddir}" %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} -C "build/%{_vpath_builddir}" %{?_smp_mflags} install \
	DESTDIR=%{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(755,root,root,755)
%{_bindir}/%{sname}
%{_bindir}/%{sname}-replication
%{_mandir}/man1/%{sname}*
%{_datadir}/%{sname}/*.style

%changelog
* Mon Apr 14 2025 Devrim Gündüz <devrim@gunduz.org> - 2.1.1-1PGDG
- Update to 2.1.1 per changes described at:
  https://github.com/osm2pgsql-dev/osm2pgsql/releases/tag/2.1.1
- Disable osmium and generalizations support on RHEL >= 9 because
  of lack of dependent packages.

* Tue Apr 8 2025 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-1PGDG
- Update to 2.1.0 per changes described at:
  https://github.com/osm2pgsql-dev/osm2pgsql/releases/tag/2.1.0
- Remove generalization support (osm2pgsql-gen binary). It is causing
  some dependency problems.

* Mon Dec 2 2024 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-1PGDG
- Update to 2.0.1 per changes described at:
  https://github.com/osm2pgsql-dev/osm2pgsql/releases/tag/2.0.1

* Thu Sep 19 2024 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-1PGDG
- Update to 2.0.0 per changes described at:
  https://github.com/osm2pgsql-dev/osm2pgsql/releases/tag/2.0.0
- Do not use external FMT library, per:
  https://github.com/osm2pgsql-dev/osm2pgsql/issues/2256
- Build and install osm2pgsql-gen binary.

* Sun Feb 18 2024 Devrim Gündüz <devrim@gunduz.org> - 1.11.0-1PGDG
- Update to 1.11.0
- Build against Proj 9.3.1
- Add SLES 15 support

* Mon Dec 4 2023 Devrim Gündüz <devrim@gunduz.org> - 1.10.0-1PGDG
- Update to 1.10.0

* Mon Sep 25 2023 Devrim Gündüz <devrim@gunduz.org> - 1.9.2-1PGDG
- Initial RPM packaging for the PostgreSQL RPM Repository
