%global sname pg_oidc_validator

%{!?llvm:%global llvm 1}

# Propagate %%llvm into the actual build: PGXS decides whether to invoke
# clang/llvm-config based on with_llvm from the installed postgresql*-devel's
# Makefile.global, not from this spec's %%llvm. Without passing with_llvm=no
# through to make, setting %%llvm 0 here only drops the llvm BuildRequires/
# subpackage/files, while the build still tries to run clang regardless.
%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif


Summary:	OAuth validator for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.1.0
Release:	3PGDG%{?dist}
License:	Apache 2.0
URL:		https://github.com/percona/%{sname}
Source0:	https://github.com/percona/%{sname}/archive/refs/tags/%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
%if 0%{?suse_version} >= 1500
BuildRequires:	libstdc++-devel
%else
BuildRequires:	libstdc++-static
%endif
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
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} %{with_llvm_arg} PG_CXXFLAGS="%{optflags}" COMPILER='g++ $(CXXFLAGS)'

%install
%{__rm} -rf %{buildroot}

PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} %{with_llvm_arg} install DESTDIR=%{buildroot} PG_CXXFLAGS="%{optflags}" COMPILER='g++ $(CXXFLAGS)'


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
* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1.0-3PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51

* Mon Aug 17 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1.0-2PGDG
- Rebuild on RHEL 10.2 x86_64 because of package signing issue

* Fri Aug 14 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1.0-1PGDG
- Update to 1.1.0

* Tue Aug 11 2026 Devrim Gunduz <devrim@gunduz.org> - 1.0.0-1PGDG
- Update to 1.0.0

* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 0.2.0-2PGDG
- Add Amazon Linux 2023 support.

* Mon Jun 29 2026 - Devrim Gündüz <devrim@gunduz.org> 0.2.0-1PGDG
- Initial RPM packaging for PostgreSQL RPM Repository
