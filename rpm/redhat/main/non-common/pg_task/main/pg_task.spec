%global sname	pg_task

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

Summary:	PostgreSQL and Greenplum job scheduler
Name:		%{sname}_%{pgmajorversion}
Version:	3.0.0
Release:	2PGDG%{?dist}
License:	MIT
URL:		https://github.com/RekGRpth/%{sname}
Source0:	https://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
# The build generates exec.c from the server's postgres.c, which upstream's
# postgres.sh downloads from GitHub during the build. Ship it per PG major
# version instead (SourceNN is for PG NN), so that the build works offline.
Source13:	https://raw.githubusercontent.com/postgres/postgres/REL_13_23/src/backend/tcop/postgres.c#/postgres-REL_13_23.c
Source14:	https://raw.githubusercontent.com/postgres/postgres/REL_14_24/src/backend/tcop/postgres.c#/postgres-REL_14_24.c
Source15:	https://raw.githubusercontent.com/postgres/postgres/REL_15_19/src/backend/tcop/postgres.c#/postgres-REL_15_19.c
Source16:	https://raw.githubusercontent.com/postgres/postgres/REL_16_15/src/backend/tcop/postgres.c#/postgres-REL_16_15.c
Source17:	https://raw.githubusercontent.com/postgres/postgres/REL_17_11/src/backend/tcop/postgres.c#/postgres-REL_17_11.c
Source18:	https://raw.githubusercontent.com/postgres/postgres/REL_18_6/src/backend/tcop/postgres.c#/postgres-REL_18_6.c
BuildRequires:	krb5-devel
BuildRequires:	postgresql%{pgmajorversion}-devel pcre2-tools
%if 0%{?suse_version} >= 1500
Requires:	libopenssl3
BuildRequires:	libopenssl-3-devel
%endif
%if 0%{?fedora} >= 43 || 0%{?rhel} >= 8
Requires:	openssl-libs >= 1.1.1k
BuildRequires:	openssl-devel
%endif

Requires:	postgresql%{pgmajorversion}-server
%if %runselftest
BuildRequires:	postgresql%{pgmajorversion}-server pgdg-srpm-macros >= 2.0.0
%endif

%description
pg_task allows to execute any sql command at any specific time at background
asynchronously.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_task
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
This package provides JIT support for pg_task
%endif

%prep
%setup -q -n %{sname}-%{version}
# The shell scripts call pcregrep, which is called pcre2grep on most distros.
sed -i "s:pcregrep:pcre2grep:g" *.sh
%{__cp} -p %{expand:%%{SOURCE%{pgmajorversion}}} postgres.c

%build
%{__make} PG_CONFIG=%{pginstdir}/bin/pg_config PATH=%{pginstdir}/bin/:$PATH USE_PGXS=1 %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
%{__make} PG_CONFIG=%{pginstdir}/bin/pg_config PATH=%{pginstdir}/bin/:$PATH USE_PGXS=1 %{?_smp_mflags} %{with_llvm_arg} DESTDIR=%{buildroot} install
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__mv} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%check
%if %runselftest
# The tests need pg_task in shared_preload_libraries and enough background
# workers for the tasks they start in parallel, and run with
# --use-existing in the database pg_task works in, postgres by default
%pgdg_check_init
pgdg_check_start main "shared_preload_libraries = 'pg_task'" "max_worker_processes = 64"
pgdg_installcheck %{with_llvm_arg} REGRESS_OPTS="--use-existing --dbname=postgres"
%endif

%files
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%defattr(-,root,root,-)
%{pginstdir}/lib/%{sname}.so

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
    %{pginstdir}/lib/bitcode/%{sname}*.bc
%endif

%changelog
* Tue Sep 29 2026 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-2PGDG
- Add %%check, running the regression tests with the %%check helpers
  from pgdg-srpm-macros 2.0.0. It is disabled by default; enable it
  with --define 'runselftest 1'.
- Ship the server's postgres.c for each PG major version as a source,
  instead of letting the build download it from GitHub, which fails
  in builds without network access. Drop the now unused wget BR.

* Sat Sep 19 2026 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-1PGDG
- Update to 3.0.0
- Use pcre2grep (pcre2-tools) instead of pcregrep in the shell scripts.

* Thu Sep 10 2026 Devrim Gündüz <devrim@gunduz.org> - 2.1.29-2PGDG
- Add missing BR

* Mon Aug 31 2026 Devrim Gunduz <devrim@gunduz.org> - 2.1.29-1PGDG
- Update to 2.1.29

* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - 2.1.27-4PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51

* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 2.1.27-3PGDG
- Add Amazon Linux 2023 support.

* Mon Apr 27 2026 Devrim Gündüz <devrim@gunduz.org> - 2.1.27-2PGDG
- Add missing BR. Fixes https://github.com/RekGRpth/pg_task/issues/15

* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 2.1.27-1PGDG
- Update to 2.1.27
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 2.1.7-4PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Wed Feb 26 2025 - Devrim Gündüz <devrim@gunduz.org> - 2.1.7-3PGDG
- Add missing BR

* Sat Jan 11 2025 - Devrim Gündüz <devrim@gunduz.org> - 2.1.7-2PGDG
- Update LLVM dependencies

* Tue Sep 24 2024 - Devrim Gündüz <devrim@gunduz.org> - 2.1.7-1PGDG
- Update to 2.1.7

* Tue Sep 3 2024 - Devrim Gündüz <devrim@gunduz.org> - 2.1.5-1PGDG
- Initial RPM packaging for the PostgreSQL RPM repository.
