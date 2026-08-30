%global sname pg_textsearch

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

Summary:	Modern ranked text search for Postgres
Name:		%{sname}_%{pgmajorversion}
Version:	1.4.0
Release:	2PGDG%{?dist}
URL:		https://github.com/timescale/%{sname}
Source0:	https://github.com/timescale/%{sname}/archive/refs/tags/v%{version}.tar.gz
License:	PostgreSQL
BuildRequires:	postgresql%{pgmajorversion}-devel

%description
* Simple syntax: ORDER BY content <@> 'search terms'
* BM25 ranking with configurable parameters (k1, b)
* Works with Postgres text search configurations (english, french, german, etc.)
* Expression indexes for JSONB fields, multi-column search, and text transformations
* Partial indexes for scoped search and multilingual tables
* Fast top-k queries via Block-Max WAND optimization
* Parallel index builds for large tables
* Supports partitioned tables
* Best in class performance and scalability
* Display formatted contents of a PostgreSQL heap/index/control file.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_textsearch
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
This package provides JIT support for pg_textsearch
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg} DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}.index.bc
    %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
    %{pginstdir}/lib/bitcode/%{sname}/src/*/*.bc
%endif

%changelog
* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - 1.4.0-2PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51

* Tue Aug 18 2026 Devrim Gunduz <devrim@gunduz.org> - 1.4.0-1PGDG
- Update to 1.4.0 per changes described at:
  https://github.com/timescale/pg_textsearch/releases/tag/v1.4.0

* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 1.3.1-2PGDG
- Add Amazon Linux 2023 support.

* Thu Jul 23 2026 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-1PGDG
- Initial packaging for the PostgreSQL RPM Repository
