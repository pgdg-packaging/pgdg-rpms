%global sname plsh

%{!?llvm:%global llvm 1}

Summary:	Sh shell procedural language handler for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.20220917
Release:	7PGDG%{?dist}
License:	BSD
Source0:	https://github.com/petere/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/petere/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 1.20200522-2

%description
PL/sh is a procedural language handler for PostgreSQL that
allows you to write stored procedures in a shell of your choice.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for plsh
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
This packages provides JIT support for plsh
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)

%{pginstdir}/lib/%{sname}.so
%doc NEWS README.md
%license COPYING
%{pginstdir}/share/extension/%{sname}--1--2.sql
%{pginstdir}/share/extension/%{sname}--2.sql
%{pginstdir}/share/extension/%{sname}--unpackaged--1.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Fri Jan 10 2025 Devrim Gunduz <devrim@gunduz.org> - 1.20220917-7PGDG
- Update LLVM dependencies

* Tue Jul 30 2024 Devrim Gunduz <devrim@gunduz.org> - 1.20220917-6PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Fri Feb 23 2024 Devrim Gunduz <devrim@gunduz.org> - 1.20220917-5PGDG
- Cleanup rpmlint warning

* Mon Aug 21 2023 Devrim Gunduz <devrim@gunduz.org> - 1.20220917-4PGDG
- Remove RHEL 6 bits

* Sun Jul 23 2023 Devrim Gunduz <devrim@gunduz.org> - 1.20220917-3PGDG
- Cleanup rpmlint warnings
- Add PGDG branding.

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.20220917-2.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.20220917-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu Sep 29 2022 Devrim Gündüz <devrim@gunduz.org> - 1.20220917-1
- Update to 1.20220917
- Update llvm code

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.20200522-3
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.20200522-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Wed Aug 12 2020 Devrim Gündüz <devrim@gunduz.org> - 1.20200522-1
- Update to 1.20200522

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Sun Jan 20 2019 Devrim Gündüz <devrim@gunduz.org> - 1.20171014-1.2
- Fix PostgreSQL 11 builds

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.20171014-1.1
- Rebuild against PostgreSQL 11.0

* Tue Mar 27 2018 - Devrim Gündüz <devrim@gunduz.org> 1.20171014
- Update to 1.20171014

* Tue Jan 26 2016 - Devrim Gündüz <devrim@gunduz.org> 1.20130823-2
- Cosmetic cleanup
- Use more macros for unified spec file

* Mon Mar 17 2014 - Devrim Gündüz <devrim@gunduz.org> 1.20130823-1
- Update to 1.20130823
- Update download URL

* Tue Nov 27 2012 - Devrim Gündüz <devrim@gunduz.org> 1.20121018-1
- Rewrite the spec file based on the new version, and update
  to 1.20121018

* Sun Jan 20 2008 - Devrim Gündüz <devrim@gunduz.org> 1.3-2
- Move .so file to the correct directory

* Tue Jan 15 2008 - Devrim Gündüz <devrim@gunduz.org> 1.3-1
- Initial RPM packaging for Fedora
