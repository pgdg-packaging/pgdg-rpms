%global sname pgfaceting

Name:		%{sname}_%{pgmajorversion}
Version:	0.2.0
Release:	1PGDG%{?dist}
Summary:	Faceted query acceleration for PostgreSQL using roaring bitmaps
License:	BSD
URL:		https://github.com/cybertec-postgresql/%{sname}
Source0:	https://github.com/cybertec-postgresql/%{sname}/archive/refs/tags/v%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion} pg_roaringbitmap_%{pgmajorversion}

%description
PostgreSQL extension to quickly calculate facet counts using inverted indexes
built with roaring bitmaps. Requires pg_roaringbitmap to be installed.
Faceting means counting number occurrences of each value in a result set for a,
set of attributes. Typical example of faceting is a web shop where you can see
how many items are remaining after filtering your search by red, green or blue,
and how many when filtering by size small, medium or large.

%prep
%setup -q -n %{sname}-%{version}

%build
echo no build stage needed

%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p %{buildroot}%{pginstdir}/share/extension
%{__install} *.control %{buildroot}%{pginstdir}/share/extension/
%{__install} sql/* %{buildroot}%{pginstdir}/share/extension/

%files
%defattr(644,root,root,755)
%doc README.md
%license LICENSE
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Mon Apr 14 2025 Devrim Gündüz <devrim@gunduz.org> 0.2.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository
