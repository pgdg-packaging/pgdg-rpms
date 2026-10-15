%global sname	babelfish_extensions

# Babelfish upstream publishes no tags for the 6.x (PostgreSQL 18) line, only
# BABEL_6_x_STABLE branches, so build from pinned commits for reproducibility.
# The commit of postgresql_modified_for_babelfish is needed for the PG_SRC
# files (grammar, keyword lists, headers) the extensions are generated from.
%global bbfcommit	67bab86e64d606d9a7c2c37239e4b2a52aca4edb
%global pgsrccommit	d4e1b9879d472cab700cc676d7c5eb1d54dae05f

# Build and install against the Babelfish-patched engine, which has its own prefix.
%global bbfpginstdir	/usr/babelfish-%{pgmajorversion}
%global pginstdir	%{bbfpginstdir}

# Babelfish extensions are tied to one PostgreSQL major version.
%if 0%{?pgmajorversion} != 18
%{error:%{sname} is only packaged for PostgreSQL 18 for now}
%endif

Summary:	SQL Server compatibility extensions for PostgreSQL (Babelfish)
Name:		%{sname}_%{pgmajorversion}
Version:	6.3.0
Release:	6PGDG%{?dist}
# Dual licensed: either license may be used.
License:	Apache-2.0 OR PostgreSQL
Source0:	https://github.com/babelfish-for-postgresql/%{sname}/archive/%{bbfcommit}.tar.gz#/%{sname}-%{bbfcommit}.tar.gz
Source1:	https://github.com/babelfish-for-postgresql/postgresql_modified_for_babelfish/archive/%{pgsrccommit}.tar.gz#/postgresql_modified_for_babelfish-%{pgsrccommit}.tar.gz
URL:		https://babelfishpg.org/
# Upstream commit 16eb0df3: fixes -Werror build failures with newer GCC, glibc,
# OpenSSL and CMake. Not in BABEL_6_3_STABLE yet; drop once it is.
Patch0:		%{sname}-%{version}-newer-toolchain.patch

# These extensions only work with the PostgreSQL engine patched for Babelfish
# (postgresql_modified_for_babelfish), packaged as babelfish_postgresqlNN.
BuildRequires:	babelfish_postgresql%{pgmajorversion}-devel
BuildRequires:	gcc gcc-c++ make cmake bison flex perl
BuildRequires:	libicu-devel libxml2-devel openssl-devel
BuildRequires:	antlr4-cpp-runtime-devel >= 4.13.2
Requires:	babelfish_postgresql%{pgmajorversion}-server
# uuid-ossp is a run-time dependency of Babelfish
Requires:	babelfish_postgresql%{pgmajorversion}-contrib
Requires:	antlr4-cpp-runtime >= 4.13.2

# ANTLR tool (bundled jar) runs on Java, pinned per distro
%if 0%{?rhel} == 8
BuildRequires:	java-11-openjdk-headless
%endif
%if 0%{?rhel} == 9
BuildRequires:	java-17-openjdk-headless
%endif
%if 0%{?rhel} == 10
BuildRequires:	java-21-openjdk-headless
%endif
%if 0%{?fedora}
BuildRequires:	java-latest-openjdk-headless
%endif

%description
Babelfish adds additional syntax, functions, data types, and more to
PostgreSQL to help in the migration from SQL Server. This package contains the
four extensions that comprise Babelfish: babelfishpg_common, babelfishpg_money,
babelfishpg_tds and babelfishpg_tsql.

