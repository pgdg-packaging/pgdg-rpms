%global sname pllua

%global plluangmajver 2
%global plluangmidver 0
%global plluangminver 12

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

Summary:	Procedural language interface between PostgreSQL and Lua
Name:		%{sname}_%{pgmajorversion}
Version:	%{plluangmajver}.%{plluangmidver}.%{plluangminver}
Release:	8PGDG%{?dist}
License:	MIT
Source0:	https://github.com/%{sname}/%{sname}/archive/refs/tags/REL_%{plluangmajver}_%{plluangmidver}_%{plluangminver}.tar.gz
URL:		https://github.com/%{sname}/%{sname}

BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
%if 0%{?suse_version} >= 1500
BuildRequires:	lua54-devel
Requires:	liblua5_4-5
%else
BuildRequires:	lua-devel
Requires:	lua-libs
%endif

%description
PL/Lua is a procedural language module for the PostgreSQL database that
allows server-side functions to be written in Lua.

%package devel
Summary:	PL/Lua development header files and libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package includes development libraries for PL/Lua

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pllua
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
This package provides JIT support for pllua
%endif

%prep
%setup -q -n %{sname}-REL_%{plluangmajver}_%{plluangmidver}_%{plluangminver}

%build
%if 0%{?suse_version} >= 1500
export LUA_INCDIR="%{_includedir}/lua5.4"
%else
export LUA_INCDIR="%{_includedir}"
%endif
LUALIB="-L%{libdir} -l lua" LUAC="%{_bindir}/luac" LUA="%{_bindir}/lua" \
	PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
%if 0%{?suse_version} >= 1500
export LUA_INCDIR="%{_includedir}/lua5.4"
%else
export LUA_INCDIR="%{_includedir}"
%endif
LUALIB="-L%{libdir} -l lua" LUAC="%{_bindir}/luac" LUA="%{_bindir}/lua" \
	PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} %{with_llvm_arg} install DESTDIR=%{buildroot}
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension/
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%license LICENSE
%defattr(644,root,root,755)
%{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}u*.sql
%{pginstdir}/share/extension/%{sname}u.control

%files devel
%dir %{pginstdir}/include/server/extension/%{sname}
%{pginstdir}/include/server/extension/%{sname}/*

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %dir %{pginstdir}/lib/bitcode/%{sname}
    %{pginstdir}/lib/bitcode/%{sname}/*
%endif

%changelog
* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0.12-8PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51

* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0.12-7PGDG
- Add Amazon Linux 2023 support.

* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 2.0.12-6PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 2.0.12-5PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Wed Jan 22 2025 Devrim Gündüz <devrim@gunduz.org> - 2.0.12-4PGDG
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 2.0.12-3PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Mon Feb 26 2024 Devrim Gündüz <devrim@gunduz.org> - 2.0.12-2PGDG
- Update LLVM dependencies
- Add SLES 15 support

* Mon Jul 31 2023 Devrim Gündüz <devrim@gunduz.org> - 2.0.12-1PGDG
- Update to 2.0.12
- Add PGDG branding
- Switch to new repo

* Thu May 11 2023 Devrim Gündüz <devrim@gunduz.org> - 2.0.11-1
- Update to 2.0.11

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.0.10-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu Sep 16 2021 Devrim Gündüz <devrim@gunduz.org> - 2.0.10-1
- Update to 2.0.10

* Mon Apr 26 2021 Devrim Gündüz <devrim@gunduz.org> - 2.0.9-1
- Initial packaging for PostgreSQL RPM Repository
