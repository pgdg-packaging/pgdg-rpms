%global sname	pg_incremental

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


Summary:	Incremental Data Processing in PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.5.0
Release:	1PGDG%{?dist}
License:	PostgreSQL
Group:		Applications/Databases
URL:		https://github.com/CrunchyData/%{sname}
Source0:	https://github.com/CrunchyData/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server pg_cron_%{pgmajorversion}

%description
pg_incremental is a simple extension that helps you do fast, reliable,
incremental batch processing in PostgreSQL.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_incremental
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
This package provides JIT support for pg_incremental
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
%{__make} PG_CONFIG=%{pginstdir}/bin/pg_config USE_PGXS=1 %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
%{__make} PG_CONFIG=%{pginstdir}/bin/pg_config USE_PGXS=1 %{?_smp_mflags} %{with_llvm_arg} DESTDIR=%{buildroot} install
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__mv} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%defattr(-,root,root,-)
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}*.control

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Mon Aug 31 2026 Devrim Gunduz <devrim@gunduz.org> - 1.5.0-1PGDG
- Update to 1.5.0 per changes described at:
  https://github.com/CrunchyData/pg_incremental/releases/tag/v1.5.0
  https://github.com/CrunchyData/pg_incremental/releases/tag/v1.4.1
  https://github.com/CrunchyData/pg_incremental/releases/tag/v1.3.0
  https://github.com/CrunchyData/pg_incremental/releases/tag/v1.2.0
  https://github.com/CrunchyData/pg_incremental/releases/tag/v1.1.1
  https://github.com/CrunchyData/pg_incremental/releases/tag/v1.1.0
  https://github.com/CrunchyData/pg_incremental/releases/tag/v1.0.1

* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - 1.0.0-5PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51

* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 1.0.0-4PGDG
- Add Amazon Linux 2023 support.

* Tue Oct 7 2025 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-3PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.0.0-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Thu Jan 9 2025 - Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1PGDG
- Initial RPM packaging for the PostgreSQL RPM repository.
