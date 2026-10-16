%undefine _package_note_file

%global sname	babelfish_postgresql
%global pgpackageversion	18
%global prevmajorversion	17

# PostgreSQL engine patched for Babelfish. Babelfish extensions only build and
# run against this engine, not against the stock PGDG server, so it is
# installed under its own prefix and can coexist with stock postgresqlNN.
%global bbfpginstdir	/usr/babelfish-%{pgmajorversion}

# Pinned commit of BABEL_6_3_STABLE__PG_18_7 (upstream has no tags for 6.x)
%global pgsrccommit	d4e1b9879d472cab700cc676d7c5eb1d54dae05f

%if 0%{?pgmajorversion} != 18
%{error:%{sname} is only packaged for PostgreSQL 18 for now}
%endif

%{!?enabletaptests:%global enabletaptests 0}
%{!?icu:%global icu 1}
%{!?kerberos:%global kerberos 1}
%{!?ldap:%global ldap 1}
%{!?libnuma:%global libnuma 1}
# RHEL 8 does not have io_uring support:
%if 0%{?rhel} == 8
%{!?liburing:%global liburing 0}
%else
%{!?liburing:%global liburing 1}
%endif
%{!?llvm:%global llvm 1}
%{!?nls:%global nls 1}
%{!?pam:%global pam 1}
%{!?plperl:%global plperl 1}
%{!?plpython3:%global plpython3 1}
%{!?pltcl:%global pltcl 1}
%{!?runselftest:%global runselftest 0}
%{!?ssl:%global ssl 1}
%{!?test:%global test 1}
%{!?uuid:%global uuid 1}
%{!?xml:%global xml 1}

