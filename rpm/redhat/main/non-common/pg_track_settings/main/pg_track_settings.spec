%global sname pg_track_settings

Summary:	PostgreSQL extension to keep track of settings modification
Name:		%{sname}_%{pgmajorversion}
Version:	2.1.2
Release:	3PGDG%{?dist}
License:	BSD
Source0:	https://github.com/rjuju/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/rjuju/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

BuildArch:	noarch

%description
pg_track_settings is a small extension that helps you keep track of
postgresql settings configuration.

It provides a function (pg_track_settings_snapshot()), that must be
called regularly. At each call, it will store the settings that have
been changed since last call. It will also track the postgresql
start time if it's different from the last one.

This extension tracks both overall settings (the pg_settings view)
and overloaded settings (the pg_db_role_setting table).

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

#Avoid conflict with some other README file:
%{__mv} %{buildroot}%{pginstdir}/doc/extension/README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Fri Jan 17 2025 Devrim Gündüz <devrim@gunduz.org> - 2.1.2-3PGDG
- Mark package as noarch.

* Mon Aug 21 2023 Devrim Gündüz <devrim@gunduz.org> - 2.1.2-2PGDG
- Remove RHEL 6 bits
- Fix rpmlint warnings
- Add PGDG branding

* Tue May 16 2023 Devrim Gündüz <devrim@gunduz.org> - 2.1.2-1
- Update to 4.1.2

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Fri Sep 23 2022 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-1
- Update to 2.1.0

* Sat Jun 5 2021 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-3
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Tue Oct 6 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-1
- Update to 2.0.1

* Thu Sep 24 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-2
- Switch to pgdg-srpm-macros

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-1.1
- Rebuild for PostgreSQL 12

* Fri Sep 6 2019 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-1
- Update to 2.0.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0.1-1.1
- Rebuild against PostgreSQL 11.0

* Sun Jul 15 2018 - Devrim Gündüz <devrim@gunduz.org> 1.0.1-1
- Update to 1.0.1

* Mon Jan 4 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-2
- Update for 9.5 doc layout.

* Thu Jul 23 2015 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
