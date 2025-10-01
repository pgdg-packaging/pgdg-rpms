%global sname	pgaudit

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL Audit Extension
Name:		%{sname}_%{pgmajorversion}
Version:	17.1
Release:	1PGDG%{?dist}
License:	BSD
Source0:	https://github.com/pgaudit/pgaudit/archive/refs/tags/%{version}.tar.gz
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

* Mon Mar 3 2025 Devrim Gündüz <devrim@gunduz.org> - 17.1-1PGDG
- Update to 17.1 per changes described at:
  https://github.com/pgaudit/pgaudit/releases/tag/17.1

* Tue Feb 25 2025 Devrim Gündüz <devrim@gunduz.org> - 17.0-3PGDG
- Add missing BRs

* Fri Feb 21 2025 Devrim Gündüz <devrim@gunduz.org> - 17.0-2PGDG
- Update LLVM dependencies

* Sun Sep 8 2024 Devrim Gündüz <devrim@gunduz.org> - 17.0-1PGDG
- Update to 17.0 per changes described at
  https://github.com/pgaudit/pgaudit/releases/tag/17.0

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 17beta1-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Fri Jul 12 2024 Devrim Gunduz <devrim@gunduz.org> - 17beta1-1PGDG
- Initial packaging for pgAudit 17 & PostgreSQL 17
