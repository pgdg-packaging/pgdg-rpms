%global sname pg_qualstats

%{!?llvm:%global llvm 1}

Summary:	A PostgreSQL extension collecting statistics about predicates
Name:		%{sname}_%{pgmajorversion}
Version:	2.1.3
Release:	1PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/powa-team/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/powa-team/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
pg_qualstats is a PostgreSQL extension keeping statistics on
predicates found in WHERE statements and JOIN clauses.

This is useful if you want to be able to analyze what are
the most-often executed quals (predicates) on your database.
The powa project makes use of this to provide index
suggestions.

It also allows you to identify correlated columns, by
identifying which columns are most frequently queried
together.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_qualstats
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} == 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?suse_version} == 1600
BuildRequires:	llvm19-devel clang19-devel
Requires:	llvm19
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for pg_qualstats
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file.
%{__install} -d %{buildroot}%{pginstdir}/doc/extension/
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Wed Oct 15 2025 Devrim Gündüz <devrim@gunduz.org> - 2.1.3-1PGDG
- Update to 2.1.3 per changes described at:
  https://github.com/powa-team/pg_qualstats/releases/tag/2.1.3

* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 2.1.2-3PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 2.1.2-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Thu Jul 10 2025 Devrim Gündüz <devrim@gunduz.org> - 2.1.2-1PGDG
- Update to 2.1.2

* Fri Feb 21 2025 Devrim Gündüz <devrim@gunduz.org> - 2.1.1-2PGDG
- Update LLVM dependencies
- Remove redundant BR

* Thu Sep 26 2024 Devrim Gündüz <devrim@gunduz.org> - 2.1.1-1PGDG
- Update to 2.1.1

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Tue Sep 19 2023 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-1PGDG
- Update to 2.1.0

* Fri Sep 8 2023 Devrim Gunduz <devrim@gunduz.org> - 2.0.4-3PGDG
- Add PGDG branding
- Cleanup rpmlint warnings

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 2.0.4-2.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.0.4-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue May 17 2022 Devrim Gündüz <devrim@gunduz.org> - 2.0.4-1
- Update to 2.0.4

* Mon Jun 7 2021 Devrim Gündüz <devrim@gunduz.org> - 2.0.3-1
- Update to 2.0.3

* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> - 2.0.2-3
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.2-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu May 28 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.2-1
- Update to 2.0.2

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-1
- Update to 2.0.1

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-1
- Update to 2.0.0
- Require pgdg-srpm-macros

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0.9-1.1
- Rebuild for PostgreSQL 12

* Fri Sep 6 2019 - Devrim Gündüz <devrim@gunduz.org> - 1.0.9-1
- Update to 1.0.9

* Wed Nov 21 2018 - Devrim Gündüz <devrim@gunduz.org> - 1.0.7-1
- Update to 1.0.7

* Fri Nov 9 2018 - Devrim Gündüz <devrim@gunduz.org> - 1.0.6-1
- Update to 1.0.6

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Fri Aug 10 2018 - Devrim Gündüz <devrim@gunduz.org> - 1.0.5-2
- Ignore .bc files on PPC arch.

* Sun Aug 5 2018 - Devrim Gündüz <devrim@gunduz.org> - 1.0.5-1
- Update to 1.0.5
- Add PG 11 RPM support

* Sun Apr 15 2018 - Devrim Gündüz <devrim@gunduz.org> - 1.0.4-1
- Update to 1.0.4
- Update URLs again.

* Sat Nov 18 2017 - Devrim Gündüz <devrim@gunduz.org> - 1.0.3-1
- Update to 1.0.3, per #2883.
- Update URLs

* Mon Oct 24 2016 - Devrim Gündüz <devrim@gunduz.org> - 1.0.2-1
- Update to 1.0.2

* Wed Sep 7 2016 - Devrim Gündüz <devrim@gunduz.org> - 1.0.1-1
- Update to 1.0.1
- Add LICENSE file
- Update %%description

* Sun Mar 6 2016 - Devrim Gündüz <devrim@gunduz.org> 0.0.9-1
- Update to 0.0.9

* Mon Jan 4 2016 - Devrim Gündüz <devrim@gunduz.org> 0.0.7-1
- Update to 0.0.7
- Update for 9.5 doc layout.

* Thu Sep 10 2015 - Devrim Gündüz <devrim@gunduz.org> 0.0.6-1
- Update to 0.0.6

* Tue Mar 17 2015 - Devrim Gündüz <devrim@gunduz.org> 0.0.4-1
- Initial RPM packaging for PostgreSQL RPM Repository
