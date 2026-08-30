%global sname credcheck

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

Name:		%{sname}_%{pgmajorversion}
Version:	5.0
Release:	4PGDG%{?dist}
Summary:	PostgreSQL username/password checks
License:	PostgreSQL
URL:		https://github.com/HexaCluster/%{sname}
Source0:	https://github.com/HexaCluster//%{sname}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel krb5-devel
%if 0%{?suse_version} >= 1500
Requires:	libopenssl3
BuildRequires:	libopenssl-3-devel
%endif
%if 0%{?fedora} >= 41 || 0%{?rhel} >= 8 || 0%{?amzn}
Requires:	openssl-libs >= 1.1.1k
BuildRequires:	openssl-devel
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
The credcheck PostgreSQL extension provides few general credential checks,
which will be evaluated during the user creation, during the password change
and user renaming. By using this extension, we can define a set of rules to
allow a specific set of credentials, and a set of rules to reject a certain
type of credentials. This extension is developed based on the PostgreSQL's
check_password_hook hook.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for credcheck
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
This package provides JIT support for credcheck
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot} %{with_llvm_arg}

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension//%{sname}.control
%{pginstdir}/share/extension/%{sname}*sql
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

* Sun Jun 21 2026 Devrim Gunduz <devrim@gunduz.org> - 5.0-1PGDG
- Update to 5.0 per changes described at
  https://github.com/HexaCluster/credcheck/releases/tag/v5.0

* Sun Apr 19 2026 Devrim Gunduz <devrim@gunduz.org> - 4.7-1PGDG
- Update to 4.7 per changes described at
  https://github.com/HexaCluster/credcheck/releases/tag/v4.7

* Thu Feb 19 2026 Devrim Gunduz <devrim@gunduz.org> - 4.6-1PGDG
- Update to 4.6 per changes described at
  https://github.com/HexaCluster/credcheck/releases/tag/v4.6

* Tue Jan 27 2026 Devrim Gunduz <devrim@gunduz.org> - 4.5-1PGDG
- Update to 4.5 per changes described at
  https://github.com/HexaCluster/credcheck/releases/tag/v4.5

* Wed Jan 14 2026 Devrim Gunduz <devrim@gunduz.org> - 4.4-1PGDG
- Update to 4.4 per changes described at
  https://github.com/HexaCluster/credcheck/releases/tag/v4.4

* Thu Dec 25 2025 Devrim Gunduz <devrim@gunduz.org> - 4.3-1PGDG
- Update to 4.3 per changes described at
  https://github.com/HexaCluster/credcheck/releases/tag/v4.3

* Wed Nov 5 2025 Devrim Gunduz <devrim@gunduz.org> - 4.2-2PGDG
- Rebuild against OpenSSL 3 on SLES 15

* Fri Oct 24 2025 Devrim Gunduz <devrim@gunduz.org> - 4.2-1PGDG
- Update to 4.2 per changes described at
  https://github.com/HexaCluster/credcheck/releases/tag/v4.2

* Mon Oct 20 2025 Devrim Gunduz <devrim@gunduz.org> - 4.1-1PGDG
- Update to 4.1 per changes described at
  https://github.com/HexaCluster/credcheck/releases/tag/v4.1
- Update OpenSSL dependencies

* Thu Oct 16 2025 Devrim Gunduz <devrim@gunduz.org> - 4.0-1PGDG
- Update to 4.0 per changes described at
  https://github.com/MigOpsRepos/credcheck/releases/tag/v4.0

* Sun Oct 5 2025 Devrim Gunduz <devrim@gunduz.org> - 3.0-3PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 3.0-3PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Tue Feb 25 2025 Devrim Gunduz <devrim@gunduz.org> - 3.0-2PGDG
- Add missing BR

* Thu Jan 2 2025 Devrim Gunduz <devrim@gunduz.org> - 3.0-1PGDG
- Update to 3.0 per changes described at
  https://github.com/MigOpsRepos/credcheck/releases/tag/v3.0

* Mon Aug 5 2024 Devrim Gunduz <devrim@gunduz.org> - 2.8-1PGDG
- Update to 2.8 per changes described at
  https://github.com/MigOpsRepos/credcheck/releases/tag/v2.8

* Mon Jul 29 2024 Devrim Gunduz <devrim@gunduz.org> - 2.7-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Sat Apr 27 2024 Devrim Gündüz <devrim@gunduz.org> - 2.7-1PGDG
- Update to 2.7, per changes described at:
  https://github.com/MigOpsRepos/credcheck/releases/tag/v2.7

* Tue Jan 30 2024 Devrim Gündüz <devrim@gunduz.org> - 2.6-1PGDG
- Update to 2.6, per changes described at:
  https://github.com/MigOpsRepos/credcheck/releases/tag/v2.6

* Tue Jan 30 2024 Devrim Gündüz <devrim@gunduz.org> - 2.4-1PGDG
- Update to 2.4, per changes described at:
  https://github.com/MigOpsRepos/credcheck/releases/tag/v2.4

* Fri Nov 3 2023 Devrim Gündüz <devrim@gunduz.org> - 2.3-1PGDG
- Update to 2.3, per changes described at:
  https://github.com/MigOpsRepos/credcheck/releases/tag/v2.3

* Sun Sep 17 2023 Devrim Gündüz <devrim@gunduz.org> - 2.2-1PGDG
- Update to 2.2, per changes described at:
  https://github.com/MigOpsRepos/credcheck/releases/tag/v2.2

* Mon Jul 24 2023 Devrim Gündüz <devrim@gunduz.org> - 2.1-1PGDG
- Update to 2.1, per changes described at:
  https://github.com/MigOpsRepos/credcheck/releases/tag/v2.1
- Add PGDG branding

* Mon Jun 12 2023 Devrim Gündüz <devrim@gunduz.org> - 2.0-1
- Update to 2.0, per changes described at:
  https://github.com/MigOpsRepos/credcheck/releases/tag/v2.0

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.2-1.1
- Rebuild against LLVM 15 on SLES 15

* Tue May 16 2023 Devrim Gündüz <devrim@gunduz.org> - 1.2-1
- Update to 1.2

* Fri Apr 7 2023 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Update to 1.0

* Mon Feb 27 2023 Devrim Gündüz <devrim@gunduz.org> - 0.2.0-3
- Fix summary of the package, per report from Didier Ros.

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 0.2.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon Sep 20 2021 Devrim Gündüz <devrim@gunduz.org> - 0.2.0-1
- Update to 0.2.0

* Fri Jan 8 2021 Devrim Gündüz <devrim@gunduz.org> - 0.1.1-2
- Initial packaging for PostgreSQL YUM repository.

