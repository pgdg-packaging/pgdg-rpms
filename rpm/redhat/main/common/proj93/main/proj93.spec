%global	_vpath_builddir .
%global sname proj

%pgdg_set_gis_variables

Name:		%{sname}93
Version:	9.3.1
Release:	3PGDG%{?dist}
Epoch:		0
Summary:	Cartographic projection software (PROJ)

License:	MIT
URL:		https://proj.org
Source0:	http://download.osgeo.org/%{sname}/%{sname}-%{version}.tar.gz
Source2:	%{name}-pgdg-libs.conf

BuildRequires:	sqlite-devel >= 3.7 gcc-c++ libcurl-devel cmake
BuildRequires:	libtiff-devel pgdg-srpm-macros >= 1.0.29

%if 0%{?suse_version} >= 1315
# Unfortunately SLES 15 ships the libraries with -devel subpackage:
Requires:	sqlite3-devel >= 3.7
%else
# All other sane distributions have a separate -libs subpackage:
Requires:	sqlite-libs >= 3.7
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
LDFLAGS="-Wl,-rpath,%{proj93instdir}/lib64 ${LDFLAGS}" ; export LDFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{proj93instdir}/lib64" ; export SHLIB_LINK

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
cmake ..\
%endif
%else
cmake .. \
%endif
	-DCMAKE_INSTALL_PREFIX:PATH=%{proj93instdir} \
	-DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
	-DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}"

%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags}
popd

%install
pushd build
%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} install/fast \
	DESTDIR=%{buildroot}
popd

%{__install} -d %{buildroot}%{proj93instdir}/share/%{sname}
%{__install} -d %{buildroot}%{proj93instdir}/share/doc/
%{__install} -p -m 0644 NEWS AUTHORS COPYING README ChangeLog %{buildroot}%{proj93instdir}/share/doc/

# Install linker config file:
%{__mkdir} -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%{__install} %{SOURCE2} %{buildroot}%{_sysconfdir}/ld.so.conf.d/

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc %{proj93instdir}/share/doc/*
%{proj93instdir}/bin/*
%{proj93instdir}/share/man/man1/*.1
%{proj93instdir}/share/proj/*
%{proj93instdir}/lib64/libproj.so.25*
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%files devel
%defattr(-,root,root,-)
%{proj93instdir}/share/man/man1/*.1
%{proj93instdir}/include/*.h
%{proj93instdir}/include/proj/*
%{proj93instdir}/lib64/*.so
%attr(0755,root,root) %{proj93instdir}/lib64/pkgconfig/%{sname}.pc
%{proj93instdir}/lib64/cmake/%{sname}/*cmake
%{proj93instdir}/lib64/cmake/%{sname}4/*cmake

%changelog
* Sat Sep 12 2026 Devrim Gunduz <devrim@gunduz.org> - 0:9.3.1-3PGDG
- Fix build against CMake 4 on Fedora/RHEL/AL2023 (cmake3 no longer
  exists as a package; use cmake instead)

* Thu Feb 15 2024 Devrim Gündüz <devrim@gunduz.org> - 0:9.3.1-2PGDG
- Fix SLES 15 builds.

* Mon Jan 15 2024 Devrim Gündüz <devrim@gunduz.org> - 0:9.3.1-1PGDG
- Update to 9.3.1

* Sun Sep 17 2023 Devrim Gündüz <devrim@gunduz.org> - 0:9.3.0-1PGDG
- Initial 9.3 packaging for PostgreSQL RPM Repository.
