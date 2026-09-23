%global sname proj

%if 0%{?rhel} == 7 || 0%{?suse_version} >= 1315
%global sqlitepname	sqlite33
%global sqlite33dir	/usr/sqlite330
%else
%global sqlitepname	sqlite
%endif

%pgdg_set_gis_variables

Name:		%{sname}82
Version:	8.2.1
Release:	3%{?dist}
Epoch:		0
Summary:	Cartographic projection software (PROJ)

License:	MIT
URL:		https://proj.org
Source0:	http://download.osgeo.org/%{sname}/%{sname}-%{version}.tar.gz
Source2:	%{name}-pgdg-libs.conf

BuildRequires:	%{sqlitepname}-devel >= 3.7 gcc-c++ libcurl-devel
BuildRequires:	libtiff-devel pgdg-srpm-macros >= 1.0.16

%if 0%{?fedora} > 30 || 0%{?rhel} == 8
Requires:	%{sqlitepname}-libs >= 3.7
%else
Requires:	%{sqlitepname}
%endif

%package devel
Summary:	Development files for PROJ
Requires:	%{name} = %{version}-%{release}

%package static
Summary:	Development files for PROJ
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description
Proj and invproj perform respective forward and inverse transformation of
cartographic data to or from cartesian data with a wide range of selectable
projection functions. Proj docs: http://www.remotesensing.org/dl/new_docs/

%description devel
This package contains libproj and the appropriate header files and man pages.

%description static
This package contains libproj static library.

%prep
%setup -q -n %{sname}-%{version}

%build

LDFLAGS="-Wl,-rpath,%{proj82instdir}/lib64 ${LDFLAGS}" ; export LDFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{proj82instdir}/lib" ; export SHLIB_LINK

%if 0%{?rhel} == 7 || 0%{?suse_version} >= 1315
export SQLITE3_LIBS="-L%{sqlite33dir}/lib -lsqlite3"
export SQLITE3_INCLUDE_DIR='%{sqlite33dir}/include'
export SQLITE3_CFLAGS="-I%{sqlite33dir}/include"
export PATH=%{sqlite33dir}/bin/:$PATH
LDFLAGS="-Wl,-rpath,%{sqlite33dir}/lib ${LDFLAGS}" ; export LDFLAGS
CPPFLAGS="-I%{sqlite33dir}/include/ ${CFLAGS}" ; export CPPFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{sqlite33dir}/lib" ; export SHLIB_LINK
%endif

./configure --prefix=%{proj82instdir} --with-curl

%{__make} %{?_smp_mflags}

%install
%if 0%{?rhel} == 7 || 0%{?suse_version} >= 1315
export SQLITE3_LIBS="-L%{sqlite33dir}/lib -lsqlite3"
export SQLITE3_INCLUDE_DIR='%{sqlite33dir}/include'
export PATH=%{sqlite33dir}/bin/:$PATH
LDFLAGS="-Wl,-rpath,%{sqlite33dir}/lib ${LDFLAGS}" ; export LDFLAGS
CPPFLAGS="-I%{sqlite33dir}/include/ ${CFLAGS}" ; export CPPFLAGS
SHLIB_LINK="$SHLIB_LINK -Wl,-rpath,%{sqlite33dir}/lib" ; export SHLIB_LINK
%endif

%{__rm} -rf %{buildroot}
%make_install
%{__install} -d %{buildroot}%{proj82instdir}/share/%{sname}
%{__install} -d %{buildroot}%{proj82instdir}/share/doc/
%{__install} -p -m 0644 NEWS AUTHORS COPYING README ChangeLog %{buildroot}%{proj82instdir}/share/doc/

# Install linker config file:
%{__mkdir} -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%{__install} %{SOURCE2} %{buildroot}%{_sysconfdir}/ld.so.conf.d/

# Remove .la file
%{__rm} -f %{buildroot}%{proj82instdir}/lib/libproj.la

%clean
%{__rm} -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc %{proj82instdir}/share/doc/*
%{proj82instdir}/bin/*
%{proj82instdir}/share/man/man1/*.1
%{proj82instdir}/share/proj/*
%{proj82instdir}/lib/libproj.so.22*
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%files devel
%defattr(-,root,root,-)
%{proj82instdir}/share/man/man1/*.1
%{proj82instdir}/include/*.h
%{proj82instdir}/include/proj/*
%{proj82instdir}/lib/*.so
%{proj82instdir}/lib/*.a
%attr(0755,root,root) %{proj82instdir}/lib/pkgconfig/%{sname}.pc

%files static
%defattr(-,root,root,-)

%changelog
* Tue Dec 6 2022 Devrim Gündüz <devrim@gunduz.org> - 0:8.2.1-3
- Remove Advance Toolchain support from RHEL 7 - ppc64le.

* Wed Oct 19 2022 Devrim Gündüz <devrim@gunduz.org> - 0:8.2.1-2
- Don't install .la file to fix build error on Fedora 37.

* Fri Jan 7 2022 Devrim Gündüz <devrim@gunduz.org> - 0:8.2.1-1
- Update to 8.2.1

* Thu Dec 16 2021 Devrim Gündüz <devrim@gunduz.org> - 0:8.2.0-1
- Initial 8.2 packaging for PostgreSQL RPM Repository.
