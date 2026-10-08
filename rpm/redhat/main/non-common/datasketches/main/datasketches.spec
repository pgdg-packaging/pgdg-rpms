%global sname	datasketches

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

# Use the headers of the datasketches-cpp package and the system Boost instead
# of the bundled copies that upstream's Makefile expects. Upstream asks for
# -std=c++11, which the Boost.Math headers of newer distros do not support;
# use the compiler's default standard instead.
%global ds_make_args PG_CPPFLAGS="-fPIC -I%{_includedir}/DataSketches" PG_CXXFLAGS= SHLIB_LINK=-lstdc++

Summary:	Approximate algorithms (sketches) for PostgreSQL from Apache DataSketches
Name:		%{sname}_%{pgmajorversion}
Version:	1.7.0
Release:	1PGDG%{?dist}
License:	Apache-2.0
URL:		https://github.com/apache/%{sname}-postgresql
Source0:	https://github.com/apache/%{sname}-postgresql/archive/refs/tags/%{version}.tar.gz
# Fix for a backend crash in aod_sketch_union(), merged upstream after 1.7.0:
Patch0:		%{sname}-aod-union-num-values.patch

BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	datasketches-cpp >= 5.0.0
BuildRequires:	gcc-c++
%if 0%{?suse_version} >= 1500
BuildRequires:	libboost_headers-devel
%else
BuildRequires:	boost-devel
%endif
%if %runselftest
BuildRequires:	postgresql%{pgmajorversion}-server pgdg-srpm-macros >= 2.0.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
This extension provides the sketch algorithms of the Apache DataSketches C++
library as PostgreSQL data types and aggregate functions: CPC, HLL and Theta
sketches for distinct counting, KLL, REQ and quantiles sketches for quantiles
and histograms, a frequent items sketch, and the Array of Doubles tuple sketch.

Create it in a database with:

  CREATE EXTENSION datasketches;

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
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
This package provides JIT support for %{sname}
%endif

%prep
%setup -q -n %{sname}-postgresql-%{version}
%patch -P 0 -p0

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg} %{ds_make_args}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg} %{ds_make_args} DESTDIR=%{buildroot} install

%check
%if %runselftest
# Note: upstream's tests (test/*.sql) are plain psql scripts without expected
# output, so they are not a regression suite. This only checks that every
# script runs without an error and without crashing the server. One error is
# expected: aod_sketch_test.sql calls aod_sketch_union() with a num_values
# that does not match its sketches. That crashed the backend before Patch0,
# and raises an error now.
%pgdg_check_init
pgdg_check_start main
createdb test
for t in test/*.sql; do
	psql -X -d test -f "$t" > "$t.out" 2>&1
	if ! psql -X -d test -Atc 'SELECT 1' > /dev/null; then
		cat "$t.out"
		echo "The server crashed while running $t"
		exit 1
	fi
done
if grep -H 'ERROR:' test/*.sql.out | grep -v 'aod_sketch_test.sql.out:.*pg_aod_sketch_union_agg expects the same num_values in sketches'; then
	echo "Unexpected errors in the test scripts, see above"
	exit 1
fi
%endif

%files
%defattr(-,root,root)
%license LICENSE NOTICE
%doc README.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}.index.bc
    %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Thu Oct 08 2026 Devrim Gunduz <devrim@gunduz.org> - 1.7.0-1PGDG
- Initial packaging for the PostgreSQL RPM Repository:
  https://github.com/apache/datasketches-postgresql/releases/tag/1.7.0
- Add a patch for a backend crash in aod_sketch_union(), from
  https://github.com/apache/datasketches-postgresql/pull/78
