%global		sname libssh2
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		libssh2instdir %{pgdg_libssh2instdir}

# The library is found through the rpath only (there is no ld.so.conf.d
# file), so it must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL libssh2. Consumers require
# pgdg-libssh2 by name instead:
%global		__provides_exclude_from ^%{libssh2instdir}/
%global		__requires_exclude ^libssh2\\.so

# OpenSSL ENGINE support is deprecated on RHEL 10:
%if 0%{?rhel} >= 10
%global _preprocessor_defines %{?_preprocessor_defines} -DOPENSSL_NO_ENGINE
%endif

%{!?runselftest:%global runselftest 0}

Name:		pgdg-%{sname}
Version:	1.11.1
Release:	1PGDG%{?dist}
Summary:	A library implementing the SSH2 protocol
License:	BSD-3-Clause
URL:		https://www.libssh2.org/
Source0:	https://libssh2.org/download/%{sname}-%{version}.tar.gz
# Security fixes from the Fedora package:
# CVE-2026-7598: integer overflow via large username or password arguments
# https://github.com/libssh2/libssh2/pull/1858
Patch0:		%{sname}-1.11.1-CVE-2026-7598.patch
# CVE-2026-55200: additional boundary checks for the packet length
# https://github.com/libssh2/libssh2/pull/2052
Patch1:		97acf3dfda80c91c3a8c9f2372546301d4a1a7a8-%{sname}-1.11.1.patch
# CVE-2026-55199: check the _libssh2_get_string() return in the EXT_INFO handler
# https://github.com/libssh2/libssh2/pull/1864
Patch2:		17626857d20b3c9a1addfa45979dadcee1cd84a4.patch
# CVE-2025-15661: out of bounds read on a crafted SFTP response
# https://github.com/libssh2/libssh2/pull/1717
Patch3:		2dae302-%{sname}-1.11.1.patch

BuildRequires:	pgdg-srpm-macros >= 2.2.0
BuildRequires:	gcc make openssl-devel zlib-devel
%if %runselftest
# The test suite runs an OpenSSH server and connects to it:
BuildRequires:	openssh-server
%endif

%description
libssh2 is a library implementing the SSH2 protocol as defined by
Internet Drafts: SECSH-TRANS(22), SECSH-USERAUTH(25),
SECSH-CONNECTION(23), SECSH-ARCH(20), SECSH-FILEXFER(06)*,
SECSH-DHGEX(04), and SECSH-NUMBERS(10).

This package installs libssh2 under %{libssh2instdir}, for the
packages in the PostgreSQL RPM repository.

%package devel
Summary:	Development files for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{sname}.

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p0
%patch -P 1 -p1
%patch -P 2 -p1
%patch -P 3 -p1

%build
%configure \
	--prefix=%{libssh2instdir} \
	--libdir=%{libssh2instdir}/lib64 \
	--includedir=%{libssh2instdir}/include \
	--mandir=%{libssh2instdir}/share/man \
	--with-crypto=openssl \
	--disable-rpath \
	--disable-silent-rules \
	--disable-static \
	--enable-shared \
	--disable-examples-build \
	--disable-docker-tests
%{make_build}

%install
%{make_install} INSTALL="install -p"
find %{buildroot} -name '*.la' -delete

%check
%if %runselftest
%{__make} -C tests check
%endif

%files
%license COPYING
%doc docs/AUTHORS README RELEASE-NOTES
%dir %{libssh2instdir}
%dir %{libssh2instdir}/lib64
%{libssh2instdir}/lib64/%{sname}.so.1
%{libssh2instdir}/lib64/%{sname}.so.1.*

%files devel
%{libssh2instdir}/include/
%{libssh2instdir}/lib64/%{sname}.so
%{libssh2instdir}/lib64/pkgconfig/
%{libssh2instdir}/share/

%changelog
* Fri Oct 23 2026 Devrim Gunduz <devrim@gunduz.org> - 1.11.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-libssh2, so that pgBackRest does not need the EPEL libssh2
  package on RHEL. Based on the Fedora spec file, including its patches
  for CVE-2026-7598, CVE-2026-55200, CVE-2026-55199 and CVE-2025-15661.
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422
