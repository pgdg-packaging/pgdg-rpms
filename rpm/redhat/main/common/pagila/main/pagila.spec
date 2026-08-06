Summary:	A sample database for PostgreSQL
Name:		pagila
Version:	4.1.0
Release:	1PGDG%{?dist}
License:	BSD
URL:		https://github.com/devrimgunduz/%{name}
Source0:	https://github.com/devrimgunduz/%{name}/archive/%{name}-v%{version}.tar.gz

Requires:	postgresql-server >= 18.0

BuildArch:	noarch

%global		_pagiladir  %{_datadir}/%{name}

%description
Pagila is a port of the Sakila example database available for MySQL, which was
originally developed by Mike Hillyer of the MySQL AB documentation team. It
is intended to provide a standard schema that can be used for examples in
books, tutorials, articles, samples, etc.

%prep
%setup -q -n %{name}-%{name}-v%{version}

%build

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_pagiladir}
%{__install} -m 644 -p *.sql *.backup *.png %{buildroot}%{_pagiladir}
%{__install} -m 644 docker-compose.yml %{buildroot}%{_pagiladir}
%{__install} -m 644 Dockerfile %{buildroot}%{_pagiladir}
%{__install} -m 755 restore-pagila-data-jsonb.sh %{buildroot}%{_pagiladir}
%{__cp} -r pgadmin/ scripts/ %{buildroot}%{_pagiladir}

%files
%defattr(0644,root,root,0755)
%doc README.md
%license LICENSE.txt
%dir %{_pagiladir}
%attr(644,root,root) %{_pagiladir}/*.backup
%attr(644,root,root) %{_pagiladir}/*.png
%attr(644,root,root) %{_pagiladir}/*.sql
%attr(644,root,root) %{_pagiladir}/Dockerfile
%attr(644,root,root) %{_pagiladir}/docker-compose.yml
%attr(644,root,root) %{_pagiladir}/pgadmin/*
%attr(755,root,root) %{_pagiladir}/restore-pagila-data-jsonb.sh
%attr(644,root,root) %{_pagiladir}/scripts/*

%changelog
* Thu Aug 6 2026 Devrim Gündüz <devrim@gunduz.org> - 4.1.0-1PGDG
- Update to 4.1.0 per changes described at:
  https://github.com/devrimgunduz/pagila/releases/tag/pagila-v4.1.0

* Tue Jul 28 2026 Devrim Gündüz <devrim@gunduz.org> - 4.0.0-1PGDG
- Update to 4.0.0 per changes described at:
  https://github.com/devrimgunduz/pagila/releases/tag/pagila-v4.0.0

* Thu Feb 22 2024 Devrim Gündüz <devrim@gunduz.org> - 3.1.0-2PGDG
- Add PGDG branding

* Fri Dec 23 2022 Devrim Gündüz <devrim@gunduz.org> - 3.1.0-1
- Update to 3.1.0, per changes described at:
  https://github.com/devrimgunduz/pagila/releases/tag/pagila-v3.1.0

* Thu Jul 28 2022 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-1
- Update to 3.0.0, per changes described at:
  https://github.com/devrimgunduz/pagila/releases/tag/pagila-v3.0.0

* Sat Aug 22 2020 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-1
- Update to 2.1.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-1.1
- Rebuild against PostgreSQL 11.0

* Tue Jun 20 2017 Devrim Gündüz <devrim@gunduz.org> 2.0.1-1
- Update to 2.0.1

* Tue Jun 6 2017 Devrim Gündüz <devrim@gunduz.org> 2.0-1
- Update to 2.0, which is the version that I forked.

* Mon Sep 27 2010 Devrim Gündüz <devrim@gunduz.org> 0.10.1-2
- Apply some minor fixes for new PostgreSQL RPM layout.

* Sat Jun 14 2008 Devrim Gündüz <devrim@gunduz.org> 0.10.1-1
- Update to 0.10.1

* Fri Feb 1 2008 Devrim Gündüz <devrim@gunduz.org> 0.10.0-1
- Initial packaging for Fedora/EPEL
