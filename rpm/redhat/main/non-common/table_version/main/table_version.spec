%global sname table_version

Summary:	PostgreSQL table versioning extension
Name:		%{sname}_%{pgmajorversion}
Version:	1.11.1
Release:	2PGDG%{?dist}
License:	BSD
Source0:	https://github.com/linz/postgresql-tableversion/archive/%{version}.tar.gz
URL:		https://github.com/linz/postgresql-tableversion/
BuildRequires:	postgresql%{pgmajorversion}-devel jq
Requires:	postgresql%{pgmajorversion}-server
BuildArch:	noarch

%description
PostgreSQL table versioning extension, recording row modifications and its
history. The extension provides APIs for accessing snapshots of a table at
certain revisions and the difference generated between any two given revisions.
The extension uses a PL/PgSQL trigger based system to record and provide
access to the row revisions

%prep
%setup -q -n postgresql-tableversion-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install
# Install table_version_loader under PostgreSQL directory
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__install} -d %{buildroot}%{pginstdir}/bin
%{__mv} %{buildroot}/usr/local/bin/table_version-loader %{buildroot}/%{pginstdir}/bin/
%{__mv} %{buildroot}/usr/local/share/table_version/table_version-%{version}.sql.tpl %{buildroot}%{pginstdir}/share/extension/

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/*%{sname}.md
%license LICENSE
%attr (755, root, root) %{pginstdir}/bin/table_version-loader
%{pginstdir}/share/extension/table_version*.sql*
%{pginstdir}/share/extension/table_version.control

%changelog
* Wed Jan 29 2025 Devrim Gündüz <devrim@gunduz.org> - 1.11.1-2PGDG
- Mark shell script executable.
- Remove redundant BR

* Sat Nov 9 2024 Devrim Gündüz <devrim@gunduz.org> - 1.11.1-1PGDG
- Update to 1.11.1

* Mon Feb 26 2024 Devrim Gündüz <devrim@gunduz.org> - 1.10.3-4PGDG
- Mark package as noarch and enable -debug* subpackages.

* Wed Sep 13 2023 Devrim Gündüz <devrim@gunduz.org> - 1.10.3-3PGDG
- Add PGDG branding
- Cleanup rpmlint warning

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.10.3-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu Sep 29 2022 Devrim Gündüz <devrim@gunduz.org> - 1.10.3-1
- Update to 1.10.3

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> - 1.9.0-1
- Update to 1.9.0
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.8.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Wed Aug 12 2020 Devrim Gündüz <devrim@gunduz.org> - 1.8.0-1
- Update to 1.8.0

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 1.7.1-1.1
- Rebuild for PostgreSQL 12

* Tue Aug 6 2019 Devrim Gündüz <devrim@gunduz.org> - 1.7.1-1
- Update to 1.7.1

* Fri Feb 8 2019 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-1
- Update to 1.6.0

* Fri Oct 19 2018 Devrim Gündüz <devrim@gunduz.org> - 1.5.0-1
- Update to 1.5.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.4.3-1.1
- Rebuild against PostgreSQL 11.0

* Thu Aug 23 2018 - Devrim Gündüz <devrim@gunduz.org> 1.4.3-1
- Update to 1.4.3

* Mon Apr 9 2018 - Devrim Gündüz <devrim@gunduz.org> 1.4.2-1
- Update to 1.4.2

* Thu Feb 22 2018 - Devrim Gündüz <devrim@gunduz.org> 1.4.1-1
- Update to 1.4.1

* Sat Oct 14 2017 - Devrim Gündüz <devrim@gunduz.org> 1.3.1-1
- Update to 1.3.1

* Wed Sep 13 2017 - Devrim Gündüz <devrim@gunduz.org> 1.3.0-1
- Update to 1.3.0

* Thu May 25 2017 - Devrim Gündüz <devrim@gunduz.org> 1.1.1-1
- Update to 1.1.1

* Sun Mar 20 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.1-1
- Initial packaging for PostgreSQL RPM Repository
