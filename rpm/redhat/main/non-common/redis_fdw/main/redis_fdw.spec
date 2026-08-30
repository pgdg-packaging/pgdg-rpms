%global sname	redis_fdw

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

Summary:	A PostgreSQL Foreign Data Wrapper for Redis
Name:		%{sname}_%{pgmajorversion}
Version:	1.1
Release:	9PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/nahanni/rw_redis_fdw/
Source0:	https://github.com/nahanni/rw_redis_fdw/archive/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel hiredis-devel
BuildRequires:	postgresql%{pgmajorversion}-server
Requires:	postgresql%{pgmajorversion}-server

%if 0%{?fedora} && 0%{?rhel} >= 8
Requires:	libnsl hiredis
%endif
%if 0%{?suse_version} >= 1500
Requires:	libnsl2 libhiredis1_1_0
%endif

%description
Writable Foreign Data Wrapper for Redis

This PostgreSQL extension provides a Foreign Data Wrapper for read (SELECT)
and write (INSERT, UPDATE, DELETE) access to Redis databases
(http://redis.io). Supported Redis data types include: string, set, hash,
list, zset, and pubsub.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for redis_fdw
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
This package provides JIT support for redis_fdw
%endif

%prep
%setup -q -n rw_redis_fdw-%{version}

%build
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%defattr(-,root,root,-)
%license LICENSE
%doc README.md
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.sql
%{pginstdir}/share/extension/*.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1-9PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51

* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1-8PGDG
- Add Amazon Linux 2023 support.

* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 1.1-7PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.1-6PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.1-5PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Mon Feb 26 2024 Devrim Gunduz <devrim@gunduz.org> - 1.1-4PGDG
- Add PGDG branding
- Add SLES 15 support

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.1-3.2
- Rebuild against LLVM 15 on SLES 15

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.1-3.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org>- 1.1-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> 1.1-1
- Remove pxgs patches, and export PATH instead.

* Mon Aug 17 2020 Devrim Gündüz <devrim@gunduz.org> 1.1-1
- Update to 1.1, which supports PostgreSQL 13.

* Wed May 6 2020 Devrim Gündüz <devrim@gunduz.org> 1.0-2
- Fix suffixes in RPMs.

* Thu Apr 16 2020 Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Initial RPM for the PostgreSQL RPM repository
