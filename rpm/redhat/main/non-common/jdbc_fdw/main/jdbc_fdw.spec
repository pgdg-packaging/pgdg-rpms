%global sname	jdbc_fdw
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

Summary:	JDBC Foreign Data Wrapper for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	0.5.0
Release:	7PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/pgspider/%{sname}
Source0:	https://github.com/pgspider/%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-pgdg-rpm.patch

BuildRequires:	java-devel
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	krb5-devel
%if 0%{?suse_version} >= 1500
Requires:	libopenssl3
BuildRequires:	libopenssl-3-devel
%endif
%if 0%{?fedora} >= 41 || 0%{?rhel} >= 8 || 0%{?amzn}
Requires:	openssl-libs >= 1.1.1k
BuildRequires:	openssl-devel
%endif

Requires:	java
Requires:	postgresql%{pgmajorversion}-server

%description
This is a foreign data wrapper (FDW) to connect PostgreSQL to
any Java DataBase Connectivity (JDBC) data source.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for jdbc_fdw
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
This package provides JIT support for jdbc_fdw
%endif

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p0

%build

%if 0%{?suse_version} >= 1500
export PATH=/usr/lib64/jvm/java-openjdk/bin:$PATH
%endif
%if 0%{?fedora} || 0%{?rhel} >= 9
export PATH=/usr/lib/jvm/java-openjdk/bin:$PATH
%endif

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot} %{with_llvm_arg}
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(-,root,root,-)
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.sql
%{pginstdir}/share/extension/*.control
%{pginstdir}/doc/extension/README-%{sname}.md

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - 0.5.0-7PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51

* Mon Aug 24 2026 Devrim Gunduz <devrim@gunduz.org> - 0.5.0-6PGDG
- Fix OpenSSL dependency for Amazon Linux 2023

* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 0.5.0-5PGDG
- Add Amazon Linux 2023 support.

* Thu Nov 20 2025 Devrim Gunduz <devrim@gunduz.org> - 0.5.0-4PGDG
- Modernise OpenSSL dependencies

* Mon Oct 6 2025 Devrim Gunduz <devrim@gunduz.org> - 0.5.0-3PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 0.5.0-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Tue Mar 18 2025 Devrim Gündüz <devrim@gunduz.org> - 0.5.0-1PGDG
- Update to 0.5.0 per changes described at:
  https://github.com/pgspider/jdbc_fdw/releases/tag/v0.5.0

* Thu Jan 2 2025 Devrim Gündüz <devrim@gunduz.org> - 0.4.0-2PGDG
- Simplify Java dependencies and use correct path for java[c].

* Wed Aug 21 2024 Devrim Gündüz <devrim@gunduz.org> - 0.4.0-1PGDG
- Initial packaging for PostgreSQL RPM repositories. Patch taken from
  Debian sources.
