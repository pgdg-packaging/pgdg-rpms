Summary:	A PostgreSQL SQL syntax beautifier
Name:		pgFormatter
Version:	5.6
Release:	1PGDG%{?dist}
License:	BSD
Source0:	https://github.com/darold/%{name}/archive/v%{version}.tar.gz
URL:		https://github.com/darold/%{name}/
BuildRequires:	perl(ExtUtils::MakeMaker) make perl-macros
BuildArch:	noarch

%description
A PostgreSQL SQL syntax beautifier that can work as a console program
or as a CGI. Download from https://sourceforge.net/p/pgformatter/ and
demo site at http://sqlformat.darold.net/

%prep
%setup -q
%{__perl} Makefile.PL

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} +
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%files
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/pg_format
%{_mandir}/man1/pg_format.1.gz
%{_mandir}/man3/pgFormatter*.gz
%{perl_vendorlib}/%{name}/*.pm

%changelog
* Tue Mar 18 2025 - Devrim Gündüz <devrim@gunduz.org> 5.6-1PGDG
- Update to 5.6 per changes described at:
  https://github.com/darold/pgFormatter/releases/tag/v5.6

* Thu Feb 22 2024 - Devrim Gündüz <devrim@gunduz.org> 5.5-2PGDG
- Add PGDG branding

* Sat Feb 4 2023 - Devrim Gündüz <devrim@gunduz.org> 5.5-1
- Update to 5.5

* Wed Jan 11 2023 - Devrim Gündüz <devrim@gunduz.org> 5.4-1
- Update to 5.4

* Wed Aug 10 2022 - Devrim Gündüz <devrim@gunduz.org> 5.3-1
- Update to 5.3

* Mon Dec 6 2021 - Devrim Gündüz <devrim@gunduz.org> 5.2-1
- Update to 5.2

* Wed Sep 29 2021 - Devrim Gündüz <devrim@gunduz.org> 5.1-1
- Update to 5.1

* Thu Feb 11 2021 - Devrim Gündüz <devrim@gunduz.org> 5.0-1
- Update to 5.0

* Wed Sep 2 2020 - Devrim Gündüz <devrim@gunduz.org> 4.4-1
- Update to 4.4

* Wed May 13 2020 - Devrim Gündüz <devrim@gunduz.org> 4.3-1
- Update to 4.3

* Fri Jan 31 2020 - Devrim Gündüz <devrim@gunduz.org> 4.2-1
- Update to 4.2

* Tue Jun 11 2019 - Devrim Gündüz <devrim@gunduz.org> 4.0-1
- Update to 4.0

* Tue Dec 11 2018 - Devrim Gündüz <devrim@gunduz.org> 3.3-1
- Update to 3.3

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 3.2-1.1
- Rebuild against PostgreSQL 11.0

* Tue Oct 9 2018 - Devrim Gündüz <devrim@gunduz.org> 3.2-1
- Update to 3.2

* Mon Sep 24 2018 - Devrim Gündüz <devrim@gunduz.org> 3.1-1
- Update to 3.1

* Sun Mar 4 2018 - Devrim Gündüz <devrim@gunduz.org> 3.0-1
- Update to 3.0

* Mon Jun 5 2017 - Devrim Gündüz <devrim@gunduz.org> 2.0-1
- Update to 2.0

* Mon Jan 23 2017 - Devrim Gündüz <devrim@gunduz.org> 1.6-1
- Update to 1.6

* Sun Oct 18 2015 - Devrim Gündüz <devrim@gunduz.org> 1.5-1
- Update to 1.5

* Sun Apr 19 2015 - Devrim Gündüz <devrim@gunduz.org> 1.4-1
- Update to 1.4

* Sun Mar 29 2015 - Devrim Gündüz <devrim@gunduz.org> 1.3-1
- Initial RPM packaging for PostgreSQL RPM Repository
