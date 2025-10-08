%global sname pg_stat_kcache

%global kcachemajver 2
%global kcachemidver 3
%global kcacheminver 1

%{!?llvm:%global llvm 1}

Summary:	A PostgreSQL extension gathering CPU and disk acess statistics
Name:		%{sname}_%{pgmajorversion}
Version:	%{kcachemajver}.%{kcachemidver}.%{kcacheminver}
Release:	3PGDG%{?dist}
License:	BSD
URL:		https://github.com/powa-team/%{sname}
Source0:	https://github.com/powa-team/%{sname}/archive/REL%{kcachemajver}_%{kcachemidver}_%{kcacheminver}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-contrib

%description
Gathers statistics about real reads and writes done by the filesystem layer.
Requires pg_stat_statements extension to be installed.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_stat_kcache
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
This package provides JIT support for pg_stat_kcache
%endif

%prep
%setup -q -n %{sname}-REL%{kcachemajver}_%{kcachemidver}_%{kcacheminver}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README
%{__install} -d %{buildroot}%{pginstdir}/doc/extension/
%{__install} README.rst %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.rst

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.rst
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
 %{pginstdir}/lib/bitcode/%{sname}*.bc
 %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 2.3.1-3PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 2.3.1-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Sat Sep 27 2025 Devrim Gündüz <devrim@gunduz.org> - 2.3.1-1PGDG
- Update to 2.3.1 per changes described at:
  https://github.com/powa-team/pg_stat_kcache/releases/tag/REL2_3_1

* Tue Jan 14 2025 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-2PGDG
- Add missing -contrib requirement
- Simplify package description
- Update LLVM dependencies

* Tue Sep 17 2024 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-1PGDG
- Update to 2.3.0 per changes described at:
  https://github.com/powa-team/pg_stat_kcache/releases/tag/REL2_3_0

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 2.2.3-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Thu Jan 25 2024 Devrim Gunduz <devrim@gunduz.org> - 2.2.3-1PGDG
- Update to 2.2.3

* Thu Aug 3 2023 Devrim Gunduz <devrim@gunduz.org> - 2.2.2-1PGDG
- Update to 2.2.2
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 2.2.1-3.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon Aug 22 2022 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-1
- Update to 2.2.1

* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> - 2.2.0-2
- Remove pgxs patches, and export PATH instead.

* Sun Dec 13 2020 Devrim Gündüz <devrim@gunduz.org> - 2.2.0-1
- Update to 2.2.0

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.1.3-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Jul 9 2020 Devrim Gündüz <devrim@gunduz.org> - 2.1.3-1
- Update to 2.1.3

* Thu Jul 9 2020 Devrim Gündüz <devrim@gunduz.org> - 2.1.2-1
- Update to 2.1.2

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Wed Aug 1 2018 - Devrim Gündüz <devrim@gunduz.org> 2.1.1-1
- Update 2.1.1

* Thu Jul 26 2018 - Devrim Gündüz <devrim@gunduz.org> 2.1.0-1
- Update 2.1.0

* Sun Apr 15 2018 - Devrim Gündüz <devrim@gunduz.org> 2.0.3-2
- Update to new URL, and use macros for version numberto avoid issues.

* Wed Oct 12 2016 - Devrim Gündüz <devrim@gunduz.org> 2.0.3-1
- Update to 2.0.3

* Fri Mar 27 2015 - Devrim Gündüz <devrim@gunduz.org> 2.0.2-1
- Update to 2.0.2

* Tue Mar 17 2015 - Devrim Gündüz <devrim@gunduz.org> 2.0.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
