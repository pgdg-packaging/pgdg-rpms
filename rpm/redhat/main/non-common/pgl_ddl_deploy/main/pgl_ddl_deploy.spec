%global sname pgl_ddl_deploy

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


Summary:	Transparent Logical DDL Replication (pgl_ddl_deploy)
Name:		%{sname}_%{pgmajorversion}
Version:	2.2.1
Release:	7PGDG%{?dist}
License:	MIT
Source0:	https://github.com/enova/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/enova/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
Transparent DDL replication for both pglogical and native logical
replication.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgl_ddl_deploy
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
This package provides JIT support for pgl_ddl_deploy
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%defattr(644,root,root,755)
%{pginstdir}/share/extension/%{sname}*sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/lib/ddl_deparse.so
%{pginstdir}/lib/%{sname}.so

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
    %{pginstdir}/lib/bitcode/ddl_deparse*.bc
    %{pginstdir}/lib/bitcode/ddl_deparse/*.bc
%endif

%changelog
* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - 2.2.1-7PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51

* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 2.2.1-6PGDG
- Add Amazon Linux 2023 support.

* Tue Oct 7 2025 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-5PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 2.2.1-4PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Thu Jan 9 2025 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-3PGDG
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-2PGDG
- Update LLVM dependencies

* Thu Jul 18 2024 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-1PGDG
- Update to 2.2.1
- Remove RHEL 7 support
- Update LLVM dependencies

* Tue Oct 24 2023 Devrim Gündüz <devrim@gunduz.org> - 2.2.0-1PGDG
- Initial RPM packaging for the PostgreSQL RPM Repository
