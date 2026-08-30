%global sname pg_similarity
%global packagemajorver 1
%global packageminver 0

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

Summary:	Set of functions and operators for executing similarity queries for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	%{packagemajorver}.%{packageminver}
Release:	7PGDG%{?dist}
URL:		https://github.com/eulerto/%{sname}
Source0:	https://github.com/eulerto/%{sname}/archive/refs/tags/%{sname}_%{packagemajorver}_%{packageminver}.tar.gz
Patch0:		%{sname}-hamming.patch
License:	BSD
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
pg_similarity is an extension to support similarity queries on PostgreSQL.
The implementation is tightly integrated in the RDBMS in the sense that it
defines operators so instead of the traditional operators (= and <>) you can
use ~~~ and ! (any of these operators represents a similarity function).

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_similarity
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
This package provides JIT support for pg_similarity
%endif

%prep
%setup -q -n %{sname}-%{sname}_%{packagemajorver}_%{packageminver}
%patch -P 0 -p1

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} %{with_llvm_arg} DESTDIR=%{buildroot} install

# Install sample config file under the PostgreSQL extension directory:
%{__cp} pg_similarity.conf.sample %{buildroot}%{pginstdir}/share/extension/

# Install README file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 755 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%config %{pginstdir}/share/extension/%{sname}.conf.sample
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
* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - %{packagemajorver}.%{packageminver}-7PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51

* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 1.0-6PGDG
- Add Amazon Linux 2023 support.

* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 1.0-5PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.0-4PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Mon Jan 13 2025 Devrim Gündüz <devrim@gunduz.org> - 1.0-3PGDG
- Add a patch (from Debian) to fix builds against PostgreSQL 16+.
- Install README and sample config file.
- Update LLVM dependencies and package description

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.0-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Fri Apr 12 2024 Devrim Gunduz <devrim@gunduz.org> - 1.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository

