%global sname pg_pwhash

Summary:	A PostgreSQL extension which provides advanced password hashing methods based on adaptive implementations.
Name:		%{sname}_%{pgmajorversion}
Version:	1.0
Release:	1PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/cybertec-postgresql/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/cybertec-postgresql/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel libxcrypt-devel
Requires:	postgresql%{pgmajorversion}-server libxcrypt
%if 0%{?suse_version} >= 1500
Requires:	libopenssl3
BuildRequires:	libopenssl-3-devel
%endif
%if 0%{?fedora} >= 41 || 0%{?rhel} >= 8
Requires:	openssl-libs >= 1.1.1k
BuildRequires:	openssl-devel
%endif
%if 0%{?fedora} >= 41 || 0%{?rhel} <= 9
Requires:	libscrypt
BuildRequires:	libscrypt-devel
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	argon2-devel libscrypt-devel
Requires:	libargon2-1 libscrypt0
%endif
%if 0%{?fedora} >= 41 || 0%{?rhel} >= 8
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
%{__install} -d build
%meson
%meson_build

%install
export PATH=%{pginstdir}/bin:$PATH
%meson_install

%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension/
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/%{sname}.md

%files
%license LICENSE
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%defattr(644,root,root,755)
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/lib/%{sname}.so

%changelog
* Thu Jan 22 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0-1PGDG
- Initial RPM packaging for PostgreSQL RPM Repository per:
  https://github.com/cybertec-postgresql/pg_pwhash/releases/tag/v1.0
