%global		sname geos
%global		_geosversion	39
%global		geosinstdir /usr/%{sname}%{_geosversion}

%global		_geoslibdir lib64

Name:		%{sname}%{_geosversion}
Version:	3.9.6
Release:	1PGDG%{?dist}
Summary:	GEOS is a C++ port of the Java Topology Suite

License:	LGPLv2
URL:		http://trac.osgeo.org/geos/
Source0:	http://download.osgeo.org/%{sname}/%{sname}-%{version}.tar.bz2
Patch0:		%{name}-gcc43.patch

BuildRequires:	doxygen libtool
BuildRequires:	gcc-c++ pgdg-srpm-macros
Obsoletes:	geos36 <= 3.6.4 geos37 <= 3.7.3
Provides:	geos36 <= 3.6.4 geos37 <= 3.7.3
Provides:	geos%{_geosversion}-python >= %{version}

%description
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology
Suite (JTS). As such, it aims to contain the complete functionality of
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial
predicate functions and spatial operators, as well as specific JTS topology
functions such as IsValid()

%package devel
Summary:	Development files for GEOS
Requires:	%{name} = %{version}-%{release}
Obsoletes:	geos36 <= 3.6.4 geos37 <= 3.7.3
Provides:	geos36 <= 3.6.4 geos37 <= 3.7.3

%description devel
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology
Suite (JTS). As such, it aims to contain the complete functionality of
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial
predicate functions and spatial operators, as well as specific JTS topology
functions such as IsValid()

This package contains the development files to build applications that
use GEOS

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p0

%build

# disable internal libtool to avoid hardcoded r-path
%if 0%{?rhel} && 0%{?rhel} >= 7
for makefile in $(find . -type f -name 'Makefile.in'); do
sed -i 's|@LIBTOOL@|%{_bindir}/libtool|g' $makefile
done
%endif

./configure --prefix=%{geosinstdir} --libdir=/usr/geos%{_geosversion}/%{_geoslibdir} --disable-static --disable-dependency-tracking --disable-python

%{__make} %{?_smp_mflags}

# Make doxygen documentation files
cd doc
%{__make} doxygen-html

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install

# Create linker config file:
%{__mkdir} -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
echo "%{geosinstdir}/%{_geoslibdir}/" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%check
%{__make} DESTDIR=%{buildroot} check

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README.md
%{geosinstdir}/%{_geoslibdir}/libgeos-%{version}.so
%{geosinstdir}/%{_geoslibdir}/libgeos.so
%{geosinstdir}/%{_geoslibdir}/libgeos_c.so*
%if 0%{?rhel} && 0%{?rhel} >= 7
%exclude %{geosinstdir}/%{_geoslibdir}/*.a
%endif
%exclude %{geosinstdir}/%{_geoslibdir}/*.la
%config(noreplace) %attr (644,root,root) %{_sysconfdir}/ld.so.conf.d/%{name}-pgdg-libs.conf

%files devel
%defattr(-,root,root,-)
%doc doc/doxygen_docs
%{geosinstdir}/bin/geos-config
%{geosinstdir}/include/*
%{geosinstdir}/%{_geoslibdir}/pkgconfig/%{sname}.pc

%changelog
* Mon Aug 31 2026 Devrim Gündüz <devrim@gunduz.org> - 3.9.6-1PGDG
- Update to 3.9.6 per changes described at:
  https://github.com/libgeos/geos/releases/tag/3.9.6

* Fri Nov 17 2023 Devrim Gündüz <devrim@gunduz.org> - 3.9.5-1PGDG
- Update to 3.9.5
- Add PGDG branding

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 3.9.2-2.1
- Modernise %patch usage, which has been deprecated in Fedora 38

* Tue Dec 6 2022 Devrim Gündüz <devrim@gunduz.org> - 3.9.2-2
- Remove Advance Toolchain support from RHEL 7 - ppc64le.

* Tue Nov 2 2021 Devrim Gündüz <devrim@gunduz.org> - 3.9.2-1
- Update to 3.9.2

* Thu Mar 11 2021 Devrim Gündüz <devrim@gunduz.org> - 3.9.1-1
- 3.9.1

* Tue Dec 15 2020 Devrim Gündüz <devrim@gunduz.org> - 3.9.0-1
- 3.9.0

* Wed Dec 9 2020 Devrim Gündüz <devrim@gunduz.org> - 3.9.0beta2
- Update to beta2

* Sun Nov 29 2020 Devrim Gündüz <devrim@gunduz.org> - 3.9.0beta1
- Initial packaging of 3.9.X for PostgreSQL RPM Repository,
