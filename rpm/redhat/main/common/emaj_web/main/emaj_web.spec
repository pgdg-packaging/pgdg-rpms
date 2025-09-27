%global		sname emaj_web

Summary:	Web-based Emaj administration
Name:		%{sname}
Version:	4.7.1
Release:	1PGDG%{?dist}
License:	GPL
URL:		https://github.com/dalibo/%{sname}
Source0:	https://github.com/dalibo/%{sname}/archive/refs/tags/v%{version}.tar.gz
Source1:	%{name}.conf

Requires:	php >= 7.2
Requires:	php-pgsql >= 7.2, httpd
Requires(post):	systemd
Requires(postun):	systemd
BuildArch:	noarch

%global		_emajwebdir	%{_datadir}/%{name}

%description
Emaj_web is a php web client that interfaces the E-Maj PostgreSQL extension
(available on https://github.com/dalibo/emaj).

The main goals of E-Maj are:
- log updates performed on one or several sets of tables.
- cancel these updates if needed, and reset a tables set to a
  predefined stable state.

The client allows users to easily look at the tables groups state and
perform all E-Maj operations.

%prep
%setup -q -n %{name}-%{version}

%build

%install

%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_emajwebdir}
%{__install} -d %{buildroot}%{_emajwebdir}/conf
%{__install} -d %{buildroot}%{_sysconfdir}/%{name}
%{__install} -d %{buildroot}%{_sysconfdir}/httpd/conf.d/
%{__cp} -rp classes/ css/ images/ js/ lang/ libraries/ xloadtree/ *.php %{buildroot}%{_emajwebdir}
%{__install} -m 644 -p *.php %{buildroot}%{_emajwebdir}
%{__install} -m 755 -p %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
%{__install} -m 755 conf/* %{buildroot}%{_sysconfdir}/%{name}
%{__ln_s} -r %{_sysconfdir}/%{name}/config.inc.php %{buildroot}/%{_emajwebdir}/conf/config.inc.php
%{__ln_s} -r %{_sysconfdir}/%{name}/config.inc.php-dist %{buildroot}/%{_emajwebdir}/conf/config.inc.php-dist

%post
/usr/bin/systemctl reload httpd.service

%postun
/usr/bin/systemctl reload httpd.service

%files
%doc INSTALL.md README.md
%license LICENSE
%dir %{_emajwebdir}
%dir %{_sysconfdir}/%{name}
%dir %{_emajwebdir}/classes
%dir %{_emajwebdir}/conf
%dir %{_emajwebdir}/css
%dir %{_emajwebdir}/images
%dir %{_emajwebdir}/js
%dir %{_emajwebdir}/lang
%dir %{_emajwebdir}/libraries
%dir %{_emajwebdir}/xloadtree

%{_emajwebdir}/classes/*
%{_emajwebdir}/conf/*
%{_emajwebdir}/css/*
%{_emajwebdir}/images/*
%{_emajwebdir}/js/*
%{_emajwebdir}/lang/*
%{_emajwebdir}/libraries/*
%{_emajwebdir}/xloadtree/*

%config(noreplace) %{_sysconfdir}/%{name}/*
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%attr(644,root,root) %{_emajwebdir}/*.php

%changelog
* Sat Sep 27 2025 Devrim Gündüz <devrim@gunduz.org> - 4.7.1-1PGDG
- Update to 4.7.1

* Tue Sep 2 2025 Devrim Gündüz <devrim@gunduz.org> - 4.7.0-1PGDG
- Update to 4.7.0

* Sat Mar 22 2025 Devrim Gündüz <devrim@gunduz.org> - 4.6.0-1PGDG
- Update to 4.6.0

* Mon Sep 9 2024 Devrim Gündüz <devrim@gunduz.org> - 4.5.0-1PGDG
- Update to 4.5.0

* Sat Apr 20 2024 Devrim Gündüz <devrim@gunduz.org> - 4.4.0-1PGDG
- Update to 4.4.0
- Fix rpm build warning about the absolute symlink.

* Wed Nov 1 2023 Devrim Gündüz <devrim@gunduz.org> - 4.3.1-1PGDG
- Update to 4.3.1

* Mon Sep 18 2023 Devrim Gündüz <devrim@gunduz.org> - 4.3.0-1PGDG
- Update to 4.3.0
- Add PGDG branding

* Mon Apr 10 2023 Devrim Gündüz <devrim@gunduz.org> - 4.2.0-1
- Update to 4.2.0

* Mon Oct 3 2022 Devrim Gündüz <devrim@gunduz.org> - 4.1.0-1
- Update to 4.1.0

* Fri Apr 29 2022 Devrim Gündüz <devrim@gunduz.org> - 4.0.1-1
- Initial packaging for the PostgreSQL RPM repository.
