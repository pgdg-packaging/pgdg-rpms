%global sname	login_hook

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

Summary:	Postgres database extension to execute some code on user login, comparable to Oracle's after logon trigger.
Name:		%{sname}_%{pgmajorversion}
Version:	1.8
Release:	3PGDG%{?dist}
License:	GPLv3
URL:		https://github.com/splendiddata/%{sname}
Source0:	https://github.com/splendiddata/%{sname}/archive/refs/tags/Version_%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
Postgres database extension to execute some code on user login,
comparable to Oracle's after logon trigger.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for login_hook
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
This package provides JIT support for login_hook
%endif

%prep
%setup -q -n %{sname}-Version_%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install %{with_llvm_arg}
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
# No need to ship these files:
%{__rm} %{buildroot}%{pginstdir}/doc/extension/%{sname}.css
%{__rm} %{buildroot}%{pginstdir}/doc/extension/%{sname}.html

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - 1.8-3PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51

* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 1.8-2PGDG
- Add Amazon Linux 2023 support.

* Tue Jun 23 2026 Devrim Gündüz <devrim@gunduz.org> - 1.8-1PGDG
- Update to 1.8 per changes described at:
  https://github.com/splendiddata/login_hook/releases/tag/Version_1.8

* Mon Oct 6 2025 Devrim Gunduz <devrim@gunduz.org> - 1.7-3PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.7-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Mon May 5 2025 Devrim Gündüz <devrim@gunduz.org> - 1.7-1PGDG
- Update to 1.7 per changes described at:
  https://github.com/splendiddata/login_hook/releases/tag/Version_1.7

* Thu Jan 9 2025 Devrim Gündüz <devrim@gunduz.org> - 1.6-2PGDG
- Update LLVM dependencies

* Fri Aug 16 2024 Devrim Gündüz <devrim@gunduz.org> - 1.6-1PGDG
- Update to 1.6 per changes described at:
  https://github.com/splendiddata/login_hook/releases/tag/Version_1.6

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.5-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Mon Oct 30 2023 Devrim Gunduz <devrim@gunduz.org> - 1.5-1PGDG
- Initial packaging for PostgreSQL RPM Repository
