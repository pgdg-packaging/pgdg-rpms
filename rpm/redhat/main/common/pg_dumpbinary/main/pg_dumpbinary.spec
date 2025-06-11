Summary:	Dump a PostgreSQL database with data dumped in binary format
Name:		pg_dumpbinary
Version:	2.20
Release:	1PGDG%{?dist}
License:	BSD
Source0:	https://github.com/lzlabs/%{name}/archive/v%{version}.tar.gz
URL:		https://github.com/lzlabs/%{name}
Requires:	perl-Time-HiRes
BuildRequires:	perl-ExtUtils-MakeMaker
BuildArch:	noarch

%description
pg_dumpbinary is a program used to dump a PostgreSQL database with data
dumped in binary format. The resulting dumps must be restored using
pg_restorebinary.

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
%{__install} -m 755 pg_dumpbinary pg_restorebinary %{buildroot}%{_bindir}/
%{__install} -m 644 blib/man1/pg_dumpbinary.1p blib/man1/pg_restorebinary.1p %{buildroot}%{_mandir}/man1

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{_bindir}/pg_dumpbinary
%{_bindir}/pg_restorebinary
%{_mandir}/man1/pg_dumpbinary.1p.gz
%{_mandir}/man1/pg_restorebinary.1p.gz

%changelog
* Wed Jun 11 2025 Devrim Gündüz <devrim@gunduz.org> - 2.20-1PGDG
- Update to 2.20, per changes described at:
  https://github.com/lzlabs/pg_dumpbinary/releases/tag/v2.20

* Tue Apr 8 2025 Devrim Gündüz <devrim@gunduz.org> - 2.19-1PGDG
- Update to 2.19, per changes described at:
  https://github.com/lzlabs/pg_dumpbinary/releases/tag/v2.19

* Mon Jul 1 2024 Devrim Gündüz <devrim@gunduz.org> - 2.18-1PGDG
- Update to 2.18, per changes described at:
  https://github.com/lzlabs/pg_dumpbinary/releases/tag/v2.18

* Sun Apr 7 2024 Devrim Gündüz <devrim@gunduz.org> - 2.16-1PGDG
- Update to 2.16, per changes described at:
  https://github.com/lzlabs/pg_dumpbinary/releases/tag/v2.16

* Fri Feb 16 2024 Devrim Gündüz <devrim@gunduz.org> - 2.15-1PGDG
- Update to 2.15, per changes described at:
  https://github.com/lzlabs/pg_dumpbinary/releases/tag/v2.15

* Wed Jan 10 2024 Devrim Gündüz <devrim@gunduz.org> - 2.14-1PGDG
- Update to 2.14, per changes described at:
  https://github.com/lzlabs/pg_dumpbinary/releases/tag/v2.14

* Wed Oct 4 2023 Devrim Gündüz <devrim@gunduz.org> - 2.13-1PGDG
- Update to 2.13, per changes described at:
  https://github.com/lzlabs/pg_dumpbinary/releases/tag/v2.13
- Add PGDG branding

* Fri May 26 2023 Devrim Gündüz <devrim@gunduz.org> - 2.11-1
- Update to 2.11, per changes described at:
  https://github.com/lzlabs/pg_dumpbinary/releases/tag/v2.11

* Thu Mar 30 2023 Devrim Gündüz <devrim@gunduz.org> - 2.10-1
- Update to 2.10

* Tue Feb 7 2023 Devrim Gündüz <devrim@gunduz.org> - 2.9-1
- Update to 2.9

* Tue Nov 15 2022 Devrim Gündüz <devrim@gunduz.org> - 2.7-1
- Update to 2.7

* Thu Sep 9 2021 Devrim Gündüz <devrim@gunduz.org> - 2.5-1
- Update to 2.5

* Thu Jun 24 2021 Devrim Gündüz <devrim@gunduz.org> - 2.4-1
- Update to 2.4

* Wed Feb 5 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0-1
- Update to 2.0

* Sun Sep 1 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Initial packaging for PostgreSQL RPM Repository.
