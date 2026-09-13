%global	realname Bucardo
Name:		bucardo_%{pgmajorversion}
Version:	5.6.0
Release:	2PGDG%{?dist}
Summary:	Postgres replication system for both multi-master and multi-slave operations

License:	BSD
URL:		https://bucardo.org/wiki/Bucardo
Source0:	https://bucardo.org/downloads/Bucardo-%{version}.tar.gz
Source1:	bucardo-master-master-replication-example.txt
Source2:	bucardo.init

Obsoletes:	bucardo <= 5.3.0

BuildArch:	noarch

BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(DBI)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(Sys::Hostname)
BuildRequires:	perl(Sys::Syslog)
BuildRequires:	perl(Net::SMTP)
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	libdbi-drivers-dbd-pgsql
%endif
%else
BuildRequires:	perl(DBD::Pg)
%endif

Requires:	perl(ExtUtils::MakeMaker)
Requires:	postgresql%{pgmajorversion}-plperl

Requires:	perl(DBI)
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
Requires:	libdbi-drivers-dbd-pgsql
%endif
%else
Requires:	perl(DBD::Pg)
%endif
Requires:	perl(IO::Handle)
Requires:	perl(Sys::Hostname)
Requires:	perl(Sys::Syslog)
Requires:	perl(Net::SMTP)

#testsuite
Requires:	perl(Test::Simple)
Requires:	perl(Test::Harness)

%description
Bucardo is an asynchronous PostgreSQL replication system, allowing for both
multi-master and multi-slave operations.It was developed at Backcountry.com
primarily by Greg Sabino Mullane of End Point Corporation.

%prep
%setup -q -n %{realname}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} +
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

sed -i -e '1d;2i#!/usr/bin/perl' bucardo

%{__rm} -f %{buildroot}/%{_bindir}/bucardo
%{__install} -Dp -m 755 bucardo %{buildroot}/%{_sbindir}/bucardo

%{__install} -Dp -m 644 %{SOURCE1} .

# Install init script
%{__install} -d %{buildroot}/etc/rc.d/init.d
%{__install} -m 755 %{SOURCE2} %{buildroot}/etc/rc.d/init.d/%{name}

#Install built-in scripts
%{__cp} scripts/bucardo* scripts/check_bucardo_sync scripts/slony_migrator.pl %{buildroot}/%{_bindir}

%{_fixperms} %{buildroot}

%post
%{__mkdir} -p /var/run/bucardo
%{__mkdir} -p /var/log/bucardo
%{__chown} -R postgres:postgres /var/run/bucardo
%{__chown} -R postgres:postgres /var/log/bucardo
chkconfig --add %{name}

%preun
if [ $1 = 0 ] ; then
	/sbin/service %{name} condstop >/dev/null 2>&1
	chkconfig --del %{name}
fi

%postun
if [ $1 -ge 1 ]; then
	/sbin/service %{name} condrestart >/dev/null 2>&1
fi

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc bucardo.html  Bucardo.pm.html Changes
%doc LICENSE README SIGNATURE TODO
%doc bucardo-master-master-replication-example.txt
%{perl_vendorlib}/*
%{_datadir}/bucardo/bucardo.schema
/etc/rc.d/init.d/%{name}
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_sbindir}/bucardo
%{_bindir}/bucardo-report
%{_bindir}/bucardo_rrd
%{_bindir}/check_bucardo_sync
%{_bindir}/slony_migrator.pl

%changelog
* Sun Sep 13 2026 Devrim Gündüz <devrim@gunduz.org> - 5.6.0-2PGDG
- Add PGDG branding
- Remove obsoleted BR

* Tue Mar 10 2020 Devrim Gündüz <devrim@gunduz.org> - 5.6.0-1
- Update to 5.6.0

* Tue Oct 30 2018 Devrim Gündüz <devrim@gunduz.org> - 5.5.0-1
- Update to 5.5.0
- Add PostgreSQL Remove hardcoded PostgreSQL version number, per PG bug
  #15469

* Tue Oct 30 2018 Devrim Gündüz <devrim@gunduz.org> - 5.4.1-2
- Remove hardcoded PostgreSQL version number, per PG bug #15469

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 5.4.1-1.1
- Rebuild against PostgreSQL 11.0

* Sun Mar 6 2016 Devrim Gündüz <devrim@gunduz.org> - 5.4.1-1
- Update to 5.4.1

* Fri Sep 11 2015 Devrim Gündüz <devrim@gunduz.org> - 5.4.0-1
- Update to 5.4.0
- Fix rpmlint warnings.
- Update init script per some rpmlint warnings.

* Tue Dec 23 2014 Devrim Gündüz <devrim@gunduz.org> - 5.3.0-1
- Update to 5.3.0
- Update download URL
- Also install built-in scripts

* Thu Sep 6 2012 Devrim Gündüz <devrim@gunduz.org> - 4.5.0-1
- Update to 4.5.0

* Sat Apr 7 2012 Devrim Gündüz <devrim@gunduz.org> - 4.4.8-1
- Update to 4.4.8

* Tue Sep 27 2011 Devrim Gündüz <devrim@gunduz.org> - 4.4.6-2
- Fix PostgreSQL major number version. Per report from Phil Sorber .

* Tue Aug 9 2011 Devrim Gündüz <devrim@gunduz.org> - 4.4.6-1
- Update to 4.4.6

* Mon Apr 18 2011 Devrim Gündüz <devrim@gunduz.org> - 4.4.3-1
- Update to 4.4.3

* Thu Jan 6 2011 Devrim Gündüz <devrim@gunduz.org> - 4.4.0-3
- Add 9.0 dependency.

* Fri Mar 12 2010 Devrim Gündüz <devrim@gunduz.org> - 4.4.0-2
- Sync with Fedora spec again.
