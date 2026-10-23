%global		sname libsodium
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		libsodiuminstdir %{pgdg_libsodiuminstdir}

# The library is found through the rpath only (there is no ld.so.conf.d
# file), so it must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL libsodium. Consumers require
# pgdg-libsodium by name instead:
%global		__provides_exclude_from ^%{libsodiuminstdir}/
%global		__requires_exclude ^libsodium\\.so

# A configure test uses assembler code but does not link the object files,
# so it always succeeds with LTO. -ffat-lto-objects avoids that (Fedora):
%define _lto_cflags -flto=auto -ffat-lto-objects

%{!?runselftest:%global runselftest 0}

Name:		pgdg-%{sname}
Version:	1.0.22
Release:	1PGDG%{?dist}
Summary:	The Sodium crypto library
License:	ISC
URL:		https://libsodium.org/
Source0:	https://download.libsodium.org/%{sname}/releases/%{sname}-%{version}.tar.gz

BuildRequires:	pgdg-srpm-macros >= 2.3.0
BuildRequires:	gcc make

%description
Sodium is a new, easy-to-use software library for encryption, decryption,
signatures, password hashing and more. It is a portable, cross-compilable,
installable, packageable fork of NaCl, with a compatible API, and an
extended API to improve usability even further. Its goal is to provide all
of the core operations needed to build higher-level cryptographic tools.

This package installs libsodium under %{libsodiuminstdir}, for the
packages in the PostgreSQL RPM repository.

%package devel
Summary:	Development files for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{sname}.

%prep
%setup -q -n %{sname}-%{version}

%build
# --disable-opt: no -march=native
%configure \
	--prefix=%{libsodiuminstdir} \
	--libdir=%{libsodiuminstdir}/lib64 \
	--includedir=%{libsodiuminstdir}/include \
	--disable-silent-rules \
	--disable-static \
	--disable-opt
%{make_build}

%install
%{make_install}
find %{buildroot} -name '*.la' -delete

%check
%if %runselftest
%{__make} check
%endif

%files
%license LICENSE
%doc AUTHORS ChangeLog README.markdown THANKS
%dir %{libsodiuminstdir}
%dir %{libsodiuminstdir}/lib64
%{libsodiuminstdir}/lib64/%{sname}.so.26*

%files devel
%{libsodiuminstdir}/include/
%{libsodiuminstdir}/lib64/%{sname}.so
%{libsodiuminstdir}/lib64/pkgconfig/

%changelog
* Fri Oct 23 2026 Devrim Gunduz <devrim@gunduz.org> - 1.0.22-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-libsodium, so that pgsodium does not need the EPEL libsodium
  package on RHEL. Based on the Fedora spec file. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
