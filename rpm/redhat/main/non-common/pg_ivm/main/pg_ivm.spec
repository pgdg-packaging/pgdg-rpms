%global sname	pg_ivm

%{!?llvm:%global llvm 1}

Summary:	Incremental View Maintenance (IVM) feature for PostgreSQL.
Name:		%{sname}_%{pgmajorversion}
Version:	1.12
Release:	1PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/sraoss/%{sname}/
Source0:	https://github.com/sraoss/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
Incremental View Maintenance (IVM) is a way to make materialized views
up-to-date in which only incremental changes are computed and applied on
views rather than recomputing the contents from scratch as REFRESH
MATERIALIZED VIEW does. IVM can update materialized views more efficiently
than recomputation when only small parts of the view are changed.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_ivm
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
This package provides JIT support for pg_ivm
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} INSTALL_PREFIX=%{buildroot} DESTDIR=%{buildroot} install

%files
%defattr(-,root,root,-)
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Thu Sep 4 2025 Devrim Gündüz <devrim@gunduz.org> - 1.12-1PGDG
- Update to 1.12 per changes described at:
  https://github.com/sraoss/pg_ivm/releases/tag/v1.12

* Mon May 26 2025 Devrim Gündüz <devrim@gunduz.org> - 1.11-1PGDG
- Update to 1.11 per changes described at:
  https://github.com/sraoss/pg_ivm/releases/tag/v1.11

* Wed Mar 12 2025 Devrim Gündüz <devrim@gunduz.org> - 1.10-1PGDG
- Update to 1.10 per changes described at:
  https://github.com/sraoss/pg_ivm/releases/tag/v1.10

* Thu Jan 9 2025 Devrim Gündüz <devrim@gunduz.org> - 1.9-2PGDG
- Update LLVM dependencies

* Tue Aug 6 2024 Devrim Gündüz <devrim@gunduz.org> - 1.9-1PGDG
- Update to 1.9 per changes described at:
  https://github.com/sraoss/pg_ivm/releases/tag/v1.9

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.8-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Sun Mar 3 2024 Devrim Gündüz <devrim@gunduz.org> - 1.8-1PGDG
- Update to 1.8 per changes described at:
  https://github.com/sraoss/pg_ivm/releases/tag/v1.8

* Fri Feb 23 2024 Devrim Gündüz <devrim@gunduz.org> - 1.7-2PGDG
- Add missing BR and Requires
- Enable -debug* subpackages

* Wed Sep 13 2023 Devrim Gündüz <devrim@gunduz.org> - 1.7-1PGDG
- Update to 1.7

* Mon Sep 4 2023 Devrim Gündüz <devrim@gunduz.org> - 1.6-1PGDG
- Update to 1.6
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.5.1-1.1
- Rebuild against LLVM 15 on SLES 15

* Thu Mar 2 2023 Devrim Gündüz <devrim@gunduz.org> - 1.5.1-1
- Update to 1.5.1

* Tue Feb 7 2023 Devrim Gündüz <devrim@gunduz.org> - 1.5-1
- Update to 1.5

* Tue Dec 20 2022 Devrim Gündüz <devrim@gunduz.org> - 1.4-1
- Update to 1.4

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.3-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon Oct 3 2022 Devrim Gündüz <devrim@gunduz.org> - 1.3-1
- Update to 1.3

* Mon Aug 8 2022 Devrim Gündüz <devrim@gunduz.org> - 1.2-1
- Update to 1.2

* Fri Jun 24 2022 Devrim Gündüz <devrim@gunduz.org> - 1.1-1
- Update to 1.1

* Wed May 11 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Update to 1.0

* Fri May 6 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0-alpha-1
- Initial RPM packaging for the PostgreSQL RPM Repository.
