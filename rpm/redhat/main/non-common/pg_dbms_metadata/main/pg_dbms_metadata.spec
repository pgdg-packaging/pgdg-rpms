%global sname	pg_dbms_metadata

Summary:	PostgreSQL extension to extract DDL of database objects in a way compatible to Oracle DBMS_METADATA package.
Name:		%{sname}_%{pgmajorversion}
Version:	1.0.0
Release:	2PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/hexacluster/%{sname}/
Source0:	https://github.com/hexacluster/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

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

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Tue Feb 25 2025 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-2PGDG
- Add missing BRs and dependency

* Thu Jan 11 2024 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1PGDG
- Initial RPM packaging for the PostgreSQL RPM Repository:
  https://github.com/HexaCluster/pg_dbms_metadata/releases/tag/v1.0.0
