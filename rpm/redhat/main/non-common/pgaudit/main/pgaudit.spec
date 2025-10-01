%global sname	pgaudit

%if %{pgmajorversion} == 15
%global pgauditversion 17
%global pversion 1.7.1
%endif
%if %{pgmajorversion} == 14
%global pgauditversion 16
%global pversion 1.6.3
%endif
%if %{pgmajorversion} == 13
%global pgauditversion 15
%global pversion 1.5.3
%endif

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL Audit Extension
Name:		%{sname}%{pgauditversion}_%{pgmajorversion}
Version:	%{pversion}
Release:	1PGDG%{?dist}
License:	BSD
Source0:	https://github.com/%{sname}/%{sname}/archive/refs/tags/%{version}.tar.gz
URL:		https://www.pgaudit.org
BuildRequires:	postgresql%{pgmajorversion}-devel postgresql%{pgmajorversion}
BuildRequires:	openssl-devel krb5-devel
Requires:	postgresql%{pgmajorversion}-server

%description
The PostgreSQL Audit extension (pgaudit) provides detailed session
and/or object audit logging via the standard PostgreSQL logging
facility.

The goal of the PostgreSQL Audit extension (pgaudit) is to provide
PostgreSQL users with capability to produce audit logs often required to
comply with government, financial, or ISO certifications.

An audit is an official inspection of an individual's or organization's
accounts, typically by an independent body. The information gathered by
the PostgreSQL Audit extension (pgaudit) is properly called an audit
trail or audit log. The term audit log is used in this documentation.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgaudit
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
This package provides JIT support for pgaudit
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/pgaudit--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Mon Mar 3 2025 Devrim Gunduz <devrim@gunduz.org> - %{pversion}-1PGDG
- Update to 1.7.1, 1.6.3 and 1.5.3 per changes described at:
  https://github.com/pgaudit/pgaudit/releases/tag/1.7.1
  https://github.com/pgaudit/pgaudit/releases/tag/1.6.3
  https://github.com/pgaudit/pgaudit/releases/tag/1.5.3

* Tue Feb 25 2025 Devrim Gunduz <devrim@gunduz.org> - %{pversion}-8PGDG
- Add missing BRs

* Fri Feb 21 2025 Devrim Gunduz <devrim@gunduz.org> - %{pversion}-7PGDG
- Update LLVM dependencies
- Remove redundant BR

* Mon Jul 29 2024 Devrim Gunduz <devrim@gunduz.org> - %{pversion}-6PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Tue Jul 9 2024 Devrim Gunduz <devrim@gunduz.org> - %{pversion}-5PGDG
- Fix builds on RHEL 8. Per report from Christoph Berg.

* Thu Feb 22 2024 Devrim Gunduz <devrim@gunduz.org> - %{pversion}-4PGDG
- Cleanup an rpmlint warning

* Mon Jul 31 2023 Devrim Gunduz <devrim@gunduz.org> - %{pversion}-3PGDG
- Unify spec file for all pgaudit versions
- Add PGDG branding
- Clean up rpmlint warnings
