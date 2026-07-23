%global sname pg_textsearch

%{!?llvm:%global llvm 1}

Summary:	Modern ranked text search for Postgres
Name:		%{sname}_%{pgmajorversion}
Version:	1.3.1
Release:	1PGDG%{?dist}
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
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for pg_textsearch
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

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
* Thu Jul 23 2026 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-1PGDG
- Initial packaging for the PostgreSQL RPM Repository
