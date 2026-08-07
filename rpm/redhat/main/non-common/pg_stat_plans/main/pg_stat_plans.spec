%global sname pg_stat_plans

%{!?llvm:%global llvm 1}

Summary:	Track per-plan call counts, execution times and EXPLAIN texts in Postgres
Name:		%{sname}_%{pgmajorversion}
Version:	2.1.0
Release:	2PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/pganalyze/%{sname}
Source0:	https://github.com/pganalyze/%{sname}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
pg_stat_plans is designed for low overhead tracking of aggregate plan
statistics in Postgres, by relying on hashing the plan tree with a plan ID
calculation. It aims to help identify plan regressions, and get an example
plan for each Postgres query run, slow and fast. Additionally, it allows
showing the plan for a currently running query.

Plan texts are stored in shared memory for efficiency reasons (instead of a
local file), with support for zstd compression to compress large plan texts.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_stat_plans
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
This packages provides JIT support for pg_stat_plans
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README
%{__install} -d %{buildroot}%{pginstdir}/doc/extension/
%{__install} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%license LICENSE
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
 %{pginstdir}/lib/bitcode/%{sname}*.bc
 %{pginstdir}/lib/bitcode/%{sname}/*.bc
  %if %{pgmajorversion} <= 17
     %{pginstdir}/lib/bitcode/%{sname}/compat_16_17/*.bc
  %endif
%endif

%changelog
* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 2.1.0-2PGDG
- Add Amazon Linux 2023 support.

* Sun Jun 7 2026 - Devrim Gündüz <devrim@gunduz.org> - 2.1.0-1PGDG
- Initial RPM packaging for PostgreSQL RPM Repository
