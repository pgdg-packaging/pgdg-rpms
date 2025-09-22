%undefine _package_note_file

# These are macros to be used with find_lang and other stuff
%global packageversion 180
%global pgpackageversion 18
%global prevmajorversion 17
%global sname postgresql
%global pgbaseinstdir	/usr/pgsql-%{pgmajorversion}

%global beta 0
%{?beta:%global __os_install_post /usr/lib/rpm/brp-compress}

%{!?enabletaptests:%global enabletaptests 1}
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
%{!?sdt:%global sdt 1}
%{!?selinux:%global selinux 1}
%{!?ssl:%global ssl 1}
%{!?test:%global test 1}
%{!?uuid:%global uuid 1}
%{!?xml:%global xml 1}

#Filter out some Perl "dependencies"
%global __requires_exclude ^perl\\((PostgresVersion|PostgresNode|RecursiveCopy|SimpleTee|TestLib|PostgreSQL::Test::BackgroundPsql)
%global __provides_exclude ^perl\\((PostgresVersion|PostgresNode|RecursiveCopy|SimpleTee|TestLib|PostgreSQL::Test::BackgroundPsql)

Summary:	PostgreSQL client programs and libraries
Name:		%{sname}%{pgmajorversion}
Version:	18
%if 0%{?suse_version} >= 1500
# SuSE upstream packages have release numbers like 150200.5.19.1
# which overrides our packages. Increase our release number on SuSE.
Release:	rc1_4200002PGDG%{?dist}
%else
Release:	rc1_2PGDG%{?dist}
%endif
License:	PostgreSQL
Url:		https://www.postgresql.org/
Source0:	https://download.postgresql.org/pub/source/v%{version}rc1/postgresql-%{version}rc1.tar.bz2
Source4:	%{sname}-%{pgmajorversion}-Makefile.regress
Source5:	%{sname}-%{pgmajorversion}-pg_config.h
Source6:	%{sname}-%{pgmajorversion}-README.rpm-dist
Source7:	%{sname}-%{pgmajorversion}-ecpg_config.h
Source9:	%{sname}-%{pgmajorversion}-libs.conf
Source12:	https://www.postgresql.org/files/documentation/pdf/%{pgpackageversion}/%{sname}-%{pgpackageversion}-A4.pdf
%if 0%{?suse_version}
Source14:	%{sname}-%{pgmajorversion}.pam.suse
%else
Source14:	%{sname}-%{pgmajorversion}.pam
%endif
Source17:	%{sname}-%{pgmajorversion}-setup
Source10:	%{sname}-%{pgmajorversion}-check-db-dir
Source18:	%{sname}-%{pgmajorversion}.service
Source19:	%{sname}-%{pgmajorversion}-tmpfiles.d
Source20:	%{sname}-%{pgmajorversion}-sysusers.conf

Patch1:		%{sname}-%{pgmajorversion}-rpm-pgsql.patch
Patch3:		%{sname}-%{pgmajorversion}-conf.patch
Patch5:		%{sname}-%{pgmajorversion}-var-run-socket.patch
Patch6:		%{sname}-%{pgmajorversion}-perl-rpath.patch

BuildRequires:	perl glibc-devel bison >= 3.0.4 flex >= 2.6.1
BuildRequires:	gcc-c++ libcurl-devel >= 7.61.0
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

# This dependency is needed for Source 16:
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
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
%endif
%if 0%{?fedora} || 0%{?rhel}
BuildRequires:	llvm-devel => 17.0 clang-devel >= 17.0
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

%if %sdt
BuildRequires:	systemtap-sdt-devel
%endif

%if %selinux
# All supported distros have libselinux-devel package:
BuildRequires:	libselinux-devel >= 2.9
# SLES: SLES 15 does not have selinux-policy package.
# RHEL/Fedora has selinux-policy:
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	selinux-policy >= 3.4.3
%endif
%endif

%if %ssl
BuildRequires:	openssl-devel
%if 0%{?fedora} >= 41
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

BuildRequires:		systemd, systemd-devel
# We require this to be present for %%{_prefix}/lib/tmpfiles.d
Requires:		systemd
%if 0%{?suse_version} >= 1500
Requires(post):		systemd-sysvinit
%else
Requires(post):		systemd-sysv
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
%endif

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

Provides:	%{sname} >= %{version}-%{release}

%description
PostgreSQL is an advanced Object-Relational database management system (DBMS).
The base postgresql package contains the client programs that you'll need to
access a PostgreSQL DBMS server. These client programs can be located on the
same machine as the PostgreSQL server, or on a remote machine that accesses a
PostgreSQL server over a network connection. The PostgreSQL server can be found
in the postgresql%{pgmajorversion}-server sub-package.

If you want to manipulate a PostgreSQL database on a local or remote PostgreSQL
server, you need this package. You also need to install this package
if you're installing the postgresql%{pgmajorversion}-server package.

%package contrib
Summary:	Contributed source and binaries distributed with PostgreSQL
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Provides:	postgresql-contrib >= %{version}-%{release}

%description contrib
The postgresql%{pgmajorversion}-contrib package contains various extension
modules that are included in the PostgreSQL distribution.

%package devel
Summary:	PostgreSQL development header files and libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%if %icu
Requires:	libicu-devel
%endif

%if %llvm
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
Requires:	llvm17-devel clang17-devel
%endif
%if 0%{?fedora} || 0%{?rhel}
Requires:	llvm-devel => 17.0 clang-devel >= 17.0
%endif
%endif

%if %enabletaptests
BuildRequires:	perl-IPC-Run perl-Test-Harness perl-Test-Simple
Requires:	perl-IPC-Run
# SLES 15 does not have a separate perl-TimeHires package. It is part
# of the main perl package.
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	perl-Time-HiRes
%endif
%endif

Provides:	postgresql-devel >= %{version}-%{release}
Obsoletes:	libpq-devel <= 42.0

%description devel
The postgresql%{pgmajorversion}-devel package contains the header files and
libraries needed to compile C or C++ applications which will directly interact
with a PostgreSQL database management server. You need to install this package
if you want to develop applications which will interact with a PostgreSQL
server.

%package docs
Summary:	Extra documentation for PostgreSQL
Provides:	postgresql-docs >= %{version}-%{release}
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	docbook-style-xsl libxslt
%endif
%if 0%{?suse_version} >= 1499
BuildRequires:	docbook-xsl-stylesheets
%endif

%description docs
The postgresql%{pgmajorversion}-docs package includes the SGML source for the
documentation as well as the documentation in PDF format and some extra
documentation. Install this package if you want to help with the PostgreSQL
documentation project, or if you want to generate printed documentation. This
package also includes HTML version of the documentation.

%package ecpg-libs
Summary:	Run-time libraries for ECPG programs

%if 0%{?suse_version} >= 1500
Requires:	libopenssl1_1
%else
Requires:	openssl-libs >= 1.1.1k
%endif

%description ecpg-libs
The postgresql%{pgmajorversion}-ecpg-libs is used by programs built with ECPG
(Embedded PostgreSQL for C).

%package ecpg-devel
Summary:	Development files for ECPG (Embedded PostgreSQL for C)
Requires:	%{name}-ecpg-libs%{?_isa} = %{version}-%{release}

%if 0%{?suse_version} >= 1500
Requires:	libopenssl1_1
%else
Requires:	openssl-libs >= 1.1.1k
%endif

%description ecpg-devel
The postgresql%{pgmajorversion}-ecpg-devel package contains the necessary
files to build ECPG (Embedded PostgreSQL for C) programs. It includes the
development libraries and the preprocessor program ecpg.

%package libs
Summary:	The shared libraries required for any PostgreSQL clients
Provides:	postgresql-libs = %{pgmajorversion} libpq5 >= 10.0

%if 0%{?suse_version} >= 1500
Requires:	libopenssl1_1
%else
Requires:	openssl-libs >= 1.1.1k
%endif

%description libs
The postgresql%{pgmajorversion}-libs package provides the essential shared
libraries for any PostgreSQL client program or interface. You will need to
install this package to use any other PostgreSQL package or any clients that
need to connect to a PostgreSQL server.

%package libs-oauth
Summary:	The shared libraries required for any PostgreSQL clients - OAuth flow
Provides:	postgresql-libs-oauth = %{pgmajorversion}
Requires:	postgresql%{pgmajorversion}-libs%{?_isa} = %{version}-%{release}

%if 0%{?suse_version} >= 1500
Requires:	libcurl4
%else
Requires:	curl
%endif

%description libs-oauth
The postgresql%{pgmajorversion}-libs-oauth is an optional module for
postgresql%{pgmajorversion}-libs implementing the Device Authorization flow for
OAuth clients (RFC 8628). It is maintained as its own shared library in order
to isolate its dependency on libcurl. If a connection string allows the use of
OAuth, and the server asks for it, and a libpq client has not installed its own
custom OAuth flow, libpq will attempt to delay-load this module using dlopen()
and the following ABI. Failure to load results in a failed connection.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for PostgreSQL
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
Requires:	libLLVM17
%endif
%if 0%{?fedora} || 0%{?rhel}
Requires:	llvm => 17
%endif

Provides:	postgresql-llvmjit >= %{version}-%{release}

%description llvmjit
The postgresql%{pgmajorversion}-llvmjit package contains support for
just-in-time compiling parts of PostgreSQL queries. Using LLVM it compiles e.g.
expressions and tuple deforming into native code, with the goal of accelerating
analytics queries.
%endif

%if %plperl
%package plperl
Summary:	The Perl procedural language for PostgreSQL
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Provides:	postgresql-plperl >= %{version}-%{release}

%description plperl
The postgresql%{pgmajorversion}-plperl package contains the PL/Perl procedural
language, which is an extension to the PostgreSQL database server. Install this
if you want to write database functions in Perl.
%endif

%if %plpython3
%package plpython3
Summary:	The Python3 procedural language for PostgreSQL
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Provides:	postgresql-plpython3 >= %{version}-%{release}
%if 0%{?suse_version} >= 1500
Requires:	python3-base
%else
Requires:	python3-libs
%endif

%description plpython3
The postgresql%{pgmajorversion}-plpython3 package contains the PL/Python3
procedural language, which is an extension to the PostgreSQL database server.
Install this if you want to write database functions in Python 3.
%endif

%if %pltcl
%package pltcl
Summary:	The Tcl procedural language for PostgreSQL
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Requires:	tcl
Provides:	postgresql-pltcl >= %{version}-%{release}

%description pltcl
PostgreSQL is an advanced Object-Relational database management
system. The %{name}-pltcl package contains the PL/Tcl language
for the backend.
%endif

%package server
Summary:	The programs needed to create and run a PostgreSQL server
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
# pre/post stuff needs systemd too

%if 0%{?suse_version} >= 1500
Requires(post):		systemd
%else
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
%endif

Provides:	postgresql-server >= %{version}-%{release}

%description server
PostgreSQL is an advanced Object-Relational database management system (DBMS).
The postgresql%{pgmajorversion}-server package contains the programs needed to
create and run a PostgreSQL server, which will in turn allow you to create and
maintain PostgreSQL databases.

%if %test
%package test
Summary:	The test suite distributed with PostgreSQL
Requires:	%{name}-server%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}
Provides:	postgresql-test >= %{version}-%{release}

%description test
The postgresql%{pgmajorversion}-test package contains files needed for various
tests for the PostgreSQL database management system, including regression tests
and benchmarks.
%endif

%prep
%setup -q -n %{sname}-%{pgpackageversion}rc1

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

# We need to export these even though they are under the standard
# path. Buildfarm utilises ccache which may not be available on
# users' instances, and that breaks extension builds as shown here:
# https://www.postgresql.org/message-id/CACMiCkV%2BfQ4yAZqygyWx7ZQ8eWsj1AjoC6CGEUoyxY9jUm7paA%40mail.gmail.com
# Previously reported by Muralikrishna Bandaru.
export CLANG=%{_bindir}/clang LLVM_CONFIG=%{_bindir}/llvm-config

./configure --enable-rpath \
	--prefix=%{pgbaseinstdir} \
	--includedir=%{pgbaseinstdir}/include \
	--mandir=%{pgbaseinstdir}/share/man \
	--datadir=%{pgbaseinstdir}/share \
	--libdir=%{pgbaseinstdir}/lib \
	--with-lz4 \
	--with-zstd \
%if %beta
	--enable-debug \
	--enable-cassert \
%endif
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
%if %sdt
	--enable-dtrace \
%endif
%if %selinux
	--with-selinux \
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
	--with-system-tzdata=%{_datadir}/zoneinfo \
	--sysconfdir=/etc/sysconfig/pgsql \
	--docdir=%{pgbaseinstdir}/doc \
	--htmldir=%{pgbaseinstdir}/doc/html

cd src/backend
MAKELEVEL=0 %{__make} submake-generated-headers
cd ../..

# Have to hack makefile to put correct path into tutorial scripts
sed "s|C=\`pwd\`;|C=%{pgbaseinstdir}/lib/tutorial;|" < src/tutorial/Makefile > src/tutorial/GNUmakefile
%{__make} %{?_smp_mflags} -C src/tutorial NO_PGXS=1 all
%{__rm} -f src/tutorial/GNUmakefile

MAKELEVEL=0 %{__make} %{?_smp_mflags} all
%{__make} %{?_smp_mflags} -C doc all
%{__make} %{?_smp_mflags} -C contrib all
%if %uuid
%{__make} %{?_smp_mflags} -C contrib/uuid-ossp all
%endif


# run_testsuite WHERE
# -------------------
# Run 'make check' in WHERE path. When that command fails, return the logs
# given by PostgreSQL build system and set 'test_failure=1'.

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

%if %runselftest
	run_testsuite "src/test/regress"
	%{__make} clean -C "src/test/regress"
	run_testsuite "src/pl"
%if %plpython3
	run_testsuite "src/pl/plpython"
%endif
	run_testsuite "contrib"
%endif

%if %test
	pushd src/test/regress
	%{__make} all
	popd
%endif

%install
%{__rm} -rf %{buildroot}

%{__make} DESTDIR=%{buildroot} install

%if %plpython3
	# Install PL/Python3
	pushd src/pl/plpython
	%{__make} DESTDIR=%{buildroot} install
	popd
%endif

%{__mkdir} -p %{buildroot}%{pgbaseinstdir}/share/extensions/
%{__make} -C contrib DESTDIR=%{buildroot} install
%if %uuid
%{__make} -C contrib/uuid-ossp DESTDIR=%{buildroot} install
%endif

# multilib header hack; note pg_config.h is installed in two places!
# we only apply this to known Red Hat multilib arches, per bug #177564
case `uname -i` in
	i386 | x86_64 | ppc | ppc64 | s390 | s390x)
		%{__mv} %{buildroot}%{pgbaseinstdir}/include/pg_config.h %{buildroot}%{pgbaseinstdir}/include/pg_config_`uname -i`.h
		%{__install} -m 644 %{SOURCE5} %{buildroot}%{pgbaseinstdir}/include/pg_config.h
		%{__mv} %{buildroot}%{pgbaseinstdir}/include/server/pg_config.h %{buildroot}%{pgbaseinstdir}/include/server/pg_config_`uname -i`.h
		%{__install} -m 644 %{SOURCE5} %{buildroot}%{pgbaseinstdir}/include/server/pg_config.h
		%{__mv} %{buildroot}%{pgbaseinstdir}/include/ecpg_config.h %{buildroot}%{pgbaseinstdir}/include/ecpg_config_`uname -i`.h
		%{__install} -m 644 %{SOURCE7} %{buildroot}%{pgbaseinstdir}/include/ecpg_config.h
		;;
	*)
	;;
