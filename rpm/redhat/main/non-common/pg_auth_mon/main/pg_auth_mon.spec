%global sname	pg_auth_mon

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


Summary:	PostgreSQL extension to store authentication attempts
Name:		%{sname}_%{pgmajorversion}
Version:	5.0
Release:	4PGDG%{?dist}
License:	MIT
Source0:	https://github.com/RafiaSabih/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/RafiaSabih/%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel krb5-devel
%if 0%{?suse_version} >= 1500
Requires:	libopenssl3
BuildRequires:	libopenssl-3-devel
%endif
%if 0%{?fedora} >= 41 || 0%{?rhel} >= 8 || 0%{?amzn}
Requires:	openssl-libs >= 1.1.1k
BuildRequires:	openssl-devel
%endif
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-libs

%description
This extension eases monitoring of login attempts to your database. Postgres
writes each login attempt to a log file, but it is hard to identify through
that information alone if your database is under malicious activity.
Maintaining separately information like the total number of successful login
attempts, or a timestamp of the last failed login helps to answer questions
like:
 - when has a user successfully logged in for the last time ?
 - has a user genuinely mistyped their password or has their username been compromised?
 - is there any particular time when a malicious role is active?

Once we have spot a suspicious activity, we may dig deeper by using this
information along with the log file to identify the particular IP address etc.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_auth_mon
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
This package provides JIT support for pg_auth_mon
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - 5.0-4PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51

* Mon Aug 24 2026 Devrim Gunduz <devrim@gunduz.org> - 5.0-3PGDG
- Fix OpenSSL dependency for Amazon Linux 2023

* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 5.0-2PGDG
- Add Amazon Linux 2023 support.

* Thu Jul 2 2026 Devrim Gunduz <devrim@gunduz.org> - 5.0-1PGDG
- Update to 5.0 per changes described at:
  https://github.com/RafiaSabih/pg_auth_mon/releases/tag/v5.0

* Thu Jun 25 2026 Devrim Gunduz <devrim@gunduz.org> - 4.0-1PGDG
- Update to 4.0 per changes described at:
  https://github.com/RafiaSabih/pg_auth_mon/releases/tag/v4.0

* Thu Nov 20 2025 Devrim Gündüz <devrim@gunduz.org> - 3.0-6PGDG
- Modernise OpenSSL dependencies.

* Tue Oct 7 2025 Devrim Gündüz <devrim@gunduz.org> - 3.0-5PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 3.0-4PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Tue Feb 25 2025 Devrim Gunduz <devrim@gunduz.org> - 3.0-3PGDG
- Add missing BRs

* Thu Sep 19 2024 Devrim Gunduz <devrim@gunduz.org> - 3.0-2PGDG
- Update description and LLVM dependencies.

* Tue Aug 6 2024 Devrim Gunduz <devrim@gunduz.org> - 3.0-1PGDG
- Update to 3.0 per changes described at:
  https://github.com/RafiaSabih/pg_auth_mon/releases/tag/v3.0

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 2.0-3PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Fri Feb 23 2024 Devrim Gunduz <devrim@gunduz.org> - 2.0-2PGDG
- Add PGDG branding

* Sun Jun 4 2023 Devrim Gunduz <devrim@gunduz.org> - 2.0-1
- Update to 2.0

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.0-2.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu Feb 25 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Initial packaging for PostgreSQL RPM Repository
