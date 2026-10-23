%global		sname libscrypt
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		libscryptinstdir %{pgdg_libscryptinstdir}

# The library is found through the rpath only (there is no ld.so.conf.d
# file), so it must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL libscrypt. Consumers require
# pgdg-libscrypt by name instead:
%global		__provides_exclude_from ^%{libscryptinstdir}/
%global		__requires_exclude ^libscrypt\\.so

%{!?runselftest:%global runselftest 0}

Name:		pgdg-%{sname}
Version:	1.22
Release:	1PGDG%{?dist}
Summary:	Library that implements the secure password hashing function "scrypt"
License:	BSD-2-Clause
URL:		https://github.com/technion/%{sname}
Source0:	https://github.com/technion/%{sname}/archive/v%{version}.tar.gz
# From the Fedora package:
Patch0:		0001-sysendian.h-fix-aliasing-violations.patch
Patch1:		0002-b64-fix-Wold-style-definition.patch
Patch2:		0003-crypto_scrypt-nosse-fix-aliasing-violations.patch

BuildRequires:	pgdg-srpm-macros >= 2.3.0
BuildRequires:	gcc make

%description
libscrypt is a shared library that implements scrypt() functionality, a
replacement for bcrypt().

This package installs libscrypt under %{libscryptinstdir}, for the
packages in the PostgreSQL RPM repository.

%package devel
Summary:	Development files for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{sname}.

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1

%build
export CFLAGS="%{optflags} -fPIC"
export LDFLAGS="%{build_ldflags} -Wl,-soname,libscrypt.so.0 -Wl,--version-script=libscrypt.version"
%{make_build}

%install
%{make_install} PREFIX=%{libscryptinstdir} LIBDIR=%{libscryptinstdir}/lib64 \
	INCLUDEDIR=%{libscryptinstdir}/include

%check
%if %runselftest
%{__make} check
%endif

%files
%license LICENSE
%doc README.md
%dir %{libscryptinstdir}
%dir %{libscryptinstdir}/lib64
%{libscryptinstdir}/lib64/%{sname}.so.0

%files devel
%{libscryptinstdir}/include/
%{libscryptinstdir}/lib64/%{sname}.so

%changelog
* Fri Oct 23 2026 Devrim Gunduz <devrim@gunduz.org> - 1.22-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-libscrypt, so that pg_pwhash does not need the EPEL libscrypt
  package on RHEL 8 and 9, and gets scrypt support on RHEL 10, where EPEL
  does not have libscrypt. Based on the Fedora spec file, including its
  patches. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422
