%global sname e-maj
%global pname emaj

%{!?runselftest:%global runselftest 0}

Name:		%{sname}_%{pgmajorversion}
Version:	5.0.0
Release:	2PGDG%{?dist}
Summary:	A table update logger for PostgreSQL
License:	GPLv2
URL:		https://github.com/dalibo/%{pname}/
Source0:	https://github.com/dalibo/%{pname}/archive/refs/tags/v%{version}.tar.gz
Source1:	%{pname}-check.sh

BuildArch:	noarch
Requires:	postgresql%{pgmajorversion}-contrib
%if %runselftest
# Upstream's expected output for PostgreSQL 17 is older than the release
%if %{pgmajorversion} != 17
BuildRequires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-contrib
BuildRequires:	pgdg-srpm-macros >= 2.0.0
# The client test runs the perl clients of client/
BuildRequires:	perl(DBI) perl(DBD::Pg) perl(Time::HiRes)
%endif
%endif

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
%{__install} -d %{buildroot}%{pginstdir}/share/extension/ %{buildroot}%{pginstdir}/share/%{pname}/
# emaj.control sets "directory = 'emaj'", so PostgreSQL looks for the SQL
# scripts in share/emaj, as upstream installs them:
%{__cp} -r sql/* %{buildroot}%{pginstdir}/share/%{pname}/
%{__cp} %{pname}.control %{buildroot}%{pginstdir}/share/extension

%check
%if %runselftest
%if %{pgmajorversion} != 17
# The regression tests of upstream's tools/regress.sh, see emaj-check.sh
%pgdg_check_init
PGDG_PGMAJORVERSION=%{pgmajorversion}
PGDG_EMAJ_VERSION=%{version}
. %{SOURCE1}
%endif
%endif

%files
%defattr(-,root,root,-)
%license LICENSE
%doc CHANGES.md docs README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/%{pname}/

%changelog
* Tue Oct 13 2026 Devrim Gunduz <devrim@gunduz.org> - 5.0.0-2PGDG
- Install the SQL scripts into share/emaj, where emaj.control ("directory =
  'emaj'") makes PostgreSQL look for them, as upstream does. They were in
  share/extension, so CREATE EXTENSION emaj failed, and so did every query of
  pg_available_extension_versions on servers with this package installed.
- Add %%check, running the standard regression test scenario of upstream's
  tools/regress.sh (including the tests of the perl clients) with the
  %%check helpers from pgdg-srpm-macros 2.0.0, in emaj-check.sh. It is
  disabled by default; enable it with --define 'runselftest 1'. Not on
  PostgreSQL 17: upstream's expected output for it is older than 5.0.0.

* Sun Jul 26 2026 Devrim Gündüz <devrim@gunduz.org> - 5.0.0-1PGDG
- Update to 5.0.0

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
