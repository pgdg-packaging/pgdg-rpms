%global pname pgsql_gzip
%global sname pgsql-gzip

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

Summary:	PostgreSQL gzip/gunzip functions
Name:		%{pname}_%{pgmajorversion}
Version:	1.1.1
Release:	3PGDG%{?dist}
URL:		https://github.com/pramsey/%{sname}
Source0:	https://github.com/pramsey/%{sname}/archive/refs/tags/v%{version}.tar.gz
# INT_MAX is used without including limits.h, which fails against
# PostgreSQL 19
Patch0:		%{pname}-%{version}-limits_h.patch
License:	MIT
BuildRequires:	postgresql%{pgmajorversion}-devel

%if 0%{?fedora} == 40
BuildRequires:	zlib-ng-compat-devel
Requires:	zlib-ng-compat
%endif
%if 0%{?fedora} >= 41
BuildRequires:	zlib-devel
Requires:	zlib
%endif
%if 0%{?rhel} >= 8
BuildRequires:	zlib-devel
Requires:	zlib
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	zlib-devel
Requires:	libz1
%endif

Requires:	postgresql%{pgmajorversion}-server
%if %runselftest
BuildRequires:	postgresql%{pgmajorversion}-server pgdg-srpm-macros >= 2.0.0
%endif

%description
Sometimes you just need to compress your bytea object before you return it to
the client.

Sometimes you receive a compressed bytea from the client, and you have to
uncompress it before you can work with it.

This extension is for that.

This extension is not for storage compression. PostgreSQL already does tuple
compression on the fly if your tuple gets large enough, manually
pre-compressing your data using this function won't make things smaller.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgsql_gzip
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
This package provides JIT support for pgsql_gzip
%endif

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p0

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} %{with_llvm_arg} DESTDIR=%{buildroot} install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%check
%if %runselftest
%pgdg_check_installcheck %{with_llvm_arg}
%endif

%files
%defattr(-,root,root)
%{pginstdir}/lib/gzip.so
%{pginstdir}/share/extension/gzip*.sql
%{pginstdir}/share/extension/gzip*.control

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/gzip.index*.bc
    %{pginstdir}/lib/bitcode/gzip/*.bc
%endif

%changelog
* Tue Sep 29 2026 Devrim Gündüz <devrim@gunduz.org> - 1.1.1-3PGDG
- Add %%check, running the regression tests with the %%check helpers
  from pgdg-srpm-macros 2.0.0. It is disabled by default; enable it
  with --define 'runselftest 1'.
- Add a patch to include limits.h for INT_MAX, to fix the build against
  PostgreSQL 19.

* Thu Sep 10 2026 Devrim Gündüz <devrim@gunduz.org> - 1.1.1-2PGDG
- Add missing BR

* Mon Aug 31 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1.1-1PGDG
- Update to 1.1.1 per changes described at:
  https://github.com/pramsey/pgsql-gzip/releases/tag/v1.1.1

* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1.0-3PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51

* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1.1-2PGDG
- Add Amazon Linux 2023 support.

* Thu Jul 9 2026 Devrim Gündüz <devrim@gunduz.org> - 1.1.1-1PGDG
- Update to 1.1.1 per changes described at:
  https://github.com/pramsey/pgsql-gzip/releases/tag/v1.1.0
  https://github.com/pramsey/pgsql-gzip/releases/tag/v1.1.1

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.0.0-7PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Wed Mar 12 2025 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-6PGDG
- Remove duplicate BR

* Tue Feb 25 2025 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-5PGDG
- Add missing BR

* Mon Jan 13 2025 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-4PGDG
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-3PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Sun May 12 2024 Devrim Gunduz <devrim@gunduz.org> - 1.0.0-2PGDG
- Fix dependency on RHEL 8

* Fri May 10 2024 Devrim Gunduz <devrim@gunduz.org> - 1.0.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository

