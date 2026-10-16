%global sname	pg_stat_tcpinfo

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

Summary:	PostgreSQL extension that shows detailed TCP connection information
Name:		%{sname}_%{pgmajorversion}
Version:	1.1
Release:	1PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/jakubwartakEDB/%{sname}
Source0:	https://github.com/jakubwartakEDB/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel
%if %runselftest
BuildRequires:	postgresql%{pgmajorversion}-server pgdg-srpm-macros >= 2.0.0
%endif
Requires:	postgresql%{pgmajorversion}-server

%description
pg_stat_tcpinfo is a Linux-only PostgreSQL extension that exposes
ss/netstat-style TCP socket details as a view. It reports every TCP socket
owned by the OS user the server runs as, with the kernel's full TCP info
(RTT, congestion window, retransmits, queues, socket memory, timers,
congestion control) as jsonb. Access is restricted to pg_read_all_stats
(and therefore pg_monitor).

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
# The test looks for the server's listening socket on 127.0.0.1.
%pgdg_check_init
pgdg_check_start main "listen_addresses = '127.0.0.1'"
pgdg_installcheck %{with_llvm_arg}
%endif

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}.index.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1-1PGDG
- Initial packaging for the PostgreSQL RPM Repository:
  https://github.com/jakubwartakEDB/pg_stat_tcpinfo/releases/tag/v1.1
