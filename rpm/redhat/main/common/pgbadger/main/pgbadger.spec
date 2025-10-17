Summary:	A fast PostgreSQL log analyzer
Name:		pgbadger
Version:	13.1
Release:	2PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/darold/%{name}
Source0:	https://github.com/darold/%{name}/archive/v%{version}.tar.gz
# Should be removed in next release.
# Needed for perl 5.42:
Patch0:		%{name}-13.1-precedence.patch
BuildArch:	noarch
BuildRequires:	perl make
Requires:	perl-Text-CSV_XS perl

%description
pgBadger is a PostgreSQL log analyzer build for speed with fully
detailed reports from your PostgreSQL log file. It's a single and small
Perl script that aims to replace and outperform the old php script
pgFouine.

pgBadger is written in pure Perl language. It uses a javascript library
to draw graphs so that you don't need additional Perl modules or any
other package to install. Furthermore, this library gives us more
features such as zooming.

pgBadger is able to autodetect your log file format (syslog, stderr or
csvlog). It is designed to parse huge log files as well as gzip
compressed file.

%prep
%setup -q
%patch -P0 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} pure_install PERL_INSTALL_ROOT=%{buildroot}
# Remove .packlist file (per rpmlint)
%{__rm} -f %{buildroot}/%perl_vendorarch/auto/pgBadger/.packlist

%files
%doc README
%license LICENSE
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/%{name}.1p.gz

%changelog
* Fri Oct 17 2025 - Devrim Gündüz <devrim@gunduz.org> 13.1-2PGDG
- Add a patch from upstream to fix Perl 5.42 builds

* Tue Mar 18 2025 - Devrim Gündüz <devrim@gunduz.org> 13.1-1PGDG
- Update to 13.1, per changes described at:
  https://github.com/darold/pgbadger/releases/tag/v13.1

* Mon Dec 9 2024 - Devrim Gündüz <devrim@gunduz.org> 13.0-1PGDG
- Update to 13.0, per changes described at:
  https://github.com/darold/pgbadger/releases/tag/v13.0

* Mon Dec 25 2023 - Devrim Gündüz <devrim@gunduz.org> 12.4-1PGDG
- Update to 12.4, per changes described at:
  https://github.com/darold/pgbadger/releases/tag/v12.4

* Mon Dec 4 2023 - Devrim Gündüz <devrim@gunduz.org> 12.3-1PGDG
- Update to 12.3, per changes described at:
  https://github.com/darold/pgbadger/releases/tag/v12.3

* Mon Aug 21 2023 - Devrim Gündüz <devrim@gunduz.org> 12.2-1PGDG
- Update to 12.2, per changes described at:
  https://github.com/darold/pgbadger/releases/tag/v12.2
- Add PGDG branding
- Remove RHEL 6 bits

* Tue Mar 21 2023 - Devrim Gündüz <devrim@gunduz.org> 12.1-1
- Update to 12.1, per changes described at:
  https://github.com/darold/pgbadger/releases/tag/v12.1

* Wed Sep 14 2022 - Devrim Gündüz <devrim@gunduz.org> 12.0-1
- Update to 11.8, per changes described at:
  https://github.com/darold/pgbadger/releases/tag/v12.0

* Wed Apr 13 2022 - Devrim Gündüz <devrim@gunduz.org> 11.8-1
- Update to 11.8, per changes described at:
  https://github.com/darold/pgbadger/releases/tag/v11.8

* Mon Jan 24 2022 - Devrim Gündüz <devrim@gunduz.org> 11.7-1
- Update to 11.7, per changes described at:
  https://github.com/darold/pgbadger/releases/tag/v11.7

* Mon Sep 6 2021 - Devrim Gündüz <devrim@gunduz.org> 11.6-1
- Update to 11.6, per changes described at:
  https://github.com/darold/pgbadger/releases/tag/v11.6

* Thu Feb 18 2021 - Devrim Gündüz <devrim@gunduz.org> 11.5-1
- Update to 11.5

* Tue Nov 24 2020 - Devrim Gündüz <devrim@gunduz.org> 11.4-1
- Update to 11.4

* Tue Jul 28 2020 - Devrim Gündüz <devrim@gunduz.org> 11.3-1
- Update to 11.3

* Tue Mar 17 2020 - Devrim Gündüz <devrim@gunduz.org> 11.2-1
- Update to 11.2

* Thu Oct 3 2019 - Devrim Gündüz <devrim@gunduz.org> 11.1-1
- Update to 11.1

* Tue Jun 25 2019 - Devrim Gündüz <devrim@gunduz.org> 11.0-1
- Update to 11.0

* Sun Apr 14 2019 - Devrim Gündüz <devrim@gunduz.org> 10.3-1
- Update to 10.3

* Wed Jan 2 2019 - Devrim Gündüz <devrim@gunduz.org> 10.2-1
- Update to 10.2