esac

# This is only for systemd supported distros:
# prep the setup script, including insertion of some values it needs
sed -e 's|^PGVERSION=.*$|PGVERSION=%{pgmajorversion}|' \
	-e 's|^PGENGINE=.*$|PGENGINE=%{pgbaseinstdir}/bin|' \
	-e 's|^PREVMAJORVERSION=.*$|PREVMAJORVERSION=%{prevmajorversion}|' \
	<%{SOURCE17} >postgresql-%{pgmajorversion}-setup
%{__install} -m 755 postgresql-%{pgmajorversion}-setup %{buildroot}%{pgbaseinstdir}/bin/postgresql-%{pgmajorversion}-setup
# Create a symlink of the setup script under $PATH
%{__mkdir} -p %{buildroot}%{_bindir}
%{__ln_s} ../../../../../../../../../../../../../../%{pgbaseinstdir}/bin/postgresql-%{pgmajorversion}-setup %{buildroot}%{_bindir}/

# prep the startup check script, including insertion of some values it needs
sed -e 's|^PGVERSION=.*$|PGVERSION=%{pgmajorversion}|' \
	-e 's|^PREVMAJORVERSION=.*$|PREVMAJORVERSION=%{prevmajorversion}|' \
	-e 's|^PGDOCDIR=.*$|PGDOCDIR=%{_pkgdocdir}|' \
	<%{SOURCE10} >%{sname}-%{pgmajorversion}-check-db-dir
