%global	sname ldap2pg
%global	debug_package %{nil}
%global	_missing_build_ids_terminate_build 0

Summary:	Synchronize Postgres roles and ACLs from any LDAP directory
Name:		%{sname}
Version:	6.4.0
Release:	1PGDG%{?dist}
License:	BSD
Url:		https://github.com/dalibo/%{sname}
Source0:	https://github.com/dalibo/%{sname}/releases/download/v%{version}/%{sname}_%{version}_linux_amd64.tar.gz
Source1:	%{sname}.yml

Requires:	libpq5 >= 10.0

%description
Swiss-army knife to synchronize Postgres roles and privileges from YAML or LDAP.

Features:
* Reads settings from an expressive YAML config file.
* Creates, alters and drops PostgreSQL roles from LDAP searches.
* Creates static roles from YAML to complete LDAP entries.
* Manages role parents (alias groups).
* Grants or revokes privileges statically or from LDAP entries.
* Dry run, check mode.
* Logs LDAP searches as ldapsearch(1) commands.
* Logs every SQL statements.

%prep
%setup -q -c

%build

%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p %{buildroot}/%{_bindir}
%{__mkdir} -p %{buildroot}/%{_sysconfdir}
%{__cp} %{sname} %{buildroot}/%{_bindir}
%{__cp} %{SOURCE1} %{buildroot}/%{_sysconfdir}

%files
%defattr(-,root,root)
%doc CHANGELOG.md README.md
%license LICENSE
%config %{_sysconfdir}/%{sname}.yml
%{_bindir}/%{sname}

%changelog
* Wed Apr 9 2025 Devrim Gündüz <devrim@gunduz.org> - 6.4.0-1PGDG
- Update to 6.4.0

* Sun Feb 9 2025 Devrim Gündüz <devrim@gunduz.org> - 6.3-1PGDG
- Update to 6.3

* Fri Nov 22 2024 Devrim Gündüz <devrim@gunduz.org> - 6.2-1PGDG
* Move package to extras repository as we are now using prebuilt
  files from upstream git repo.
- Update to 6.2

* Sun Feb 18 2024 Devrim Gündüz <devrim@gunduz.org> - 5.9-3PGDG
- Add PGDG branding
- Mark package as noarch.

* Wed Jun 14 2023 Devrim Gündüz <devrim@gunduz.org> - 5.9-2
- Install sample config file
- Simplify install section, no need to use a function as we
  support only one Python version.

* Wed Apr 12 2023 Devrim Gündüz <devrim@gunduz.org> - 5.9-1
- Update to 5.9

* Tue Dec 6 2022 Devrim Gündüz <devrim@gunduz.org> - 5.8-2
- Remove Advance Toolchain support from RHEL 7 - ppc64le.

* Fri Sep 16 2022 Devrim Gündüz <devrim@gunduz.org> - 5.8-1
- Update to 5.8

* Tue Feb 8 2022 Devrim Gündüz <devrim@gunduz.org> - 5.7-1
- Update to 5.7

* Sat Oct 16 2021 Devrim Gündüz <devrim@gunduz.org> - 5.6-1
- Update to 5.6

* Mon Apr 26 2021 Devrim Gündüz <devrim@gunduz.org> - 5.5-1
- Update to 5.5

* Wed Nov 18 2020 Devrim Gündüz <devrim@gunduz.org> - 5.4-2
- Fix RHEL 7 dependency, per report from Magnus.

* Sun Jun 14 2020 Devrim Gündüz <devrim@gunduz.org> - 5.4-1
- Update to 5.4

* Wed May 13 2020 Devrim Gündüz <devrim@gunduz.org> - 5.2-2
- Depend on "libpq5", which is now provided by the latest
  PostgreSQL 10+ minor update set.

* Tue Sep 3 2019 Devrim Gündüz <devrim@gunduz.org> - 5.2-1
- Update to 5.2
- Switch to PY3-only
- Depend on versionless postgresql-libs

* Tue Sep 3 2019 Devrim Gündüz <devrim@gunduz.org> - 5.0-1
- Update to 5.0

* Tue Apr 16 2019 Devrim Gündüz <devrim@gunduz.org> - 4.18-1
- Update to 4.18

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 4.12-1.1
- Rebuild against PostgreSQL 11.0

* Tue Aug 21 2018 Devrim Gündüz <devrim@gunduz.org> 4.12-1
- Update to 4.12

* Sun Jul 1 2018 Devrim Gündüz <devrim@gunduz.org> 4.11-1
- Update to 4.11

* Thu May 24 2018 Devrim Gündüz <devrim@gunduz.org> 4.9-1
- Update to 4.9
- Fix various packaging issues, per Magnus

* Thu Mar 1 2018 Devrim Gündüz <devrim@gunduz.org> 4.6-1
- Update to 4.6

* Fri Sep 15 2017 Devrim Gündüz <devrim@gunduz.org> 3.0-1
- Update to 3.0

* Sat Aug 5 2017 Devrim Gündüz <devrim@gunduz.org> 2.0-1
- Initial packaging for PostgreSQL YUM repository.
