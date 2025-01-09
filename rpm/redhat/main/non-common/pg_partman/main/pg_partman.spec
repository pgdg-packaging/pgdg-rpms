%global sname pg_partman

%{!?llvm:%global llvm 1}

Summary:	A PostgreSQL extension to manage partitioned tables by time or ID

Name:		%{sname}_%{pgmajorversion}
Version:	5.2.4
Release:	2PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/pgpartman/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/pgpartman/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
Requires:	python3-psycopg2

Obsoletes:	%{sname}%{pgmajorversion} < 4.4.0-2

%description
pg_partman is an extension to create and manage both time-based and
number-based table partition sets.

The declarative partitioning built into PostgreSQL provides the commands to
create a partitioned table and its children. pg_partman uses the built-in
declarative features that PostgreSQL provides and builds upon those with
additional features and enhancements to make managing partitions easier.
One key way that pg_partman extends partitioning in Postgres is by providing
a means to automate the child table maintenance over time (Ex. adding new
children, dropping old ones based on a retention policy). pg_partman also
has features to turn an existing table into a partitioned table or vice versa.

A background worker (BGW) process is included to automatically run partition
maintenance without the need of an external scheduler (cron, etc) in most
cases.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_partman
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 17.0 clang-devel >= 17.0
Requires:	llvm => 17.0
%endif

%description llvmjit
This packages provides JIT support for pg_partman
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
# Change Python path in the scripts:
find . -iname "*.py" -exec sed -i "s/\/usr\/bin\/env python/\/usr\/bin\/python3/g" {} \;

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/%{sname}.md
%{pginstdir}/lib/%{sname}_bgw.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/doc/extension/fix_missing_procedures.md
%{pginstdir}/doc/extension/migrate_to_declarative.md
%{pginstdir}/doc/extension/migrate_to_partman.md
%{pginstdir}/doc/extension/pg_partman_*_upgrade.md
%{pginstdir}/doc/extension/pg_partman_howto.md
%attr(755, root, -) %{pginstdir}/bin/check_unique_constraint.py
%attr(755, root, -) %{pginstdir}/bin/dump_partition.py
%attr(755, root, -) %{pginstdir}/bin/vacuum_maintenance.py

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/src/pg_partman_bgw.index.bc
   %{pginstdir}/lib/bitcode/src/pg_partman_bgw/src/pg_partman_bgw.bc
%endif

%changelog
* Thu Jan 9 2025 Devrim Gündüz <devrim@gunduz.org> - 5.2.4-2PGDG
- Update description

* Thu Jan 2 2025 Devrim Gündüz <devrim@gunduz.org> - 5.2.4-1PGDG
- Update to 5.2.4 per changes described at:
  https://github.com/pgpartman/pg_partman/releases/tag/v5.2.4

* Tue Dec 31 2024 Devrim Gündüz <devrim@gunduz.org> - 5.2.3-1PGDG
- Update to 5.2.3 per changes described at:
  https://github.com/pgpartman/pg_partman/releases/tag/v5.2.3

* Wed Dec 11 2024 Devrim Gündüz <devrim@gunduz.org> - 5.2.2-1PGDG
- Update to 5.2.2 per changes described at:
  https://github.com/pgpartman/pg_partman/releases/tag/v5.2.2

* Tue Dec 3 2024 Devrim Gündüz <devrim@gunduz.org> - 5.2.1-1PGDG
- Update to 5.2.1 per changes described at:
  https://github.com/pgpartman/pg_partman/releases/tag/v5.2.1

* Sat Nov 23 2024 Devrim Gündüz <devrim@gunduz.org> - 5.2.0-1PGDG
- Update to 5.2.0 per changes described at:
  https://github.com/pgpartman/pg_partman/releases/tag/v5.2.0
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 5.1.0-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Sun Apr 7 2024 Devrim Gündüz <devrim@gunduz.org> - 5.1.0-1PGDG
- Update to 5.1.0 per changes described at:
  https://github.com/pgpartman/pg_partman/releases/tag/v5.1.0

* Mon Jan 22 2024 Devrim Gündüz <devrim@gunduz.org> - 5.0.1-1PGDG
- Update to 5.0.1 per changes described at:
  https://github.com/pgpartman/pg_partman/releases/tag/v5.0.1

* Wed Oct 18 2023 Devrim Gündüz <devrim@gunduz.org> - 5.0.0-1PGDG
- Update to 5.0.0

* Thu Sep 14 2023 Devrim Gündüz <devrim@gunduz.org> - 4.7.4-1PGDG
- Update to 4.7.4
- Add PGDG branding
- Cleanup rpmlint warnings

* Mon Jun 05 2023 John Harvey <john.harvey@crunchydata.com> - 4.7.3-3
- Fix deprecated python script issue from f7312222dd

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org>
- Rebuild against LLVM 15 on SLES 15

* Thu May 25 2023 Devrim Gündüz <devrim@gunduz.org> - 4.7.3-2
- Remove Python 2 related portions.

* Thu Apr 6 2023 Devrim Gündüz <devrim@gunduz.org> - 4.7.3-1
- Update to 4.7.3

* Wed Dec 21 2022 John Harvey <john.harvey@crunchydata.com> - 4.7.2-1
- Update to 4.7.2

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 4.7.1-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue Oct 18 2022 John Harvey <john.harvey@crunchydata.com> - 4.7.1-1
- Update to 4.7.1

* Thu Sep 22 2022 John Harvey <john.harvey@crunchydata.com> - 4.7.0-2
- SUSE should use python3 by default

