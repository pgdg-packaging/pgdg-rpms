%global sname pgreplay
%global vname PGREPLAY_1_5_0

Summary:	PostgreSQL log file re-player
Name:		%{sname}
Version:	1.5.0
Release:	1PGDG%{?dist}
License:	BSD
Source0:	https://github.com/laurenz/%{sname}/archive/%{vname}.tar.gz
URL:		https://github.com/laurenz/%{sname}
Requires:	postgresql-server >= 10.0
BuildRequires:	libpq5-devel

%description
pgreplay reads a PostgreSQL log file (not a WAL file), extracts the SQL
statements and executes them in the same order and relative time against
a PostgreSQL database cluster.

If the execution of statements gets behind schedule, warning messages
are issued that indicate that the server cannot handle the load in a
timely fashion. The idea is to replay a real-world database workload as
exactly as possible.

pgreplay is useful for performance tests, particularly in the following
situations:

* You want to compare the performance of your PostgreSQL application
on different hardware or different operating systems.
* You want to upgrade your database and want to make sure that the new
database version does not suffer from performance regressions that
affect you.

%prep
%setup -q -n %{sname}-%{vname}

%build
%configure --with-postgres=%{pginstdir}/bin
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%defattr(-,root,root,-)
%doc %{sname}.html README.md CHANGELOG
%{_bindir}/%{sname}
%{_mandir}/man1/%{sname}*

%changelog
* Thu Nov 13 2025 - Devrim Gündüz <devrim@gunduz.org> 1.5.0-1PGDG
- Update to 1.5.0

* Tue Feb 20 2024 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-5PGDG
- Add PGDG branding

* Tue Dec 6 2022 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-4
- Remove Advance Toolchain support from RHEL 7 - ppc64le.

* Tue Sep 21 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-3
- Move this package to common repository.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-1.2
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-1.1
- Rebuild against PostgreSQL 11.0

* Thu Jun 1 2017 - Devrim Gündüz <devrim@gunduz.org> 1.3.0-1
- Update to 1.3.0

* Mon Sep 10 2012 - Devrim Gündüz <devrim@gunduz.org> 1.2.0-1
- Initial RPM packaging for Fedora

