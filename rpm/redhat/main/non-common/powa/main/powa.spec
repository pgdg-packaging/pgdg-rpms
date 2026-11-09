%global sname powa

Summary:	PostgreSQL Workload Analyzer Meta Package
Name:		%{sname}_%{pgmajorversion}
Version:	5.1.0
Release:	2PGDG%{?dist}
License:	PostgreSQL
URL:		https://powa.readthedocs.io/
Requires:	postgresql%{pgmajorversion}-contrib
Requires:	powa-archivist_%{pgmajorversion} pg_qualstats_%{pgmajorversion}
Requires:	pg_stat_kcache_%{pgmajorversion} hypopg_%{pgmajorversion}

%description
PoWA is PostgreSQL Workload Analyzer that gathers performance stats and
provides real-time charts and graphs to help monitor and tune your
PostgreSQL servers. It is similar to Oracle AWR or SQL Server MDW.

This is the meta package.

%prep

%build

%install

%files

%changelog
* Mon Nov 9 2026 Devrim Gündüz <devrim@gunduz.org> - 5.1.0-2PGDG
- Rebuild against latest PostgreSQL minor releases

* Mon Nov 24 2025 Devrim Gunduz <devrim@gunduz.org> - 5.1.0-1PGDG
- Update to 5.1.0

* Wed Dec 11 2024 Devrim Gunduz <devrim@gunduz.org> - 5.0.1-1PGDG
- Update to 5.0.1

* Tue Nov 28 2023 Devrim Gunduz <devrim@gunduz.org> - 4.2.2-1PGDG
- Update to 4.2.2

* Mon Oct 30 2023 Devrim Gunduz <devrim@gunduz.org> - 4.2.1-1PGDG
- Update to 4.2.1

* Thu Sep 21 2023 Devrim Gunduz <devrim@gunduz.org> - 4.2.0-1PGDG
- Initial RPM packaging for PostgreSQL RPM Repository
