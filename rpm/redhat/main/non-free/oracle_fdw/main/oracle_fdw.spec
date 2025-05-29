%global sname	oracle_fdw
%global ofdwmajver 2
%global ofdwmidver 8
%global ofdwminver 0

%{!?oi_release:%global oi_release 23.8.0.25.04}

%global		__find_requires %{SOURCE1}

# Disable tests by default.
%{!?runselftest:%global runselftest 0}

Summary:	A PostgreSQL Foreign Data Wrapper for Oracle.
Name:		%{sname}_%{pgmajorversion}
Version:	%{ofdwmajver}.%{ofdwmidver}.%{ofdwminver}
Release:	6PGDG%{?dist}
License:	PostgreSQL
URL:		https://laurenz.github.io/%{sname}
Source0:	https://github.com/laurenz/%{sname}/archive/ORACLE_FDW_%{ofdwmajver}_%{ofdwmidver}_%{ofdwminver}.tar.gz
Source1:	%{sname}-filter-requires-libclntsh.sh
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 2.3.0-2

Requires:	postgresql%{pgmajorversion}-server
# Package builder needs to adjust this as needed.
BuildRequires:	oracle-instantclient-basic >= %{oi_release}
BuildRequires:	oracle-instantclient-devel >= %{oi_release}
Requires:	oracle-instantclient-basic >= %{oi_release}

%description
Provides a Foreign Data Wrapper for easy and efficient read access from
PostgreSQL to Oracle databases, including pushdown of WHERE conditions and
required columns as well as comprehensive EXPLAIN support.

%prep
%setup -q -n %{sname}-ORACLE_FDW_%{ofdwmajver}_%{ofdwmidver}_%{ofdwminver}

%build

PATH=%{pginstdir}/bin:$PATH USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH USE_PGXS=1 %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%check
%if %runselftest
%{__make} installcheck PG_CONFIG=%{pginstdir}/bin/pg_config %{?_smp_mflags} PGUSER=postgres PGPORT=5416
%endif

%files
%defattr(-,root,root,-)
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.sql
%{pginstdir}/share/extension/*.control
%{pginstdir}/doc/extension/README.%{sname}

%changelog
* Wed May 28 2025 Devrim Gündüz <devrim@gunduz.org> 2.8.0-6PGDG
- Update OIC dependency to 23.8.0.25.04

* Mon May 12 2025 Devrim Gündüz <devrim@gunduz.org> 2.8.0-5PGDG
- Update to 2.8.0 per changes described at:
  https://github.com/laurenz/oracle_fdw/releases/tag/ORACLE_FDW_2_8_0

* Mon Feb 10 2025 Devrim Gündüz <devrim@gunduz.org> 2.7.0-5PGDG
- Update OIC dependency to 23.7.0.25.01

* Thu Dec 19 2024 Devrim Gündüz <devrim@gunduz.org> 2.7.0-4PGDG
- Update OIC dependency to 23.6.0.24.10

* Fri Aug 2 2024 Devrim Gündüz <devrim@gunduz.org> 2.7.0-1PGDG
- Update to 2.7.0 per changes described at:
  https://github.com/laurenz/oracle_fdw/releases/tag/ORACLE_FDW_2_7_0
- Update OIC dependency to 23.5.0.24.07

* Sat Mar 16 2024 Devrim Gündüz <devrim@gunduz.org> 2.6.0-3PGDG
- Rebuild against OIC 21.13.0.0.0

* Mon Sep 11 2023 Devrim Gündüz <devrim@gunduz.org> 2.6.0-1PGDG
- Update to 2.6.0
- Add PGDG branding
- Build against OIC 21.11.0.0.0

* Mon Apr 24 2023 Devrim Gündüz <devrim@gunduz.org> 2.5.0-3
- Rebuild against OIC 21.10

* Fri Feb 3 2023 Devrim Gündüz <devrim@gunduz.org> 2.5.0-2
- Rebuild against OIC 21.9

* Fri Oct 28 2022 Devrim Gündüz <devrim@gunduz.org> 2.5.0-1
- Update to 2.5.0
- Rebuild against OIC 21.8

* Sat Sep 10 2022 Devrim Gündüz <devrim@gunduz.org> 2.4.0-3
- Rebuild against OIC 21.7
- Remove pgxs patches, and export PATH instead.

* Fri Sep 24 2021 Devrim Gündüz <devrim@gunduz.org> 2.4.0-1
- Update to 2.4.0

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 2.3.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 24 2020 Devrim Gündüz <devrim@gunduz.org> 2.3.0-1
- Update to 2.3.0

* Wed Sep 2 2020 Devrim Gündüz <devrim@gunduz.org> 2.2.0-2
- Update LLVM dependencies
- Switch to pgdg-srpm-macros

* Fri Oct 11 2019 Devrim Gündüz <devrim@gunduz.org> 2.2.0-1
- Update to 2.2.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-1.1
- Rebuild against PostgreSQL 11.0

* Fri Oct 5 2018 Devrim Gündüz <devrim@gunduz.org> 2.1.0-1
- Update to 2.1.0

* Tue Sep 19 2017 Devrim Gündüz <devrim@gunduz.org> 2.0.0-1
- Update to 2.0.0

* Wed Sep 28 2016 Devrim Gündüz <devrim@gunduz.org> 1.5.0-1
- Update to 1.5.0

* Thu Jul 7 2016 Devrim Gündüz <devrim@gunduz.org> 1.4.0-1
- Update to 1.4.0

* Thu Jan 21 2016 Devrim Gündüz <devrim@gunduz.org> 1.3.0-1
- Update to 1.3.0
- Put check into conditional, and disable it by default.
- Update for new doc layout.

* Tue Feb 3 2015 Devrim Gündüz <devrim@gunduz.org> 1.2.0-1
- Update to 1.2.0
- Add a patch for PGXS compilation.
- Ran dos2unix against the spec file, to fix build issues.

* Thu Dec 26 2013 Devrim Gündüz <devrim@gunduz.org> 0.9.10-1
- Update to 0.9.10-1

* Mon Oct 8 2012 David E. Wheeler <david.wheeler@iovation.com> 0.9.7-1
- Initial RPM
 
