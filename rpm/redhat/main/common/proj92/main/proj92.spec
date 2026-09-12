%global	_vpath_builddir .
%global sname proj

%if 0%{?rhel} == 7 || 0%{?suse_version} >= 1315
%global sqlitepname	sqlite33
%global sqlite33dir	/usr/sqlite330
%else
%global sqlitepname	sqlite
%endif

%pgdg_set_gis_variables

Name:		%{sname}92
Version:	9.2.1
Release:	2PGDG%{?dist}
Epoch:		0
Summary:	Cartographic projection software (PROJ)

License:	MIT
URL:		https://proj.org
Source0:	http://download.osgeo.org/%{sname}/%{sname}-%{version}.tar.gz
Source2:	%{name}-pgdg-libs.conf

BuildRequires:	%{sqlitepname}-devel >= 3.7 gcc-c++ libcurl-devel cmake
BuildRequires:	libtiff-devel pgdg-srpm-macros >= 1.0.29

%if 0%{?fedora} > 30 || 0%{?rhel} == 8
Requires:	%{sqlitepname}-libs >= 3.7
%else
Requires:	%{sqlitepname}
%endif

%package devel
Summary:	Development files for PROJ
Requires:	%{name} = %{version}-%{release}

%description
Proj and invproj perform respective forward and inverse transformation of
cartographic data to or from cartesian data with a wide range of selectable
projection functions. Proj docs: http://www.remotesensing.org/dl/new_docs/

%description devel
This package contains libproj and the appropriate header files and man pages.

%prep
%setup -q -n %{sname}-%{version}

%build

%{__install} -d build
pushd build
LDFLAGS="-Wl,-rpath,%{proj92instdir}/lib64 ${LDFLAGS}" ; export LDFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{proj92instdir}/lib64" ; export SHLIB_LINK

%if 0%{?rhel} == 7 || 0%{?suse_version} >= 1315
export SQLITE3_LIBS="-L%{sqlite33dir}/lib -lsqlite3"
export SQLITE3_INCLUDE_DIR='%{sqlite33dir}/include'
export SQLITE3_CFLAGS="-I%{sqlite33dir}/include"
export PATH=%{sqlite33dir}/bin/:$PATH
LDFLAGS="-Wl,-rpath,%{sqlite33dir}/lib ${LDFLAGS}" ; export LDFLAGS
CPPFLAGS="-I%{sqlite33dir}/include/ ${CFLAGS}" ; export CPPFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{sqlite33dir}/lib" ; export SHLIB_LINK
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
cmake ..\
%endif
%else
cmake .. \
%endif
	-DCMAKE_INSTALL_PREFIX:PATH=%{proj92instdir} \
	-DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
	-DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}"

%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags}
popd

%install
pushd build
%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} install/fast \
	DESTDIR=%{buildroot}
popd

%{__install} -d %{buildroot}%{proj92instdir}/share/%{sname}
%{__install} -d %{buildroot}%{proj92instdir}/share/doc/
%{__install} -p -m 0644 NEWS AUTHORS COPYING README ChangeLog %{buildroot}%{proj92instdir}/share/doc/

# Install linker config file:
%{__mkdir} -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%{__install} %{SOURCE2} %{buildroot}%{_sysconfdir}/ld.so.conf.d/

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc %{proj92instdir}/share/doc/*
%{proj92instdir}/bin/*
%{proj92instdir}/share/man/man1/*.1
%{proj92instdir}/share/proj/*
%{proj92instdir}/lib64/libproj.so.25*
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%files devel
%defattr(-,root,root,-)
%{proj92instdir}/share/man/man1/*.1
%{proj92instdir}/include/*.h
%{proj92instdir}/include/proj/*
%{proj92instdir}/lib64/*.so
%attr(0755,root,root) %{proj92instdir}/lib64/pkgconfig/%{sname}.pc
%{proj92instdir}/lib64/cmake/%{sname}/*cmake
%{proj92instdir}/lib64/cmake/%{sname}4/*cmake

%changelog
* Sat Sep 12 2026 Devrim Gunduz <devrim@gunduz.org> - 0:9.2.1-2PGDG
- Fix build against CMake 4 on Fedora/RHEL/AL2023 (cmake3 no longer
  exists as a package; use cmake instead)

* Sun Jun 4 2023 Devrim Gündüz <devrim@gunduz.org> - 0:9.2.1-1PGDG
- Update to 9.2.1
- Add PGDG branding

* Wed Mar 15 2023 Devrim Gündüz <devrim@gunduz.org> - 0:9.2.0-1
- Initial 9.2 packaging for PostgreSQL RPM Repository.
