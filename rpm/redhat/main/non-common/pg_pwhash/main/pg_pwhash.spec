%global sname pg_pwhash

%{!?runselftest:%global runselftest 0}

# On RHEL, libargon2 and libscrypt come from pgdg-libargon2 and
# pgdg-libscrypt (EPEL is not needed), which do not provide their sonames;
# they are found through the rpath:
%if 0%{?rhel}
%global __requires_exclude ^lib(argon2|scrypt)\\.so
%endif

Summary:	A PostgreSQL extension which provides advanced password hashing methods based on adaptive implementations.
Name:		%{sname}_%{pgmajorversion}
Version:	1.0
Release:	4PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/cybertec-postgresql/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/cybertec-postgresql/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel libxcrypt-devel meson gcc
Requires:	postgresql%{pgmajorversion}-server libxcrypt
%if %runselftest
BuildRequires:	postgresql%{pgmajorversion}-server pgdg-srpm-macros >= 2.0.0
# The build uses meson; installcheck needs the PGXS Makefile
BuildRequires:	make
%endif
%if 0%{?suse_version} >= 1500
Requires:	libopenssl3
BuildRequires:	libopenssl-3-devel
%endif
%if 0%{?fedora} >= 41 || 0%{?rhel} >= 8 || 0%{?amzn}
Requires:	openssl-libs >= 1.1.1k
BuildRequires:	openssl-devel
%endif
%if 0%{?rhel}
BuildRequires:	pgdg-srpm-macros >= 2.3.0
BuildRequires:	pgdg-libargon2-devel pgdg-libscrypt-devel
Requires:	pgdg-libargon2%{?_isa} pgdg-libscrypt%{?_isa}
%else
Requires:	libscrypt
BuildRequires:	libscrypt-devel
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	argon2-devel libscrypt-devel
Requires:	libargon2-1 libscrypt0
%endif
%if 0%{?fedora} >= 41
BuildRequires:	libargon2-devel
Requires:	libargon2
%endif

%description
pg_pwhash provides advanced password hashing methods based on adaptive
implementations. The following hashing algorithms are supported if all
requirements are met:
 - yescrypt
 - Argon2 based on RFC 9106
 - scrypt

%prep
%setup -q -n %{sname}-%{version}

%build
export PATH=%{pginstdir}/bin:$PATH
%if 0%{?rhel}
export CFLAGS="%{build_cflags} -I%{pgdg_libargon2instdir}/include -I%{pgdg_libscryptinstdir}/include"
export LDFLAGS="%{build_ldflags} -L%{pgdg_libargon2instdir}/lib64 -L%{pgdg_libscryptinstdir}/lib64 -Wl,-rpath,%{pgdg_libargon2instdir}/lib64:%{pgdg_libscryptinstdir}/lib64"
%endif
%{__install} -d build
%meson
%meson_build

%install
export PATH=%{pginstdir}/bin:$PATH
%meson_install

%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension/
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/%{sname}.md

%check
%if %runselftest
%pgdg_check_installcheck
%endif

%files
%license LICENSE
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%defattr(644,root,root,755)
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/lib/%{sname}.so

%changelog
* Tue Sep 29 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0-4PGDG
- Add %%check, running the regression tests with the %%check helpers
  from pgdg-srpm-macros 2.0.0. It is disabled by default; enable it
  with --define 'runselftest 1'.
- Add gcc to BuildRequires: the meson build needs a C compiler, which
  nothing else pulls in, so the build failed in a clean build root.
- RHEL: build against pgdg-libargon2 and pgdg-libscrypt (installed under
  /usr/pgdg-libargon2 and /usr/pgdg-libscrypt), so that pg_pwhash does not
  need the EPEL libargon2 and libscrypt packages anymore. This also enables
  the libscrypt support on RHEL 10, where EPEL does not have libscrypt. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Sun Sep 20 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0-3PGDG
- Add missing meson BR, as the spec uses %%meson and %%meson_build.
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/237

* Mon Aug 24 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0-2PGDG
- Fix OpenSSL dependency for Amazon Linux 2023

* Thu Jan 22 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0-1PGDG
- Initial RPM packaging for PostgreSQL RPM Repository per:
  https://github.com/cybertec-postgresql/pg_pwhash/releases/tag/v1.0
