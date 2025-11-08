%global _vpath_builddir .
%global pgroutingmajorversion 4.0
%global sname	pgrouting

Summary:	Routing functionality for PostGIS
Name:		%{sname}_%{pgmajorversion}
Version:	%{pgroutingmajorversion}.0
Release:	1PGDG%{dist}
License:	GPLv2+
Source0:	https://github.com/pgRouting/%{sname}/archive/v%{version}.tar.gz
URL:		https://pgrouting.org/
BuildRequires:	cmake >= 3.12 boost-devel >= 1.56
BuildRequires:	gcc-c++ gmp-devel perl-version
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion} postgis

%description
pgRouting extends the PostGIS / PostgreSQL geospatial database to
provide geospatial routing functionality.

Advantages of the database routing approach are:

- Data and attributes can be modified by many clients, like QGIS and
uDig through JDBC, ODBC, or directly using Pl/pgSQL. The clients can
either be PCs or mobile devices)
- Data changes can be reflected instantaneously through the routing
engine. There is no need for precalculation.
- The “cost” parameter can be dynamically calculated through SQL and its
value can come from multiple fields or tables.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__install} -d build
pushd build
%if 0%{?suse_version} >= 1500
cmake .. \
%else
%cmake3 .. \
%endif
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DPOSTGRESQL_BIN=%{pginstdir}/bin \
	-DCMAKE_BUILD_TYPE=Release \
	-DBUILD_HTML=OFF -DBUILD_DOXY=OFF \
	-DLIB_SUFFIX=64

popd

%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} build

%install
%{__rm} -rf %{buildroot}
pushd build
%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} install \
	DESTDIR=%{buildroot}
popd

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%license LICENSE
%doc README.md BOOST_LICENSE_1_0.txt
%attr(755,root,root) %{pginstdir}/lib/libpgrouting-%{pgroutingmajorversion}.so
%{pginstdir}/share/extension/%{sname}*

%changelog
* Sat Nov 8 2025 Devrim Gündüz <devrim@gunduz.org> - 4.0.0-1PGDG
- Update to 4.0.0 per changes described at:
  https://github.com/pgRouting/pgrouting/releases/tag/v4.0.0

* Mon May 5 2025 Devrim Gündüz <devrim@gunduz.org> - 3.8.0-1PGDG
- Update to 3.8.0 per changes described at:
  https://github.com/pgRouting/pgrouting/releases/tag/v3.8.0

* Tue Feb 25 2025 Devrim Gündüz <devrim@gunduz.org> - 3.7.3-2PGDG
- Add missing BR

* Tue Feb 11 2025 Devrim Gündüz <devrim@gunduz.org> - 3.7.3-1PGDG
- Update to 3.7.3 per changes described at:
  https://github.com/pgRouting/pgrouting/releases/tag/v3.7.3

* Mon Jan 20 2025 Devrim Gündüz <devrim@gunduz.org> - 3.7.2-1PGDG
- Update to 3.7.2 per changes described at:
  https://github.com/pgRouting/pgrouting/releases/tag/v3.7.2

* Tue Dec 24 2024 Devrim Gündüz <devrim@gunduz.org> - 3.7.1-1PGDG
- Update to 3.7.1 per changes described at:
  https://github.com/pgRouting/pgrouting/releases/tag/v3.7.1

* Fri Nov 15 2024 Devrim Gündüz <devrim@gunduz.org> - 3.7.0-1PGDG
- Update to 3.7.0 per changes described at:
  https://github.com/pgRouting/pgrouting/releases/tag/v3.7.0

* Sat Oct 19 2024 Devrim Gündüz <devrim@gunduz.org> - 3.6.3-1PGDG
- Update to 3.6.3 per changes described at:
  https://github.com/pgRouting/pgrouting/releases/tag/v3.6.3

* Mon Sep 23 2024 Devrim Gündüz <devrim@gunduz.org> - 3.6.2-2PGDG
- Fix bogus changelog date

* Tue Apr 9 2024 Devrim Gündüz <devrim@gunduz.org> - 3.6.2-1PGDG
- Update to 3.6.2

* Mon Dec 18 2023 Devrim Gündüz <devrim@gunduz.org> - 3.6.1-1PGDG
- Update to 3.6.1

* Fri Nov 24 2023 Devrim Gündüz <devrim@gunduz.org> - 3.6.0-1PGDG
- pgRouting 3.6.0
