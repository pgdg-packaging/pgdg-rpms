%global sname pg_statement_rollback

%{!?llvm:%global llvm 1}

Summary:	Server side rollback at statement level for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.5
Release:	2PGDG%{?dist}
License:	ISC
Source0:	https://github.com/lzlabs/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/lzlabs/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
pg_statement_rollback is a PostgreSQL extension to add server side
transaction with rollback at statement level like in Oracle or DB2.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_statement_rollback
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for pg_statement_rollback
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension/
# Install documentation with a better name:
%{__mv} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} %{buildroot}%{pginstdir}/doc/contrib/README.md

%files
%defattr(644,root,root,755)
%{pginstdir}/lib/%{sname}.so
%doc %{pginstdir}/doc/extension/README-%{sname}.md

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.5-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Mon Sep 29 2025 Devrim Gündüz <devrim@gunduz.org> - 1.5-1PGDG
- Update to 1.5 per changes described at:
  https://github.com/lzlabs/pg_statement_rollback/releases/tag/v1.5

* Mon Jan 13 2025 Devrim Gündüz <devrim@gunduz.org> - 1.4-4PGDG
- Update LLVM dependencies and fix license.

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.4-3PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Mon Sep 11 2023 Devrim Gündüz <devrim@gunduz.org> - 1.4-2PGDG
- Add PGDG branding
- Cleanup rpmlint warnings

* Sun Jun 4 2023 Devrim Gündüz <devrim@gunduz.org> - 1.4-1
- Update to 1.4

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.3-2.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.3-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon Oct 25 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3-1
- Update to 1.3

* Mon Jun 7 2021 Devrim Gündüz <devrim@gunduz.org> - 1.2-1
- Update to 1.2

* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> - 1.1-2
- Remove pgxs patches, and export PATH instead.

* Thu Nov 12 2020 Devrim Gündüz <devrim@gunduz.org> - 1.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
