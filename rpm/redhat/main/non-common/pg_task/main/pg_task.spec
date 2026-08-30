%global sname	pg_task

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

Summary:	PostgreSQL and Greenplum job scheduler
Name:		%{sname}_%{pgmajorversion}
Version:	2.1.27
Release:	4PGDG%{?dist}
License:	MIT
URL:		https://github.com/RekGRpth/%{sname}
Source0:	https://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
BuildRequires:	postgresql%{pgmajorversion}-devel wget pcre-tools
Requires:	postgresql%{pgmajorversion}-server

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

%build
%{__make} PG_CONFIG=%{pginstdir}/bin/pg_config PATH=%{pginstdir}/bin/:$PATH USE_PGXS=1 %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
%{__make} PG_CONFIG=%{pginstdir}/bin/pg_config PATH=%{pginstdir}/bin/:$PATH USE_PGXS=1 %{?_smp_mflags} %{with_llvm_arg} DESTDIR=%{buildroot} install
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__mv} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

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
