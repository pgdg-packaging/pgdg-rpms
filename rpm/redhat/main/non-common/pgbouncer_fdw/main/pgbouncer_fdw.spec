%global debug_package %{nil}
%global sname pgbouncer_fdw

Summary:	pgbouncer Foreign Data Wrapper
Name:		%{sname}_%{pgmajorversion}
Version:	1.2.0
Release:	2PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/CrunchyData/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/CrunchyData/%{sname}

BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-contrib
Requires:	pgbouncer >= 1.17

%description
pgbouncer_fdw provides a direct SQL interface to the pgbouncer SHOW commands.
It takes advantage of the dblink_fdw feature to provide a more typical,
table-like interface to the current status of your pgbouncer server(s).
This makes it easier to set up monitoring or other services that require
direct access to pgbouncer statistics.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%defattr(644,root,root,755)
%license LICENSE.txt
%doc %{pginstdir}/doc/extension/*%{sname}.md
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}*.control

%changelog
* Thu Jan 9 2025 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-2PGDG
- Remove obsoleted BR

* Wed Oct 2 2024 Devrim Gündüz <devrim@gunduz.org> 1.2.0-1PGDG
- Update to 1.2.0 per changes described at:
  https://github.com/CrunchyData/pgbouncer_fdw/releases/tag/v1.2.0

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Tue Oct 31 2023 Devrim Gündüz <devrim@gunduz.org> 1.1.0-1PGDG
- Update to 1.1.0

* Thu Sep 14 2023 Devrim Gündüz <devrim@gunduz.org> 1.0.1-1PGDG
- Update to 1.0.1
- Add PGDG branding

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 0.4-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon Mar 7 2022 Devrim Gündüz <devrim@gunduz.org> 0.4-2
- 0.4 requires pgbouncer 1.16.0+

* Sat Oct 16 2021 Devrim Gündüz <devrim@gunduz.org> 0.4-1
- Update to 0.4

* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> 0.3-2
- Remove pgxs patches, and export PATH instead.

* Tue Nov 17 2020 Devrim Gündüz <devrim@gunduz.org> 0.3-1
- Update to 0.3

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 0.2-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Mon Sep 28 2020 Devrim Gündüz <devrim@gunduz.org> - 0.2-1
- Initial packaging for PostgreSQL RPM Repository
