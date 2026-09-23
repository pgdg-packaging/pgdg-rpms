%global	_vpath_builddir .
%global sname proj

%pgdg_set_gis_variables

Name:		%{sname}95
Version:	9.5.1
Release:	2PGDG%{?dist}
Epoch:		0
Summary:	Cartographic projection software (PROJ)

License:	MIT
URL:		https://proj.org
Source0:	https://download.osgeo.org/%{sname}/%{sname}-%{version}.tar.gz
Source2:	%{name}-pgdg-libs.conf

BuildRequires:	sqlite-devel >= 3.7 libcurl-devel cmake
BuildRequires:	libtiff-devel pgdg-srpm-macros >= 1.0.44

# Default GCC version on SLES 15 is not sufficient to build PROJ 9.4,
# so use a newer one:
%if 0%{?suse_version} >= 1315
BuildRequires:	gcc12-c++
%else
# The rest is safe:
BuildRequires:	gcc-c++
%endif

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
LDFLAGS="-Wl,-rpath,%{proj95instdir}/lib64 ${LDFLAGS}" ; export LDFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{proj95instdir}/lib64" ; export SHLIB_LINK

%if 0%{?suse_version} >= 1315
export CXX=/usr/bin/g++-12
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
cmake ..\
%endif
%else
cmake .. \
%endif
	-DCMAKE_INSTALL_PREFIX:PATH=%{proj95instdir} \
	-DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
	-DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}"

%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags}
popd

%install
pushd build
%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} install/fast \
	DESTDIR=%{buildroot}
popd

%{__install} -d %{buildroot}%{proj95instdir}/share/%{sname}
%{__install} -d %{buildroot}%{proj95instdir}/share/doc/
%{__install} -p -m 0644 NEWS.md AUTHORS.md COPYING README.md ChangeLog %{buildroot}%{proj95instdir}/share/doc/

# Install linker config file:
%{__mkdir} -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%{__install} %{SOURCE2} %{buildroot}%{_sysconfdir}/ld.so.conf.d/

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc %{proj95instdir}/share/doc/*
%{proj95instdir}/bin/*
%{proj95instdir}/share/man/man1/*.1
%{proj95instdir}/share/proj/*
%{proj95instdir}/lib64/libproj.so.25*
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%files devel
%defattr(-,root,root,-)
%{proj95instdir}/share/man/man1/*.1
%{proj95instdir}/include/*.h
%{proj95instdir}/include/proj/*
%{proj95instdir}/lib64/*.so
%attr(0755,root,root) %{proj95instdir}/lib64/pkgconfig/%{sname}.pc
%{proj95instdir}/lib64/cmake/%{sname}/*cmake
%{proj95instdir}/lib64/cmake/%{sname}4/*cmake

%changelog
* Sat Sep 12 2026 Devrim Gunduz <devrim@gunduz.org> - 0:9.5.1-2PGDG
- Fix build against CMake 4 on Fedora/RHEL/AL2023 (cmake3 no longer
  exists as a package; use cmake instead)

* Mon Dec 2 2024 Devrim Gündüz <devrim@gunduz.org> - 0:9.5.1-1PGDG
- Update to 9.5.1 per changes described at:
  https://github.com/OSGeo/PROJ/releases/tag/9.5.1

* Mon Sep 16 2024 Devrim Gündüz <devrim@gunduz.org> - 0:9.5.0-1PGDG
- Initial 9.5 packaging for PostgreSQL RPM Repository.
