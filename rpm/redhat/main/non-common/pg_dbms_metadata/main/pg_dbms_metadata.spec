%global sname	pg_dbms_metadata

%{!?runselftest:%global runselftest 0}

Summary:	PostgreSQL extension to extract DDL of database objects in a way compatible to Oracle DBMS_METADATA package.
Name:		%{sname}_%{pgmajorversion}
Version:	1.0.0
Release:	4PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/hexacluster/%{sname}/
Source0:	https://github.com/hexacluster/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	make
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
%if %runselftest
BuildRequires:	postgresql%{pgmajorversion}-server pgdg-srpm-macros >= 2.0.0
%endif

BuildArch:	noarch

%description
PostgreSQL extension to extract DDL of database objects in a way
compatible to Oracle DBMS_METADATA package. This extension serves a
dual purpose—not only does it provide compatibility with the Oracle
DBMS_METADATA package, but it also establishes a systematic approach
to programmatically retrieve DDL for objects. You now have the
flexibility to generate DDL for an object either from a plain SQL
query or from PL/pgSQL code. This also enables the extraction of DDL
using any client that can execute plain SQL queries. These features
distinguishes it from standard methods like pg_dump.

%prep
%setup -q -n %{sname}-%{version}

%build

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} INSTALL_PREFIX=%{buildroot} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%check
%if %runselftest
%pgdg_check_installcheck
%endif

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Tue Sep 29 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-4PGDG
- Add %%check, running the regression tests with the %%check helpers
  from pgdg-srpm-macros 2.0.0. It is disabled by default; enable it
  with --define 'runselftest 1'.

* Thu Sep 10 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-3PGDG
- Add missing BR

* Tue Feb 25 2025 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-2PGDG
- Add missing BRs and dependency

* Thu Jan 11 2024 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1PGDG
- Initial RPM packaging for the PostgreSQL RPM Repository:
  https://github.com/HexaCluster/pg_dbms_metadata/releases/tag/v1.0.0
