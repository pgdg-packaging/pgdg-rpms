%global sname pgmeminfo

%global pmeminfomajver 1
%global pmeminfomidver 0
%global pmeminfominver 1

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


Name:		%{sname}_%{pgmajorversion}
Version:	%{pmeminfomajver}.%{pmeminfomidver}.%{pmeminfominver}
Release:	3PGDG%{?dist}
Summary:	PostgreSQL extension to allow to access to memory usage diagnostics
License:	BSD
URL:		https://github.com/okbob/%{sname}
Source0:	https://github.com/okbob/pgmeminfo/archive/refs/tags/VERSION_%{pmeminfomajver}_%{pmeminfomidver}_%{pmeminfominver}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}

%description
The pgmeminfo extension can be used to display memory usage information of
a PostgreSQL server.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgmeminfo
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
This package provides JIT support for pgmeminfo
%endif

%prep
%setup -q -n %{sname}-VERSION_%{pmeminfomajver}_%{pmeminfomidver}_%{pmeminfominver}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} DESTDIR=%{buildroot} install

%files
%defattr(644,root,root,755)
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{sname}*.bc
%{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - %{pmeminfomajver}.%{pmeminfomidver}.%{pmeminfominver}-3PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51
- Also wrap %%files llvmjit in %%if %%llvm, which was missing and broke
  parsing entirely whenever %%llvm was set to 0.

* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 1.0.1-2PGDG
- Add Amazon Linux 2023 support.

* Sat Jun 20 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0.1-1PGDG
- Update to 1.0.1 per changes described at:
  https://github.com/okbob/pgmeminfo/releases/tag/VERSION_1_0_1

* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-5PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.0.0-4PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Thu Jan 9 2025 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-3PGDG
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-2PGDG
- Update LLVM dependencies

* Tue Mar 5 2024 Devrim Gündüz <devrim@gunduz.org> 1.0.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository
