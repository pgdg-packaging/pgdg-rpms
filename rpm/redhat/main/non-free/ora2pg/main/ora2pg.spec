%global _libdir /usr/lib64

Summary:	Oracle, MySQL and SQL Server to PostgreSQL database schema converter
Name:		ora2pg
Version:	25.0
Release:	2PGDG%{?dist}
License:	GPLv3
URL:		http://ora2pg.darold.net/
Source0:	https://github.com/darold/%{name}/archive/v%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	perl
Requires:	perl(DBD::Oracle) perl-DBD-Pg
Requires:	perl-DBD-MySQL perl(DBI) perl(String::Random) perl(IO::Compress::Base)

%description
This package contains a Perl module and a companion scripts to convert an Oracle, MySQL
and SQL Server databases schema to PostgreSQL and to migrate the data from these databases
to a PostgreSQL database.

%prep
%setup -q

%build
# Make Perl and Ora2Pg distrib files
%{__perl} Makefile.PL \
    INSTALLDIRS=vendor \
    QUIET=1 \
    CONFDIR=%{_sysconfdir} \
    DOCDIR=%{_docdir}/%{name}-%{version} \
    DESTDIR=%{buildroot}
%{__make}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
# SLES suggest these macros to be used:
# https://en.opensuse.org/openSUSE:Packaging_Perl
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1500
 %perl_process_packlist
 %perl_gen_filelist
%endif
%endif

# Remove unpackaged files.
%{__rm} -f `find %{buildroot}/%{_libdir}/perl*/ -name .packlist -type f`
%{__rm} -f `find %{buildroot}/%{_libdir}/perl*/ -name perllocal.pod -type f`

%files
%defattr(-, root, root, 0755)
%attr(0755,root,root) %{_bindir}/%{name}
%attr(0755,root,root) %{_bindir}/%{name}_scanner
%attr(0644,root,root) %{_mandir}/man3/%{name}.3.gz
%config(noreplace) %{_sysconfdir}/%{name}.conf.dist
%{perl_vendorlib}/Ora2Pg/MSSQL.pm
%{perl_vendorlib}/Ora2Pg/MySQL.pm
%{perl_vendorlib}/Ora2Pg/Oracle.pm
%{perl_vendorlib}/Ora2Pg/PLSQL.pm
%{perl_vendorlib}/Ora2Pg/GEOM.pm
%{perl_vendorlib}/Ora2Pg.pm
%{_docdir}/%{name}-%{version}/*

%changelog
* Sun Sep 28 2025 Devrim Gündüz <devrim@gunduz.org> 25.0-2PGDG
- Rebuild

* Sun Apr 20 2025 Devrim Gündüz <devrim@gunduz.org> 25.0-1PGDG
- Update to 25.0 per changes described at:
  https://github.com/darold/ora2pg/releases/tag/v25.0

* Fri Mar 29 2024 Devrim Gündüz <devrim@gunduz.org> 24.3-1PGDG
- Update to 24.3 per changes described at:
  https://github.com/darold/ora2pg/releases/tag/v24.3

* Tue Mar 12 2024 Devrim Gündüz <devrim@gunduz.org> 24.2-1PGDG
- Update to 24.2

* Tue Sep 12 2023 Devrim Gündüz <devrim@gunduz.org> 24.1-1PGDG
- Update to 24.1

* Thu Jul 6 2023 Devrim Gündüz <devrim@gunduz.org> 24.0-1PGDG
- Update to 24.0
- Add PGDG branding

* Mon Oct 10 2022 Devrim Gündüz <devrim@gunduz.org> 23.2-1
- Update to 23.2

* Tue Feb 15 2022 Devrim Gündüz <devrim@gunduz.org> 23.1-1
- Update to 23.1

* Tue Nov 16 2021 Devrim Gündüz <devrim@gunduz.org> 23.0-1
- Update to 23.0

* Tue Sep 7 2021 Devrim Gündüz <devrim@gunduz.org> 22.1-2
- Add perl-DBD-Pg dependency

* Fri Jul 2 2021 Devrim Gündüz <devrim@gunduz.org> 22.1-1
- Update to 22.1

* Fri Apr 2 2021 Devrim Gündüz <devrim@gunduz.org> 21.1-1
- Update to 21.1

* Tue Oct 13 2020 Devrim Gündüz <devrim@gunduz.org> 21.0-1
- Update to 21.0

* Sat Jan 26 2019 Devrim Gündüz <devrim@gunduz.org> 20.0-1
- Update to 20.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 19.1-1.1
- Rebuild against PostgreSQL 11.0

* Mon Oct 1 2018 Devrim Gündüz <devrim@gunduz.org> 19.1-1
- Update to 19.1

* Tue Aug 21 2018 Devrim Gündüz <devrim@gunduz.org> 19.0-1
- Update to 19.0

* Sun Sep 3 2017 Devrim Gündüz <devrim@gunduz.org> 18.2-1
- Update to 18.2

* Fri Feb 24 2017 Devrim Gündüz <devrim@gunduz.org> 18.1-1
- Update to 18.1

* Tue Jan 31 2017 Devrim Gündüz <devrim@gunduz.org> 18.0-1
- Update to 18.0

* Mon Nov 21 2016 Devrim Gündüz <devrim@gunduz.org> 17.6-1
- Update to 17.6

* Fri Oct 21 2016 Devrim Gündüz <devrim@gunduz.org> 17.5-1
- Update to 17.5

* Mon Apr 18 2016 Devrim Gündüz <devrim@gunduz.org> 17.3-1
- Update to 17.3

* Fri Mar 25 2016 Devrim Gündüz <devrim@gunduz.org> 17.2-1
- Update to 17.2

* Wed Mar 9 2016 Devrim Gündüz <devrim@gunduz.org> 17.1-1
- Update to 17.1

* Thu Jan 21 2016 Devrim Gündüz <devrim@gunduz.org> 16.2-1
- Update to 16.2

* Wed Dec 30 2015 Devrim Gündüz <devrim@gunduz.org> 16.1-1
- Update to 16.1

* Fri Feb 6 2015 Devrim Gündüz <devrim@gunduz.org> 15.1-1
- Update to 15.1, per changes described at:
  http://www.postgresql.org/message-id/54D49C0B.2000006@dalibo.com

* Wed Oct 23 2013 Devrim Gündüz <devrim@gunduz.org> 12.0-1
- Update to 12.0, per changes described at:
  http://www.postgresql.org/message-id/52664854.30200@dalibo.com

* Thu Sep 12 2013 Devrim Gündüz <devrim@gunduz.org> 11.4-1
- Update to 11.4

* Thu Sep 13 2012 Devrim Gündüz <devrim@gunduz.org> 9.2-1
- Update to 9.2
- Update URL, License, Group tags
- Fix spec per rpmlint warnings
- Apply some changes from upstream spec

* Fri Mar 20 2009 Devrim Gündüz <devrim@gunduz.org> 5.0-1
- Initial release, based on Peter's spec file.
