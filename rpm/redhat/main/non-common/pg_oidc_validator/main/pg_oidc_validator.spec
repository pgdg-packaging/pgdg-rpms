%global sname pg_oidc_validator

%{!?llvm:%global llvm 1}

Summary:	OAuth validator for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.1.0
Release:	1PGDG%{?dist}
License:	Apache 2.0
URL:		https://github.com/percona/%{sname}
Source0:	https://github.com/percona/%{sname}/archive/refs/tags/%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
OAuth validator library for PostgreSQL 18.

NOTE: This library is still experimental and not intended for production use.

This library should support most providers that implement OIDC and provide a
valid JWT as an access token.


%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_oidc_validator
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} == 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?suse_version} == 1600
BuildRequires:	llvm19-devel clang19-devel
Requires:	llvm19
%endif
%if 0%{?amzn}
BuildRequires:	llvm-devel >= 15.0 clang-devel >= 15.0
Requires:	llvm >= 15.0
%endif
%if ( 0%{?fedora} || 0%{?rhel} >= 8 ) && !0%{?amzn}
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm >= 19.0
%endif

%description llvmjit
This packages provides JIT support for pg_oidc_validator
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README
%{__install} -d %{buildroot}%{pginstdir}/doc/extension/
%{__install} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%license LICENSE.txt
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so

%if %llvm
%files llvmjit
 %{pginstdir}/lib/bitcode/%{sname}*.bc
 %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Fri Aug 14 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1.0-1PGDG
- Update to 1.1.0

* Tue Aug 11 2026 Devrim Gunduz <devrim@gunduz.org> - 1.0.0-1PGDG
- Update to 1.0.0

* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 0.2.0-2PGDG
- Add Amazon Linux 2023 support.

* Mon Jun 29 2026 - Devrim Gündüz <devrim@gunduz.org> 0.2.0-1PGDG
- Initial RPM packaging for PostgreSQL RPM Repository
