%global sname check_pgactivity

%global		_tag REL2_8

Name:		nagios-plugins-pgactivity
Version:	2.8
Release:	1PGDG%{dist}
Summary:	PostgreSQL monitoring plugin for Nagios
License:	PostgreSQL
Url:		http://opm.io
Source0:	https://github.com/OPMDG/%{sname}/archive/%{_tag}.tar.gz
BuildArch:	noarch
Requires:	nagios-plugins
Provides:	%{sname} = %{version}

%description
check_pgactivity is a monitoring plugin of PostgreSQL for Nagios. It provides
many checks and allow the gathering of many performance counters.
check_pgactivity is part of Open PostgreSQL Monitoring.

%prep
%setup -q -n %{sname}-%{_tag}

%build

%install
%{__install} -D -p -m 0755 %{sname} %{buildroot}/%{_libdir}/nagios/plugins/%{sname}

%files
%defattr(-,root,root,0755)
%{_libdir}/nagios/plugins/%{sname}
%doc README
%license LICENSE

%changelog
* Tue Oct 14 2025 Devrim Gündüz <devrim@gunduz.org> 2.8-1PGDG
- Update to 2.8 per changes described at:
  https://github.com/OPMDG/check_pgactivity/releases/tag/REL2_8

* Mon Aug 21 2023 Devrim Gündüz <devrim@gunduz.org> 2.6-2PGDG
- Remove RHEL 6 bits
- Add PGDG branding

* Mon Jul 11 2022 Devrim Gündüz <devrim@gunduz.org> 2.6-1
- Update to 2.6

* Tue Dec 1 2020 Devrim Gündüz <devrim@gunduz.org> 2.5-1
- Update to 2.5

* Mon Apr 27 2020 Devrim Gündüz <devrim@gunduz.org> 2.4-2
- Remove PostgreSQL dependency, per #5418
- Actually use 2.4 tarball.

* Thu Jan 31 2019 Devrim Gündüz <devrim@gunduz.org> 2.4-1
- Update to 2.4

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.3-1.1
- Rebuild against PostgreSQL 11.0

* Tue Dec 5 2017 Devrim Gündüz <devrim@gunduz.org> 2.3-1
- Update to 2.3

* Mon May 29 2017 Devrim Gündüz <devrim@gunduz.org> 2.2-1
- Update to 2.2

* Sun Sep 18 2016 Devrim Gündüz <devrim@gunduz.org> 2.0-1
- Update to 2.0

* Wed Feb 10 2016 Devrim Gündüz <devrim@gunduz.org> 1.25-1
- Update to 1.25

* Wed Jan 06 2016 Devrim Gündüz <devrim@gunduz.org> 1.25-beta1-1
- Update to 1.25 beta1
- Fix rpmlint warnings, and adjust to PGDG release format.

* Wed Dec 10 2014 Nicolas Thauvin <nicolas.thauvin@dalibo.com> 1.19-1
- update to release 1.19

* Fri Sep 19 2014 Nicolas Thauvin <nicolas.thauvin@dalibo.com> 1.15-1
- Initial version
