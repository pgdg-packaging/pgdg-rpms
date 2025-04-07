Summary:	PostgreSQL monitoring script
Name:		check_postgres
Version:	2.26.0
Release:	3PGDG%{?dist}
License:	BSD
Source0:	https://github.com/bucardo/%{name}/archive/%{version}.tar.gz
URL:		https://bucardo.org/wiki/Check_postgres
BuildArch:	noarch
BuildRequires:	perl-ExtUtils-MakeMaker make
BuildRequires:	perl-DBD-Pg >= 2.0 perl-DBI >= 1.51
Requires:	perl-File-Temp perl-Time-HiRes perl-Digest-MD5
%if 0%{?fedora} || 0%{?rhel}
Requires:	perl-Getopt-Long
%endif
%if 0%{?suse_version} >= 1500
Requires:	perl-Getopt-Long-Descriptive
%endif

%description
check_postgres is a script for monitoring various attributes of your
database. It is designed to work with Nagios, MRTG, or in standalone
scripts.

%prep
%setup -q

%build
%{__perl} Makefile.PL NO_PACKLIST=1 INSTALLDIRS=vendor
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} %{?_smp_mflags} pure_install DESTDIR=%{buildroot}

%if 0%{?suse_version} >= 1500
%perl_process_packlist
%perl_gen_filelist
%endif

%files
%defattr(-,root,root,-)
%doc %{name}.pl.html README.md
%{_mandir}/man1/%{name}*
%{_bindir}/%{name}.pl

%changelog
* Mon Apr 7 2025 - Devrim Gündüz <devrim@gunduz.org> 2.26.0-3PGDG
- Add missing BR
- Build with NO_PACKLIST=1
- Spec file cleanup

* Fri Feb 16 2024 - Devrim Gündüz <devrim@gunduz.org> 2.26.0-2PGDG
- Add PGDG branding
- Fix rpmlint warning

* Wed Apr 12 2023 - Devrim Gündüz <devrim@gunduz.org> 2.26.0-1
- Update to 2.26.0

* Mon Nov 1 2021 - Devrim Gündüz <devrim@gunduz.org> 2.25.0-3
- Fix SLES dependencies

* Wed May 13 2020 - Devrim Gündüz <devrim@gunduz.org> 2.25.0-2
- Update BR and remove obsoleted dependency, per Justin Pryzby.

* Wed May 13 2020 - Devrim Gündüz <devrim@gunduz.org> 2.25.0-2
- Update BR and remove obsoleted dependency, per Justin Pryzby.

* Tue Feb 4 2020 - Devrim Gündüz <devrim@gunduz.org> 2.25.0-1
- Update to 2.25.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.24.0-1.1
- Rebuild against PostgreSQL 11.0

* Fri Jul 13 2018 - Devrim Gündüz <devrim@gunduz.org> 2.24.0-1
- Update to 2.24.0

* Thu Mar 29 2018 - Devrim Gündüz <devrim@gunduz.org> 2.23.0-2
- Add some missing Requires to support all commands.

* Thu Nov 9 2017 - Devrim Gündüz <devrim@gunduz.org> 2.23.0-1
- Update to 2.23.0, per changes described at
  https://mail.endcrypt.com/pipermail/check_postgres-announce/2017-November/000036.html

* Sun Jul 5 2015 - Devrim Gündüz <devrim@gunduz.org> 2.22.0-1
- Update to 2.22.0, per changes described at
  https://mail.endcrypt.com/pipermail/check_postgres-announce/2015-July/000035.html
- Update description

* Wed Oct 9 2013 - Devrim Gündüz <devrim@gunduz.org> 2.21.0-1
- Update to 2.21.0
- Simplify spec file.

* Tue Jul 2 2013 - Devrim Gündüz <devrim@gunduz.org> 2.20.1-1
- Update to 2.20.1

* Mon Apr 29 2013 - Devrim Gündüz <devrim@gunduz.org> 2.20.0-1
- Update to 2.20.0

* Sun Feb 26 2012 - Devrim Gündüz <devrim@gunduz.org> 2.19.0-1
- Update to 2.19.0, per changes described at
  https://mail.endcrypt.com/pipermail/check_postgres-announce/2012-January/000028.html

* Sun Oct 2 2011 - Devrim Gündüz <devrim@gunduz.org> 2.18.0-1
- Update to 2.18.0, per changes described at
  https://mail.endcrypt.com/pipermail/check_postgres-announce/2011-October/000027.html

* Fri Jan 28 2011 - Devrim Gündüz <devrim@gunduz.org> 2.16.0-1
- Update to 2.16.0

* Mon Jan 10 2011 - Devrim Gündüz <devrim@gunduz.org> 2.15.4-1
- Update to 2.15.4

* Wed Mar 10 2010 - Devrim Gündüz <devrim@gunduz.org> 2.14.3-1
- Update to 2.14.3

* Sat Feb 27 2010 - Devrim Gündüz <devrim@gunduz.org> 2.14.2-1
- Update to 2.14.2
- Add -p options to install, per bz review #543917, comment #3.
- Remove postgresql-server requirement, since this plugin can be used to
  control remote PostgreSQL servers.

* Mon Feb 1 2010 - Devrim Gündüz <devrim@gunduz.org> 2.13.0-1
- Update to 2.13.0
- Refactor spec file:
  * Use tarball, instead of .pl file directly.
  * Add man page

* Wed Sep 2 2009 - Devrim Gündüz <devrim@gunduz.org> 2.12.0-1
- Update to 2.12.0

* Wed Sep 2 2009 - Devrim Gündüz <devrim@gunduz.org> 2.11.1-1
- Update to 2.11.1

* Tue Aug 4 2009 - Devrim Gündüz <devrim@gunduz.org> 2.9.10-1
- Update to 2.9.10

* Tue Jul 28 2009 - Devrim Gündüz <devrim@gunduz.org> 2.9.2-1
- Update to 2.9.2

* Sat Jul 4 2009 - Devrim Gündüz <devrim@gunduz.org> 2.9.1-1
- Update to 2.9.1

* Mon May 18 2009 - Devrim Gündüz <devrim@gunduz.org> 2.8.1-1
- Update to 2.8.1

* Thu May 7 2009 - Devrim Gündüz <devrim@gunduz.org> 2.8.0-1
- Update to 2.8.0

* Tue Feb 17 2009 - Devrim Gündüz <devrim@gunduz.org> 2.7.3-1
- Update to 2.7.3

* Sun Feb 1 2009 - Devrim Gündüz <devrim@gunduz.org> 2.6.0-1
- Update to 2.6.0

* Fri Dec 19 2008 - Devrim Gündüz <devrim@gunduz.org> 2.5.3-1
- Update to 2.5.3

* Wed Dec 17 2008 - Devrim Gündüz <devrim@gunduz.org> 2.5.2-1
- Update to 2.5.2

* Sun Dec 7 2008 - Devrim Gündüz <devrim@gunduz.org> 2.5.0-1
- Update to 2.5.0

* Tue Dec 2 2008 - Devrim Gündüz <devrim@gunduz.org> 2.4.3-1
- Update to 2.4.3

* Tue Oct 7 2008 - Devrim Gündüz <devrim@gunduz.org> 2.3.0-1
- Update to 2.3.0
- Make package noarch

* Mon Sep 29 2008 - Devrim Gündüz <devrim@gunduz.org> 2.2.1-1
- Update to 2.2.1

* Tue Sep 23 2008 - Devrim Gündüz <devrim@gunduz.org> 2.1.4-1
- Initial RPM packaging for yum.postgresql.org
