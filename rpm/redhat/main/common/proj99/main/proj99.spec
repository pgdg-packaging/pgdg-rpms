%global	_vpath_builddir .
%global sname proj

%global projinstdir /usr/proj99

%pgdg_set_gis_variables

Name:		%{sname}99
Version:	9.9.0
Release:	1PGDG%{?dist}
Summary:	Cartographic projection software (PROJ)

License:	MIT
URL:		https://proj.org
Source0:	https://download.osgeo.org/%{sname}/%{sname}-%{version}.tar.gz
Source2:	%{name}-pgdg-libs.conf

BuildRequires:	sqlite-devel >= 3.7 libcurl-devel cmake >= 3.16 sqlite
BuildRequires:	libtiff-devel pgdg-srpm-macros >= 1.0.53

# Default GCC version on SLES 15 is not sufficient to build PROJ 9.9:
# so use a newer one:
%if 0%{?suse_version} == 1500
BuildRequires:	gcc12-c++
%else
# The rest is safe:
BuildRequires:	gcc-c++
%endif

%if 0%{?suse_version} >= 1500
# SLES ships the libraries with -devel subpackage:
Requires:	sqlite3-devel >= 3.7
%else
# All other sane distributions have a separate -libs subpackage:
Requires:	sqlite-libs >= 3.7
%endif

# Do not provide the sonames of the libraries under /usr/proj99:
# they clash with the libraries of the OS, and dnf would satisfy the
# dependencies of OS packages with ours. Our packages find them through
# rpaths, and require this package by name. Per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global __provides_exclude_from ^%{projinstdir}/
# Nothing provides these sonames now, so do not require them either,
# e.g. from the binaries of this package.
%global __requires_exclude ^lib(geos|geos_c|proj|gdal|geotiff|spatialite)\.so

%package devel
Summary:	Development files for PROJ
Requires:	%{name} = %{version}-%{release}

%description
PROJ is a generic coordinate transformation software that transforms
geospatial coordinates from one coordinate reference system (CRS) to another.
This includes cartographic projections as well as geodetic transformations.

%description devel
This package contains libproj and the appropriate header files and man pages.

%prep
%setup -q -n %{sname}-%{version}

%build

%{__install} -d build
pushd build
LDFLAGS="-Wl,-rpath,%{projinstdir}/lib64 ${LDFLAGS}" ; export LDFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{projinstdir}/lib64" ; export SHLIB_LINK

%if 0%{?suse_version} == 1500
export CXX=/usr/bin/g++-12
%endif

cmake ..\
	-DCMAKE_INSTALL_PREFIX:PATH=%{projinstdir} \
	-DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
	-DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}"

%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags}
popd

%install
pushd build
%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} install/fast \
	DESTDIR=%{buildroot}
popd

%{__install} -d %{buildroot}%{projinstdir}/share/%{sname}
%{__install} -d %{buildroot}%{projinstdir}/share/doc/
%{__install} -p -m 0644 NEWS.md AUTHORS.md COPYING README.md ChangeLog %{buildroot}%{projinstdir}/share/doc/

# Install linker config file:
%{__mkdir} -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%{__install} %{SOURCE2} %{buildroot}%{_sysconfdir}/ld.so.conf.d/

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc %{projinstdir}/share/doc/*
%{projinstdir}/share/bash-completion/completions/projinfo
%{projinstdir}/bin/*
%{projinstdir}/share/man/man1/*.1
%{projinstdir}/share/proj/*
%{projinstdir}/lib64/libproj.so.25*
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%files devel
%defattr(-,root,root,-)
%{projinstdir}/share/man/man1/*.1
%{projinstdir}/include/*.h
%{projinstdir}/include/proj/*
%{projinstdir}/lib64/*.so
%attr(0755,root,root) %{projinstdir}/lib64/pkgconfig/%{sname}.pc
%{projinstdir}/lib64/cmake/%{sname}/*cmake
%{projinstdir}/lib64/cmake/%{sname}4/*cmake

%changelog
* Mon Oct 12 2026 Devrim Gündüz <devrim@gunduz.org> - 9.9.0-1PGDG
- Initial 9.9 packaging for the PostgreSQL RPM Repository.
