%global sname	pgsphere
%global pname	pg_sphere

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

Summary:	R-Tree implementation using GiST for spherical objects
Name:		%{sname}_%{pgmajorversion}
Version:	1.5.2
Release:	5PGDG%{?dist}
%if 0%{?pgminorversion:1}
# pgminorversion is the PostgreSQL minor release that the build servers
# build against (global/Makefile.global): require at least that one, at
# build time and at runtime.
# The other postgresqlNN-* dependencies need no version here: the PostgreSQL
# subpackages require each other's exact version-release (all of them pin
# the client package, which pins -libs), so the server, contrib etc. follow
# -devel at build time and -libs at runtime.
BuildRequires:	postgresql%{pgmajorversion}-devel >= %{pgminorversion}
Requires:	postgresql%{pgmajorversion}-libs%{?_isa} >= %{pgminorversion}
%endif
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/postgrespro/%{sname}/archive/refs/tags/%{version}.tar.gz
# Alternate expected output of the moc test for PostgreSQL 19, from upstream:
# https://github.com/postgrespro/pgsphere/commit/54c07d0b2a11 (issue #147)
Patch0:		pgsphere-1.5.2-pg19-moc-expected.patch
URL:		https://github.com/postgrespro/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel zlib-devel
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 8
BuildRequires:	healpix-c++-devel
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	healpix_cxx-devel
%endif

Requires:	postgresql%{pgmajorversion}-server
%if %runselftest
BuildRequires:	postgresql%{pgmajorversion}-server pgdg-srpm-macros >= 2.0.0
%endif

%description
pgSphere is a server side module for PostgreSQL. It contains methods for
working with spherical coordinates and objects. It also supports indexing of
spherical objects.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgsphere
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
This package provides JIT support for pgsphere
%endif

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p1

%build
%{__make} PG_CONFIG=%{pginstdir}/bin/pg_config USE_PGXS=1 %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
%{__make} PG_CONFIG=%{pginstdir}/bin/pg_config USE_PGXS=1 %{?_smp_mflags} %{with_llvm_arg} DESTDIR=%{buildroot} install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%check
%if %runselftest
%pgdg_check_installcheck %{with_llvm_arg}
%endif

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README.%{pname}
%license %{pginstdir}/doc/extension/COPYRIGHT.%{pname}
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}*.sql
%{pginstdir}/share/extension/%{pname}.control

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{pname}.index.bc
    %{pginstdir}/lib/bitcode/%{pname}/src/*.bc
    %{pginstdir}/lib/bitcode/%{pname}/healpix_bare/*bc
%endif

%changelog
* Mon Nov 9 2026 Devrim Gündüz <devrim@gunduz.org> - 1.5.2-5PGDG
- Rebuild against latest PostgreSQL minor releases
- Require at least the PostgreSQL minor release that the package is
  built against (pgminorversion, set by the build server Makefiles).
- Add the upstream alternate expected output of the moc test, which
  failed with PostgreSQL 19: an error for a function called with the
  wrong number of arguments now has a DETAIL instead of a HINT.

* Tue Sep 29 2026 Devrim Gunduz <devrim@gunduz.org> - 1.5.2-4PGDG
- Add %%check, running the regression tests with the %%check helpers
  from pgdg-srpm-macros 2.0.0. It is disabled by default; enable it
  with --define 'runselftest 1'.

* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - 1.5.2-3PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51

* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 1.5.2-2PGDG
- Add Amazon Linux 2023 support.

* Mon Oct 20 2025 Devrim Gündüz <devrim@gunduz.org> - 1.5.2-1PGDG
- Update to 1.5.2 per changes described at:
  https://github.com/postgrespro/pgsphere/releases/tag/1.5.2

* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 1.5.1-6PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.5.1-5PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Tue Feb 25 2025 Devrim Gündüz <devrim@gunduz.org> - 1.5.1-4PGDG
- Add missing BR

* Mon Jan 13 2025 Devrim Gündüz <devrim@gunduz.org> - 1.5.1-3PGDG
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.5.1-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Fri May 10 2024 - Devrim Gündüz <devrim@gunduz.org> - 1.5.1-1PGDG
- Update to 1.5.1 per chages described at:
  https://github.com/postgrespro/pgsphere/releases/tag/1.5.1

* Fri Feb 23 2024 - Devrim Gündüz <devrim@gunduz.org> - 1.4.2-2PGDG
- Add SLES 15 support

* Thu Dec 21 2023 - Devrim Gündüz <devrim@gunduz.org> - 1.4.2-1PGDG
- Initial RPM packaging for the PostgreSQL RPM repository.