* Tue Aug 9 2022 John Harvey <john.harvey@crunchydata.com> - 4.7.0-1
- Update to 4.7.0

* Thu May 19 2022 Devrim Gündüz <devrim@gunduz.org> - 4.6.2-1
- Update to 4.6.2

* Mon Apr 18 2022 Devrim Gündüz <devrim@gunduz.org> - 4.6.1-1
- Update to 4.6.1

* Wed Oct 13 2021 Devrim Gündüz <devrim@gunduz.org> - 4.6.0-1
- Update to 4.6.0

* Fri May 21 2021 Devrim Gündüz <devrim@gunduz.org> - 4.5.1-2
- Remove pgxs patches, and export PATH instead.

* Fri May 21 2021 Devrim Gündüz <devrim@gunduz.org> - 4.5.1-1
- Update to 4.5.1

* Wed Apr 14 2021 John Harvey <john.harvey@crunchydata.com> - 4.5.0-1
- Update to 4.5.0

* Thu Jan 21 2021 Devrim Gündüz <devrim@gunduz.org> - 4.4.1-1
- Update to 4.4.1

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 4.4.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Wed May 13 2020 Devrim Gündüz <devrim@gunduz.org> - 4.4.0-1
- Update to 4.4.0

* Wed Mar 11 2020 Devrim Gündüz <devrim@gunduz.org> - 4.3.0-1
- Update to 4.3.0
- Switch to PY3 on RHEL 7

* Fri Nov 1 2019 Devrim Gündüz <devrim@gunduz.org> - 4.2.2-2
- Depend on python3-psycopg2 on RHEL >= 7, and Fedora. Use python-psycopg2
  on RHEL 6.

* Fri Oct 25 2019 Devrim Gündüz <devrim@gunduz.org> - 4.2.2-1
- Update to 4.2.2

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Thu Aug 22 2019 Devrim Gündüz <devrim@gunduz.org> - 4.2.0-1
- Update to 4.2.0

* Thu Apr 25 2019 Devrim Gündüz <devrim@gunduz.org> - 4.1.0-1
- Update to 4.1.0
- Fix Python paths.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 4.0.0-1.1
- Rebuild against PostgreSQL 11.0

* Mon Oct 15 2018 - John K. Harvey <john.harvey@crunchydata.com> 4.0.0-1
- Update to 4.0.0

* Fri Jul 27 2018 - Devrim Gündüz <devrim@gunduz.org> 3.2.1-1
- Update to 3.2.1, per #3519

* Sat Jul 14 2018 - Devrim Gündüz <devrim@gunduz.org> 3.2.0-1
- Update to 3.2.0

* Tue Apr 24 2018 - Devrim Gündüz <devrim@gunduz.org> 3.1.3-1
- Update to 3.1.3

* Sun Feb 4 2018 - Devrim Gündüz <devrim@gunduz.org> 3.1.2-1
- Update to 3.1.2

* Fri Jan 12 2018 - Devrim Gündüz <devrim@gunduz.org> 3.1.1-1
- Update to 3.1.1

* Thu Oct 5 2017 - Devrim Gündüz <devrim@gunduz.org> 3.1.0-1
- Update to 3.1.0

* Fri Jun 2 2017 - Devrim Gündüz <devrim@gunduz.org> 3.0.1-1
- Update to 3.0.1

* Sat Dec 3 2016 - Devrim Gündüz <devrim@gunduz.org> 2.6.2-1
- Update to 2.6.2

* Mon Oct 24 2016 - Devrim Gündüz <devrim@gunduz.org> 2.6.1-1
- Update to 2.6.1

* Wed Aug 31 2016 - Devrim Gündüz <devrim@gunduz.org> 2.6.0-1
- Update to 2.6.0

* Mon Jul 4 2016 - Devrim Gündüz <devrim@gunduz.org> 2.4.1-1
- Update to 2.4.1

* Thu Mar 3 2016 - Devrim Gündüz <devrim@gunduz.org> 2.2.3-1
- Update to 2.2.3

* Mon Jan 4 2016 - Devrim Gündüz <devrim@gunduz.org> 2.2.2-1
- Update to 2.2.2

* Fri Sep 25 2015 - Devrim Gündüz <devrim@gunduz.org> 2.1.0-1
- Update to 2.1.0

* Tue Jun 16 2015 - Devrim Gündüz <devrim@gunduz.org> 2.0.0-1
- Update to 2.0.0

* Wed Feb 25 2015 - Devrim Gündüz <devrim@gunduz.org> 1.8.0-1
- Update to 1.8.0
- Remove executable bit from docs

* Wed Jun 18 2014 - Devrim Gündüz <devrim@gunduz.org> 1.7.2-1
- Update to 1.7.2

* Tue Apr 29 2014 - Devrim Gündüz <devrim@gunduz.org> 1.7.0-1
- Update to 1.7.0

* Thu Mar 6 2014 - Devrim Gündüz <devrim@gunduz.org> 1.6.1-1
- Update to 1.6.1

* Sat Feb 15 2014 - Devrim Gündüz <devrim@gunduz.org> 1.6.0-1
- Update to 1.6.0

* Wed Jan 15 2014 - Devrim Gündüz <devrim@gunduz.org> 1.5.1-1
- Update to 1.5.1

* Thu Oct 31 2013 - Devrim Gündüz <devrim@gunduz.org> 1.4.3-1
- Initial RPM packaging for PostgreSQL RPM Repository
