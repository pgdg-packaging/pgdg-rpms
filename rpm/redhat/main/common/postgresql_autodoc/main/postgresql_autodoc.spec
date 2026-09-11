Name:		postgresql_autodoc
Version:	1.41.1
Release:	3PGDG%{?dist}
Summary:	PostgreSQL AutoDoc Utility
License:	BSD
URL:		https://github.com/devrimgunduz/%{name}/
Source0:	https://github.com/devrimgunduz/%{name}/archive/%{version}.tar.gz
Patch0:		%{name}-makefile.patch
BuildArch:	noarch

BuildRequires:	make
BuildRequires:	perl(DBD::Pg)
BuildRequires:	perl(HTML::Template), perl(Term::ReadKey)

Requires:	postgresql-server, perl-TermReadKey
Requires:	perl(DBD::Pg)

%description
This is a utility which will run through PostgreSQL system
tables and returns HTML, Dot, Dia and DocBook XML which
describes the database.

%prep
%setup -q
%patch -P 0 -p0

%build
# Temp fix.
%{__mv} %{name}.1 %{name}.1.in
PREFIX=%{_usr} make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
DESTDIR=%{buildroot} PREFIX=%{_usr} make install %{?_smp_mflags}

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man1/%{name}.1.gz

%changelog
* Thu Sep 10 2026 Devrim Gunduz <devrim@gunduz.org> - 1.41.1-3PGDG
- Add missing BR

* Wed Feb 21 2024 Devrim Gunduz <devrim@gunduz.org> - 1.41.1-2PGDG
- Add PGDG branding

- Modernise %patch usage, which has been deprecated in Fedora 38

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.41.1-1.1
- Rebuild against PostgreSQL 11.0

* Wed Jan 27 2016 - Devrim Gündüz <devrim@gunduz.org> 1.41.1-1
- Move to new repo, as the old one gives 404 for a long time.
- Minor cleanup

* Tue Feb 26 2013 - Devrim Gündüz <devrim@gunduz.org> 1.41-1
- Update to 1.41

* Tue Oct 13 2009 - Devrim Gündüz <devrim@gunduz.org> 1.40-1
- Update to 1.40

* Mon Mar 17 2008 - Devrim Gündüz <devrim@gunduz.org> 1.31-1
- Update to 1.31

* Sat Jun 9 2007 - Devrim Gündüz <devrim@gunduz.org> 1.30-2
- Some more fixes ber bugzilla review #200630

* Tue Jan 2 2007 - Devrim Gündüz <devrim@gunduz.org> 1.30-1
- Updated to 1.30
- Removed patch, since it is in now upstream

* Fri Dec 29 2006 - Devrim Gündüz <devrim@gunduz.org> 1.25-5
- Added a patch from Toshio Kuratomi

* Sat Aug 19 2006 - Devrim Gündüz <devrim@gunduz.org> 1.25-4
- Fixed spec file per bugzilla review #200630

* Wed Aug 9 2006 - Devrim Gündüz <devrim@gunduz.org> 1.25-3
- Fixed license

* Thu Dec 29 2005 - Devrim Gündüz <devrim@gunduz.org> 1.25-2
- Rebuilt for Fedora Core Extras submission
- Fixed rpmlint errors and warnings

* Thu Dec 29 2005 - Devrim Gündüz <devrim@gunduz.org> 1.25-1
- Initial version
