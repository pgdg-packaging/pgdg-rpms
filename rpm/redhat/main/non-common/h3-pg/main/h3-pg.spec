%global _vpath_builddir .
%global sname	h3-pg

Summary:	Uber's H3 Hexagonal Hierarchical Geospatial Indexing System in PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	4.2.0
Release:	1PGDG%{dist}
License:	Apache
URL:		https://github.com/zachasme/%{sname}
Source0:	https://github.com/zachasme/%{sname}/archive/refs/tags/v%{version}.tar.gz
Patch0:		%{sname}-useosh3.patch
BuildRequires:	cmake >= 3.20 h3-devel
BuildRequires:	postgresql%{pgmajorversion}-devel

Requires:	postgresql%{pgmajorversion} h3

%description
This library provides PostgreSQL bindings for the H3 Core Library.

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p0

%build
%{__install} -d build
pushd build
# h3-pg cannot find the header file on Fedora, so export CFLAGS:
%if 0%{?fedora}
CFLAGS="$CFLAGS -I%{_includedir}/h3"; export CFLAGS
%endif
%if 0%{?suse_version} >= 1315
cmake -DCMAKE_BUILD_TYPE=Release .. \
%else
%cmake3 .. -DCMAKE_BUILD_TYPE=Release .. \
%endif
	-DPostgreSQL_CONFIG=%{pginstdir}/bin/pg_config
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
%doc README.md
%{pginstdir}/lib/h3.so
%{pginstdir}/lib/h3_postgis.so
%{pginstdir}/share/extension/h3*.sql
%{pginstdir}/share/extension/h3.control
%{pginstdir}/share/extension/h3_postgis.control

%changelog
* Mon Jan 20 2025 Devrim Gündüz <devrim@gunduz.org> - 4.2.0-1PGDG
- Update to 4.2.0 per changes described at:
  https://github.com/zachasme/h3-pg/releases/tag/v4.2.0

* Wed Nov 6 2024 Devrim Gündüz <devrim@gunduz.org> - 4.1.4-1PGDG
- Update to 4.1.4 per changes described at:
  https://github.com/zachasme/h3-pg/releases/tag/v4.1.4

* Thu Sep 19 2024 Devrim Gündüz <devrim@gunduz.org> - 4.1.3-3PGDG
- Fix builds on Fedora

* Thu May 23 2024 Devrim Gündüz <devrim@gunduz.org> - 4.1.3-2PGDG
- Fix changelog date.

* Sun Nov 5 2023 Devrim Gündüz <devrim@gunduz.org> - 4.1.3-1PGDG
- Initial packaging of h3-pg.
