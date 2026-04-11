%global	_vpath_builddir .
%global sname proj

%pgdg_set_gis_variables

Name:		%{sname}98
Version:	9.8.1
Release:	1PGDG%{?dist}
Summary:	Cartographic projection software (PROJ)

License:	MIT
URL:		https://proj.org
Source0:	https://download.osgeo.org/%{sname}/%{sname}-%{version}.tar.gz
Source2:	%{name}-pgdg-libs.conf

BuildRequires:	sqlite-devel >= 3.7 libcurl-devel cmake >= 3.16 sqlite
BuildRequires:	libtiff-devel pgdg-srpm-macros >= 1.0.53

# Default GCC version on SLES 15 is not sufficient to build PROJ 9.8,
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
LDFLAGS="-Wl,-rpath,%{proj98instdir}/lib64 ${LDFLAGS}" ; export LDFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{proj98instdir}/lib64" ; export SHLIB_LINK

%if 0%{?suse_version} == 1500
export CXX=/usr/bin/g++-12
%endif

cmake ..\
	-DCMAKE_INSTALL_PREFIX:PATH=%{proj98instdir} \
	-DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
	-DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}"

%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags}
popd

%install
pushd build
%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} install/fast \
	DESTDIR=%{buildroot}
popd

%{__install} -d %{buildroot}%{proj98instdir}/share/%{sname}
%{__install} -d %{buildroot}%{proj98instdir}/share/doc/
%{__install} -p -m 0644 NEWS.md AUTHORS.md COPYING README.md ChangeLog %{buildroot}%{proj98instdir}/share/doc/

# Install linker config file:
%{__mkdir} -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%{__install} %{SOURCE2} %{buildroot}%{_sysconfdir}/ld.so.conf.d/

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc %{proj98instdir}/share/doc/*
%{proj98instdir}/share/bash-completion/completions/projinfo
%{proj98instdir}/bin/*
%{proj98instdir}/share/man/man1/*.1
%{proj98instdir}/share/proj/*
%{proj98instdir}/lib64/libproj.so.25*
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%files devel
%defattr(-,root,root,-)
%{proj98instdir}/share/man/man1/*.1
%{proj98instdir}/include/*.h
%{proj98instdir}/include/proj/*
%{proj98instdir}/lib64/*.so
%attr(0755,root,root) %{proj98instdir}/lib64/pkgconfig/%{sname}.pc
%{proj98instdir}/lib64/cmake/%{sname}/*cmake
%{proj98instdir}/lib64/cmake/%{sname}4/*cmake

%changelog
* Sat Apr 11 2026 Devrim Gündüz <devrim@gunduz.org> - 9.8.1-1PGDG
- Update to 9.8.1 per changes described at:
  https://github.com/OSGeo/PROJ/releases/tag/9.8.1

* Tue Mar 10 2026 Devrim Gündüz <devrim@gunduz.org> - 9.8.0-1PGDG
- Initial 9.8 packaging for the PostgreSQL RPM Repository.