touch -r %{SOURCE10} %{sname}-%{pgmajorversion}-check-db-dir
%{__install} -m 755 %{sname}-%{pgmajorversion}-check-db-dir %{buildroot}%{pgbaseinstdir}/bin/%{sname}-%{pgmajorversion}-check-db-dir

%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE18} %{buildroot}%{_unitdir}/%{sname}-%{pgmajorversion}.service

%if %pam
%{__install} -d %{buildroot}/etc/pam.d
%{__install} -m 644 %{SOURCE14} %{buildroot}/etc/pam.d/%{sname}
%endif

# Create the directory for sockets.
%{__install} -d -m 755 %{buildroot}%{_rundir}/%{sname}
# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}/%{_tmpfilesdir}
%{__install} -m 0644 %{SOURCE19} %{buildroot}/%{_tmpfilesdir}/%{sname}-%{pgmajorversion}.conf

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
%{__install} -d -m 700 %{buildroot}/var/lib/pgsql/%{pgmajorversion}/data

# backups of data go here...
%{__install} -d -m 700 %{buildroot}/var/lib/pgsql/%{pgmajorversion}/backups

# Create the multiple PostgreSQL version startup directory
%{__install} -d -m 700 %{buildroot}/etc/sysconfig/pgsql/%{pgmajorversion}

# Install linker conf file under postgresql installation directory.
# We will install the latest version via alternatives.
%{__install} -d -m 755 %{buildroot}%{pgbaseinstdir}/share/
%{__install} -m 700 %{SOURCE9} %{buildroot}%{pgbaseinstdir}/share/

# Install sysusers.d config file to allow rpm to create users/groups automatically.
%{__install} -m 0644 -D %{SOURCE20} %{buildroot}%{_sysusersdir}/%{sname}%{pgpackageversion}-pgdg.conf

%if %test
	# tests. There are many files included here that are unnecessary,
	# but include them anyway for completeness. We replace the original
	# Makefiles, however.
	%{__mkdir} -p %{buildroot}%{pgbaseinstdir}/lib/test
	%{__cp} -a src/test/regress %{buildroot}%{pgbaseinstdir}/lib/test
	%{__rm} -f %{buildroot}%{pgbaseinstdir}/lib/test/regress/refint.so
	%{__rm} -f %{buildroot}%{pgbaseinstdir}/lib/test/regress/autoinc.so
	# pg_regress binary should be only in one subpackage,
	# there will be a symlink from -test to -devel
	%{__rm} -f %{buildroot}%{pgbaseinstdir}/lib/test/regress/pg_regress
	%{__mkdir} -p %{buildroot}%{pgbaseinstdir}/lib/pgsql/test/regress/
	%{__ln_s} -f ../../pgxs/src/test/regress/pg_regress %{buildroot}%{pgbaseinstdir}/lib/test/regress/pg_regress
	pushd %{buildroot}%{pgbaseinstdir}/lib/test/regress
	strip *.so
	%{__rm} -f GNUmakefile Makefile *.o
	chmod 0755 pg_regress regress.so
	popd
	%{__cp} %{SOURCE4} %{buildroot}%{pgbaseinstdir}/lib/test/regress/Makefile
	chmod 0644 %{buildroot}%{pgbaseinstdir}/lib/test/regress/Makefile