# Filter out some Perl "dependencies"
%global __requires_exclude ^perl\\((PostgresVersion|PostgresNode|RecursiveCopy|SimpleTee|TestLib|PostgreSQL::Test::BackgroundPsql)
%global __provides_exclude ^perl\\((PostgresVersion|PostgresNode|RecursiveCopy|SimpleTee|TestLib|PostgreSQL::Test::BackgroundPsql)

Summary:	PostgreSQL client programs and libraries, patched for Babelfish
Name:		%{sname}%{pgmajorversion}
Version:	18.7
%if 0%{?suse_version} >= 1500
# SuSE upstream packages have release numbers like 150200.5.19.1
# which overrides our packages. Increase our release number on SuSE.
Release:	4200005PGDG%{?dist}
%else
Release:	8PGDG%{?dist}
%endif
License:	PostgreSQL
URL:		https://github.com/babelfish-for-postgresql/postgresql_modified_for_babelfish
Source0:	https://github.com/babelfish-for-postgresql/postgresql_modified_for_babelfish/archive/%{pgsrccommit}.tar.gz#/postgresql_modified_for_babelfish-%{pgsrccommit}.tar.gz
Source4:	%{sname}-%{pgmajorversion}-Makefile.regress
Source5:	%{sname}-%{pgmajorversion}-pg_config.h
Source6:	%{sname}-%{pgmajorversion}-README.rpm-dist
Source7:	%{sname}-%{pgmajorversion}-ecpg_config.h
# The PDF is built from the Babelfish source, so it is shipped locally.
Source12:	%{sname}-%{pgmajorversion}-A4.pdf
%if 0%{?suse_version}
Source14:	%{sname}-%{pgmajorversion}.pam.suse
%else
Source14:	%{sname}-%{pgmajorversion}.pam
%endif
Source10:	%{sname}-%{pgmajorversion}-check-db-dir
Source17:	%{sname}-%{pgmajorversion}-setup
Source18:	%{sname}-%{pgmajorversion}.service
Source19:	%{sname}-%{pgmajorversion}-tmpfiles.d
Source20:	%{sname}-%{pgmajorversion}-sysusers.conf

# Upstream PR #807 (merged to BABEL_6_X_DEV__PG_18_X): GCC 15 / C23 build fixes.
# Not in BABEL_6_3_STABLE__PG_18_7; drop once it is.
Patch0:		postgresql_modified_for_babelfish-%{version}-gcc15-c23.patch
Patch1:		%{sname}-%{pgmajorversion}-rpm-pgsql.patch
Patch3:		%{sname}-%{pgmajorversion}-conf.patch
Patch5:		%{sname}-%{pgmajorversion}-var-run-socket.patch
Patch6:		%{sname}-%{pgmajorversion}-perl-rpath.patch

BuildRequires:	perl glibc-devel bison >= 3.0.4 flex >= 2.6.1
BuildRequires:	gcc gcc-c++ make libcurl-devel >= 7.61.0
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	readline-devel zlib-devel >= 1.0.4
BuildRequires:	libxml2-devel libxslt-devel

# lz4 dependency
%if 0%{?suse_version} >= 1500
BuildRequires:	liblz4-devel
Requires:	liblz4-1
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	lz4-devel
Requires:	lz4-libs
%endif

# zstd dependency
%if 0%{?suse_version} >= 1500
BuildRequires:	libzstd-devel >= 1.4.0
Requires:	libzstd1 >= 1.4.0
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	libzstd-devel >= 1.4.0
Requires:	libzstd >= 1.4.0
%endif

%if 0%{?fedora} || 0%{?rhel}
BuildRequires:	perl-generators
%endif

Requires:	/sbin/ldconfig

%if %icu
BuildRequires:	libicu-devel
Requires:	libicu
%endif

%if %kerberos
BuildRequires:	krb5-devel
BuildRequires:	e2fsprogs-devel
%endif

%if %ldap
%if 0%{?suse_version} >= 1500
BuildRequires:	openldap2-devel
%else
BuildRequires:	openldap-devel
%endif
%endif

%if %libnuma
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	numactl-devel
Requires:	numactl-libs
%else
BuildRequires:	libnuma-devel
Requires:	libnuma1
%endif
%endif

%if %liburing
BuildRequires:	liburing-devel
%endif

%if %llvm
%if 0%{?suse_version} == 1500
BuildRequires:	llvm17-devel clang17-devel
%endif
%if 0%{?suse_version} == 1600
BuildRequires:	llvm19-devel clang19-devel
%endif
%if 0%{?amzn}
BuildRequires:	llvm-devel >= 15.0 clang-devel >= 15.0
%endif
%if ( 0%{?fedora} || 0%{?rhel} ) && !0%{?amzn}
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
%endif
%endif

%if %nls
BuildRequires:	gettext >= 0.19.8
%endif

%if %pam
BuildRequires:	pam-devel
%endif

%if %plperl
%if 0%{?fedora} || 0%{?rhel}
BuildRequires:	perl-devel
BuildRequires:	perl-ExtUtils-Embed
%else
BuildRequires:	perl
%endif
%endif

%if %plpython3
BuildRequires:	python3-devel
%endif

%if %pltcl
BuildRequires:	tcl-devel
%endif

%if %ssl
%if 0%{?suse_version} >= 1500
Requires:	libopenssl3
BuildRequires:	libopenssl-3-devel
%endif
%if 0%{?fedora} >= 43 || 0%{?rhel} >= 9 || 0%{?amzn}
Requires:	openssl-libs >= 3.2.2
%endif
%if 0%{?fedora} >= 43 || 0%{?rhel} >= 9 || 0%{?amzn}
BuildRequires:	openssl-devel
%endif
%if 0%{?fedora} && 0%{?fedora} <= 44 && !0%{?amzn}
BuildRequires:	openssl-devel-engine
%endif
%endif

%if %uuid
%if 0%{?suse_version} >= 1500
BuildRequires:	uuid-devel
%else
BuildRequires:	libuuid-devel
%endif
%endif

%if %enabletaptests
BuildRequires:	perl-IPC-Run perl-Test-Simple
%endif

BuildRequires:		systemd, systemd-devel
# We require this to be present for %%{_prefix}/lib/tmpfiles.d
Requires:		systemd
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description
PostgreSQL is an advanced Object-Relational database management system (DBMS)
-- here the engine patched for Babelfish for PostgreSQL (SQL Server
compatibility), installed under %{bbfpginstdir}. It does not replace the stock
PostgreSQL packages. The base package contains the client programs that you'll
need to access a PostgreSQL DBMS server. The server can be found in the
%{name}-server sub-package.

It is required to build and run the babelfish_extensions packages.

%package contrib
Summary:	Contributed source and binaries distributed with PostgreSQL (Babelfish)
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-server%{?_isa} = %{version}-%{release}

%description contrib
The %{name}-contrib package contains various extension modules that are
included in the PostgreSQL distribution, built for the Babelfish engine.
Babelfish needs uuid-ossp from this package at run time.

%package devel
Summary:	PostgreSQL development header files and libraries (Babelfish)
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%if %icu
Requires:	libicu-devel
%endif

%if %llvm
%if 0%{?suse_version} == 1500
Requires:	llvm17-devel clang17-devel
%endif
%if 0%{?suse_version} == 1600
Requires:	llvm19-devel clang19-devel
%endif
%if 0%{?amzn}
Requires:	llvm-devel >= 15.0 clang-devel >= 15.0
%endif
%if ( 0%{?fedora} || 0%{?rhel} ) && !0%{?amzn}
Requires:	llvm-devel >= 19.0 clang-devel >= 19.0
%endif
%endif

%if %enabletaptests
Requires:	perl-IPC-Run
%endif

%description devel
The %{name}-devel package contains the header files and libraries needed to
compile C or C++ applications, and extensions (PGXS) such as
babelfish_extensions, against the Babelfish-patched PostgreSQL engine.

%package docs
Summary:	Extra documentation for PostgreSQL (Babelfish)
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	docbook-style-xsl docbook-dtds libxslt
%endif
%if 0%{?suse_version} >= 1499
BuildRequires:	docbook-xsl-stylesheets docbook_4 libxslt
%endif

%description docs
The %{name}-docs package includes the SGML source for the documentation as well
as the documentation in PDF format and some extra documentation. Install this
package if you want to help with the PostgreSQL documentation project, or if
you want to generate printed documentation. This package also includes HTML
version of the documentation.

%package ecpg-libs
Summary:	Run-time libraries for ECPG programs

%if 0%{?suse_version} == 1500
Requires:	libopenssl3
%endif
%if 0%{?suse_version} == 1600
Requires:	libopenssl3
%endif
%if 0%{?fedora} >= 43 || 0%{?rhel} >= 9 || 0%{?amzn}
Requires:	openssl-libs >= 3.2.2
%endif

%description ecpg-libs
The %{name}-ecpg-libs is used by programs built with ECPG
(Embedded PostgreSQL for C).

%package ecpg-devel
Summary:	Development files for ECPG (Embedded PostgreSQL for C)
Requires:	%{name}-ecpg-libs%{?_isa} = %{version}-%{release}

%description ecpg-devel
The %{name}-ecpg-devel package contains the necessary files to build ECPG
(Embedded PostgreSQL for C) programs. It includes the development libraries and
the preprocessor program ecpg.

%package libs
Summary:	The shared libraries required for any PostgreSQL clients (Babelfish)

%if 0%{?suse_version} == 1500
Requires:	libopenssl3
%endif
%if 0%{?suse_version} == 1600
Requires:	libopenssl3
%endif
%if 0%{?fedora} >= 43 || 0%{?rhel} >= 9 || 0%{?amzn}
Requires:	openssl-libs >= 3.2.2
%endif

%description libs
The %{name}-libs package provides the shared libraries for the client programs
of the Babelfish-patched PostgreSQL. They are found through the binaries'
rpath and are deliberately not added to the system linker path.

%package libs-oauth
Summary:	The shared libraries required for any PostgreSQL clients - OAuth flow
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%if 0%{?suse_version} >= 1500
Requires:	libcurl4
%else
Requires:	curl
%endif

%description libs-oauth
The %{name}-libs-oauth is an optional module for %{name}-libs implementing the
Device Authorization flow for OAuth clients (RFC 8628). It is maintained as its
own shared library in order to isolate its dependency on libcurl.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for PostgreSQL (Babelfish)
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} == 1500
Requires:	libLLVM17
%endif
%if 0%{?suse_version} == 1600
Requires:	libLLVM19
%endif
%if 0%{?amzn}
Requires:	llvm >= 15
%endif
%if ( 0%{?fedora} || 0%{?rhel} ) && !0%{?amzn}
Requires:	llvm >= 19
%endif

%description llvmjit
The %{name}-llvmjit package contains support for just-in-time compiling parts
of PostgreSQL queries. Using LLVM it compiles e.g. expressions and tuple
deforming into native code, with the goal of accelerating analytics queries.
%endif

%if %plperl
%package plperl
Summary:	The Perl procedural language for PostgreSQL (Babelfish)
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description plperl
The %{name}-plperl package contains the PL/Perl procedural language, which is
an extension to the PostgreSQL database server. Install this if you want to
write database functions in Perl.
%endif

%if %plpython3
%package plpython3
Summary:	The Python3 procedural language for PostgreSQL (Babelfish)
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
Requires:	python3-base
%else
Requires:	python3-libs
%endif

%description plpython3
The %{name}-plpython3 package contains the PL/Python3 procedural language,
which is an extension to the PostgreSQL database server. Install this if you
want to write database functions in Python 3.
%endif

%if %pltcl
%package pltcl
Summary:	The Tcl procedural language for PostgreSQL (Babelfish)
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Requires:	tcl

%description pltcl
The %{name}-pltcl package contains the PL/Tcl language for the backend.
%endif

%package server
Summary:	The programs needed to create and run a PostgreSQL server (Babelfish)
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	util-linux
%if %liburing
%if 0%{?fedora} || 0%{?rhel}
Requires:	liburing
%else
Requires:	liburing2
%endif
%endif
# for /sbin/ldconfig
Requires(post):		glibc
Requires(postun):	glibc
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd

Provides:	group(postgres) user(postgres)

%description server
The %{name}-server package contains the programs needed to create and run a
PostgreSQL server patched for Babelfish, which will in turn allow you to create
and maintain Babelfish databases. Use the babelfish_postgresql-%{pgmajorversion}
service and the babelfish_postgresql-%{pgmajorversion}-setup script.

%package static
Summary:	Statically linked PostgreSQL libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Statically linked PostgreSQL libraries that do not have dynamically linked
counterparts.

%if %test
%package test
Summary:	The test suite distributed with PostgreSQL (Babelfish)
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description test
The %{name}-test package contains files needed for various tests for the
PostgreSQL database management system, including regression tests and
benchmarks.
%endif

%prep
%setup -q -n postgresql_modified_for_babelfish-%{pgsrccommit}

%patch -P 0 -p1
%patch -P 1 -p0
%patch -P 3 -p0
%patch -P 5 -p0
%patch -P 6 -p0

%{__cp} -p %{SOURCE12} .

%build

# fail quickly and obviously if user tries to build as root
%if %runselftest
	if [ x"`id -u`" = x0 ]; then
		echo "postgresql's regression tests fail if run as root."
		echo "If you really need to build the RPM as root, use"
		echo "--define='runselftest 0' to skip the regression tests."
		exit 1
	fi
%endif

CFLAGS="${CFLAGS:-%optflags}"
# Strip out -ffast-math from CFLAGS....
CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`
%if 0%{?rhel}
LDFLAGS="-Wl,--as-needed"; export LDFLAGS
%endif

export CFLAGS

# Options follow upstream's contrib/README.md (libxml, uuid, icu, openssl) plus
# the usual PGDG RPM options. No SELinux (sepgsql) or SystemTap support in
# this engine package. rpath is used (like stock PGDG) instead of
# adding the libraries to the system linker path.
# We need to export these even though they are under the standard path, so
# that ccache from a buildfarm-like environment cannot break extension builds.
export CLANG=%{_bindir}/clang LLVM_CONFIG=%{_bindir}/llvm-config

./configure --enable-rpath \
	--prefix=%{bbfpginstdir} \
	--includedir=%{bbfpginstdir}/include \
	--mandir=%{bbfpginstdir}/share/man \
	--datadir=%{bbfpginstdir}/share \
	--libdir=%{bbfpginstdir}/lib \
	--with-lz4 \
	--with-zstd \
%if %enabletaptests
	--enable-tap-tests \
%endif
%if %icu
	--with-icu \
%endif
%if %kerberos
	--with-gssapi \
	--with-includes=%{_includedir} \
	--with-libraries=%{_libdir} \
%endif
%if %libnuma
	--with-libnuma \
%endif
%if %liburing
	--with-liburing \
%endif
%if %ldap
	--with-ldap \
%endif
%if %llvm
	--with-llvm \
%endif
%if %nls
	--enable-nls \
%endif
%if %pam
	--with-pam \
%endif
%if %plperl
	--with-perl \
%endif
%if %plpython3
	--with-python \
%endif
%if %pltcl
	--with-tcl \
	--with-tclconfig=%{_libdir} \
%endif
%if %ssl
	--with-openssl \
%endif
%if %uuid
	--with-uuid=e2fs \
%endif
%if %xml
	--with-libxml \
	--with-libxslt \
%endif
	--with-libcurl \
	--with-systemd \
	--with-extra-version=" (Babelfish)" \
	--with-system-tzdata=%{_datadir}/zoneinfo \
	--sysconfdir=/etc/sysconfig/pgsql \
	--docdir=%{bbfpginstdir}/doc \
	--htmldir=%{bbfpginstdir}/doc/html

MAKELEVEL=0 %{__make} -C src/backend generated-headers

# Have to hack makefile to put correct path into tutorial scripts
sed "s|C=\`pwd\`;|C=%{bbfpginstdir}/lib/tutorial;|" < src/tutorial/Makefile > src/tutorial/GNUmakefile
%{__make} %{?_smp_mflags} -C src/tutorial NO_PGXS=1 all
%{__rm} -f src/tutorial/GNUmakefile

# world-bin does not depend on the generated headers (errcodes.h etc.), unlike
# the plain "all" target, so they are built first (above).
# The Babelfish source is a git snapshot, so unlike the release tarballs it
# has no prebuilt man pages and HTML: build them here.
MAKELEVEL=0 %{__make} %{?_smp_mflags} world-bin
%{__make} %{?_smp_mflags} -C doc all
%if %uuid
%{__make} %{?_smp_mflags} -C contrib/uuid-ossp all
%endif

%if %test
	pushd src/test/regress
	%{__make} all
	popd
%endif

%install
%{__rm} -rf %{buildroot}

%{__make} DESTDIR=%{buildroot} install-world-bin

%if %plpython3
	# Install PL/Python3
	pushd src/pl/plpython
	%{__make} DESTDIR=%{buildroot} install
	popd
%endif

%{__mkdir} -p %{buildroot}%{bbfpginstdir}/share/pgsql/extension/
%{__make} -C contrib DESTDIR=%{buildroot} install
%if %uuid
%{__make} -C contrib/uuid-ossp DESTDIR=%{buildroot} install
%endif

# multilib header hack; note pg_config.h is installed in two places!
# we only apply this to known Red Hat multilib arches, per bug #177564
case `uname -i` in
	i386 | x86_64 | ppc | ppc64 | s390 | s390x)
		%{__mv} %{buildroot}%{bbfpginstdir}/include/pg_config.h %{buildroot}%{bbfpginstdir}/include/pg_config_`uname -i`.h
		%{__install} -m 644 %{SOURCE5} %{buildroot}%{bbfpginstdir}/include/pg_config.h
		%{__mv} %{buildroot}%{bbfpginstdir}/include/pgsql/server/pg_config.h %{buildroot}%{bbfpginstdir}/include/pgsql/server/pg_config_`uname -i`.h
		%{__install} -m 644 %{SOURCE5} %{buildroot}%{bbfpginstdir}/include/pgsql/server/pg_config.h
		%{__mv} %{buildroot}%{bbfpginstdir}/include/ecpg_config.h %{buildroot}%{bbfpginstdir}/include/ecpg_config_`uname -i`.h
		%{__install} -m 644 %{SOURCE7} %{buildroot}%{bbfpginstdir}/include/ecpg_config.h
		;;
	*)
	;;
esac

# prep the setup script, including insertion of some values it needs
sed -e 's|^PGVERSION=.*$|PGVERSION=%{pgmajorversion}|' \
	-e 's|^PGENGINE=.*$|PGENGINE=%{bbfpginstdir}/bin|' \
	-e 's|^PREVMAJORVERSION=.*$|PREVMAJORVERSION=%{prevmajorversion}|' \
	<%{SOURCE17} >%{sname}-%{pgmajorversion}-setup
%{__install} -m 755 %{sname}-%{pgmajorversion}-setup %{buildroot}%{bbfpginstdir}/bin/%{sname}-%{pgmajorversion}-setup
# Create a symlink of the setup script under $PATH
%{__mkdir} -p %{buildroot}%{_bindir}
%{__ln_s} ../..%{bbfpginstdir}/bin/%{sname}-%{pgmajorversion}-setup %{buildroot}%{_bindir}/

# prep the startup check script, including insertion of some values it needs
sed -e 's|^PGVERSION=.*$|PGVERSION=%{pgmajorversion}|' \
	-e 's|^PREVMAJORVERSION=.*$|PREVMAJORVERSION=%{prevmajorversion}|' \
	-e 's|^PGDOCDIR=.*$|PGDOCDIR=%{_pkgdocdir}|' \
	<%{SOURCE10} >%{sname}-%{pgmajorversion}-check-db-dir
touch -r %{SOURCE10} %{sname}-%{pgmajorversion}-check-db-dir
%{__install} -m 755 %{sname}-%{pgmajorversion}-check-db-dir %{buildroot}%{bbfpginstdir}/bin/%{sname}-%{pgmajorversion}-check-db-dir

%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE18} %{buildroot}%{_unitdir}/%{sname}-%{pgmajorversion}.service

%if %pam
# The server looks for the "postgresql" PAM service. Same content as the
# stock PGDG packages, which RPM allows to be shared.
%{__install} -d %{buildroot}/etc/pam.d
%{__install} -m 644 %{SOURCE14} %{buildroot}/etc/pam.d/postgresql
%endif

# Create the directory for sockets.
%{__install} -d -m 755 %{buildroot}%{_rundir}/postgresql
# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}/%{_tmpfilesdir}
%{__install} -m 0644 %{SOURCE19} %{buildroot}/%{_tmpfilesdir}/%{sname}-%{pgmajorversion}.conf

# Home directory of the postgres user, which is shared with stock PostgreSQL.
%{__install} -d -m 700 %{buildroot}/var/lib/pgsql

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
%{__install} -d -m 700 %{buildroot}/var/lib/babelfish/%{pgmajorversion}/data

# backups of data go here...
%{__install} -d -m 700 %{buildroot}/var/lib/babelfish/%{pgmajorversion}/backups

# Install sysusers.d config file to allow rpm to create users/groups automatically.
%{__install} -m 0644 -D %{SOURCE20} %{buildroot}%{_sysusersdir}/%{sname}%{pgpackageversion}-pgdg.conf

%if %test
	# tests. There are many files included here that are unnecessary,
	# but include them anyway for completeness. We replace the original
	# Makefiles, however.
	%{__mkdir} -p %{buildroot}%{bbfpginstdir}/lib/test
	%{__cp} -a src/test/regress %{buildroot}%{bbfpginstdir}/lib/test
	%{__rm} -f %{buildroot}%{bbfpginstdir}/lib/test/regress/refint.so
	%{__rm} -f %{buildroot}%{bbfpginstdir}/lib/test/regress/autoinc.so
	# pg_regress binary should be only in one subpackage,
	# there will be a symlink from -test to -devel
	%{__rm} -f %{buildroot}%{bbfpginstdir}/lib/test/regress/pg_regress
	%{__ln_s} -f ../../pgsql/pgxs/src/test/regress/pg_regress %{buildroot}%{bbfpginstdir}/lib/test/regress/pg_regress
	pushd %{buildroot}%{bbfpginstdir}/lib/test/regress
	strip *.so
	%{__rm} -f GNUmakefile Makefile *.o
	chmod 0755 pg_regress regress.so
	popd
	%{__cp} %{SOURCE4} %{buildroot}%{bbfpginstdir}/lib/test/regress/Makefile
	# The stock Makefile carries a placeholder bindir
	sed -i "s|--bindir='[^']*'|--bindir='%{bbfpginstdir}/bin/'|" %{buildroot}%{bbfpginstdir}/lib/test/regress/Makefile
	chmod 0644 %{buildroot}%{bbfpginstdir}/lib/test/regress/Makefile
%endif

%if %plpython3
# Quick hack:
%{__rm} -f %{buildroot}/%{bbfpginstdir}/share/pgsql/extension/*plpython2u*
%{__rm} -f %{buildroot}/%{bbfpginstdir}/share/pgsql/extension/*plpythonu-*
%{__rm} -f %{buildroot}/%{bbfpginstdir}/share/pgsql/extension/*_plpythonu.control
%endif

# Fix some more documentation
%{__cp} %{SOURCE6} README.rpm-dist
%{__mkdir} -p %{buildroot}%{bbfpginstdir}/share/doc/html
%{__mv} doc/src/sgml/html doc
%{__mkdir} -p %{buildroot}%{bbfpginstdir}/share/man/
%{__mv} doc/src/sgml/man1 doc/src/sgml/man3 doc/src/sgml/man7 %{buildroot}%{bbfpginstdir}/share/man/
%{__rm} -rf %{buildroot}%{_docdir}/pgsql

# Initialize file lists
%{__cp} /dev/null main.lst
%{__cp} /dev/null libs.lst
%{__cp} /dev/null server.lst
%{__cp} /dev/null devel.lst
%{__cp} /dev/null pg_plperl.lst
%{__cp} /dev/null pg_pltcl.lst
%{__cp} /dev/null pg_plpython3.lst

%if %nls
%find_lang ecpg-%{pgmajorversion}
%find_lang ecpglib6-%{pgmajorversion}
%find_lang initdb-%{pgmajorversion}
%find_lang libpq5-%{pgmajorversion}
%find_lang pg_amcheck-%{pgmajorversion}
%find_lang pg_archivecleanup-%{pgmajorversion}
%find_lang pg_basebackup-%{pgmajorversion}
%find_lang pg_checksums-%{pgmajorversion}
%find_lang pg_config-%{pgmajorversion}
%find_lang pg_combinebackup-%{pgmajorversion}
%find_lang pg_controldata-%{pgmajorversion}
%find_lang pg_ctl-%{pgmajorversion}
%find_lang pg_dump-%{pgmajorversion}
%find_lang pg_resetwal-%{pgmajorversion}
%find_lang pg_rewind-%{pgmajorversion}
%find_lang pg_test_fsync-%{pgmajorversion}
%find_lang pg_test_timing-%{pgmajorversion}
%find_lang pg_upgrade-%{pgmajorversion}
%find_lang pg_verifybackup-%{pgmajorversion}
%find_lang pg_waldump-%{pgmajorversion}
%find_lang pg_walsummary-%{pgmajorversion}
%find_lang pgscripts-%{pgmajorversion}
%if %plperl
%find_lang plperl-%{pgmajorversion}
cat plperl-%{pgmajorversion}.lang > pg_plperl.lst
%endif
%find_lang plpgsql-%{pgmajorversion}
%if %plpython3
%find_lang plpython-%{pgmajorversion}
cat plpython-%{pgmajorversion}.lang >> pg_plpython3.lst
%endif
%if %pltcl
%find_lang pltcl-%{pgmajorversion}
cat pltcl-%{pgmajorversion}.lang > pg_pltcl.lst
%endif
%find_lang postgres-%{pgmajorversion}
%find_lang psql-%{pgmajorversion}

cat pg_amcheck-%{pgmajorversion}.lang > pg_contrib.lst
cat libpq5-%{pgmajorversion}.lang > pg_libpq5.lst
cat pg_config-%{pgmajorversion}.lang > pg_devel.lst
cat ecpg-%{pgmajorversion}.lang ecpglib6-%{pgmajorversion}.lang > ecpg.lst

# find_lang lists only the .mo files; own the locale directory tree, too.
# -libs is the base of the dependency chain. -ecpg-libs does not require it.
find %{buildroot}%{bbfpginstdir}/share/locale -type d | sed "s|^%{buildroot}|%%dir |" > pg_localedirs.lst
cat pg_localedirs.lst >> pg_libpq5.lst
cat pg_localedirs.lst >> ecpg.lst
cat initdb-%{pgmajorversion}.lang pg_ctl-%{pgmajorversion}.lang psql-%{pgmajorversion}.lang pg_dump-%{pgmajorversion}.lang pg_basebackup-%{pgmajorversion}.lang pgscripts-%{pgmajorversion}.lang pg_combinebackup-%{pgmajorversion}.lang pg_walsummary-%{pgmajorversion}.lang > pg_main.lst
cat postgres-%{pgmajorversion}.lang pg_resetwal-%{pgmajorversion}.lang pg_checksums-%{pgmajorversion}.lang pg_verifybackup-%{pgmajorversion}.lang pg_controldata-%{pgmajorversion}.lang plpgsql-%{pgmajorversion}.lang pg_test_timing-%{pgmajorversion}.lang pg_test_fsync-%{pgmajorversion}.lang pg_archivecleanup-%{pgmajorversion}.lang pg_waldump-%{pgmajorversion}.lang pg_rewind-%{pgmajorversion}.lang pg_upgrade-%{pgmajorversion}.lang > pg_server.lst
%endif

%check
%if %runselftest
# run_testsuite WHERE
# -------------------
# Run 'make check' in WHERE path. When that command fails, print the logs
# given by PostgreSQL build system and set 'test_failure=1', so that the
# other test suites still run before the build fails.

test_failure=0

# Our postgresql.conf.sample enables the logging collector, but the TAP tests
# read the server log from the file that pg_ctl writes. Turn it off for the
# test instances.
echo "logging_collector = off" > pgdg_test.conf
export TEMP_CONFIG="$PWD/pgdg_test.conf"

run_testsuite()
{
	%{__make} -C "$1" MAX_CONNECTIONS=5 check && return 0

	test_failure=1

	(
		set +x
		echo "=== trying to find all regression.diffs files in build directory ==="
		find -name 'regression.diffs' | \
		while read line; do
			echo "=== make failure: $line ==="
			cat "$line"
		done
	)
}

	run_testsuite "src/test/regress"
	# src/pl includes PL/pgSQL, PL/Perl, PL/Python and PL/Tcl
	run_testsuite "src/pl"
	run_testsuite "contrib"

	if [ $test_failure -ne 0 ]; then
		echo "=== regression tests failed, see above ==="
		exit 1
	fi
%endif

%pre server
%sysusers_create_package %{name} %SOURCE20

%post server
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
   /bin/systemctl daemon-reload >/dev/null 2>&1 || :
   %systemd_post %{sname}-%{pgmajorversion}.service
fi

%preun server
if [ $1 -eq 0 ] ; then
	# Package removal, not upgrade
	/bin/systemctl --no-reload disable %{sname}-%{pgmajorversion}.service >/dev/null 2>&1 || :
	/bin/systemctl stop %{sname}-%{pgmajorversion}.service >/dev/null 2>&1 || :
fi

%postun server
/sbin/ldconfig
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
	# Package upgrade, not uninstall
	/bin/systemctl try-restart %{sname}-%{pgmajorversion}.service >/dev/null 2>&1 || :
fi

# Unlike the stock packages, there are no update-alternatives entries and no
# linker configuration file: everything stays under %{bbfpginstdir}.

# FILES section.

%files -f pg_main.lst
%defattr(-,root,root)
%if %llvm
# Install bitcode directory along with the main package,
# so that extensions can use this dir.
%dir %{bbfpginstdir}/lib/pgsql/bitcode
%endif
%dir %{bbfpginstdir}/bin
%dir %{bbfpginstdir}/share/man
%dir %{bbfpginstdir}/share/man/man1
%doc doc/KNOWN_BUGS doc/MISSING_FEATURES
%doc COPYRIGHT
%doc README.rpm-dist
%{bbfpginstdir}/bin/clusterdb
%{bbfpginstdir}/bin/createdb
%{bbfpginstdir}/bin/createuser
%{bbfpginstdir}/bin/dropdb
%{bbfpginstdir}/bin/dropuser
%{bbfpginstdir}/bin/pgbench
%{bbfpginstdir}/bin/pg_basebackup
%{bbfpginstdir}/bin/pg_combinebackup
%{bbfpginstdir}/bin/pg_config
%{bbfpginstdir}/bin/pg_createsubscriber
%{bbfpginstdir}/bin/pg_dump
%{bbfpginstdir}/bin/pg_dumpall
%{bbfpginstdir}/bin/pg_isready
%{bbfpginstdir}/bin/pg_receivewal
%{bbfpginstdir}/bin/pg_restore
%{bbfpginstdir}/bin/pg_waldump
%{bbfpginstdir}/bin/pg_walsummary
%{bbfpginstdir}/bin/psql
%{bbfpginstdir}/bin/reindexdb
%{bbfpginstdir}/bin/vacuumdb
%{bbfpginstdir}/share/pgsql/errcodes.txt
%{bbfpginstdir}/share/man/man1/clusterdb.*
%{bbfpginstdir}/share/man/man1/createdb.*
%{bbfpginstdir}/share/man/man1/createuser.*
%{bbfpginstdir}/share/man/man1/dropdb.*
%{bbfpginstdir}/share/man/man1/dropuser.*
%{bbfpginstdir}/share/man/man1/pgbench.1
%{bbfpginstdir}/share/man/man1/pg_basebackup.*
%{bbfpginstdir}/share/man/man1/pg_combinebackup.*
%{bbfpginstdir}/share/man/man1/pg_config.*
%{bbfpginstdir}/share/man/man1/pg_createsubscriber.*
%{bbfpginstdir}/share/man/man1/pg_dump.*
%{bbfpginstdir}/share/man/man1/pg_dumpall.*
%{bbfpginstdir}/share/man/man1/pg_isready.*
%{bbfpginstdir}/share/man/man1/pg_receivewal.*
%{bbfpginstdir}/share/man/man1/pg_restore.*
%{bbfpginstdir}/share/man/man1/pg_waldump.*
%{bbfpginstdir}/share/man/man1/pg_walsummary.*
%{bbfpginstdir}/share/man/man1/psql.*
%{bbfpginstdir}/share/man/man1/reindexdb.*
%{bbfpginstdir}/share/man/man1/vacuumdb.*
%{bbfpginstdir}/share/man/man3
%{bbfpginstdir}/share/man/man7

%files contrib -f pg_contrib.lst
%defattr(-,root,root)
%dir %{bbfpginstdir}/doc/pgsql
%dir %{bbfpginstdir}/doc/pgsql/extension
%doc %{bbfpginstdir}/doc/pgsql/extension/*.example
%{bbfpginstdir}/lib/pgsql/_int.so
%{bbfpginstdir}/lib/pgsql/amcheck.so
%{bbfpginstdir}/lib/pgsql/auth_delay.so
%{bbfpginstdir}/lib/pgsql/autoinc.so
%{bbfpginstdir}/lib/pgsql/auto_explain.so
%{bbfpginstdir}/lib/pgsql/basebackup_to_shell.so
%{bbfpginstdir}/lib/pgsql/basic_archive.so
%{bbfpginstdir}/lib/pgsql/bloom.so
%{bbfpginstdir}/lib/pgsql/btree_gin.so
%{bbfpginstdir}/lib/pgsql/btree_gist.so
%{bbfpginstdir}/lib/pgsql/citext.so
%{bbfpginstdir}/lib/pgsql/cube.so
%{bbfpginstdir}/lib/pgsql/dblink.so
%{bbfpginstdir}/lib/pgsql/earthdistance.so
%{bbfpginstdir}/lib/pgsql/file_fdw.so*
%{bbfpginstdir}/lib/pgsql/fuzzystrmatch.so
%{bbfpginstdir}/lib/pgsql/insert_username.so
%{bbfpginstdir}/lib/pgsql/isn.so
%{bbfpginstdir}/lib/pgsql/hstore.so
%if %plperl
%{bbfpginstdir}/lib/pgsql/hstore_plperl.so
%{bbfpginstdir}/lib/pgsql/jsonb_plperl.so
%{bbfpginstdir}/share/pgsql/extension/jsonb_plperl*.sql
%{bbfpginstdir}/share/pgsql/extension/jsonb_plperl*.control
%endif
%if %plpython3
%{bbfpginstdir}/lib/pgsql/hstore_plpython3.so
%{bbfpginstdir}/lib/pgsql/jsonb_plpython3.so
%{bbfpginstdir}/lib/pgsql/ltree_plpython3.so
%endif
%{bbfpginstdir}/lib/pgsql/lo.so
%{bbfpginstdir}/lib/pgsql/ltree.so
%{bbfpginstdir}/lib/pgsql/moddatetime.so
%{bbfpginstdir}/lib/pgsql/pageinspect.so
%{bbfpginstdir}/lib/pgsql/passwordcheck.so
%if %ssl
%{bbfpginstdir}/lib/pgsql/pgcrypto.so
%endif
%{bbfpginstdir}/lib/pgsql/pgrowlocks.so
%{bbfpginstdir}/lib/pgsql/pgstattuple.so
%{bbfpginstdir}/lib/pgsql/pg_buffercache.so
%{bbfpginstdir}/lib/pgsql/pg_freespacemap.so
%{bbfpginstdir}/lib/pgsql/pg_logicalinspect.so
%{bbfpginstdir}/lib/pgsql/pg_overexplain.so
%{bbfpginstdir}/lib/pgsql/pg_prewarm.so
%{bbfpginstdir}/lib/pgsql/pg_stat_statements.so
%{bbfpginstdir}/lib/pgsql/pg_surgery.so
%{bbfpginstdir}/lib/pgsql/pg_trgm.so
%{bbfpginstdir}/lib/pgsql/pg_visibility.so
%{bbfpginstdir}/lib/pgsql/pg_walinspect.so
%{bbfpginstdir}/lib/pgsql/postgres_fdw.so
%{bbfpginstdir}/lib/pgsql/refint.so
%{bbfpginstdir}/lib/pgsql/seg.so
%if %ssl
%{bbfpginstdir}/lib/pgsql/sslinfo.so
%endif
%{bbfpginstdir}/lib/pgsql/tablefunc.so
%{bbfpginstdir}/lib/pgsql/tcn.so
%{bbfpginstdir}/lib/pgsql/test_decoding.so
%{bbfpginstdir}/lib/pgsql/tsm_system_rows.so
%{bbfpginstdir}/lib/pgsql/tsm_system_time.so
%{bbfpginstdir}/lib/pgsql/unaccent.so
%if %xml
%{bbfpginstdir}/lib/pgsql/pgxml.so
%endif
%if %uuid
%{bbfpginstdir}/lib/pgsql/uuid-ossp.so
%endif
%{bbfpginstdir}/share/pgsql/extension/amcheck*
%{bbfpginstdir}/share/pgsql/extension/autoinc*
%{bbfpginstdir}/share/pgsql/extension/bloom*
%{bbfpginstdir}/share/pgsql/extension/btree_gin*
%{bbfpginstdir}/share/pgsql/extension/btree_gist*
%{bbfpginstdir}/share/pgsql/extension/citext*
%{bbfpginstdir}/share/pgsql/extension/cube*
%{bbfpginstdir}/share/pgsql/extension/dblink*
%{bbfpginstdir}/share/pgsql/extension/dict_int*
%{bbfpginstdir}/share/pgsql/extension/dict_xsyn*
%{bbfpginstdir}/share/pgsql/extension/earthdistance*
%{bbfpginstdir}/share/pgsql/extension/file_fdw*
%{bbfpginstdir}/share/pgsql/extension/fuzzystrmatch*
%{bbfpginstdir}/share/pgsql/extension/hstore.control
%{bbfpginstdir}/share/pgsql/extension/hstore--*.sql
%if %plperl
%{bbfpginstdir}/share/pgsql/extension/hstore_plperl*
%endif
%{bbfpginstdir}/share/pgsql/extension/insert_username*
%{bbfpginstdir}/share/pgsql/extension/intagg*
%{bbfpginstdir}/share/pgsql/extension/intarray*
%{bbfpginstdir}/share/pgsql/extension/isn*
%{bbfpginstdir}/share/pgsql/extension/lo*
%{bbfpginstdir}/share/pgsql/extension/ltree.control
%{bbfpginstdir}/share/pgsql/extension/ltree--*.sql
%{bbfpginstdir}/share/pgsql/extension/moddatetime*
%{bbfpginstdir}/share/pgsql/extension/pageinspect*
%{bbfpginstdir}/share/pgsql/extension/pg_buffercache*
%{bbfpginstdir}/share/pgsql/extension/pg_freespacemap*
%{bbfpginstdir}/share/pgsql/extension/pg_logicalinspect*
%{bbfpginstdir}/share/pgsql/extension/pg_prewarm*
%{bbfpginstdir}/share/pgsql/extension/pg_stat_statements*
%{bbfpginstdir}/share/pgsql/extension/pg_surgery*
%{bbfpginstdir}/share/pgsql/extension/pg_trgm*
%{bbfpginstdir}/share/pgsql/extension/pg_visibility*
%{bbfpginstdir}/share/pgsql/extension/pg_walinspect*
%if %ssl
%{bbfpginstdir}/share/pgsql/extension/pgcrypto*
%endif
%{bbfpginstdir}/share/pgsql/extension/pgrowlocks*
%{bbfpginstdir}/share/pgsql/extension/pgstattuple*
%{bbfpginstdir}/share/pgsql/extension/postgres_fdw*
%{bbfpginstdir}/share/pgsql/extension/refint*
%{bbfpginstdir}/share/pgsql/extension/seg*
%if %ssl
%{bbfpginstdir}/share/pgsql/extension/sslinfo*
%endif
%{bbfpginstdir}/share/pgsql/extension/tablefunc*
%{bbfpginstdir}/share/pgsql/extension/tcn*
%{bbfpginstdir}/share/pgsql/extension/tsm_system_rows*
%{bbfpginstdir}/share/pgsql/extension/tsm_system_time*
%{bbfpginstdir}/share/pgsql/extension/unaccent*
%if %uuid
%{bbfpginstdir}/share/pgsql/extension/uuid-ossp*
%endif
%if %xml
%{bbfpginstdir}/share/pgsql/extension/xml2*
%endif
%{bbfpginstdir}/bin/oid2name
%{bbfpginstdir}/bin/pg_amcheck
%{bbfpginstdir}/bin/pg_recvlogical
%{bbfpginstdir}/bin/vacuumlo
%{bbfpginstdir}/share/man/man1/pg_amcheck.1
%{bbfpginstdir}/share/man/man1/oid2name.1
%{bbfpginstdir}/share/man/man1/pg_recvlogical.1
%{bbfpginstdir}/share/man/man1/vacuumlo.1

%files devel -f pg_devel.lst
%defattr(-,root,root)
%dir %{bbfpginstdir}/include
%{bbfpginstdir}/include/libpq*.h
%{bbfpginstdir}/include/pg_config*.h
%{bbfpginstdir}/include/postgres_ext.h
%{bbfpginstdir}/include/pgsql/internal
%{bbfpginstdir}/include/libpq
%{bbfpginstdir}/include/pgsql/server

%{bbfpginstdir}/lib/libpq.so
%{bbfpginstdir}/lib/libpq.a
%{bbfpginstdir}/lib/libpq-oauth.a
%{bbfpginstdir}/lib/libpgcommon.a
%{bbfpginstdir}/lib/libpgcommon_shlib.a
%{bbfpginstdir}/lib/libpgport.a
%{bbfpginstdir}/lib/libpgport_shlib.a
%{bbfpginstdir}/lib/pgsql/pgxs
%dir %{bbfpginstdir}/lib/pkgconfig
%{bbfpginstdir}/lib/pkgconfig/libpq.pc

%files docs
%defattr(-,root,root)
%doc doc/src/*
%doc *-A4.pdf
%doc src/tutorial
%doc doc/html

%files ecpg-libs -f ecpg.lst
%defattr(-,root,root)
%dir %{bbfpginstdir}
%dir %{bbfpginstdir}/lib
%dir %{bbfpginstdir}/share
%dir %{bbfpginstdir}/share/man
%dir %{bbfpginstdir}/share/man/man1
%{bbfpginstdir}/lib/libecpg.so*
%{bbfpginstdir}/lib/libecpg_compat.so*
%{bbfpginstdir}/lib/libecpg.a
%{bbfpginstdir}/lib/libecpg_compat.a
%{bbfpginstdir}/lib/libpgtypes.a
%{bbfpginstdir}/lib/libpgtypes.so*
%{bbfpginstdir}/share/man/man1/ecpg.*

%files ecpg-devel
%defattr(-,root,root)
%dir %{bbfpginstdir}/bin
%{bbfpginstdir}/bin/ecpg
%dir %{bbfpginstdir}/include
%{bbfpginstdir}/include/pgsql/informix
%{bbfpginstdir}/include/pgtypes*h
%{bbfpginstdir}/include/ecpg*.h
%{bbfpginstdir}/include/sql3types.h
%{bbfpginstdir}/include/sqlca.h
%{bbfpginstdir}/include/sqlda*.h
%dir %{bbfpginstdir}/lib/pkgconfig
%{bbfpginstdir}/lib/pkgconfig/libecpg*.pc
%{bbfpginstdir}/lib/pkgconfig/libpgtypes.pc

%files libs -f pg_libpq5.lst
%defattr(-,root,root)
%dir %{bbfpginstdir}
%dir %{bbfpginstdir}/lib
%dir %{bbfpginstdir}/share
%{bbfpginstdir}/lib/libpq.so.*
%{bbfpginstdir}/lib/pgsql/libpqwalreceiver.so

%files libs-oauth
%defattr(-,root,root)
%{bbfpginstdir}/lib/libpq-oauth-%{pgmajorversion}.so

%if %llvm
%files llvmjit
%defattr(-,root,root)
%{bbfpginstdir}/lib/pgsql/bitcode/*
%{bbfpginstdir}/lib/pgsql/llvmjit.so
%{bbfpginstdir}/lib/pgsql/llvmjit_types.bc
%endif

%if %plperl
%files plperl -f pg_plperl.lst
%defattr(-,root,root)
%{bbfpginstdir}/lib/pgsql/bool_plperl.so
%{bbfpginstdir}/lib/pgsql/plperl.so
%{bbfpginstdir}/share/pgsql/extension/plperl*
%{bbfpginstdir}/share/pgsql/extension/bool_plperl*
%endif

%if %pltcl
%files pltcl -f pg_pltcl.lst
%defattr(-,root,root)
%{bbfpginstdir}/lib/pgsql/pltcl.so
%{bbfpginstdir}/share/pgsql/extension/pltcl*
%endif

%if %plpython3
%files plpython3 -f pg_plpython3.lst
%defattr(-,root,root)
%{bbfpginstdir}/share/pgsql/extension/plpython3*
%{bbfpginstdir}/lib/pgsql/plpython3.so
%{bbfpginstdir}/share/pgsql/extension/*_plpython3u*
%endif

%files server -f pg_server.lst
%defattr(-,root,root)
%{bbfpginstdir}/bin/%{sname}-%{pgmajorversion}-setup
%{_bindir}/%{sname}-%{pgmajorversion}-setup
%{bbfpginstdir}/bin/%{sname}-%{pgmajorversion}-check-db-dir
%{_sysusersdir}/%{sname}%{pgpackageversion}-pgdg.conf
%{_tmpfilesdir}/%{sname}-%{pgmajorversion}.conf
%{_unitdir}/%{sname}-%{pgmajorversion}.service
%if %pam
%config(noreplace) /etc/pam.d/postgresql
%endif
%{bbfpginstdir}/bin/initdb
%{bbfpginstdir}/bin/pg_archivecleanup
%{bbfpginstdir}/bin/pg_checksums
%{bbfpginstdir}/bin/pg_controldata
%{bbfpginstdir}/bin/pg_ctl
%{bbfpginstdir}/bin/pg_resetwal
%{bbfpginstdir}/bin/pg_rewind
%{bbfpginstdir}/bin/pg_test_fsync
%{bbfpginstdir}/bin/pg_test_timing
%{bbfpginstdir}/bin/pg_upgrade
%{bbfpginstdir}/bin/pg_verifybackup
%{bbfpginstdir}/bin/postgres
%{bbfpginstdir}/share/man/man1/initdb.*
%{bbfpginstdir}/share/man/man1/pg_archivecleanup.1
%{bbfpginstdir}/share/man/man1/pg_checksums.*
%{bbfpginstdir}/share/man/man1/pg_controldata.*
%{bbfpginstdir}/share/man/man1/pg_ctl.*
%{bbfpginstdir}/share/man/man1/pg_resetwal.*
%{bbfpginstdir}/share/man/man1/pg_rewind.1
%{bbfpginstdir}/share/man/man1/pg_test_fsync.1
%{bbfpginstdir}/share/man/man1/pg_test_timing.1
%{bbfpginstdir}/share/man/man1/pg_upgrade.1
%{bbfpginstdir}/share/man/man1/pg_verifybackup.*
%{bbfpginstdir}/share/man/man1/postgres.*
%{bbfpginstdir}/share/pgsql/postgres.bki
%{bbfpginstdir}/share/pgsql/system_constraints.sql
%{bbfpginstdir}/share/pgsql/system_functions.sql
%{bbfpginstdir}/share/pgsql/system_views.sql
%{bbfpginstdir}/share/pgsql/*.sample
%{bbfpginstdir}/share/pgsql/timezonesets
%dir %{bbfpginstdir}/share/pgsql/tsearch_data
%{bbfpginstdir}/share/pgsql/tsearch_data/*.affix
%{bbfpginstdir}/share/pgsql/tsearch_data/*.dict
%{bbfpginstdir}/share/pgsql/tsearch_data/*.ths
%{bbfpginstdir}/share/pgsql/tsearch_data/*.rules
%{bbfpginstdir}/share/pgsql/tsearch_data/*.stop
%{bbfpginstdir}/share/pgsql/tsearch_data/*.syn
%{bbfpginstdir}/lib/pgsql/dict_int.so
%{bbfpginstdir}/lib/pgsql/dict_snowball.so
%{bbfpginstdir}/lib/pgsql/dict_xsyn.so
%{bbfpginstdir}/lib/pgsql/euc2004_sjis2004.so
%{bbfpginstdir}/lib/pgsql/pgoutput.so
%{bbfpginstdir}/lib/pgsql/plpgsql.so
%dir %{bbfpginstdir}/share/pgsql/extension
%{bbfpginstdir}/share/pgsql/extension/plpgsql*

%attr(700,postgres,postgres) %dir /var/lib/pgsql
%attr(700,postgres,postgres) %dir /var/lib/babelfish
%attr(700,postgres,postgres) %dir /var/lib/babelfish/%{pgmajorversion}
%attr(700,postgres,postgres) %dir /var/lib/babelfish/%{pgmajorversion}/data
%attr(700,postgres,postgres) %dir /var/lib/babelfish/%{pgmajorversion}/backups
%attr(755,postgres,postgres) %dir %{_rundir}/postgresql

%{bbfpginstdir}/lib/pgsql/*_and_*.so
%{bbfpginstdir}/share/pgsql/information_schema.sql
%{bbfpginstdir}/share/pgsql/snowball_create.sql
%{bbfpginstdir}/share/pgsql/sql_features.txt

%files static
%{bbfpginstdir}/lib/libpgfeutils.a

%if %test
%files test
%defattr(-,postgres,postgres)
%attr(-,postgres,postgres) %{bbfpginstdir}/lib/test/*
%attr(-,postgres,postgres) %dir %{bbfpginstdir}/lib/test
%endif

%changelog
* Mon Oct 5 2026 Devrim Gunduz <devrim@gunduz.org> - 18.7-8PGDG
- Move PGDATA from /var/lib/pgsql/18-babelfish/data to
  /var/lib/babelfish/18/data (also the backups, initdb and pg_upgrade log
  directories and the setup script defaults). The postgres user's home
  directory stays /var/lib/pgsql.
- The prefix no longer contains "pgsql", so PostgreSQL installs the
  loadable modules and pgxs under lib/pgsql, the server and internal headers
  under include/pgsql, and the extension and other data files under
  share/pgsql. Adjust %%install and %%files accordingly.
- Build against openssl-devel only on Fedora 43 and later, RHEL 9 and later and
  Amazon Linux 2023.
- Require openssl-libs >= 3.2.2 on the same distributions.

* Mon Oct 5 2026 Devrim Gunduz <devrim@gunduz.org> - 18.7-7PGDG
- Install under /usr/babelfish-18 instead of /usr/pgsql-18-babelfish.

* Mon Oct 5 2026 Devrim Gunduz <devrim@gunduz.org> - 18.7-6PGDG
- Use the locally built A4 PDF documentation (Source12) instead of the one
  from postgresql.org.

* Mon Oct 5 2026 Devrim Gunduz <devrim@gunduz.org> - 18.7-5PGDG
- Rework the spec after the stock postgresql18 one: add the RPM-specific
  patches (rpm-pgsql, conf, var-run-socket, perl-rpath), the systemd unit
  (babelfish_postgresql-18.service), the setup and check-db-dir scripts,
  sysusers/tmpfiles/PAM files, README.rpm-dist and the multilib header
  wrappers. Split into base, contrib, devel, docs, ecpg-libs, ecpg-devel, libs,
  libs-oauth, llvmjit, plperl, plpython3, pltcl, server, static and test
  subpackages. The man pages and HTML docs are built from the git snapshot.
  Everything stays under /usr/pgsql-18-babelfish, with its own service and
  PGDATA (/var/lib/pgsql/18-babelfish/data), so it can coexist with the stock
  packages. No update-alternatives or linker path changes. No SELinux or
  SystemTap support.

* Mon Oct 5 2026 Devrim Gunduz <devrim@gunduz.org> - 18.7-4PGDG
- Replace the -std=gnu17 workaround with upstream PR #807, which declares
  the hook typedefs with real prototypes (C23 fix) and fixes a discarded
  const qualifier in format_type.c:
  https://github.com/babelfish-for-postgresql/postgresql_modified_for_babelfish/pull/807

* Mon Oct 5 2026 Devrim Gunduz <devrim@gunduz.org> - 18.7-3PGDG
- Build with -std=gnu17: GCC 15+ defaults to C23, where the unprototyped
  hook typedefs mean (void) and break calls with arguments.

* Mon Oct 5 2026 Devrim Gunduz <devrim@gunduz.org> - 18.7-2PGDG
- Build the generated headers (utils/errcodes.h etc.) before world-bin, which
  does not depend on them and failed with a missing utils/errcodes.h.

* Mon Oct 5 2026 Devrim Gunduz <devrim@gunduz.org> - 18.7-1PGDG
- Initial packaging of the PostgreSQL 18.7 engine patched for Babelfish
  (BABEL_6_3_STABLE__PG_18_7), installed under its own prefix. It is
  needed to build the babelfish_extensions package.
