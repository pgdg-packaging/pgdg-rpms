%global		sname libargon2
%global		gh_commit 62358ba2123abd17fccf2a108a301d4b52c01a7c
%global		gh_short %(c=%{gh_commit}; echo ${c:0:7})
%global		gh_project phc-winner-argon2
%global		soname 1
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		libargon2instdir %{pgdg_libargon2instdir}

# The library is found through the rpath only (there is no ld.so.conf.d
# file), so it must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL libargon2. Consumers require
# pgdg-libargon2 by name instead:
%global		__provides_exclude_from ^%{libargon2instdir}/
%global		__requires_exclude ^libargon2\\.so

%{!?runselftest:%global runselftest 0}

Name:		pgdg-%{sname}
Version:	20190702
Release:	1PGDG%{?dist}
Summary:	The password-hashing library
License:	CC0-1.0 OR Apache-2.0
URL:		https://github.com/P-H-C/%{gh_project}
Source0:	https://github.com/P-H-C/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRequires:	pgdg-srpm-macros >= 2.3.0
BuildRequires:	gcc make

%description
Argon2 is a password-hashing function that summarizes the state of the art
in the design of memory-hard functions and can be used to hash passwords
for credential storage, key derivation, or other applications. This
package contains the library, and the argon2 command line tool.

This package installs libargon2 under %{libargon2instdir}, for the
packages in the PostgreSQL RPM repository.

%package devel
Summary:	Development files for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{sname}.

%prep
%setup -q -n %{gh_project}-%{gh_commit}

if ! grep -q 'ABI_VERSION = %{soname}' Makefile; then
	: soname has changed
	grep soname Makefile
	exit 1
fi

# Fix the pkgconfig file:
sed -e 's:lib/@HOST_MULTIARCH@:lib64:;s/@UPSTREAM_VER@/%{version}/' -i %{sname}.pc.in

%build
# Use the default RPM build options, the library path and the rpath (for
# the argon2 tool), not -march=native (Fedora):
sed -e '/^CFLAGS/s:^CFLAGS:LDFLAGS=%{build_ldflags} -Wl,-rpath,%{libargon2instdir}/lib64\nCFLAGS:' \
    -e 's:-O3 -Wall:%{optflags}:' \
    -e '/^LIBRARY_REL/s:lib:lib64:' \
    -e 's:-march=\$(OPTTARGET) :${CFLAGS} :' \
    -e 's:CFLAGS += -march=\$(OPTTARGET)::' \
    -i Makefile

# Parallel builds are not supported:
%{__make} -j1 PREFIX=%{libargon2instdir} LIBRARY_REL=lib64

%install
%{__make} install DESTDIR=%{buildroot} PREFIX=%{libargon2instdir} LIBRARY_REL=lib64

%{__rm} %{buildroot}%{libargon2instdir}/lib64/%{sname}.a

chmod -x %{buildroot}%{libargon2instdir}/include/argon2.h
chmod +x %{buildroot}%{libargon2instdir}/lib64/%{sname}.so.%{soname}

%check
%if %runselftest
%{__make} test
%endif

%files
%license LICENSE
%dir %{libargon2instdir}
%dir %{libargon2instdir}/bin
%dir %{libargon2instdir}/lib64
%{libargon2instdir}/bin/argon2
%{libargon2instdir}/lib64/%{sname}.so.%{soname}

%files devel
%doc *.md
%{libargon2instdir}/include/
%{libargon2instdir}/lib64/%{sname}.so
%{libargon2instdir}/lib64/pkgconfig/

%changelog
* Fri Oct 23 2026 Devrim Gunduz <devrim@gunduz.org> - 20190702-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-libargon2, so that pg_pwhash does not need the EPEL libargon2
  package on RHEL. Based on the Fedora spec file. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
