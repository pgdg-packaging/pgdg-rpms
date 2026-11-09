%undefine _package_note_file
%global sname pgcopydb

Summary:	Automate pg_dump | pg_restore between two running Postgres servers
Name:		%{sname}
Version:	0.18
Release:	5PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/dimitri/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/dimitri/%{sname}
BuildRequires:	gcc make
# pgcopydb is a client tool, built once for all PostgreSQL versions. It
# uses the headers and the static libpgcommon/libpgport of one major
# version (%%{pgmajorversion}, set by the common build), and libpq5 at runtime:
BuildRequires:	postgresql%{pgmajorversion}-devel libpq5-devel
%if 0%{?rhel} >= 10
# RHEL 10 does not ship gc; use our package, installed under
# /usr/pgdg-gc, instead of the EPEL one:
BuildRequires:	pgdg-gc-devel
Requires:	pgdg-gc%{?_isa}
%global __requires_exclude ^libgc\\.so
%else
BuildRequires:	gc-devel
%endif
# The static libraries (libpgcommon, libpgport) are in the -static subpackage
# as of PostgreSQL 19:
%if %{pgmajorversion} >= 19
BuildRequires:	postgresql%{pgmajorversion}-static
%endif
BuildRequires:	bison flex krb5-devel libselinux-devel >= 2.9 sqlite-devel
# zstd dependency
%if 0%{?suse_version} >= 1500
BuildRequires:	libzstd-devel >= 1.4.0
Requires:	libzstd1 >= 1.4.0
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	libzstd-devel >= 1.4.0
Requires:	libzstd >= 1.4.0
%endif
# lz4 dependency
%if 0%{?suse_version} >= 1500
BuildRequires:	liblz4-devel
Requires:	liblz4-1
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	lz4-devel
Requires:	lz4-libs
%endif
# OpenSSL dependency
%if 0%{?suse_version} >= 1500
Requires:	libopenssl3
BuildRequires:	libopenssl-3-devel
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	numactl-devel
Requires:	numactl-libs
%else
BuildRequires:	libnuma-devel
Requires:	libnuma1
%endif
%if 0%{?fedora} >= 43 || 0%{?rhel} >= 8 || 0%{?amzn}
Requires:	openssl-libs >= 1.1.1k
BuildRequires:	openssl-devel
%endif
BuildRequires:	libxml2-devel libxslt-devel pam-devel
BuildRequires:	readline-devel zlib-devel
%if 0%{?fedora} >= 43 || (0%{?rhel} >= 8 && 0%{?rhel} < 10)
Requires:	gc
%endif
%if 0%{?suse_version} >= 1500
Requires:	libgc1
%endif
# psql, pg_dump and pg_restore, found through PG_CONFIG or PATH:
Requires:	postgresql
# Any libpq of the supported PostgreSQL versions (14 and later) has all the
# functions it uses; postgresqlNN-libs also provide libpq5:
Requires:	libpq5

%description
pgcopydb is a tool that automates running pg_dump | pg_restore between
two running Postgres servers. To make a copy of a database to another
server as quickly as possible, one would like to use the parallel
options of pg_dump and still be able to stream the data to as many
pg_restore jobs.

%prep
%setup -q -n %{sname}-%{version}
# Link to libpq5 by its full path, instead of the libpq of the PostgreSQL
# version used for the build, and do not add its rpath from pg_config
# --ldflags (the rest of it is in the RPM LDFLAGS already):
grep -q '^LIBS += -lpq$' src/bin/pgcopydb/Makefile
grep -q '^LIBS += $(shell $(PG_CONFIG) --ldflags)$' src/bin/pgcopydb/Makefile
%{__sed} -i -e 's|^LIBS += -lpq$|LIBS += %{_libdir}/libpq.so|' \
	-e '/^LIBS += $(shell $(PG_CONFIG) --ldflags)$/d' \
	src/bin/pgcopydb/Makefile
