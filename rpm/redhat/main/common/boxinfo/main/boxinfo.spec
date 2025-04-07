Summary:	Gather information about a particular computer
Name:		boxinfo
Version:	1.4.0
Release:	3PGDG%{?dist}
License:	BSD
Source0:	%{name}.pl
Source2:	README.%{name}
URL:		https://bucardo.org/wiki/Boxinfo
BuildArch:	noarch

%description
boxinfo is a Perl script for quickly gathering all sorts of interesting
information about a particular computer, which is then put into a HTML
or MediaWiki page. It is very handy for being able to see a quick
overview of the boxes that you are responsible for. The script has a
highly developed Postgres section. It was developed at End Point
Corporation by Greg Sabino Mullane.

%prep
echo no prep stage needed

%build
echo no build stage needed

%install
%{__rm} -rf %{buildroot}

%{__install} -d -m 755 %{buildroot}%{_bindir}
%{__install} -d -m 755 %{buildroot}%{_docdir}/%{name}

%{__install} -m 755 %{SOURCE0} %{buildroot}%{_bindir}/%{name}.pl
%{__install} -m 644 %{SOURCE2} %{buildroot}%{_docdir}/%{name}/

%files
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/%{name}*
%attr(644,root,root) %{_docdir}/%{name}/README.%{name}

%changelog
* Mon Apr 7 2025 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-3PGDG
- Fix instalation issue on recent platforms

* Fri Feb 16 2024 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-2PGDG
- Modernise the spec file.
- Add PGDG branding.
- Fix rpmlint warning.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-1.1
- Rebuild against PostgreSQL 11.0

* Sat Apr 7 2012 - Devrim Gündüz <devrim@gunduz.org> 1.4.0-1
- Update to 1.4.0

* Mon Aug 22 2011 - Devrim Gündüz <devrim@gunduz.org> 1.3.3-1
- Update to 1.3.3

* Thu Nov 18 2010 - Devrim Gündüz <devrim@gunduz.org> 1.3.2-1
- Initial RPM packaging for PostgreSQL RPM Repository
