Summary:	a unix pager optimized for psql
Name:		pspg
Version:	5.8.11
Release:	42PGDG%{?dist}
License:	BSD
URL:		https://github.com/okbob/%{name}
Source:		https://github.com/okbob/%{name}/archive/%{version}.tar.gz
BuildRequires:	ncurses-devel readline-devel
Requires:	ncurses readline

%description
pspg is a unix pager optimized for psql. It can freeze rows, freeze
columns, and lot of color themes are included.

%prep
%setup -q

%build
CFLAGS="%{optflags} -I/usr/include/ncurses/"
%configure
%{__make} %{_smp_mflags} \
	prefix=%{_prefix} \
	all

%install
%{__rm} -rf %{buildroot}
%{__make} %{_smp_mflags} DESTDIR=%{buildroot} \
	prefix=%{_prefix} bindir=%{_bindir} mandir=%{_mandir} \
	install

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md
%{_bindir}/*

%changelog
* Wed May 7 2025 Devrim Gündüz <devrim@gunduz.org> - 5.8.11-42PGDG
- Update to 5.8.11 per changes described at:
  https://github.com/okbob/pspg/releases/tag/5.8.11

* Mon May 5 2025 Devrim Gündüz <devrim@gunduz.org> - 5.8.10-42PGDG
- Update to 5.8.10 per changes described at:
  https://github.com/okbob/pspg/releases/tag/5.8.10

* Tue Apr 29 2025 Devrim Gündüz <devrim@gunduz.org> - 5.8.9-42PGDG
- Update to 5.8.9 per changes described at:
  https://github.com/okbob/pspg/releases/tag/5.8.9

* Fri Mar 7 2025 Devrim Gündüz <devrim@gunduz.org> - 5.8.8-42PGDG
- Update to 5.8.8 per changes described at:
  https://github.com/okbob/pspg/releases/tag/5.8.8

* Fri Sep 27 2024 Devrim Gündüz <devrim@gunduz.org> - 5.8.7-42PGDG
- Update to 5.8.7 per changes described at:
  https://github.com/okbob/pspg/releases/tag/5.8.7

* Fri May 10 2024 Devrim Gündüz <devrim@gunduz.org> - 5.8.6-42PGDG
- Update to 5.8.6 per changes described at:
  https://github.com/okbob/pspg/releases/tag/5.8.6

* Sat Apr 27 2024 Devrim Gündüz <devrim@gunduz.org> - 5.8.5-1PGDG
- Update to 5.8.5 per changes described at:
  https://github.com/okbob/pspg/releases/tag/5.8.5

* Mon Apr 22 2024 Devrim Gündüz <devrim@gunduz.org> - 5.8.4-1PGDG
- Update to 5.8.4 per changes described at:
  https://github.com/okbob/pspg/releases/tag/5.8.4

* Mon Apr 15 2024 Devrim Gündüz <devrim@gunduz.org> - 5.8.3-1PGDG
- Update to 5.8.3 per changes described at:
  https://github.com/okbob/pspg/releases/tag/5.8.3

* Tue Mar 26 2024 Devrim Gündüz <devrim@gunduz.org> - 5.8.2-1PGDG
- Update to 5.8.2 per changes described at:
  https://github.com/okbob/pspg/releases/tag/5.8.2

* Fri Nov 17 2023 Devrim Gündüz <devrim@gunduz.org> - 5.8.1-1PGDG
- Update to 5.8.1

* Fri Aug 11 2023 Devrim Gündüz <devrim@gunduz.org> - 5.8.0-42PGDG
- Don't allow OS packages to override our package.

* Tue Aug 8 2023 Devrim Gündüz <devrim@gunduz.org> - 5.8.0-1PGDG
- Update to 5.8.0

* Sun Jul 23 2023 Devrim Gündüz <devrim@gunduz.org> - 5.7.8-1PGDG
- Update to 5.7.8
- Add to PGDG branding

* Wed Jun 14 2023 Devrim Gündüz <devrim@gunduz.org> - 5.7.7-1
- Update to 5.7.7

* Fri Apr 21 2023 Devrim Gündüz <devrim@gunduz.org> - 5.7.6-1
- Update to 5.7.6

* Tue Apr 18 2023 Devrim Gündüz <devrim@gunduz.org> - 5.7.5-1
- Update to 5.7.5

* Tue Feb 14 2023 Devrim Gündüz <devrim@gunduz.org> - 5.7.4-1
- Update to 5.7.4

* Mon Jan 23 2023 Devrim Gündüz <devrim@gunduz.org> - 5.7.2-1
- Update to 5.7.2

* Mon Jan 2 2023 Devrim Gündüz <devrim@gunduz.org> - 5.7.1-1
- Update to 5.7.1

* Thu Dec 22 2022 Devrim Gündüz <devrim@gunduz.org> - 5.7.0-1
- Update to 5.7.0

* Tue Dec 6 2022 Devrim Gündüz <devrim@gunduz.org> - 5.6.4-1
- Update to 5.6.4

* Mon Nov 28 2022 Devrim Gündüz <devrim@gunduz.org> - 5.6.0-1
- Update to 5.6.0

* Mon Nov 28 2022 Devrim Gündüz <devrim@gunduz.org> - 5.5.13-1
- Update to 5.5.13

* Tue Nov 22 2022 Devrim Gündüz <devrim@gunduz.org> - 5.5.12-1
- Update to 5.5.12

* Tue Nov 8 2022 Devrim Gündüz <devrim@gunduz.org> - 5.5.9-1
- Update to 5.5.9

* Fri Oct 7 2022 Devrim Gündüz <devrim@gunduz.org> - 5.5.8-1
- Update to 5.5.8

* Fri Sep 16 2022 Devrim Gündüz <devrim@gunduz.org> - 5.5.7-1
- Update to 5.5.7

* Mon Aug 8 2022 Devrim Gündüz <devrim@gunduz.org> - 5.5.6-1
- Update to 5.5.6

* Mon Jul 18 2022 Devrim Gündüz <devrim@gunduz.org> - 5.5.5-1
- Update to 5.5.5

* Mon Feb 21 2022 Devrim Gündüz <devrim@gunduz.org> - 5.5.4-1
- Update to 5.5.4

* Wed Dec 22 2021 Devrim Gündüz <devrim@gunduz.org> - 5.5.3-1
- Update to 5.5.3

* Mon Nov 8 2021 Devrim Gündüz <devrim@gunduz.org> - 5.5.1-1
- Update to 5.5.1

* Tue Nov 2 2021 Devrim Gündüz <devrim@gunduz.org> - 5.5.0-1
- Update to 5.5.0

* Thu Oct 14 2021 Devrim Gündüz <devrim@gunduz.org> - 5.4.1-1
- Update to 5.4.1

* Mon Oct 11 2021 Devrim Gündüz <devrim@gunduz.org> - 5.4.0-1
- Update to 5.4.0

* Mon Sep 13 2021 Devrim Gündüz <devrim@gunduz.org> - 5.3.5-1
- Update to 5.3.5

* Tue Aug 17 2021 Devrim Gündüz <devrim@gunduz.org> - 5.3.4-1
- Update to 5.3.4

* Wed Aug 11 2021 Devrim Gündüz <devrim@gunduz.org> - 5.3.3-1
- Update to 5.3.3

* Wed Aug 4 2021 Devrim Gündüz <devrim@gunduz.org> - 5.3.2-1
- Update to 5.3.2 (only for RHEL 7)

* Sun Aug 1 2021 Devrim Gündüz <devrim@gunduz.org> - 5.3.1-1
- Update to 5.3.1

* Mon Jul 26 2021 Devrim Gündüz <devrim@gunduz.org> - 5.1.3-1
- Update to 5.1.3

* Mon Jul 5 2021 Devrim Gündüz <devrim@gunduz.org> - 5.0.5-1
- Update to 5.0.5

* Mon Jun 21 2021 Devrim Gündüz <devrim@gunduz.org> - 5.0.4-1
- Update to 5.0.4

* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> - 5.0.2-1
- Update to 5.0.2
- Remove RHEL 6 stuff.

* Wed Apr 28 2021 Devrim Gündüz <devrim@gunduz.org> - 4.6.3-1
- Update to 4.6.3

* Fri Apr 23 2021 Devrim Gündüz <devrim@gunduz.org> - 4.6.1-1
- Update to 4.6.1

* Mon Apr 19 2021 Devrim Gündüz <devrim@gunduz.org> - 4.6.0-1
- Update to 4.6.0

* Sun Mar 28 2021 Devrim Gündüz <devrim@gunduz.org> - 4.5.0-1
- Update to 4.5.0

* Sun Mar 21 2021 Devrim Gündüz <devrim@gunduz.org> - 4.4.0-1
- Update to 4.4.0

* Thu Mar 11 2021 Devrim Gündüz <devrim@gunduz.org> - 4.3.1-1
- Update to 4.3.1

* Tue Feb 9 2021 Devrim Gündüz <devrim@gunduz.org> - 4.2.1-1
- Update to 4.2.1

* Fri Feb 5 2021 Devrim Gündüz <devrim@gunduz.org> - 4.1.0-1
- Update to 4.1.0

* Tue Oct 20 2020 Devrim Gündüz <devrim@gunduz.org> - 3.1.5-1
- Update to 3.1.5

* Thu Sep 17 2020 Devrim Gündüz <devrim@gunduz.org> - 3.1.4-1
- Update to 3.1.4

* Fri Aug 28 2020 Devrim Gündüz <devrim@gunduz.org> - 3.1.3-1
- Update to 3.1.3

* Wed Jul 29 2020 Devrim Gündüz <devrim@gunduz.org> - 3.1.2-1
- Update to 3.1.2

* Wed May 13 2020 Devrim Gündüz <devrim@gunduz.org> - 3.0.7-1
- Update to 3.0.7

* Fri Mar 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.7.0-1
- Update to 2.7.0

* Fri Jan 31 2020 Devrim Gündüz <devrim@gunduz.org> - 2.6.6-1
- Update to 2.6.6

* Thu Nov 21 2019 Devrim Gündüz <devrim@gunduz.org> - 2.5.5-1
- Update to 2.5.5

* Fri Oct 18 2019 Devrim Gündüz <devrim@gunduz.org> - 2.1.8-1
- Update to 2.1.8

* Tue Oct 15 2019 Devrim Gündüz <devrim@gunduz.org> - 2.1.7-1
- Update to 2.1.7

* Fri Sep 13 2019 Devrim Gündüz <devrim@gunduz.org> - 2.0.3-1
- Update to 2.0.3

* Mon Sep 9 2019 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-1
- Update to 2.0.1

* Sun Sep 1 2019 Devrim Gündüz <devrim@gunduz.org> - 1.7.1-1
- Update to 1.7.1

* Sun Aug 11 2019 Devrim Gündüz <devrim@gunduz.org> - 1.6.8-1
- Update to 1.6.8

* Wed Jul 24 2019 Devrim Gündüz <devrim@gunduz.org> - 1.6.6-1
- Update to 1.6.6

* Tue Apr 16 2019 Devrim Gündüz <devrim@gunduz.org> - 1.6.5-1
- Update to 1.6.5

* Sun Mar 24 2019 Devrim Gündüz <devrim@gunduz.org> - 1.6.4-1
- Update to 1.6.4

* Thu Nov 29 2018 Devrim Gündüz <devrim@gunduz.org> - 1.6.3-1
- Update to 1.6.3

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.6.1-1.1
- Rebuild against PostgreSQL 11.0

* Fri Sep 7 2018 Devrim Gündüz <devrim@gunduz.org> 1.6.1-1
- Update to 1.6.1, per #3626

* Thu Aug 23 2018 Devrim Gündüz <devrim@gunduz.org> 1.3.0-1
- Update to 1.3.0

* Fri Jul 27 2018 Devrim Gündüz <devrim@gunduz.org> 1.2.2-1
- Update to 1.2.2, per #3517

* Tue May 1 2018 Devrim Gündüz <devrim@gunduz.org> 1.1.1-1
- Update to 1.1.1, per #3315 ( RHEL 7 only)

* Sun Apr 29 2018 Devrim Gündüz <devrim@gunduz.org> 1.1.0-1
- Update to 1.1.0, per #3315

* Fri Mar 16 2018 Devrim Gündüz <devrim@gunduz.org> 1.0.0-1
- Update to 1.0.0, per #3210

* Mon Feb 12 2018 Devrim Gündüz <devrim@gunduz.org> 0.9.3-1
- Update to 0.9.3, per #3102.

* Fri Jan 12 2018 Devrim Gündüz <devrim@gunduz.org> 0.9.2-1
- Update to 0.9.2, per #3006 .

* Mon Dec 4 2017 Devrim Gündüz <devrim@gunduz.org> 0.7.5-1
- Update to 0.7.5, per #2932 .

* Sun Nov 26 2017 Devrim Gündüz <devrim@gunduz.org> 0.7.2-1
- Update to 0.7.2, per #2912.

* Fri Nov 17 2017 Devrim Gündüz <devrim@gunduz.org> 0.5-1
- Update to 0.5

* Fri Sep 15 2017 Devrim Gündüz <devrim@gunduz.org> 0.1-1
- Initial packaging for PostgreSQL RPM repository, based on the spec
  file written by Pavel. Fixes #2704
