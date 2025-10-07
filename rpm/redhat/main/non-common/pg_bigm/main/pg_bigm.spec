%global pgbigmpackagever 20250903
%global pgbigmver 1.2
%global sname pg_bigm
%{!?llvm:%global llvm 1}

Summary:	2-gram (bigram) index for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	%{pgbigmver}_%{pgbigmpackagever}
Release:	3PGDG%{?dist}
URL:		https://github.com/pgbigm/%{sname}
Source0:	https://github.com/pgbigm/%{sname}/archive/refs/tags/v%{pgbigmver}-%{pgbigmpackagever}.tar.gz
License:	PostgreSQL
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
The pg_bigm module provides full text search capability in PostgreSQL.
This module allows a user to create 2-gram (bigram) index for faster
full text search.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_bigm
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
This package provides JIT support for pg_bigm
%endif

%prep
%setup -q -n %{sname}-%{pgbigmver}-%{pgbigmpackagever}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} DESTDIR=%{buildroot} install

# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/pg_bigm.so
%{pginstdir}/share/extension/pg_bigm*.sql
%{pginstdir}/share/extension/pg_bigm.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.2_20250903-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Tue Sep 2 2025 Devrim Gunduz <devrim@gunduz.org> - 1.2-20250903-1PGDG
- Update to 1.2-20250903 per changes described at:
  https://github.com/pgbigm/pg_bigm/releases/tag/v1.2-20250903

* Mon Jul 29 2024 Devrim Gunduz <devrim@gunduz.org> - 1.2-20240606-2PGDG
- Update LLVM dependencies and update license.

* Mon Jul 29 2024 Devrim Gunduz <devrim@gunduz.org> - 1.2-20240606-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Wed Jun 26 2024 Devrim Gunduz <devrim@gunduz.org> - 1.2-20240606-1PGDG
- Update to 1.2-20240606 per changes described at:
  https://github.com/pgbigm/pg_bigm/releases/tag/v1.2-20240606

* Wed Apr 3 2024 Devrim Gunduz <devrim@gunduz.org> - 1.2-20200228-1PGDG
- Initial packaging for the PostgreSQL RPM repository

