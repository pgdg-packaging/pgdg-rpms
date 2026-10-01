%global sname	age

%{!?runselftest:%global runselftest 0}

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

# 1.8.0-rc0 only exists for PostgreSQL 18 and 19. PostgreSQL 17 stays on 1.7.0,
# so it keeps its own Release to not go backwards.
# rpm on EL-8 (4.14) does not support %%elif, so use nested %%if blocks.
%if %{pgmajorversion} == 17
%global ageversion 1.7.0
%global agerelease rc0_5
%else
%if %{pgmajorversion} == 18 || %{pgmajorversion} == 19
%global ageversion 1.8.0
%global agerelease rc0_2
%else
%{error:age is not available for PostgreSQL %{pgmajorversion}}
%endif
%endif

Summary:	Graph database optimized for fast analysis and real-time data processing.
Name:		%{sname}_%{pgmajorversion}
Version:	%{ageversion}
Release:	%{agerelease}PGDG%{?dist}
License:	Apache 2.0
URL:		https://github.com/apache/%{sname}/
# The tag tarballs of different PostgreSQL versions have the same file name, so
# save each one under a per-version name to not reuse another version's source.
Source0:	https://github.com/apache/age/archive/refs/tags/PG%{pgmajorversion}/v%{version}-rc0.tar.gz#/%{name}-%{version}-rc0.tar.gz
BuildRequires:	bison flex postgresql%{pgmajorversion}-devel
%if 0%{?fedora} >= 43 || 0%{?rhel} >= 9
BuildRequires:	perl-FindBin perl-lib
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	perl
%endif
Requires:	postgresql%{pgmajorversion}-server
%if %runselftest
BuildRequires:	postgresql%{pgmajorversion}-server pgdg-srpm-macros >= 2.0.0
%endif

%description
Apache AGE is an extension for PostgreSQL that enables users to leverage a
graph database on top of the existing relational databases. AGE is an acronym
for A Graph Extension and is inspired by Bitnine's AgensGraph, a multi-model
database fork of PostgreSQL. The basic principle of the project is to create
a single storage that handles both the relational and graph data model so that
the users can use the standard ANSI SQL along with openCypher, one of the most
popular graph query languages today. There is a strong need for cohesive,
easy-to-implement multi-model databases. As an extension of PostgreSQL, AGE
supports all the functionalities and features of PostgreSQL while also
offering a graph model to boot.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for age
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
This package provides JIT support for age
%endif

%prep
%setup -q -n %{sname}-PG%{pgmajorversion}-v%{version}-rc0/

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} INSTALL_PREFIX=%{buildroot} DESTDIR=%{buildroot} install %{with_llvm_arg}

# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%check
%if %runselftest
# AGE's installcheck runs the tests in a temporary instance of its own, so
# there is no need to start a server here.
%pgdg_check_init
pgdg_installcheck %{with_llvm_arg}
%endif

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*
%endif

%changelog
* Tue Sep 29 2026 Devrim Gündüz <devrim@gunduz.org> - 1.8.0-rc0_2PGDG
- Add %%check, running the regression tests with the %%check helpers
  from pgdg-srpm-macros 2.0.0. It is disabled by default; enable it
  with --define 'runselftest 1'. PostgreSQL 17 is now 1.7.0-rc0_5PGDG.
- Replace %%elif with nested %%if blocks: rpm on EL-8 does not support
  %%elif, so the spec failed with "age is not available" on PostgreSQL 18.

* Sun Sep 20 2026 Devrim Gündüz <devrim@gunduz.org> - 1.8.0-1PGDG
- Update to 1.8.0-rc0 on PostgreSQL 18 and 19 per changes described at:
  PostgreSQL 18: https://github.com/apache/age/releases/tag/PG18%2Fv1.8.0-rc0
  PostgreSQL 19: https://github.com/apache/age/releases/tag/PG19%2Fv1.8.0-rc0
  PostgreSQL 17 stays on 1.7.0-rc0 (1.7.0-4PGDG), as there is no 1.8.0 for it.
- Save the source tarball under a per-PostgreSQL-version name, as the tag
  tarballs of PostgreSQL 18 and 19 have the same file name.
- Error out on PostgreSQL versions that age is not packaged for.

* Sun Sep 13 2026 Devrim Gunduz <devrim@gunduz.org> - 1.7.0-4PGDG
- Add missing BRs, per https://github.com/pgdg-packaging/pgdg-rpms/issues/237

* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - 1.7.0-3PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51

* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 1.7.0-rc0-2PGDG
- Add Amazon Linux 2023 support.

* Fri Feb 13 2026 Devrim Gündüz <devrim@gunduz.org> - 1.7.0-rc0-1PGDG
- Update to 1.7.0-rc0 per changes described at:
  PostgreSQL 18: https://github.com/apache/age/releases/tag/PG18%2Fv1.7.0-rc0
  PostgreSQL 17: https://github.com/apache/age/releases/tag/PG17%2Fv1.7.0-rc0

* Thu Jan 15 2026 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-rc0-1PGDG
- Initial RPM packaging for the PostgreSQL RPM Repository.
