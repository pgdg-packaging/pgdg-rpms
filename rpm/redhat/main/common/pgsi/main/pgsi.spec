Summary:	PostgreSQL Log Analyzer Script
Name:		pgsi
Version:	1.7.1
Release:	3PGDG%{?dist}
License:	BSD
Source0:	http://bucardo.org/downloads/%{name}-%{version}.tar.gz
URL:		http://bucardo.org/pgsi
Requires:	perl(Data::Dumper) perl(Getopt::Long) perl(IO::Handle) perl(Time::Local)
BuildRequires:	make perl-Pod-Html
BuildRequires:	perl-Test-Simple >= 0.80 perl-ExtUtils-MakeMaker
BuildArch:	noarch

%description
PGSI is a Perl utility for parsing and analyzing PostgreSQL logs to
produce wiki-ready system impact reports.

%prep
%setup -q

%build
%{__perl} Makefile.PL
%{__make}

%install
%{__rm} -rf %{buildroot}

# We install everthing manually, as make install points
# to /usr/local directory.
%{__install} -d %{buildroot}%{_bindir}/
%{__install} -d %{buildroot}%{_mandir}/man1
%{__install} -d %{buildroot}%{_docdir}/%{name}-%{version}
%{__install} -m 755 pgsi.pl %{buildroot}%{_bindir}/
%{__install} -m 644 blib/man1/pgsi.pl.1 %{buildroot}%{_mandir}/man1
%{__install} -m 644 pgsi.html %{buildroot}%{_docdir}/%{name}-%{version}/

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%license LICENSE
%{_bindir}/%{name}.pl
%{_mandir}/man1/*
%dir %{_docdir}/%{name}-%{version}
%{_docdir}/%{name}-%{version}/*

%changelog
* Thu Sep 10 2026 Devrim Gündüz <devrim@gunduz.org> - 1.7.1-3PGDG
- Add missing BR

* Mon Aug 21 2023 Devrim Gündüz <devrim@gunduz.org> - 1.7.1-2PGDG
- Remove RHEL 6 bits
- Add PGDG branding

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.7.1-1.1
- Rebuild against PostgreSQL 11.0

* Tue Jan 26 2016 - Devrim Gündüz <devrim@gunduz.org> 1.7.1-1
- Update to 1.7.1
- Use more macros, for unified spec file
- Cosmetic updates

* Thu May 27 2010 - Devrim Gündüz <devrim@gunduz.org> 1.2.0-1
- Update to 1.2.0

* Sun Feb 15 2009 - Devrim Gündüz <devrim@gunduz.org> 1.1.1-1
- Initial RPM packaging for yum.postgresql.org
