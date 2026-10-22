%global		sname gpsbabel
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		gpsbabelinstdir %{pgdg_gpsbabelinstdir}

%global		__requires_exclude ^libshp\\.so

%if 0%{?rhel} == 8
%undefine __cmake_in_source_build
%endif

Name:		pgdg-%{sname}
# GPSBabel 1.10 needs Qt 6, which RHEL 8 and 9 do not ship. 1.9 is the last
# release that builds with Qt 5:
%if 0%{?rhel} && 0%{?rhel} <= 9
Version:	1.9.0
%else
Version:	1.10.0
%endif
Release:	1PGDG%{?dist}
Summary:	A tool to convert between various formats used by GPS devices
License:	GPL-2.0-or-later
URL:		https://www.gpsbabel.org
Source0:	https://github.com/GPSBabel/%{sname}/archive/%{sname}_%(echo %{version} | tr . _).tar.gz#/%{sname}-%{version}.tar.gz

BuildRequires:	pgdg-srpm-macros >= 2.1.0
BuildRequires:	cmake gcc-c++
%if 0%{?suse_version} >= 1500
BuildRequires:	cmake-full
%else
BuildRequires:	cmake-rpm-macros
%endif
BuildRequires:	libusb1-devel zlib-devel
BuildRequires:	pgdg-shapelib-devel
Requires:	pgdg-shapelib%{?_isa}
%if 0%{?rhel} && 0%{?rhel} <= 9
BuildRequires:	qt5-qtbase-devel
%else
BuildRequires:	qt6-qtbase-devel qt6-qt5compat-devel
%endif
Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

%description
Converts GPS waypoint, route, and track data from one format type
to another.

This package installs the GPSBabel command line tool (no GUI) under
%{gpsbabelinstdir}, for the packages in the PostgreSQL RPM repository,
and links it to %{_bindir}/%{sname} with alternatives.

%prep
%setup -q -n %{sname}-%{sname}_%(echo %{version} | tr . _)
# Only the command line tool is packaged:
sed -i '/^add_subdirectory(gui)$/d' CMakeLists.txt

%build
export PKG_CONFIG_PATH=%{pgdg_shapelibinstdir}/lib64/pkgconfig
%cmake \
	-DCMAKE_INSTALL_RPATH:PATH=%{pgdg_shapelibinstdir}/lib64 \
	-DCMAKE_BUILD_RPATH:PATH=%{pgdg_shapelibinstdir}/lib64 \
	-DGPSBABEL_WITH_LIBUSB=pkgconfig \
	-DGPSBABEL_WITH_ZLIB=pkgconfig \
	-DGPSBABEL_WITH_SHAPELIB=pkgconfig \
	-DGPSBABEL_MAPPREVIEW:BOOL=OFF
%cmake_build --target gpsbabel

%install
%{__install} -d -m 0755 %{buildroot}%{gpsbabelinstdir}/bin
%{__install} -p -m 0755 %{__cmake_builddir}/gpsbabel %{buildroot}%{gpsbabelinstdir}/bin/

%post
%{_sbindir}/update-alternatives --install %{_bindir}/%{sname} pgdg-%{sname} %{gpsbabelinstdir}/bin/%{sname} 100

%postun
if [ "$1" -eq 0 ]; then
	%{_sbindir}/update-alternatives --remove pgdg-%{sname} %{gpsbabelinstdir}/bin/%{sname}
fi

%files
%doc README* AUTHORS
%license COPYING
%dir %{gpsbabelinstdir}
%dir %{gpsbabelinstdir}/bin
%{gpsbabelinstdir}/bin/%{sname}

%changelog
* Wed Oct 21 2026 Devrim Gunduz <devrim@gunduz.org> - 1.10.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-gpsbabel, so that GDAL does not need the EPEL gpsbabel package
  on RHEL. Only the command line tool is built. 1.9.0 on RHEL 8 and 9, as
  GPSBabel 1.10 needs Qt 6. Built against our pgdg-shapelib package. Based
  on the Fedora spec file. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422
