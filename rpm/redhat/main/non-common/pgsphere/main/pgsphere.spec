%global sname	pgsphere
%global pname	pg_sphere

%{!?llvm:%global llvm 1}

Summary:	R-Tree implementation using GiST for spherical objects
Name:		%{sname}_%{pgmajorversion}
Version:	1.5.1
Release:	5PGDG%{?dist}
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
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 17.0 clang-devel >= 17.0
Requires:	llvm >= 17.0
%endif

%description llvmjit
This packages provides JIT support for pgsphere
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
%{__make} PG_CONFIG=%{pginstdir}/bin/pg_config USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} PG_CONFIG=%{pginstdir}/bin/pg_config USE_PGXS=1 %{?_smp_mflags} DESTDIR=%{buildroot} install

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
