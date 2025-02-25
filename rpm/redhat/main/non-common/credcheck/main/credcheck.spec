%global sname credcheck

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	3.0
Release:	2PGDG%{?dist}
Summary:	PostgreSQL username/password checks
License:	PostgreSQL
URL:		https://github.com/MigOpsRepos/%{sname}
Source0:	https://github.com/MigOpsRepos//%{sname}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	krb5-devel openssl-devel
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
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 17.0 clang-devel >= 17.0
Requires:	llvm => 17.0
%endif

%description llvmjit
This packages provides JIT support for credcheck
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

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

