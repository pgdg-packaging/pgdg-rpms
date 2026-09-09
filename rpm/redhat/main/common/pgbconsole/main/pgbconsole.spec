%global sname	pgbconsole

Summary:	top-like console for Pgbouncer - PostgreSQL connection pooler
Name:		pgbconsole
Version:	0.1.1
Release:	6PGDG%{?dist}
License:	BSD
Source0:	https://github.com/lesovsky/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/lesovsky/%{sname}
BuildRequires:	postgresql%{pgmajorversion} ncurses-devel
BuildRequires:	libpq5-devel >= 10.0 pgdg-srpm-macros
BuildRequires:	make gcc
Requires:	libpq5 >= 10.0

%description
pgbConsole is the top-like console for Pgbouncer - PostgreSQL connection
pooler. Features:

 * top-like interface
 * show information about client/servers connections, pools/databases
   info and statistics.
 * ability to perform admin commands, such as pause, resume, reload and
   others.
 * ability to show log files or edit configuration in local pgbouncers.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 %{__make} %{?_smp_mflags} CFLAGS="%{optflags} -std=gnu99 -Wall -pedantic"

%install
%{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{_bindir}
USE_PGXS=1 %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
%{__mkdir} -p %{buildroot}%{_mandir}/man1
%{__install} -m 644 doc/*.gz %{buildroot}%{_mandir}/man1

%files
%defattr(-,root,root,-)
%{_mandir}/man1/pgbconsole.1.gz
%doc README.md
%license COPYRIGHT

%{_bindir}/%{sname}

%changelog
* Wed Sep 9 2026 Devrim Gündüz <devrim@gunduz.org> 0.1.1-6PGDG
- Make sure that debug* packages are always produced.

* Mon Feb 19 2024 Devrim Gündüz <devrim@gunduz.org> 0.1.1-5PGDG
- Enable debug package on SLES 15.

* Mon Aug 21 2023 Devrim Gündüz <devrim@gunduz.org> 0.1.1-4PGDG
- Remove RHEL 6 bits
- Add PGDG branding

* Tue Dec 6 2022 Devrim Gündüz <devrim@gunduz.org> - 0.1.1-3
- Remove Advance Toolchain support from RHEL 7 - ppc64le.

* Wed Sep 2 2020 Devrim Gündüz <devrim@gunduz.org> - 0.1.1-2
- Use our own libpq5
- Switch to pgdg-srpm-macros

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.1.1-1.1
- Rebuild against PostgreSQL 11.0

* Sun Nov 6 2016 - Devrim Gündüz <devrim@gunduz.org> 0.1.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