* Wed Oct 17 2018 Devrim Gündüz <devrim@gunduz.org> - 10.1-2
- Add perl-Text-CSV_XS dependency, which is needed while parsing
  csv logs.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 10.1-1.1
- Rebuild against PostgreSQL 11.0

* Thu Sep 20 2018 - Devrim Gündüz <devrim@gunduz.org> 10.1
- Update to 10.1

* Sun Sep 9 2018 - Devrim Gündüz <devrim@gunduz.org> 10.0
- Update to 10.0

* Fri Aug 31 2018 - John K. Harvey <john.harvey@crunchydata.com> 9.2-2
- Modified github source location as it has moved.

* Mon Nov 13 2017 - Devrim Gündüz <devrim@gunduz.org> 9.2-1
- Update to 9.2

* Tue Jan 24 2017 - Devrim Gündüz <devrim@gunduz.org> 9.1-1
- Update to 9.1

* Wed Sep 7 2016 - Devrim Gündüz <devrim@gunduz.org> 9.0-1
- Update to 9.0

* Sat Aug 27 2016 - Devrim Gündüz <devrim@gunduz.org> 8.3-1
- Update to 8.3

* Sat Aug 13 2016 - Devrim Gündüz <devrim@gunduz.org> 8.2-1
- Update to 8.2

* Thu Apr 28 2016 - Devrim Gündüz <devrim@gunduz.org> 8.1-1
- Update to 8.1

* Mon Feb 22 2016 - Devrim Gündüz <devrim@gunduz.org> 8.0-1
- Update to 8.0

* Wed Jan 20 2016 - Devrim Gündüz <devrim@gunduz.org> 7.3-1
- Update to 7.3

* Wed Jan 6 2016 - Devrim Gündüz <devrim@gunduz.org> 7.2-1
- Update to 7.2
- Update license
- Use new %%license macro

* Mon Jul 13 2015 - Devrim Gündüz <devrim@gunduz.org> 7.1-1
- Update to 7.1, per changes described at:
  http://www.postgresql.org/message-id/55A0EB5C.1040900@dalibo.com
- Update download URL.

* Tue May 12 2015 - Devrim Gündüz <devrim@gunduz.org> 7.0-1
- Update to 7.0
- Minor spec file cosmetic and rpmlint updates.
- Spec file cleanups for RHEL 7 and Fedora 20+.

* Wed Apr 15 2015 - Devrim Gündüz <devrim@gunduz.org> 6.4-1
- Update to 6.4

* Mon Apr 6 2015 - Devrim Gündüz <devrim@gunduz.org> 6.3-1
- Update to 6.3
- Fix various rpmlint warnings.

* Thu Oct 16 2014 - Devrim Gündüz <devrim@gunduz.org> 6.2-1
- Update to 6.2

* Thu Oct 9 2014 - Devrim Gündüz <devrim@gunduz.org> 6.1-1
- Update to 6.1

* Wed Aug 27 2014 - Devrim Gündüz <devrim@gunduz.org> 6.0-1
- Update to 6.0

* Tue May 6 2014 - Devrim Gündüz <devrim@gunduz.org> 5.1-1
- Update to 5.1

* Thu Feb 13 2014 - Devrim Gündüz <devrim@gunduz.org> 5.0-1
- Update to 5.0, per changes described at
  http://www.postgresql.org/message-id/2c9e60c9f80fe68276178abe45311d09@dalibo.com

* Fri Nov 08 2013 - Jeff Frost <jeff@pgexperts.com> 4.1-1
- Update to 4.1

* Thu Oct 31 2013 - Jeff Frost <jeff@pgexperts.com> 4.0-1
- Update to 4.0

* Mon Sep 23 2013 - Devrim Gündüz <devrim@gunduz.org> 3.6-1
- Update to 3.6

* Mon Sep 16 2013 - Devrim Gündüz <devrim@gunduz.org> 3.5-1
- Update to 3.5

* Thu Jun 20 2013 - Devrim Gündüz <devrim@gunduz.org> 3.4-1
- Update to 3.4

* Thu Apr 11 2013 - Devrim Gündüz <devrim@gunduz.org> 3.2-1
- Update to 3.2

* Tue Feb 26 2013 - Devrim Gündüz <devrim@gunduz.org> 3.1-1
- Update to 3.1

* Mon Jan 21 2013 - Devrim Gündüz <devrim@gunduz.org> 2.3-1
- Update to 2.3
- Update download URL.

* Wed Nov 14 2012 - Devrim Gündüz <devrim@gunduz.org> 2.2-1
- Update to 2.2

* Thu Nov 1 2012 - Devrim Gündüz <devrim@gunduz.org> 2.1-1
- Update to 2.1

* Wed Sep 26 2012 - Devrim Gündüz <devrim@gunduz.org> 2.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
