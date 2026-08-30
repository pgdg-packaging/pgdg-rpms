%global sname	pgsphere
%global pname	pg_sphere

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

Summary:	R-Tree implementation using GiST for spherical objects
Name:		%{sname}_%{pgmajorversion}
Version:	1.5.2
Release:	3PGDG%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	https://github.com/postgrespro/%{sname}/archive/refs/tags/%{version}.tar.gz
URL:		https://github.com/postgrespro/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel zlib-devel
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 8
BuildRequires:	healpix-c++-devel
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	healpix_cxx-devel
%endif

Requires:	postgresql%{pgmajorversion}-server

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

%build
%{__make} PG_CONFIG=%{pginstdir}/bin/pg_config USE_PGXS=1 %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
%{__make} PG_CONFIG=%{pginstdir}/bin/pg_config USE_PGXS=1 %{?_smp_mflags} %{with_llvm_arg} DESTDIR=%{buildroot} install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

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
