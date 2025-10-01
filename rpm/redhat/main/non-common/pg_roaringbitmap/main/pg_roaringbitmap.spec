%global sname pg_roaringbitmap
%global pname roaringbitmap

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	0.5.5
Release:	2PGDG%{?dist}
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
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 17.0 clang-devel >= 17.0
Requires:	llvm >= 17.0
%endif

%description llvmjit
This package provides JIT support for pg_roaringbitmap
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} DESTDIR=%{buildroot} install

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
* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 0.5.5-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Mon Sep 15 2025 Devrim Gündüz <devrim@gunduz.org> 0.5.5-1PGDG
- Update to 0.5.5 per changes described at:
  https://github.com/ChenHuajun/pg_roaringbitmap/releases/tag/v0.5.5

* Mon Apr 14 2025 Devrim Gündüz <devrim@gunduz.org> 0.5.4-1PGDG
- Initial packaging for the PostgreSQL RPM repository
