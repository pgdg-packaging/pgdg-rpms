%global sname	pg_plan_filter
%global modname	plan_filter

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

Summary:	PostgreSQL module to filter statements by their execution plans
Name:		%{sname}_%{pgmajorversion}
Version:	1.0.0
Release:	1PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/pgexperts/%{sname}
Source0:	https://github.com/pgexperts/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel
%if %runselftest
BuildRequires:	postgresql%{pgmajorversion}-server pgdg-srpm-macros >= 2.0.0
%endif

%description
pg_plan_filter (the plan_filter module) rejects statements by the properties
of their execution plan, currently by the estimated plan cost of a statement
or of a transaction. It is not an extension: load it with

  shared_preload_libraries = 'plan_filter'

or with session_preload_libraries or LOAD, and set the plan_filter.*
parameters, e.g. plan_filter.statement_cost_limit.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
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
This package provides JIT support for %{sname}
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg} DESTDIR=%{buildroot} install

%check
%if %runselftest
%pgdg_check_init
pgdg_check_start main
pgdg_installcheck %{with_llvm_arg}
%endif

%files
%defattr(-,root,root)
%license License
%doc README.md
%{pginstdir}/lib/%{modname}.so
%{pginstdir}/doc/contrib/%{modname}.md

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{modname}.index.bc
    %{pginstdir}/lib/bitcode/%{modname}/*.bc
%endif

%changelog
* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 1.0.0-1PGDG
- Initial packaging for the PostgreSQL RPM Repository:
  https://github.com/pgexperts/pg_plan_filter/releases/tag/v1.0.0
