%global		pgcluudatadir		/var/lib/pgcluu/data
%global		pgcluureportdir		/var/lib/pgcluu/report

Summary:	PostgreSQL performance monitoring and auditing tool
Name:		pgcluu
Version:	4.0
Release:	3PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/darold/%{name}/archive/v%{version}.tar.gz
Source1:	%{name}.service
Source2:	%{name}_collectd.service
Source3:	%{name}.timer
Source4:	%{name}-httpd.conf
Patch0:		%{name}-systemd-rpm-paths.patch
URL:		http://%{name}.darold.net/
BuildArch:	noarch
%if 0%{?rhel} && 0%{?rhel} == 7
%else
Recommends:	httpd sysstat
%endif

%description
pgCluu is a PostgreSQL performances monitoring and auditing tool.
View reports of all statistics collected from your PostgreSQL
databases cluster. pgCluu will show you the entire information
of the PostgreSQL cluster and the system utilization

%prep
%setup -q
%patch -P 0 -p0

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} pure_install PERL_INSTALL_ROOT=%{buildroot}

# Install Apache sample config file
%{__install} -d %{buildroot}%{_sysconfdir}/httpd/conf.d/
%{__install} -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf

# Install CGI
%{__install} -d %{buildroot}/var/www/cgi-bin
%{__install} -m 644 cgi-bin/%{name}.cgi %{buildroot}/var/www/cgi-bin/%{name}.cgi

# Install pgCluu config file
%{__install} -d %{buildroot}%{_sysconfdir}/
%{__install} -m 644 pgcluu.conf %{buildroot}%{_sysconfdir}/%{name}.conf

%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE1} %{SOURCE2} %{SOURCE3} %{buildroot}%{_unitdir}/

%post
%{__mkdir} -p %{pgcluudatadir}
%{__mkdir} -p %{pgcluureportdir}
%{__chown} postgres:postgres %{pgcluureportdir}
%{__chmod} u=rwX,g=rsX,o= %{pgcluureportdir}

%files
%defattr(-,root,root,-)
%doc ChangeLog
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}_collectd
%perl_vendorarch/auto/pgCluu/.packlist
%{_mandir}/man1/%{name}.1p.gz
%{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_sysconfdir}/%{name}.conf
/var/www/cgi-bin/%{name}.cgi
%{_unitdir}/%{name}_collectd.service
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.timer

%changelog
* Fri Aug 28 2026 Devrim Gündüz <devrim@gunduz.org> - 4.0-3PGDG
- Add RestartSec and StartLimitIntervalSec/StartLimitBurst to the
  pgcluu and pgcluu_collectd service files, and drop a redundant
  duplicate Restart=on-failure line from pgcluu_collectd.service, so
  that Restart=on-failure cannot crash-loop indefinitely. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/191
* Wed Dec 24 2025 Devrim Gündüz <devrim@gunduz.org> - 4.0-2PGDG
- Add Restart=on-failure to unit file. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/127

* Wed Mar 6 2024 Devrim Gündüz <devrim@gunduz.org> 4.0-1PGDG
- Update to 4.0 per changes described at:
  https://github.com/darold/pgcluu/releases/tag/v4.0

* Thu Jul 13 2023 Devrim Gündüz <devrim@gunduz.org> 3.5-1PGDG
- Update to 3.5
- Add PGDG branding

* Mon Jun 12 2023 Devrim Gündüz <devrim@gunduz.org> 3.4-2
- Add httpd (and systat) as weak dependency, per Christophe Courtois :
  https://www.postgresql.org/message-id/ba11dfd1-ded7-c7f2-5cd2-c878dada808f%40dalibo.com

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 3.4-1.1
- Modernise %%patch usage, which has been deprecated in Fedora 38

* Mon Jan 2 2023 Devrim Gündüz <devrim@gunduz.org> 3.4-1
- Update to 3.4

* Sat Jun 4 2022 Devrim Gündüz <devrim@gunduz.org> 3.3-1
- Update to 3.3

* Wed Oct 6 2021 Devrim Gündüz <devrim@gunduz.org> 3.2-1
- Update to 3.2

* Wed Jan 1 2020 Devrim Gündüz <devrim@gunduz.org> 3.1-2
- Add cgi file and config file, per #4833

* Tue Oct 29 2019 Devrim Gündüz <devrim@gunduz.org> 3.1-1
- Update to 3.1

* Thu Oct 17 2019 Devrim Gündüz <devrim@gunduz.org> 3.0-2
- Various fixes for https://redmine.postgresql.org/issues/4833

* Fri Sep 27 2019 Devrim Gündüz <devrim@gunduz.org> 3.0-1
- Update to 3.0

* Wed Jan 2 2019 Devrim Gündüz <devrim@gunduz.org> 2.9-1
- Update to 2.9

* Tue Dec 11 2018 Devrim Gündüz <devrim@gunduz.org> 2.8-1
- Update to 2.8

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.6-2.1
- Rebuild against PostgreSQL 11.0

* Sat Jul 15 2017 Devrim Gündüz <devrim@gunduz.org> 2.6-1
- Update to 2.6
- Install systemd related files.
- Add a patch to fix paths in unit files.

* Sat Aug 13 2016 Devrim Gündüz <devrim@gunduz.org> 2.5-1
- Update to 2.5

* Fri Sep 11 2015 Devrim Gündüz <devrim@gunduz.org> 2.4-1
- Update to 2.4
- Fix rpmlint warning (add %%build section)
- Update download URL

* Sun Jan 11 2015 Devrim Gündüz <devrim@gunduz.org> 2.2-1
- Update to 2.2

* Fri Sep 26 2014 Devrim Gündüz <devrim@gunduz.org> 2.1-1
- Update to 2.1

* Tue Apr 1 2014 Devrim Gündüz <devrim@gunduz.org> 2.0-1
- Update to 2.0

* Wed Jan 15 2014 Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