Note that these extensions require the PostgreSQL engine patched for Babelfish
(https://github.com/babelfish-for-postgresql/postgresql_modified_for_babelfish)
and do not work with a stock PostgreSQL server.

%prep
%setup -q -n %{sname}-%{bbfcommit}
%setup -q -T -D -a 1 -n %{sname}-%{bbfcommit}
%patch -P 0 -p1

# Use the distro ANTLR runtime instead of the /usr/local one upstream expects.
%{__sed} -i 's|/usr/local/include/antlr4-runtime|%{_includedir}/antlr4-runtime|g' \
	contrib/babelfishpg_tsql/antlr/CMakeLists.txt contrib/babelfishpg_tsql/Makefile
%{__sed} -i 's|^export ANTLR4_RUNTIME_LIB_DIR=.*|export ANTLR4_RUNTIME_LIB_DIR=%{_libdir}|' \
	contrib/babelfishpg_tsql/Makefile

%build
export PG_CONFIG=%{pginstdir}/bin/pg_config
export PG_SRC=$(pwd)/postgresql_modified_for_babelfish-%{pgsrccommit}
export cmake=%{_bindir}/cmake
export PATH=%{pginstdir}/bin:$PATH

# The ANTLR-generated C++ sources (antlr4cpp_generated_src/) are only a
# prerequisite of the final link (antlr/libantlr_tsql.a), not of the objects
# that include them, so with -j the tsql objects compile before they exist.
# Generate them first.
%{__make} -C contrib/babelfishpg_tsql antlr/libantlr_tsql.a

# Same order as upstream's build instructions.
for ext in babelfishpg_money babelfishpg_common babelfishpg_tsql babelfishpg_tds
do
	%{__make} -C contrib/$ext %{?_smp_mflags}
done

%install
%{__rm} -rf %{buildroot}
export PG_CONFIG=%{pginstdir}/bin/pg_config
export PG_SRC=$(pwd)/postgresql_modified_for_babelfish-%{pgsrccommit}
export cmake=%{_bindir}/cmake
export PATH=%{pginstdir}/bin:$PATH

for ext in babelfishpg_money babelfishpg_common babelfishpg_tsql babelfishpg_tds
do
	%{__make} -C contrib/$ext DESTDIR=%{buildroot} install
done

%files
%defattr(-,root,root,-)
%license LICENSE.PostgreSQL LICENSE.Apache2 NOTICE
%doc README.md
%{pginstdir}/lib/babelfishpg_*.so
%{pginstdir}/share/extension/babelfishpg_*.control
%{pginstdir}/share/extension/babelfishpg_*.sql
%{pginstdir}/share/extension/fixeddecimal*.sql

%changelog
* Mon Oct 5 2026 Devrim Gunduz <devrim@gunduz.org> - 6.3.0-6PGDG
- Build against the Babelfish engine in /usr/babelfish-18 (was
  /usr/pgsql-18-babelfish).

* Mon Oct 5 2026 Devrim Gunduz <devrim@gunduz.org> - 6.3.0-5PGDG
- Require the -server and -contrib subpackages of the Babelfish engine, which
  is now split into subpackages like the stock PostgreSQL packages.

* Mon Oct 5 2026 Devrim Gunduz <devrim@gunduz.org> - 6.3.0-4PGDG
- Generate the ANTLR sources (antlr/libantlr_tsql.a) before the parallel build
  of babelfishpg_tsql, whose objects include the generated TSqlLexer.h.

* Mon Oct 5 2026 Devrim Gunduz <devrim@gunduz.org> - 6.3.0-3PGDG
- Build and install against the new babelfish_postgresql18 engine package
  (own prefix) instead of stock PostgreSQL, which lacks the Babelfish
  hooks and headers.

* Mon Oct 5 2026 Devrim Gunduz <devrim@gunduz.org> - 6.3.0-2PGDG
- Add upstream commit 16eb0df3 to fix the build with newer GCC, glibc,
  OpenSSL and CMake:
  https://github.com/babelfish-for-postgresql/babelfish_extensions/commit/16eb0df35dd50ceeb7d54fbdc2b477259005b111

* Mon Oct 5 2026 Devrim Gunduz <devrim@gunduz.org> - 6.3.0-1PGDG
- Initial packaging for the PostgreSQL RPM Repository, for PostgreSQL 18 only.