%if 0%{?rhel} >= 10
# Link to libgc by its full path, with an rpath, so that the EPEL library
# in /usr/lib64 is not used even if it is installed:
grep -q '^LIBS += -lgc$' src/bin/pgcopydb/Makefile
grep -q '^DEFAULT_CFLAGS += -Wformat$' src/bin/pgcopydb/Makefile
%{__sed} -i -e 's|^LIBS += -lgc$|LIBS += /usr/pgdg-gc/lib64/libgc.so -Wl,-rpath,/usr/pgdg-gc/lib64|' \
	-e 's|^DEFAULT_CFLAGS += -Wformat$|DEFAULT_CFLAGS += -Wformat -I/usr/pgdg-gc/include|' \
	src/bin/pgcopydb/Makefile
%endif

%build
# -Wl,-pie in pgcopydb's SECURITY_CFLAGS is redundant (RPM hardening specs
# handle PIE on RHEL) and broken on newer toolchains. Strip it unconditionally.
sed -i 's/ -Wl,-pie\b//g' src/bin/pgcopydb/Makefile

USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} BINDIR=%{_bindir} DESTDIR=%{buildroot} install

%files
%license LICENSE
%doc README.md
%{_bindir}/pgcopydb

%changelog
* Mon Nov 9 2026 Devrim Gunduz <devrim@gunduz.org> - 0.18-5PGDG
- Move to the common repository: pgcopydb is a client tool, and the same
  package was built for each PostgreSQL version, each one installing
  /usr/pgsql-NN/bin/pgcopydb. Install it to /usr/bin instead, and link it
  to libpq5. It finds psql, pg_dump and pg_restore through the PG_CONFIG
  environment variable or PATH, as before. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/562

* Sun Nov 8 2026 Devrim Gunduz <devrim@gunduz.org> - 0.18-4PGDG
- RHEL 10: Build against our new pgdg-gc package instead of the EPEL gc
  package, as RHEL 10 does not ship gc. Link to libgc by its full path,
  with an rpath, so that the EPEL library is not used even if it is
  installed. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/513

* Thu Sep 10 2026 Devrim Gündüz <devrim@gunduz.org> - 0.18-3PGDG
- Add missing BR
- Add postgresqlNN-static to BuildRequires for PostgreSQL 19+: libpgcommon
  and libpgport static libraries are in that subpackage now.

* Mon Aug 24 2026 Devrim Gündüz <devrim@gunduz.org> - 0.18-2PGDG
- Fix OpenSSL dependency for Amazon Linux 2023

* Sun Jun 28 2026 Devrim Gündüz <devrim@gunduz.org> - 0.18-1PGDG
- Update to 0.18 per changes described at:
  https://github.com/dimitri/pgcopydb/releases/tag/v0.18

* Thu Nov 20 2025 Devrim Gündüz <devrim@gunduz.org> - 0.17-4PGDG
- Modernise OpenSSL dependencies.

* Tue Feb 25 2025 Devrim Gündüz <devrim@gunduz.org> - 0.17-3PGDG
- Add missing BRs

* Fri Feb 21 2025 Devrim Gündüz <devrim@gunduz.org> - 0.17-2PGDG
- Remove redundant BR

* Mon Aug 19 2024 Devrim Gündüz <devrim@gunduz.org> - 0.17-1PGDG
- Update to 0.17 per changes described at:
  https://github.com/dimitri/pgcopydb/releases/tag/v0.17
  https://github.com/dimitri/pgcopydb/releases/tag/v0.16
- Fix permissions of the binary file. Fixes
  https://redmine.postgresql.org/issues/7899

* Mon Feb 5 2024 Devrim Gündüz <devrim@gunduz.org> - 0.15-1PGDG
- Update to 0.15

* Fri Sep 8 2023 Devrim Gündüz <devrim@gunduz.org> - 0.13-1PGDG
- Update to 0.13

* Sun Jul 23 2023 Devrim Gündüz <devrim@gunduz.org> - 0.12-1PGDG
- Update to 0.12
- Add PGDG branding

* Mon May 22 2023 Devrim Gündüz <devrim@gunduz.org> - 0.11-1
- Update to 0.11

* Wed Dec 14 2022 Devrim Gündüz <devrim@gunduz.org> - 0.10-1
- Update to 0.10

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 0.9-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon Oct 3 2022 - Devrim Gündüz <devrim@gunduz.org> 0.9.0-1
- Initial packaging for the PostgreSQL RPM repository
