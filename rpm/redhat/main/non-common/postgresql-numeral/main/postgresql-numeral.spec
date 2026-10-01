%global sname postgresql-numeral

%{!?llvm:%global llvm 1}
%{!?runselftest:%global runselftest 0}

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

Summary:	Numeric data types for PostgreSQL that use numerals
Name:		%{sname}_%{pgmajorversion}
Version:	1.3
Release:	8PGDG%{?dist}
License:	BSD
Source0:	https://github.com/df7cb/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/df7cb//%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel bison flex
Requires:	postgresql%{pgmajorversion}-server
%if %runselftest
BuildRequires:	postgresql%{pgmajorversion}-server pgdg-srpm-macros >= 2.0.0
%endif

%description
postgresql-numeral provides numeric data types for PostgreSQL that use
numerals (words instead of digits) for input and output. Data types:
 - numeral: English numerals (one, two, three, four, ...), short scale (10⁹ = billion)
 - zahl: German numerals (eins, zwei, drei, vier, ...), long scale (10⁹ = Milliarde)
 - roman: Roman numerals (I, II, III, IV, ...)

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for postgresql-numeral
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
This package provides JIT support for postgresql-numeral
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
# No parallel build: the bitcode of the lexers can be compiled before bison
# generated the parser headers they include.
# The Makefile greps SIZEOF_VOID_P from pg_config.h to decide whether the
# types are passed by value, but that is the multilib wrapper header on some
# distros, so the types were created without passedbyvalue, and CREATE
# EXTENSION failed. All our platforms are 64-bit, so set it here.
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} PASSEDBYVALUE="passedbyvalue,"

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} PASSEDBYVALUE="passedbyvalue," install DESTDIR=%{buildroot}
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%check
%if %runselftest
# The tests need a UTF8 database: without a locale the cluster would be
# SQL_ASCII.
export LC_ALL=C.UTF-8
%pgdg_check_installcheck %{with_llvm_arg}
%endif

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/numeral.so
%{pginstdir}/share/extension/numeral--*.sql
%{pginstdir}/share/extension/numeral.control

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/numeral*.bc
    %{pginstdir}/lib/bitcode/numeral/*.bc
%endif

%changelog
* Tue Sep 29 2026 Devrim Gunduz <devrim@gunduz.org> - 1.3-8PGDG
- Add %%check, running the regression tests with the %%check helpers
  from pgdg-srpm-macros 2.0.0. It is disabled by default; enable it
  with --define 'runselftest 1'.
- Fix CREATE EXTENSION on distros where pg_config.h is the multilib
  wrapper: the types were created without passedbyvalue, so the casts
  to bigint failed with "source and target data types are not physically
  compatible". Also build without parallel make, which failed randomly.

* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - 1.3-7PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51

* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 1.3-6PGDG
- Add Amazon Linux 2023 support.

* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 1.3-5PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.3-4PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Wed Feb 26 2025 - Devrim Gündüz <devrim@gunduz.org> 1.3-3PGDG
- Add missing BRs

* Mon Jan 27 2025 - Devrim Gündüz <devrim@gunduz.org> 1.3-2PGDG
- Update LLVM dependencies

* Mon Sep 30 2024 - Devrim Gündüz <devrim@gunduz.org> 1.3-1PGDG
- Initial RPM packaging for PostgreSQL YUM Repository
