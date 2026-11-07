%global		sname freetds
%global		freetdsinstdir /usr/pgdg-%{sname}

# The libraries are found through the rpath only (there is no ld.so.conf.d
# file), so they must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL libraries. Consumers require
# pgdg-freetds by name instead:
%global		__provides_exclude_from ^%{freetdsinstdir}/
%global		__requires_exclude ^lib(sybdb|ct)\\.so

Name:		pgdg-%{sname}
Version:	1.5.20
Release:	1PGDG%{?dist}
Summary:	Implementation of the TDS (Tabular DataStream) protocol
License:	LGPL-2.0-or-later AND GPL-2.0-or-later
URL:		https://www.freetds.org/
Source0:	https://www.freetds.org/files/stable/%{sname}-%{version}.tar.bz2

BuildRequires:	gcc make
BuildRequires:	gnutls-devel krb5-devel libgcrypt-devel readline-devel

%description
FreeTDS is a project to document and implement the TDS (Tabular
DataStream) protocol. TDS is used by Sybase(TM) and Microsoft(TM) for
client to database server communications. FreeTDS includes call
level interfaces for DB-Lib and CT-Lib.

This package installs FreeTDS under %{freetdsinstdir}, for the packages
in the PostgreSQL RPM repository. It reads its configuration from
%{_sysconfdir}/freetds.conf, if it exists, as the FreeTDS package of the
operating system or EPEL does.

%package devel
Summary:	Header files and development libraries for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for %{name}.

%prep
%setup -q -n %{sname}-%{version}

%build
# The ODBC driver is not built: tds_fdw only uses DB-Lib.
%configure \
	--prefix=%{freetdsinstdir} \
	--exec-prefix=%{freetdsinstdir} \
	--bindir=%{freetdsinstdir}/bin \
	--libdir=%{freetdsinstdir}/lib64 \
	--includedir=%{freetdsinstdir}/include \
	--datarootdir=%{freetdsinstdir}/share \
	--mandir=%{freetdsinstdir}/share/man \
	--docdir=%{freetdsinstdir}/share/doc \
	--sysconfdir=%{_sysconfdir} \
	--disable-dependency-tracking \
	--disable-static \
	--disable-odbc \
	--with-tdsver="auto" \
	--enable-msdblib \
	--enable-sybase-compat \
	--with-gnutls \
	--enable-krb5
%{__make} %{?_smp_mflags}

%install
%{__make} install DESTDIR=%{buildroot}
%{__rm} -f %{buildroot}%{freetdsinstdir}/lib64/*.la
%{__rm} -rf %{buildroot}%{freetdsinstdir}/share/doc
# osql is a script for the ODBC driver, which is not built:
%{__rm} -f %{buildroot}%{freetdsinstdir}/bin/osql
%{__rm} -f %{buildroot}%{freetdsinstdir}/share/man/man1/{osql,bsqlodbc}.1
# Do not ship the configuration files: the FreeTDS package of the OS or
# EPEL owns them, and FreeTDS works without them. They are installed as
# examples instead:
%{__mkdir} -p examples
%{__mv} %{buildroot}%{_sysconfdir}/*.conf examples/
%{__chmod} 644 examples/*

%files
%license COPYING.txt COPYING_LIB.txt
%doc AUTHORS.md NEWS.md README.md examples
%dir %{freetdsinstdir}
%{freetdsinstdir}/bin/
%dir %{freetdsinstdir}/lib64
%{freetdsinstdir}/lib64/lib*.so.*
%{freetdsinstdir}/share/

%files devel
%{freetdsinstdir}/include/
%{freetdsinstdir}/lib64/lib*.so

%changelog
* Fri Nov 6 2026 Devrim Gunduz <devrim@gunduz.org> - 1.5.20-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-freetds, so that tds_fdw does not need the EPEL freetds
  package on RHEL. Based on the Fedora spec file. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/513