%endif

%if %plpython3
# Quick hack:
%{__rm} -f %{buildroot}/%{pgbaseinstdir}/share/extension/*plpython2u*
%{__rm} -f %{buildroot}/%{pgbaseinstdir}/share/extension/*plpythonu-*
%{__rm} -f %{buildroot}/%{pgbaseinstdir}/share/extension/*_plpythonu.control
%endif

# Fix some more documentation
%{__cp} %{SOURCE6} README.rpm-dist
%{__mkdir} -p %{buildroot}%{pgbaseinstdir}/share/doc/html
%{__mv} doc/src/sgml/html doc
%{__mkdir} -p %{buildroot}%{pgbaseinstdir}/share/man/
%{__mv} doc/src/sgml/man1 doc/src/sgml/man3 doc/src/sgml/man7 %{buildroot}%{pgbaseinstdir}/share/man/
%{__rm} -rf %{buildroot}%{_docdir}/pgsql

# These file(s) should not be packaged:
%{__rm} %{buildroot}%{pgbaseinstdir}/lib/libpgfeutils.a

# Initialize file lists
%{__cp} /dev/null main.lst
%{__cp} /dev/null libs.lst
%{__cp} /dev/null server.lst
%{__cp} /dev/null devel.lst
%{__cp} /dev/null plperl.lst
%{__cp} /dev/null pltcl.lst
%{__cp} /dev/null plpython.lst
%{__cp} /dev/null pg_plpython3.lst
%{__cp} /dev/null pg_checksums.lst

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
cat initdb-%{pgmajorversion}.lang pg_ctl-%{pgmajorversion}.lang psql-%{pgmajorversion}.lang pg_dump-%{pgmajorversion}.lang pg_basebackup-%{pgmajorversion}.lang pgscripts-%{pgmajorversion}.lang pg_combinebackup-%{pgmajorversion}.lang pg_walsummary-%{pgmajorversion}.lang > pg_main.lst
cat postgres-%{pgmajorversion}.lang pg_resetwal-%{pgmajorversion}.lang pg_checksums-%{pgmajorversion}.lang pg_verifybackup-%{pgmajorversion}.lang pg_controldata-%{pgmajorversion}.lang plpgsql-%{pgmajorversion}.lang pg_test_timing-%{pgmajorversion}.lang pg_test_fsync-%{pgmajorversion}.lang pg_archivecleanup-%{pgmajorversion}.lang pg_waldump-%{pgmajorversion}.lang pg_rewind-%{pgmajorversion}.lang pg_upgrade-%{pgmajorversion}.lang > pg_server.lst
%endif

%post server
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
   /bin/systemctl daemon-reload >/dev/null 2>&1 || :
   %if 0%{?suse_version} >= 1500
   %service_add_pre postgresql-%{pgpackageversion}.service
   %else
   %systemd_post %{sname}-%{pgpackageversion}.service
   %endif
fi

# postgres' .bash_profile.
# We now don't install .bash_profile as we used to in pre 9.0. Instead, use cat,
# so that package manager will be happy during upgrade to new major version.
echo "[ -f /etc/profile ] && source /etc/profile
PGDATA=/var/lib/pgsql/%{pgmajorversion}/data
export PGDATA
# If you want to customize your settings,
# Use the file below. This is not overridden
# by the RPMS.
[ -f /var/lib/pgsql/.pgsql_profile ] && source /var/lib/pgsql/.pgsql_profile" > /var/lib/pgsql/.bash_profile
chown postgres: /var/lib/pgsql/.bash_profile
chmod 700 /var/lib/pgsql/.bash_profile

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

# Create alternatives entries for common binaries and man files
%post
%{_sbindir}/update-alternatives --install %{_bindir}/psql pgsql-psql %{pgbaseinstdir}/bin/psql %{packageversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/clusterdb pgsql-clusterdb %{pgbaseinstdir}/bin/clusterdb %{packageversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/createdb pgsql-createdb %{pgbaseinstdir}/bin/createdb %{packageversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/createuser pgsql-createuser %{pgbaseinstdir}/bin/createuser %{packageversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/dropdb pgsql-dropdb %{pgbaseinstdir}/bin/dropdb %{packageversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/dropuser pgsql-dropuser %{pgbaseinstdir}/bin/dropuser %{packageversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/pg_basebackup pgsql-pg_basebackup %{pgbaseinstdir}/bin/pg_basebackup %{packageversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/pg_combinebackup pgsql-pg_combinebackup %{pgbaseinstdir}/bin/pg_combinebackup %{packageversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/pg_createsubscriber pgsql-pg_createsubscriber %{pgbaseinstdir}/bin/pg_createsubscriber %{packageversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/pg_dump pgsql-pg_dump %{pgbaseinstdir}/bin/pg_dump %{packageversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/pg_dumpall pgsql-pg_dumpall %{pgbaseinstdir}/bin/pg_dumpall %{packageversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/pg_restore pgsql-pg_restore %{pgbaseinstdir}/bin/pg_restore %{packageversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/pg_walsummary pgsql-pg_walsummary %{pgbaseinstdir}/bin/pg_walsummary %{packageversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/reindexdb pgsql-reindexdb %{pgbaseinstdir}/bin/reindexdb %{packageversion}0
%{_sbindir}/update-alternatives --install %{_bindir}/vacuumdb pgsql-vacuumdb %{pgbaseinstdir}/bin/vacuumdb %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/clusterdb.1 pgsql-clusterdbman %{pgbaseinstdir}/share/man/man1/clusterdb.1 %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/createdb.1 pgsql-createdbman %{pgbaseinstdir}/share/man/man1/createdb.1 %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/createuser.1 pgsql-createuserman %{pgbaseinstdir}/share/man/man1/createuser.1 %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/dropdb.1 pgsql-dropdbman %{pgbaseinstdir}/share/man/man1/dropdb.1 %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/dropuser.1 pgsql-dropuserman %{pgbaseinstdir}/share/man/man1/dropuser.1 %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/pg_basebackup.1 pgsql-pg_basebackupman %{pgbaseinstdir}/share/man/man1/pg_basebackup.1 %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/pg_combinebackup.1 pgsql-pg_combinebackupman %{pgbaseinstdir}/share/man/man1/pg_combinebackup.1 %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/pg_createsubscriber.1 pgsql-pg_createsubscriberman %{pgbaseinstdir}/share/man/man1/pg_createsubscriber.1 %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/pg_dump.1 pgsql-pg_dumpman %{pgbaseinstdir}/share/man/man1/pg_dump.1 %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/pg_dumpall.1 pgsql-pg_dumpallman %{pgbaseinstdir}/share/man/man1/pg_dumpall.1 %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/pg_restore.1 pgsql-pg_restoreman %{pgbaseinstdir}/share/man/man1/pg_restore.1 %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/pg_walsummary.1 pgsql-pg_walsummaryman %{pgbaseinstdir}/share/man/man1/pg_walsummary.1 %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/psql.1 pgsql-psqlman %{pgbaseinstdir}/share/man/man1/psql.1 %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/reindexdb.1 pgsql-reindexdbman %{pgbaseinstdir}/share/man/man1/reindexdb.1 %{packageversion}0
%{_sbindir}/update-alternatives --install %{_mandir}/man1/vacuumdb.1 pgsql-vacuumdbman %{pgbaseinstdir}/share/man/man1/vacuumdb.1 %{packageversion}0

%post libs
%{_sbindir}/update-alternatives --install /etc/ld.so.conf.d/%{sname}-pgdg-libs.conf pgsql-ld-conf %{pgbaseinstdir}/share/%{sname}-%{pgmajorversion}-libs.conf %{packageversion}0
/sbin/ldconfig

# Drop alternatives entries for common binaries and man files
%postun
if [ "$1" -eq 0 ]
  then
	# Only remove these links if the package is completely removed from the system (vs.just being upgraded)
	%{_sbindir}/update-alternatives --remove pgsql-psql		%{pgbaseinstdir}/bin/psql
	%{_sbindir}/update-alternatives --remove pgsql-clusterdb	%{pgbaseinstdir}/bin/clusterdb
	%{_sbindir}/update-alternatives --remove pgsql-clusterdbman	%{pgbaseinstdir}/share/man/man1/clusterdb.1
	%{_sbindir}/update-alternatives --remove pgsql-createdb		%{pgbaseinstdir}/bin/createdb
	%{_sbindir}/update-alternatives --remove pgsql-createdbman	%{pgbaseinstdir}/share/man/man1/createdb.1
	%{_sbindir}/update-alternatives --remove pgsql-createuser	%{pgbaseinstdir}/bin/createuser
	%{_sbindir}/update-alternatives --remove pgsql-createuserman	%{pgbaseinstdir}/share/man/man1/createuser.1
	%{_sbindir}/update-alternatives --remove pgsql-dropdb		%{pgbaseinstdir}/bin/dropdb
	%{_sbindir}/update-alternatives --remove pgsql-dropdbman	%{pgbaseinstdir}/share/man/man1/dropdb.1
	%{_sbindir}/update-alternatives --remove pgsql-dropuser		%{pgbaseinstdir}/bin/dropuser
	%{_sbindir}/update-alternatives --remove pgsql-dropuserman	%{pgbaseinstdir}/share/man/man1/dropuser.1
	%{_sbindir}/update-alternatives --remove pgsql-pg_basebackup	%{pgbaseinstdir}/bin/pg_basebackup
	%{_sbindir}/update-alternatives --remove pgsql-pg_combinebackup	%{pgbaseinstdir}/bin/pg_combinebackup
	%{_sbindir}/update-alternatives --remove pgsql-pg_createsubscriber	%{pgbaseinstdir}/bin/pg_createsubscriber
	%{_sbindir}/update-alternatives --remove pgsql-pg_dump		%{pgbaseinstdir}/bin/pg_dump
	%{_sbindir}/update-alternatives --remove pgsql-pg_dumpall	%{pgbaseinstdir}/bin/pg_dumpall
	%{_sbindir}/update-alternatives --remove pgsql-pg_dumpallman	%{pgbaseinstdir}/share/man/man1/pg_dumpall.1
	%{_sbindir}/update-alternatives --remove pgsql-pg_basebackupman	%{pgbaseinstdir}/share/man/man1/pg_basebackup.1
	%{_sbindir}/update-alternatives --remove pgsql-pg_combinebackupman	%{pgbaseinstdir}/share/man/man1/pg_combinebackup.1
	%{_sbindir}/update-alternatives --remove pgsql-pg_createsubscriberman	%{pgbaseinstdir}/share/man/man1/pg_createsubscriber.1
	%{_sbindir}/update-alternatives --remove pgsql-pg_dumpman	%{pgbaseinstdir}/share/man/man1/pg_dump.1
	%{_sbindir}/update-alternatives --remove pgsql-pg_restore	%{pgbaseinstdir}/bin/pg_restore
	%{_sbindir}/update-alternatives --remove pgsql-pg_restoreman	%{pgbaseinstdir}/share/man/man1/pg_restore.1
	%{_sbindir}/update-alternatives --remove pgsql-pg_walsummary	%{pgbaseinstdir}/bin/pg_walsummary
	%{_sbindir}/update-alternatives --remove pgsql-psqlman		%{pgbaseinstdir}/share/man/man1/psql.1
	%{_sbindir}/update-alternatives --remove pgsql-reindexdb	%{pgbaseinstdir}/bin/reindexdb
	%{_sbindir}/update-alternatives --remove pgsql-reindexdbman	%{pgbaseinstdir}/share/man/man1/reindexdb.1
	%{_sbindir}/update-alternatives --remove pgsql-vacuumdb		%{pgbaseinstdir}/bin/vacuumdb
	%{_sbindir}/update-alternatives --remove pgsql-vacuumdbman	%{pgbaseinstdir}/share/man/man1/vacuumdb.1
  fi

%postun libs
if [ "$1" -eq 0 ]
  then
	%{_sbindir}/update-alternatives --remove pgsql-ld-conf		%{pgbaseinstdir}/share/%{sname}-%{pgmajorversion}-libs.conf
	/sbin/ldconfig
fi

# FILES section.

%files -f pg_main.lst
%defattr(-,root,root)
%if %llvm
# Install bitcode directory along with the main package,
# so that extensions can use this dir.
%dir %{pgbaseinstdir}/lib/bitcode
%endif
%doc doc/KNOWN_BUGS doc/MISSING_FEATURES
%doc COPYRIGHT
%doc README.rpm-dist
%{pgbaseinstdir}/bin/clusterdb
%{pgbaseinstdir}/bin/createdb
%{pgbaseinstdir}/bin/createuser
%{pgbaseinstdir}/bin/dropdb
%{pgbaseinstdir}/bin/dropuser
%{pgbaseinstdir}/bin/pgbench
%{pgbaseinstdir}/bin/pg_basebackup
%{pgbaseinstdir}/bin/pg_combinebackup
%{pgbaseinstdir}/bin/pg_config
%{pgbaseinstdir}/bin/pg_createsubscriber
%{pgbaseinstdir}/bin/pg_dump
%{pgbaseinstdir}/bin/pg_dumpall
%{pgbaseinstdir}/bin/pg_isready
%{pgbaseinstdir}/bin/pg_receivewal
%{pgbaseinstdir}/bin/pg_restore
%{pgbaseinstdir}/bin/pg_waldump
%{pgbaseinstdir}/bin/pg_walsummary
%{pgbaseinstdir}/bin/psql
%{pgbaseinstdir}/bin/reindexdb
%{pgbaseinstdir}/bin/vacuumdb
%{pgbaseinstdir}/share/errcodes.txt
%{pgbaseinstdir}/share/man/man1/clusterdb.*
%{pgbaseinstdir}/share/man/man1/createdb.*
%{pgbaseinstdir}/share/man/man1/createuser.*
%{pgbaseinstdir}/share/man/man1/dropdb.*
%{pgbaseinstdir}/share/man/man1/dropuser.*
%{pgbaseinstdir}/share/man/man1/pgbench.1
%{pgbaseinstdir}/share/man/man1/pg_basebackup.*
%{pgbaseinstdir}/share/man/man1/pg_combinebackup.*
%{pgbaseinstdir}/share/man/man1/pg_config.*
%{pgbaseinstdir}/share/man/man1/pg_createsubscriber.*
%{pgbaseinstdir}/share/man/man1/pg_dump.*
%{pgbaseinstdir}/share/man/man1/pg_dumpall.*
%{pgbaseinstdir}/share/man/man1/pg_isready.*
%{pgbaseinstdir}/share/man/man1/pg_restore.*
%{pgbaseinstdir}/share/man/man1/pg_walsummary.*
%{pgbaseinstdir}/share/man/man1/psql.*
%{pgbaseinstdir}/share/man/man1/reindexdb.*
%{pgbaseinstdir}/share/man/man1/vacuumdb.*
%{pgbaseinstdir}/share/man/man3/*
%{pgbaseinstdir}/share/man/man7/*

%files contrib -f pg_contrib.lst
%defattr(-,root,root)
%doc %{pgbaseinstdir}/doc/extension/*.example
%{pgbaseinstdir}/lib/_int.so
%{pgbaseinstdir}/lib/amcheck.so
%{pgbaseinstdir}/lib/auth_delay.so
%{pgbaseinstdir}/lib/autoinc.so
%{pgbaseinstdir}/lib/auto_explain.so
%{pgbaseinstdir}/lib/basebackup_to_shell.so
%{pgbaseinstdir}/lib/basic_archive.so
%{pgbaseinstdir}/lib/bloom.so
%{pgbaseinstdir}/lib/btree_gin.so
%{pgbaseinstdir}/lib/btree_gist.so
%{pgbaseinstdir}/lib/citext.so
%{pgbaseinstdir}/lib/cube.so
%{pgbaseinstdir}/lib/dblink.so
%{pgbaseinstdir}/lib/earthdistance.so
%{pgbaseinstdir}/lib/file_fdw.so*
%{pgbaseinstdir}/lib/fuzzystrmatch.so
%{pgbaseinstdir}/lib/insert_username.so
%{pgbaseinstdir}/lib/isn.so
%{pgbaseinstdir}/lib/hstore.so
%if %plperl
%{pgbaseinstdir}/lib/hstore_plperl.so
%{pgbaseinstdir}/lib/jsonb_plperl.so
%{pgbaseinstdir}/share/extension/jsonb_plperl*.sql
%{pgbaseinstdir}/share/extension/jsonb_plperl*.control
%endif
%if %plpython3
%{pgbaseinstdir}/lib/hstore_plpython3.so
%{pgbaseinstdir}/lib/jsonb_plpython3.so
%{pgbaseinstdir}/lib/ltree_plpython3.so
%endif
%{pgbaseinstdir}/lib/lo.so
%{pgbaseinstdir}/lib/ltree.so
%{pgbaseinstdir}/lib/moddatetime.so
%{pgbaseinstdir}/lib/pageinspect.so
%{pgbaseinstdir}/lib/passwordcheck.so
%{pgbaseinstdir}/lib/pgcrypto.so
%{pgbaseinstdir}/lib/pgrowlocks.so
%{pgbaseinstdir}/lib/pgstattuple.so
%{pgbaseinstdir}/lib/pg_buffercache.so
%{pgbaseinstdir}/lib/pg_freespacemap.so
%{pgbaseinstdir}/lib/pg_logicalinspect.so
%{pgbaseinstdir}/lib/pg_overexplain.so
%{pgbaseinstdir}/lib/pg_prewarm.so
%{pgbaseinstdir}/lib/pg_stat_statements.so
%{pgbaseinstdir}/lib/pg_surgery.so
%{pgbaseinstdir}/lib/pg_trgm.so
%{pgbaseinstdir}/lib/pg_visibility.so
%{pgbaseinstdir}/lib/pg_walinspect.so
%{pgbaseinstdir}/lib/postgres_fdw.so
%{pgbaseinstdir}/lib/refint.so
%{pgbaseinstdir}/lib/seg.so
%if %ssl
%{pgbaseinstdir}/lib/sslinfo.so
%endif
%if %selinux
%{pgbaseinstdir}/lib/sepgsql.so
%{pgbaseinstdir}/share/contrib/sepgsql.sql
%endif
%{pgbaseinstdir}/lib/tablefunc.so
%{pgbaseinstdir}/lib/tcn.so
%{pgbaseinstdir}/lib/test_decoding.so
%{pgbaseinstdir}/lib/tsm_system_rows.so
%{pgbaseinstdir}/lib/tsm_system_time.so
%{pgbaseinstdir}/lib/unaccent.so
%if %xml
%{pgbaseinstdir}/lib/pgxml.so
%endif
%if %uuid
%{pgbaseinstdir}/lib/uuid-ossp.so
%endif
%{pgbaseinstdir}/share/extension/amcheck*
%{pgbaseinstdir}/share/extension/autoinc*
%{pgbaseinstdir}/share/extension/bloom*
%{pgbaseinstdir}/share/extension/btree_gin*
%{pgbaseinstdir}/share/extension/btree_gist*
%{pgbaseinstdir}/share/extension/citext*
%{pgbaseinstdir}/share/extension/cube*
%{pgbaseinstdir}/share/extension/dblink*
%{pgbaseinstdir}/share/extension/dict_int*
%{pgbaseinstdir}/share/extension/dict_xsyn*
%{pgbaseinstdir}/share/extension/earthdistance*
%{pgbaseinstdir}/share/extension/file_fdw*
%{pgbaseinstdir}/share/extension/fuzzystrmatch*
%{pgbaseinstdir}/share/extension/hstore.control
%{pgbaseinstdir}/share/extension/hstore--*.sql
%if %plperl
%{pgbaseinstdir}/share/extension/hstore_plperl*
%endif
%{pgbaseinstdir}/share/extension/insert_username*
%{pgbaseinstdir}/share/extension/intagg*
%{pgbaseinstdir}/share/extension/intarray*
%{pgbaseinstdir}/share/extension/isn*
%{pgbaseinstdir}/share/extension/lo*
%{pgbaseinstdir}/share/extension/ltree.control
%{pgbaseinstdir}/share/extension/ltree--*.sql
%{pgbaseinstdir}/share/extension/moddatetime*
%{pgbaseinstdir}/share/extension/pageinspect*
%{pgbaseinstdir}/share/extension/pg_buffercache*
%{pgbaseinstdir}/share/extension/pg_freespacemap*
%{pgbaseinstdir}/share/extension/pg_logicalinspect*
%{pgbaseinstdir}/share/extension/pg_prewarm*
%{pgbaseinstdir}/share/extension/pg_stat_statements*
%{pgbaseinstdir}/share/extension/pg_surgery*
%{pgbaseinstdir}/share/extension/pg_trgm*
%{pgbaseinstdir}/share/extension/pg_visibility*
%{pgbaseinstdir}/share/extension/pg_walinspect*
%{pgbaseinstdir}/share/extension/pgcrypto*
%{pgbaseinstdir}/share/extension/pgrowlocks*
%{pgbaseinstdir}/share/extension/pgstattuple*
%{pgbaseinstdir}/share/extension/postgres_fdw*
%{pgbaseinstdir}/share/extension/refint*
%{pgbaseinstdir}/share/extension/seg*
%if %ssl
%{pgbaseinstdir}/share/extension/sslinfo*
%endif
%{pgbaseinstdir}/share/extension/tablefunc*
%{pgbaseinstdir}/share/extension/tcn*
%{pgbaseinstdir}/share/extension/tsm_system_rows*
%{pgbaseinstdir}/share/extension/tsm_system_time*
%{pgbaseinstdir}/share/extension/unaccent*
%if %uuid
%{pgbaseinstdir}/share/extension/uuid-ossp*
%endif
%if %xml
%{pgbaseinstdir}/share/extension/xml2*
%endif
%{pgbaseinstdir}/bin/oid2name
%{pgbaseinstdir}/bin/pg_amcheck
%{pgbaseinstdir}/bin/pg_recvlogical
%{pgbaseinstdir}/bin/vacuumlo
%{pgbaseinstdir}/share/man/man1/pg_amcheck.1
%{pgbaseinstdir}/share/man/man1/oid2name.1
%{pgbaseinstdir}/share/man/man1/pg_recvlogical.1
%{pgbaseinstdir}/share/man/man1/vacuumlo.1

%files devel -f pg_devel.lst
%defattr(-,root,root)
%{pgbaseinstdir}/include/libpq*.h
%{pgbaseinstdir}/include/pg_config*.h
%{pgbaseinstdir}/include/postgres_ext.h
%{pgbaseinstdir}/include/internal/*
%{pgbaseinstdir}/include/libpq/*
%{pgbaseinstdir}/include/server/*

%{pgbaseinstdir}/lib/libpq.so
%{pgbaseinstdir}/lib/libpq.a
%{pgbaseinstdir}/lib/libpq-oauth.a
%{pgbaseinstdir}/lib/libpgcommon.a
%{pgbaseinstdir}/lib/libpgcommon_shlib.a
%{pgbaseinstdir}/lib/libpgport.a
%{pgbaseinstdir}/lib/libpgport_shlib.a
%{pgbaseinstdir}/lib/pgxs/*
%{pgbaseinstdir}/lib/pkgconfig/libpq.pc

%files docs
%defattr(-,root,root)
%doc doc/src/*
%doc *-A4.pdf
%doc src/tutorial
%doc doc/html

%files ecpg-libs -f ecpg.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/libecpg.so*
%{pgbaseinstdir}/lib/libecpg_compat.so*
%{pgbaseinstdir}/lib/libecpg.a
%{pgbaseinstdir}/lib/libecpg_compat.a
%{pgbaseinstdir}/lib/libpgtypes.a
%{pgbaseinstdir}/lib/libpgtypes.so*
%{pgbaseinstdir}/share/man/man1/ecpg.*

%files ecpg-devel
%defattr(-,root,root)
%{pgbaseinstdir}/bin/ecpg
%{pgbaseinstdir}/include/informix/*
%{pgbaseinstdir}/include/pgtypes*h
%{pgbaseinstdir}/include/ecpg*.h
%{pgbaseinstdir}/include/sql3types.h
%{pgbaseinstdir}/include/sqlca.h
%{pgbaseinstdir}/include/sqlda*.h
%{pgbaseinstdir}/lib/pkgconfig/libecpg*.pc
%{pgbaseinstdir}/lib/pkgconfig/libpgtypes.pc

%files libs -f pg_libpq5.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/libpq.so.*
%{pgbaseinstdir}/lib/libpqwalreceiver.so
%config(noreplace) %attr (644,root,root) %{pgbaseinstdir}/share/%{sname}-%{pgmajorversion}-libs.conf

%files libs-oauth
%defattr(-,root,root)
%{pgbaseinstdir}/lib/libpq-oauth-%{pgmajorversion}.so

%if %llvm
%files llvmjit
%defattr(-,root,root)
%{pgbaseinstdir}/lib/bitcode/*
%{pgbaseinstdir}/lib/llvmjit.so
%{pgbaseinstdir}/lib/llvmjit_types.bc
%endif

%if %plperl
%files plperl -f pg_plperl.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/bool_plperl.so
%{pgbaseinstdir}/lib/plperl.so
%{pgbaseinstdir}/share/extension/plperl*
%{pgbaseinstdir}/share/extension/bool_plperl*
%endif

%if %pltcl
%files pltcl -f pg_pltcl.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/pltcl.so
%{pgbaseinstdir}/share/extension/pltcl*
%endif

%if %plpython3
%files plpython3 -f pg_plpython3.lst
%{pgbaseinstdir}/share/extension/plpython3*
%{pgbaseinstdir}/lib/plpython3.so
%{pgbaseinstdir}/share/extension/*_plpython3u*
%endif

%files server -f pg_server.lst
%defattr(-,root,root)
%{pgbaseinstdir}/bin/%{sname}-%{pgmajorversion}-setup
%{_bindir}/%{sname}-%{pgmajorversion}-setup
%{pgbaseinstdir}/bin/%{sname}-%{pgmajorversion}-check-db-dir
%{_sysusersdir}/%{sname}%{pgpackageversion}-pgdg.conf
%{_tmpfilesdir}/%{sname}-%{pgmajorversion}.conf
%{_unitdir}/%{sname}-%{pgmajorversion}.service
%if %pam
%config(noreplace) /etc/pam.d/%{sname}
%endif
%attr (755,root,root) %dir /etc/sysconfig/pgsql
%{pgbaseinstdir}/bin/initdb
%{pgbaseinstdir}/bin/pg_archivecleanup
%{pgbaseinstdir}/bin/pg_checksums
%{pgbaseinstdir}/bin/pg_controldata
%{pgbaseinstdir}/bin/pg_ctl
%{pgbaseinstdir}/bin/pg_resetwal
%{pgbaseinstdir}/bin/pg_rewind
%{pgbaseinstdir}/bin/pg_test_fsync
%{pgbaseinstdir}/bin/pg_test_timing
%{pgbaseinstdir}/bin/pg_upgrade
%{pgbaseinstdir}/bin/pg_verifybackup
%{pgbaseinstdir}/bin/postgres
%{pgbaseinstdir}/share/man/man1/initdb.*
%{pgbaseinstdir}/share/man/man1/pg_archivecleanup.1
%{pgbaseinstdir}/share/man/man1/pg_checksums.*
%{pgbaseinstdir}/share/man/man1/pg_controldata.*
%{pgbaseinstdir}/share/man/man1/pg_ctl.*
%{pgbaseinstdir}/share/man/man1/pg_resetwal.*
%{pgbaseinstdir}/share/man/man1/pg_receivewal.*
%{pgbaseinstdir}/share/man/man1/pg_rewind.1
%{pgbaseinstdir}/share/man/man1/pg_test_fsync.1
%{pgbaseinstdir}/share/man/man1/pg_test_timing.1
%{pgbaseinstdir}/share/man/man1/pg_upgrade.1
%{pgbaseinstdir}/share/man/man1/pg_verifybackup.*
%{pgbaseinstdir}/share/man/man1/pg_waldump.1
%{pgbaseinstdir}/share/man/man1/postgres.*
%{pgbaseinstdir}/share/postgres.bki
%{pgbaseinstdir}/share/system_constraints.sql
%{pgbaseinstdir}/share/system_functions.sql
%{pgbaseinstdir}/share/system_views.sql
%{pgbaseinstdir}/share/*.sample
%{pgbaseinstdir}/share/timezonesets/*
%{pgbaseinstdir}/share/tsearch_data/*.affix
%{pgbaseinstdir}/share/tsearch_data/*.dict
%{pgbaseinstdir}/share/tsearch_data/*.ths
%{pgbaseinstdir}/share/tsearch_data/*.rules
%{pgbaseinstdir}/share/tsearch_data/*.stop
%{pgbaseinstdir}/share/tsearch_data/*.syn
%{pgbaseinstdir}/lib/dict_int.so
%{pgbaseinstdir}/lib/dict_snowball.so
%{pgbaseinstdir}/lib/dict_xsyn.so
%{pgbaseinstdir}/lib/euc2004_sjis2004.so
%{pgbaseinstdir}/lib/pgoutput.so
%{pgbaseinstdir}/lib/plpgsql.so
%dir %{pgbaseinstdir}/share/extension
%{pgbaseinstdir}/share/extension/plpgsql*

%dir %{pgbaseinstdir}/lib
%dir %{pgbaseinstdir}/share
%attr(700,postgres,postgres) %dir /var/lib/pgsql
%attr(700,postgres,postgres) %dir /var/lib/pgsql/%{pgmajorversion}
%attr(700,postgres,postgres) %dir /var/lib/pgsql/%{pgmajorversion}/data
%attr(700,postgres,postgres) %dir /var/lib/pgsql/%{pgmajorversion}/backups
%attr(755,postgres,postgres) %dir %{_rundir}/%{sname}

%{pgbaseinstdir}/lib/*_and_*.so
%{pgbaseinstdir}/share/information_schema.sql
%{pgbaseinstdir}/share/snowball_create.sql
%{pgbaseinstdir}/share/sql_features.txt

%if %test
%files test
%defattr(-,postgres,postgres)
%attr(-,postgres,postgres) %{pgbaseinstdir}/lib/test/*
%attr(-,postgres,postgres) %dir %{pgbaseinstdir}/lib/test
%endif

%changelog
* Sun Sep 21 2025 Devrim Gunduz <devrim@gunduz.org> - 18.0rc1-2PGDG
- Add sysusers.d config file to allow rpm to create users/groups automatically

* Tue Sep 2 2025 Devrim Gunduz <devrim@gunduz.org> - 18.0rc1-1PGDG
- Update to 18.0 RC1

* Sat Aug 23 2025 Devrim Gunduz <devrim@gunduz.org> - 18.0beta3-3PGDG
- Move ecpg binary to ecpg-devel and also rename ecpg package to ecpg-libs.
  Per discussion with Sandeep.

* Wed Aug 20 2025 Devrim Gunduz <devrim@gunduz.org> - 18.0beta3-2PGDG
- More fixes after 3faf5edd. Per report from Muralikrishna Bandaru.

* Tue Aug 12 2025 Devrim Gunduz <devrim@gunduz.org> - 18.0beta3-1PGDG
- Update to PostgreSQL 18 beta3

* Mon Aug 11 2025 Devrim Gunduz <devrim@gunduz.org> - 18.0beta2-2PGDG
- Fix a few issues mentioned at:
  https://github.com/pgdg-packaging/pgdg-rpms/issues/69

* Tue Jul 15 2025 Devrim Gunduz <devrim@gunduz.org> - 18.0beta2-1PGDG
- Update to PostgreSQL 18 beta2

* Wed May 14 2025 Devrim Gündüz <devrim@gunduz.org> - 18.0beta1-3PGDG
- Rebuild against LLVM 19 on RHEL 8

* Tue May 13 2025 Devrim Gunduz <devrim@gunduz.org> - 18.0beta1-2PGDG
- Add explicit calls to CLANG and LLVM_CONFIG back to fix extension
  builds. Per report from Muralikrishna Bandaru and
  https://www.postgresql.org/message-id/CACMiCkV%2BfQ4yAZqygyWx7ZQ8eWsj1AjoC6CGEUoyxY9jUm7paA%40mail.gmail.com

* Tue May 6 2025 Devrim Gunduz <devrim@gunduz.org> - 18.0beta1-1PGDG
- Update to PostgreSQL 18 beta1

* Mon Jul 1 2024 Devrim Gunduz <devrim@gunduz.org> - 18.0alpha-1PGDG
- Initial cut for PostgreSQL 18

