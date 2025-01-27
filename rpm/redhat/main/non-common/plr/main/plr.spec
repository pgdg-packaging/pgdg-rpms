%global sname	plr

%global plrmajver 8
%global plrmidver 4
%global plrminver 7

%{!?llvm:%global llvm 1}

Summary:	Procedural language interface between PostgreSQL and R
Name:		%{sname}_%{pgmajorversion}
Version:	%{plrmajver}.%{plrmidver}.%{plrminver}
Release:	2PGDG%{?dist}
License:	GPLv2
Source0:	https://github.com/postgres-%{sname}/%{sname}/archive/REL%{plrmajver}_%{plrmidver}_%{plrminver}.tar.gz
URL:		https://github.com/postgres-%{sname}/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel R-devel
Requires:	postgresql%{pgmajorversion}-server

%description
Procedural Language Handler for the "R software environment for
statistical computing and graphics".

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for PL/R
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
This packages provides JIT support for PL/R
%endif

%prep
%setup -q -n %{sname}-REL%{plrmajver}_%{plrmidver}_%{plrminver}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot}/ install

# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__mv} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%doc changelog.md compilingplr.md userguide.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Mon Jan 27 2025 Devrim Gündüz <devrim@gunduz.org> - 8.4.7-2PGDG
- Update LLVM dependencies

* Mon Aug 12 2024 Devrim Gunduz <devrim@gunduz.org> - 8.4.7-1PGDG
- Update to 8.4.7

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 8.4.6-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Thu Aug 3 2023 Devrim Gunduz <devrim@gunduz.org> - 8.4.6-1PGDG
- Update to 8.4.6
- Add PGDG branding
- Use macros for version numbers

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 8.4.5-2.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 8.4.5-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu May 19 2022 Devrim Gündüz <devrim@gunduz.org> - 8.4.5-1
- Update to 8.4.5

* Tue Sep 21 2021 Devrim Gündüz <devrim@gunduz.org> - 8.4.3-1
- Update to 8.4.3

* Sat May 29 2021 Devrim Gündüz <devrim@gunduz.org> - 8.4.2-1
- Update to 8.4.2, per changes described at:
  https://github.com/postgres-plr/plr/blob/REL8_4_2/changelog.md
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 8.4.1-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Mon Sep 14 2020 Devrim Gündüz <devrim@gunduz.org> - 8.4.1-1
- Update to 8.4.1

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 8.4-2.1
- Rebuild for PostgreSQL 12

* Fri Jul 12 2019 Devrim Gündüz <devrim@gunduz.org> - 8.4-2
- Rebuilt, per a potential packaging issue reported by Dave Cramer.

* Tue Jun 4 2019 Devrim Gündüz <devrim@gunduz.org> - 8.4-1
- Update to 8.4
- Rename README file, so that it is consistent with many other packages.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Mon Oct 1 2018 - John K. Harvey <john.harvey@crunchydata.com> 8.3.0-18-1
- Update to 8.3.0.18
- PG11 LLVM support

* Wed Sep 28 2016 - Devrim Gündüz <devrim@gunduz.org> 8.3.0-17-1
- Update to 8.3.0.17

* Mon Feb 23 2015 - Devrim Gündüz <devrim@gunduz.org> 8.3.0-16-1
- Update to 8.3.0.16

* Sat Dec 28 2013 - Devrim Gündüz <devrim@gunduz.org> 8.3.0-15-1
- Update to 8.3.0.15

* Mon Mar 25 2013 - Devrim Gündüz <devrim@gunduz.org> 8.3.0-14-1
- Update to 8.3.0.14
- Remove patch that I added in 8.3.0.13-2, now it is upstream.

* Tue Oct 09 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 8.3.0.13-2
- Add a patch for plr extension to be installed on PostgreSQL 9.2. Per report
  from Jose Pedro Oliveira

* Tue Sep 11 2012 - Devrim Gündüz <devrim@gunduz.org> 8.3.0-13-1
- Update to 8.3.0.13

* Fri Oct 8 2010 - Devrim Gündüz <devrim@gunduz.org> 8.3.0-11-1
- Initial packaging for 9.0, which also suits new PostgreSQL RPM layout.
