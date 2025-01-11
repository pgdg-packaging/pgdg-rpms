%global sname	pg_repack

%{!?llvm:%global llvm 1}

Summary:	Reorganize tables in PostgreSQL databases without any locks
Name:		%{sname}_%{pgmajorversion}
Version:	1.5.2
Release:	2PGDG%{?dist}
License:	BSD
Source0:	https://github.com/reorg/%{sname}/archive/refs/tags/ver_%{version}.tar.gz
URL:		https://github.com/reorg/%{sname}/

BuildRequires:	postgresql%{pgmajorversion}-devel postgresql%{pgmajorversion}
Requires:	postgresql%{pgmajorversion}

Obsoletes:	%{sname}%{pgmajorversion} < 1.4.6-2

%description
pg_repack can re-organize tables on a postgres database without any locks so that
you can retrieve or update rows in tables being reorganized.
The module is developed to be a better alternative of CLUSTER and VACUUM FULL.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_repack
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
This packages provides JIT support for pg_repack
%endif

%prep
%setup -q -n %{sname}-ver_%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} install

%files
%defattr(644,root,root)
%doc COPYRIGHT doc/%{sname}.rst
%attr (755,root,root) %{pginstdir}/bin/%{sname}
%attr (755,root,root) %{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
   %{pginstdir}/lib/bitcode/%{sname}/pgut/*.bc
%endif

%changelog
* Sat 11 Jan 2025 Devrim Gündüz <devrim@gunduz.org> - 1.5.2-2PGDG
- Remove obsoleted BR

* Mon Dec 16 2024 Devrim Gündüz <devrim@gunduz.org> - 1.5.2-1PGDG
- Update to 1.5.2 per changes described at:
  https://github.com/reorg/pg_repack/releases/tag/ver_1.5.2

* Sat Sep 21 2024 Devrim Gündüz <devrim@gunduz.org> - 1.5.1-1PGDG
- Update to 1.5.1 per changes described at:
  https://github.com/reorg/pg_repack/releases/tag/ver_1.5.1

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.5.0-3PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Fri Feb 23 2024 Devrim Gunduz <devrim@gunduz.org> - 1.5.0-2PGDG
- Enable -debug* subpackages

* Thu Nov 23 2023 Devrim Gunduz <devrim@gunduz.org> - 1.5.0-1PGDG
- Update to 1.5.0

* Mon Sep 11 2023 Devrim Gunduz <devrim@gunduz.org> - 1.4.8-4PGDG
- Add PGDG branding
- Cleanup rpmlint warnings

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.4.8-3.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.4.8-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Nov 16 2022 Devrim Gündüz <devrim@gunduz.org> - 1.4.8-2
- Split LLVM subpackage to fix builds on RHEL 8 - ppc64le.

* Wed Oct 19 2022 Devrim Gündüz <devrim@gunduz.org> - 1.4.8-1
- Update to 1.4.8

* Mon Oct 4 2021 Devrim Gündüz <devrim@gunduz.org> - 1.4.7-1
- Update to 1.4.7

* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> - 1.4.6-3
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.4.6-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Fri Oct 4 2019 Devrim Gündüz <devrim@gunduz.org> - 1.4.6-1
- Update to 1.4.6

* Fri Oct 4 2019 Devrim Gündüz <devrim@gunduz.org> - 1.4.5-1
- Update to 1.4.5

* Thu Oct 18 2018 Devrim Gündüz <devrim@gunduz.org> - 1.4.4-1
- Update to 1.4.4

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.4.3-1.1
- Rebuild against PostgreSQL 11.0

* Thu May 24 2018 - Devrim Gündüz <devrim@gunduz.org> 1.4.3-1
- Update to 1.4.3

* Sat Oct 14 2017 - Devrim Gündüz <devrim@gunduz.org> 1.4.2-1
- Update to 1.4.2, per #2791

* Wed Aug 16 2017 - Devrim Gündüz <devrim@gunduz.org> 1.4.1-1
- Update to 1.4.1, per #2364

* Fri Apr 28 2017 - Devrim Gündüz <devrim@gunduz.org> 1.4.0-1
- Update to 1.4.0, per #2364

* Wed Jun 1 2016 - Devrim Gündüz <devrim@gunduz.org> 1.3.4-1
- Update to 1.3.4, per #1272

* Fri Feb 12 2016 - Devrim Gündüz <devrim@gunduz.org> 1.3.3-1
- Update to 1.3.3

* Wed Sep 9 2015 - Devrim Gündüz <devrim@gunduz.org> 1.3.2-1
- Update to 1.3.2

* Thu Mar 12 2015 - Devrim Gündüz <devrim@gunduz.org> 1.3.1-1
- Update to 1.3.1

* Tue May 20 2014 - Devrim Gündüz <devrim@gunduz.org> 1.2.1-1
- Update to 1.2.1

* Fri Mar 23 2012 - Devrim Gunduz <devrim@gunduz.org> 1.1.7-1
- Initial packaging for PostgreSQL RPM Repository, based on the
  NTT spec, simplified and modified for PostgreSQL RPM compatibility.
- Cleaned up various rpmlint errors and warnings.
