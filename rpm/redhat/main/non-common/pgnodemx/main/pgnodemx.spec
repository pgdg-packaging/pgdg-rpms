%global sname pgnodemx

%{!?llvm:%global llvm 1}

# Propagate %%llvm into the actual build: PGXS decides whether to invoke
# clang/llvm-config based on with_llvm from the installed postgresql*-devel's
# Makefile.global, not from this spec's %%llvm. Without passing with_llvm=no
# through to make, setting %%llvm 0 here only drops the llvm BuildRequires/
# subpackage/files, while the build still tries to run clang regardless.
%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif


Summary:	SQL functions that allow capture of node OS metrics from PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.7
Release:	5PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/CrunchyData/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/CrunchyData/%{sname}

BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-contrib

%description
pgnodemx includes SQL functions that allow capture of node OS metrics from
PostgreSQL.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgnodemx
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} == 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?suse_version} == 1600
BuildRequires:	llvm19-devel clang19-devel
Requires:	llvm19
%endif
%if 0%{?amzn}
BuildRequires:	llvm-devel >= 15.0 clang-devel >= 15.0
Requires:	llvm >= 15.0
%endif
%if ( 0%{?fedora} || 0%{?rhel} >= 8 ) && !0%{?amzn}
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for pgnodemx
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} %{with_llvm_arg} install
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%defattr(644,root,root,755)
%license LICENSE.md
%doc %{pginstdir}/doc/extension/*%{sname}.md
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/pg_proctab*.sql
%{pginstdir}/share/extension/%{sname}*.control
%{pginstdir}/share/extension/pg_proctab*.control
%{pginstdir}/lib/%{sname}*.so

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}/*bc
    %{pginstdir}/lib/bitcode/%{sname}*bc
%endif

%changelog
* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - 1.7-5PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51

* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 1.7-4PGDG
- Add Amazon Linux 2023 support.

* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 1.7-3PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.7-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Thu Jul 10 2025 Devrim Gündüz <devrim@gunduz.org> 1.7-1PGDG
- Initial packaging for PostgreSQL RPM Repository
