%global sname pg_roaringbitmap
%global pname roaringbitmap

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
Version:	1.2.0
Release:	3PGDG%{?dist}
Summary:	RoaringBitmap extension for PostgreSQL
License:	Apache 2.0
URL:		https://github.com/ChenHuajun/%{sname}
Source0:	https://github.com/ChenHuajun/%{sname}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}

%description
Roaring bitmaps are compressed bitmaps which tend to outperform conventional
compressed bitmaps such as WAH, EWAH or Concise. In some instances, roaring
bitmaps can be hundreds of times faster and they often offer significantly
better compression. They can even be faster than uncompressed bitmaps.
More information https://github.com/RoaringBitmap/CRoaring .

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_roaringbitmap
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
This package provides JIT support for pg_roaringbitmap
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} DESTDIR=%{buildroot} install

%files
%defattr(644,root,root,755)
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}--*.sql
%{pginstdir}/share/extension/%{pname}.control

%if %llvm
%files llvmjit
	%{pginstdir}/lib/bitcode/%{pname}*.bc
	%{pginstdir}/lib/bitcode/%{pname}/*.bc
%endif

%changelog
* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - 1.2.0-3PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51

* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 1.2.0-2PGDG
- Add Amazon Linux 2023 support.

* Mon Jun 29 2026 Devrim Gündüz <devrim@gunduz.org> 1.2.0-1PGDG
- Update to 1.2.0 per changes described at:
  https://github.com/ChenHuajun/pg_roaringbitmap/releases/tag/v1.2.0

* Thu Nov 13 2025 Devrim Gündüz <devrim@gunduz.org> 1.1.0-1PGDG
- Update to 1.1.0 per changes described at:
  https://github.com/ChenHuajun/pg_roaringbitmap/releases/tag/v1.1.0

* Mon Nov 10 2025 Devrim Gündüz <devrim@gunduz.org> 1.0.0-1PGDG
- Update to 1.0.0 per changes described at:
  https://github.com/ChenHuajun/pg_roaringbitmap/releases/tag/v1.0.0

* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 0.5.5-3PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 0.5.5-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Mon Sep 15 2025 Devrim Gündüz <devrim@gunduz.org> 0.5.5-1PGDG
- Update to 0.5.5 per changes described at:
  https://github.com/ChenHuajun/pg_roaringbitmap/releases/tag/v0.5.5

* Mon Apr 14 2025 Devrim Gündüz <devrim@gunduz.org> 0.5.4-1PGDG
- Initial packaging for the PostgreSQL RPM repository
