%global sname rdf_fdw

%{!?llvm:%global llvm 1}
%{!?runselftest:%global runselftest 0}

# Propagate %%llvm into the actual build: PGXS decides whether to invoke
# clang/llvm-config based on with_llvm from the installed postgresql*-devel's
# Makefile.global, not from this spec's %%llvm.
%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Summary:	PostgreSQL Foreign Data Wrapper for RDF Triplestores
Name:		%{sname}_%{pgmajorversion}
Version:	3.1
Release:	2PGDG%{?dist}
%if 0%{?pgminorversion:1}
# Built against this PostgreSQL minor release: require at least that one.
# The other postgresqlNN-* dependencies need no version here: the PostgreSQL
# subpackages require each other's exact version-release (all of them pin
# the client package, which pins -libs), so the server, contrib etc. follow
# -devel at build time and -libs at runtime.
BuildRequires:	postgresql%{pgmajorversion}-devel >= %{pgminorversion}
Requires:	postgresql%{pgmajorversion}-libs%{?_isa} >= %{pgminorversion}
%endif
License:	MIT
URL:		https://github.com/jimjonesbr/%{sname}
Source0:	https://github.com/jimjonesbr/%{sname}/archive/v%{version}.tar.gz
# Alternative expected output for PostgreSQL 14, whose psql counts emoji as
# one column wide (15 and later count them as two):
Patch0:		%{sname}-pg14-emoji-width-expected.patch

BuildRequires:	postgresql%{pgmajorversion}-devel libcurl-devel libxml2-devel
Requires:	postgresql%{pgmajorversion}-server
%if %runselftest
BuildRequires:	postgresql%{pgmajorversion}-server pgdg-srpm-macros >= 2.0.0
%endif

%description
rdf_fdw is a PostgreSQL Foreign Data Wrapper to easily access RDF
Triplestores via SPARQL endpoints, including pushdown of several SQL
clauses, and data modification (INSERT, UPDATE, DELETE) through the
rdfnode data type.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for rdf_fdw
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
This package provides JIT support for rdf_fdw
%endif

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p1

%build
PATH=%{pginstdir}/bin:$PATH USE_PGXS=1 %{__make} %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH USE_PGXS=1 %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install %{with_llvm_arg}

# Install README with a package specific name:
%{__mv} %{buildroot}%{pginstdir}/doc/extension/README.md \
	%{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%check
%if %runselftest
# Only the tests that need no triplestore or network access run by default.
# The rdfnode tests need a UTF-8 database, but the build environment may run
# with LANG=C, which would make the test cluster SQL_ASCII.
export LC_ALL=C.UTF-8
%pgdg_check_installcheck %{with_llvm_arg}
%endif

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Mon Nov 9 2026 Devrim Gündüz <devrim@gunduz.org> - 3.1-2PGDG
- Rebuild against latest PostgreSQL minor releases
- Require at least the PostgreSQL minor release that the package is
  built against (pgminorversion, set by the build server Makefiles).

* Sun Nov 8 2026 Devrim Gunduz <devrim@gunduz.org> - 3.1-1PGDG
- Initial packaging for the PostgreSQL RPM Repository, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/220
- Add a patch with alternative expected test output for PostgreSQL 14,
  whose psql counts emoji as one column wide.
- No RHEL 8 support: upstream requires libcurl >= 7.74, and RHEL 8 ships
  7.61.
