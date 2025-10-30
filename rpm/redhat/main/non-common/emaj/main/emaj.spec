%global sname e-maj
%global pname emaj

Name:		%{sname}_%{pgmajorversion}
Version:	4.7.1
Release:	2PGDG%{?dist}
Summary:	A table update logger for PostgreSQL
License:	GPLv2
URL:		https://github.com/dalibo/%{pname}/
Source0:	https://github.com/dalibo/%{pname}/archive/refs/tags/v%{version}.tar.gz

BuildArch:	noarch
Requires:	postgresql%{pgmajorversion}-contrib

%description
E-Maj is a set of PL/pgSQL functions allowing PostgreSQL Database
Administrators to record updates applied on a set of tables, with
the capability to "rollback" these updates to a predefined point
in time.

%prep
%setup -q -n %{pname}-%{version}

%build

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{pginstdir}/share/extension/
%{__cp} -r sql/* %{buildroot}%{pginstdir}/share/extension
%{__cp} %{pname}.control %{buildroot}%{pginstdir}/share/extension

%files
%defattr(-,root,root,-)
%license LICENSE
%doc CHANGES.md docs README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*.sql

%changelog
* Thu Oct 30 2025 Devrim Gündüz <devrim@gunduz.org> - 4.7.1-2PGDG
- Rebuild because of a package signing issue on Fedora 43

* Sat Sep 27 2025 Devrim Gündüz <devrim@gunduz.org> - 4.7.1-1PGDG
- Update to 4.7.1

* Tue Sep 2 2025 Devrim Gündüz <devrim@gunduz.org> - 4.7.0-1PGDG
- Update to 4.7.0

* Sat Mar 22 2025 Devrim Gündüz <devrim@gunduz.org> - 4.6.0-1PGDG
- Update to 4.6.0

* Thu Jan 9 2025 Devrim Gündüz <devrim@gunduz.org> - 4.5.0-2PGDG
- Add -contrib dependency for the required dblink extension.

* Mon Sep 9 2024 Devrim Gündüz <devrim@gunduz.org> - 4.5.0-1PGDG
- Update to 4.5.0

* Sat Apr 20 2024 Devrim Gündüz <devrim@gunduz.org> - 4.4.0-1PGDG
- Update to 4.4.0

* Wed Nov 1 2023 Devrim Gündüz <devrim@gunduz.org> - 4.3.1-1PGDG
- Update to 4.3.1

* Mon Sep 18 2023 Devrim Gündüz <devrim@gunduz.org> - 4.3.0-1PGDG
- Update to 4.3.0
- Add PGDG branding

* Mon Apr 3 2023 Devrim Gündüz <devrim@gunduz.org> - 4.2.0-1
- Update to 4.2.0

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 4.1.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Sun Oct 2 2022 Devrim Gündüz <devrim@gunduz.org> - 4.1.0-1
- Update to 4.1.0

* Fri Apr 29 2022 Devrim Gündüz <devrim@gunduz.org> - 4.0.1-1
- Update to 4.0.1
- Move this package to non-common directory, to where it belongs.

* Sun Jul 26 2020 Devrim Gündüz <devrim@gunduz.org> - 3.4.0-1
- Update to 3.4.0

* Fri Mar 27 2020 Devrim Gündüz <devrim@gunduz.org> - 3.3.0-1
- Update to 3.3.0

* Mon Nov 4 2019 Devrim Gündüz <devrim@gunduz.org> - 3.2.0-1
- Update to 3.2.0

* Sun Jun 23 2019 Devrim Gündüz <devrim@gunduz.org> - 3.1.0-1
- Update to 3.1.0

* Sun Mar 24 2019 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-1
- Update to 3.0.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.3.1-1.1
- Rebuild against PostgreSQL 11.0

* Fri Sep 7 2018 Devrim Gündüz <devrim@gunduz.org> - 2.3.1-1
- Update to 2.3.1

* Wed Mar 14 2018 Devrim Gündüz <devrim@gunduz.org> - 2.2.3-1
- Update to 2.2.3

* Sat Jan 27 2018 Devrim Gündüz <devrim@gunduz.org> - 2.2.2-1
- Update to 2.2.2

* Tue Dec 26 2017 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-1
- Update to 2.2.1

* Wed Dec 20 2017 Devrim Gündüz <devrim@gunduz.org> - 2.2.0-1
- Update to 2.2.0

* Thu Aug 3 2017 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-1
- Update to 2.1.0

* Fri Feb 24 2017 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-1
- Update to 2.0.1

* Wed Nov 16 2016 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-1
- Update to 2.0.0

* Sat Sep 17 2016 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-1
- Update to 1.3.1

* Mon Jan 4 2016 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1
- Update to 1.2.0

* Mon Nov 9 2015 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-2
- Fixes for Fedora 23 and new doc layout in 9.5.

* Wed Jan 22 2014 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1
- Update to 1.1.0

* Mon Jan 7 2013 Devrim Gündüz <devrim@gunduz.org> - 1.0.1-1
- Update to 1.0.1

* Tue Dec 11 2012 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1
- Initial RPM packaging for PostgreSQL RPM repository.
