%global sname pg_store_plans

%{!?llvm:%global llvm 1}

Summary:	Store execution plans like pg_stat_statements does for queries
Name:		%{sname}_%{pgmajorversion}
Version:	1.8
Release:	4PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/ossc-db/%{sname}/archive/%{version}.tar.gz
Source1:	README-%{sname}.txt
URL:		https://ossc-db.github.io/%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
The pg_store_plans module provides a means for tracking execution plan
statistics of all SQL statements executed by a server.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_store_plans
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 17.0 clang-devel >= 17.0
Requires:	llvm >= 17.0
%endif

%description llvmjit
This package provides JIT support for pg_store_plans
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install
# Install documentation
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} %{SOURCE1} %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/*%{sname}.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.8-4PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Fri Jan 17 2025 Devrim Gündüz <devrim@gunduz.org> - 1.8-3PGDG
- Update LLVM dependencies
- Update project URL

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.8-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Sun Feb 25 2024 Devrim Gündüz <devrim@gunduz.org> - 1.8-1PGDG
- Update to 1.8

* Sun Jul 23 2023 Devrim Gündüz <devrim@gunduz.org> - 1.7-1PGDG
- Update to 1.7
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.6.1-2.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.6.1-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Apr 20 2022 Devrim Gündüz <devrim@gunduz.org> - 1.6.1-1
- Update to 1.6.1

* Sat Jun 5 2021 Devrim Gündüz <devrim@gunduz.org> - 1.5-1
- Update to 1.5.
- Remove pgxs patches, and export PATH instead.
- Remove RHEL 6 stuff.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.4-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Fri Mar 15 2019 Devrim Gündüz <devrim@gunduz.org> - 1.3-1
- Initial packaging for PostgreSQL RPM Repository
