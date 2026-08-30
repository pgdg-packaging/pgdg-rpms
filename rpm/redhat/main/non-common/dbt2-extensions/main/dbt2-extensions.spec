%global debug_package %{nil}
%global _vpath_builddir .
%global sname	dbt2

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

Summary:	Database Test 2 Differences from the TPC-C - Extensions
Name:		%{sname}-pg%{pgmajorversion}-extensions
Version:	0.62.0
Release:	3PGDG%{dist}
License:	GPLv2+
Source0:	https://github.com/osdldbt/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/osdldbt/%{sname}/
Requires:	%{sname}-common

BuildRequires:	gcc-c++
BuildRequires:	cmake >= 3.2.0

BuildRequires:	postgresql%{pgmajorversion}-devel curl-devel

%if 0%{?suse_version} >= 1500
Requires:	libopenssl3
BuildRequires:	libopenssl-3-devel
%endif
%if 0%{?fedora} >= 41 || 0%{?rhel} >= 8 || 0%{?amzn}
Requires:	openssl-libs >= 1.1.1k
BuildRequires:	openssl-devel
%endif
%if 0%{?fedora} && 0%{?fedora} <= 44 && !0%{?amzn}
BuildRequires:	openssl-devel-engine
%endif

%if 0%{?suse_version} >= 1500
BuildRequires:	libexpat-devel
Requires:	libexpat1
%else
BuildRequires:	expat-devel libev-devel
Requires:	expat
%endif

%description
The Open Source Development Lab's Database Test 2 (DBT-2) test kit.

The database management systems that are currently supported are:

* PostgreSQL
* SQLite

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for dbt2-extensions
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
This package provides JIT support for dbt2-extensions
%endif

%prep
%setup -q -n %{sname}-%{version}

%build

CFLAGS="$CFLAGS -I%{pginstdir}/include/server -g -fPIE"; export CFLAGS
export PATH=%{pginstdir}/bin/:$PATH
%{__install} -d build
pushd build
%cmake ..
%cmake_build
popd

pushd storedproc/pgsql/c
export PATH=%{pginstdir}/bin:$PATH
%{__make} DESTDIR=%{buildroot} %{with_llvm_arg}
popd

%install
%{__rm} -rf %{buildroot}
export PATH=%{pginstdir}/bin/:$PATH
pushd build
%cmake_install
popd

pushd storedproc/pgsql/c
export PATH=%{pginstdir}/bin:$PATH
%{__make} DESTDIR=%{buildroot} %{with_llvm_arg} install
popd

# Install extrension control file
%{__mkdir} -p %{buildroot}/%{pginstdir}/share/extension
%{__mkdir} -p %{buildroot}/%{pginstdir}/share/lib
%{__cp} storedproc/pgsql/c/%{sname}.control %{buildroot}/%{pginstdir}/share/extension
%{__cp} storedproc/pgsql/c/%{sname}.so %{buildroot}/%{pginstdir}/lib
%{__cp} storedproc/pgsql/c/%{sname}--0.45.0.sql %{buildroot}/%{pginstdir}/share/extension/%{sname}--%{version}.sql

# Remove files which are installed with the common package:
%{__rm} -f %{buildroot}/%{_bindir}/*
%{__rm} -f %{buildroot}/%{_mandir}/man1/dbt2*

# Remove more files:
%{__rm} -rf %{buildroot}/usr/src/%{sname}/storedproc/

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%license LICENSE
%doc README
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/stock_level.sql
%{pginstdir}/share/delivery.sql
%{pginstdir}/share/new_order.sql
%{pginstdir}/share/order_status.sql
%{pginstdir}/share/payment.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}*.sql

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - 0.62.0-3PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51
- Note: the cmake-based dbt2 driver-tool build/install is untouched by
  this, since it's unrelated to the PGXS-based storedproc extension.

* Mon Aug 24 2026 Devrim Gunduz <devrim@gunduz.org> - 0.62.0-2PGDG
- Fix macros for Amazon Linux 2023

* Sat Aug 15 2026 Devrim Gunduz <devrim@gunduz.org> - 0.62.0-1PGDG
- Update 0.62.0

* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 0.61.7-6PGDG
- Add Amazon Linux 2023 support.

* Mon Apr 20 2026 Devrim Gunduz <devrim@gunduz.org> - 0.61.7-5PGDG
- Fix builds against CMake 4

* Thu Oct 30 2025 Devrim Gunduz <devrim@gunduz.org> - 0.61.7-4PGDG
- Rebuild because of a package signing issue on Fedora 43

* Sun Oct 5 2025 Devrim Gunduz <devrim@gunduz.org> - 0.61.7-3PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 0.61.7-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Thu Jul 10 2025 Devrim Gunduz <devrim@gunduz.org> - 0.61.7-1PGDG
- Update 0.61.7

* Mon Apr 7 2025 Devrim Gunduz <devrim@gunduz.org> - 0.61.6-2PGDG
- Spec file cleanup
- Remove more files.

* Fri Feb 21 2025 Devrim Gunduz <devrim@gunduz.org> - 0.61.6-1PGDG
- Update 0.61.6
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gunduz <devrim@gunduz.org> - 0.61.2-1PGDG
- Update 0.61.2
- Update LLVM dependencies
- Remove RHEL 7 support

* Wed Feb 21 2024 Devrim Gündüz <devrim@gunduz.org> - 0.53.9-1PGDG
- Update to 0.53.9

* Tue Oct 24 2023 Devrim Gündüz <devrim@gunduz.org> - 0.53.7-1PGDG
- Update to 0.53.7
- Add SLES 15 support

* Thu Sep 7 2023 Devrim Gündüz <devrim@gunduz.org> - 0.53.6-1PGDG
- Update to 0.53.6

* Sun Jul 23 2023 Devrim Gündüz <devrim@gunduz.org> - 0.53.4-1PGDG
- Update to 0.53.4
- Add PGDG branding

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 0.50.1-1.1
- Modernise %%patch usage, which has been deprecated in Fedora 38

* Tue Mar 7 2023 Devrim Gündüz <devrim@gunduz.org> - 0.50.1-1
- Update to 0.50.1

* Mon Feb 27 2023 Devrim Gündüz <devrim@gunduz.org> - 0.49.1-1
- Update to 0.49.1

* Wed Jan 18 2023 Devrim Gündüz <devrim@gunduz.org> - 0.48.7-1
- Update to 0.48.7

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 0.48.3-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Aug 17 2022 Devrim Gündüz <devrim@gunduz.org> - 0.48.3-2
- Foo

* Thu Aug 11 2022 Devrim Gündüz <devrim@gunduz.org> - 0.48.3-1
- Initial packaging
