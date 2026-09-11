%global sname pg_fkpart

Summary:	PostgreSQL extension to partition tables following a foreign key
Name:		%{sname}_%{pgmajorversion}
Version:	1.7.0
Release:	7PGDG%{?dist}
License:	GPLv2
Source0:	https://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
URL:		https://github.com/lemoineat/pg_fkpart
BuildRequires:	make
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server
BuildArch:	noarch

Obsoletes:	%{sname}%{pgmajorversion} < 1.7.0-2

%description
pg_fkpart is a PostgreSQL extension to partition tables following a foreign key
of a table.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %make_install install DESTDIR=%{buildroot}
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}*.sql

%changelog
* Thu Sep 10 2026 Devrim Gündüz <devrim@gunduz.org> - 1.7.0-7PGDG
- Add missing BR

* Thu Apr 25 2024  Devrim Gündüz <devrim@gunduz.org> - 1.7.0-6PGDG
- Fix bogus changelog date

* Fri Feb 23 2024  Devrim Gündüz <devrim@gunduz.org> - 1.7.0-5PGDG
- Add PGDG branding

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.7.0-4
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> 1.7.0-3
- Remove pgxs patches, and export PATH instead.
- Remove RHEL 6 stuff.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 1.7.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Fri Jul 24 2020 Devrim Gündüz <devrim@gunduz.org> - 1.7.0-1
- Update to 1.7.0

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-1.2
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-1.1
- Rebuild against PostgreSQL 11.0

* Fri Apr 28 2017 - Devrim Gündüz <devrim@gunduz.org> 1.6.0-1
- Update to 1.6.0

* Sat Aug 13 2016 - Devrim Gündüz <devrim@gunduz.org> 1.5.0-1
- Update to 1.5.0

* Thu Mar 3 2016 - Devrim Gündüz <devrim@gunduz.org> 1.3.0-1
- Update to 1.3.0

* Tue Jan 26 2016 - Devrim Gündüz <devrim@gunduz.org> 1.2.2-1
- Update to 1.2.2
- Move docs to new directory
- Update patch0
- Unified spec file for all platforms.

* Mon May 4 2015 - Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Initial packaging
