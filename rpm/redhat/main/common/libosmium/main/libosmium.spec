%global gdalcpp_version 1.3.0
%global protozero_version 1.6.3

%global testcommit ecfdeb0d5ffcfcb60939651d517d5d7d1bb041a3

%pgdg_set_gis_variables

# Override some variables:
%global geosfullversion %geos313fullversion
%global geosmajorversion %geos313majorversion
%global geosinstdir %geos313instdir
# Use GDAL 3.10 on all of the platforms except RHEL 8:
%if 0%{?rhel} == 8
%global gdalfullversion %gdal38fullversion
%global gdalmajorversion %gdal38majorversion
%global gdalinstdir %gdal38instdir
%else
%global gdalfullversion %gdal310fullversion
%global gdalmajorversion %gdal310majorversion
%global gdalinstdir %gdal310instdir
%endif

Name:		libosmium
Version:	2.22.0
Release:	42PGDG%{?dist}
Summary:	Fast and flexible C++ library for working with OpenStreetMap data

License:	BSL-1.0
URL:		http://osmcode.org/%{name}/
Source0:	https://github.com/osmcode/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:	https://github.com/osmcode/osm-testdata/archive/%{testcommit}/osm-testdata-%{testcommit}.tar.gz

BuildRequires:	cmake make gcc-c++ pgdg-srpm-macros >= 1.0.45
BuildRequires:	doxygen graphviz xmlstarlet
BuildRequires:	ruby rubygems spatialite-tools

BuildRequires:	protozero-devel >= %{protozero_version}
BuildRequires:	gdalcpp-devel >= %{gdalcpp_version}
BuildRequires:	zlib-devel sparsehash-devel
BuildRequires:	gdal%{gdalmajorversion}-devel >= %{gdalfullversion}
BuildRequires:	geos%{geosmajorversion}-devel >= %{geosfullversion}
%if 0%{?suse_version} >= 1500
BuildRequires:	liblz4-devel libbz2-devel Catch2-2-devel libexpat-devel
Requires:	libboost_headers1_66_0-devel libexpat-devel libbz2-devel
%else
BuildRequires:	lz4-devel bzip2-devel catch2-devel expat-devel
BuildRequires:	boost-devel catch2-static
Requires:	boost-devel expat-devel bzip2-devel
%endif

BuildArch:	noarch

%description
A fast and flexible C++ library for working with OpenStreetMap data.

%package	devel
Summary:	Development files for %{name}
Provides:	%{name}-static = %{version}-%{release}

Requires:	protozero-devel >= %{protozero_version}
Requires:	gdalcpp-devel >= %{gdalcpp_version}
Requires:	sparsehash-devel
Requires:	gdal%{gdalmajorversion}-devel >= %{gdalfullversion}
Requires:	geos%{geosmajorversion}-devel >= %{geosfullversion}

%description	devel
This package contains libraries and header files for developing
applications that use %{name}.

%if 0%{?fedora} >= 38 || 0%{?rhel} >= 8
%package	doc
Summary:	Documentation for %{name}
BuildArch:	noarch

%description	doc
This package contains documentation for developing
applications that use %{name}.
%endif

%prep
%setup -q -c -T -a 0 -a 1
%{__mv} %{name}-%{version} %{name}
%{__mv} osm-testdata-%{testcommit} osm-testdata
%{__rm} -rf libosmium/include/gdalcpp.h libosmium/test/catch
%{__ln_s} -f /usr/include/catch2 libosmium/test/catch
sed -i -e 's/-O3 -g//' libosmium/CMakeLists.txt

%build
cd libosmium
%cmake -DBUILD_HEADERS=ON -DBUILD_DATA_TESTS=ON \
	-DGDAL_LIBRARY=%{gdalinstdir}/lib/libgdal.so -DGDAL_INCLUDE_DIR=%{gdalinstdir}/include \
	-DGEOS_LIBRARY=%{geosinstdir}/lib64/libgeos.so -DGEOS_INCLUDE_DIR=%{geosinstdir}/include

%cmake_build
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 8
%cmake_build --target doc
%endif

%install
cd libosmium
%cmake_install
%{__rm} -rf %{buildroot}%{_docdir}

%files devel
%doc %{name}/README.md %{name}/CHANGELOG.md
%license %{name}/LICENSE
%{_includedir}/osmium

%if 0%{?fedora} >= 38 || 0%{?rhel} >= 8
%files doc
%doc libosmium/%{__cmake_builddir}/doc/html/*
%license libosmium/LICENSE
%endif

%changelog
* Tue Mar 18 2025 Devrim Gündüz <devrim@gunduz.org> - 2.20.0-42PGDG
- Update to 2.22.0 per changes described at:
  https://github.com/osmcode/libosmium/releases/tag/v2.22.0

* Mon Dec 30 2024 Devrim Gündüz <devrim@gunduz.org> - 2.20.0-45PGDG
- Rebuild against GDAL 3.10

* Fri Sep 20 2024 Devrim Gündüz <devrim@gunduz.org> - 2.20.0-44PGDG
- Rebuild against GDAL 3.9 and GeOS 3.13

* Sun Feb 18 2024 Devrim Gündüz <devrim@gunduz.org> - 2.20.0-43PGDG
- Rebuild against GDAL 3.8.4

* Mon Dec 4 2023 Devrim Gündüz <devrim@gunduz.org> - 2.20.0-42PGDG
- Initial packaging for the PostgreSQL RPM repository to support osm2pgsql
  package.
