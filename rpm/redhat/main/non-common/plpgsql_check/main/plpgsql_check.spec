%global sname plpgsql_check

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	2.8.2
Release:	1PGDG%{?dist}
Summary:	Additional tools for PL/pgSQL functions validation
License:	BSD
URL:		https://github.com/okbob/%{sname}
Source0:	https://github.com/okbob/%{sname}/archive/v%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}

%description
plpgsql_check is a PostgreSQL extension with functionality for direct
or indirect extra validation of functions in PL/pgSQL language. It verifies
a validity of SQL identifiers used in PL/pgSQL code. It also tries to identify
performance issues.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for plpgsql_check
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 17.0 clang-devel >= 17.0
Requires:	llvm >= 17.0
%endif

%description llvmjit
This package provides JIT support for plpgsql_check
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} DESTDIR=%{buildroot} install

%files
%defattr(644,root,root,755)
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Mon Jul 28 2025 Devrim Gündüz <devrim@gunduz.org> 2.8.2-1PGDG
- Update to 2.8.2 per changes described at:
  https://github.com/okbob/plpgsql_check/releases/tag/v2.8.2

* Tue Apr 29 2025 Devrim Gündüz <devrim@gunduz.org> 2.8.1-1PGDG
- Update to 2.8.1 per changes described at:
  https://github.com/okbob/plpgsql_check/releases/tag/v2.8.1

* Sat Mar 22 2025 Devrim Gündüz <devrim@gunduz.org> 2.8.0-1PGDG
- Update to 2.8.0 per changes described at:
  https://github.com/okbob/plpgsql_check/releases/tag/v2.8.0

* Fri Feb 7 2025 Devrim Gündüz <devrim@gunduz.org> 2.7.15-1PGDG
- Update to 2.7.15 per changes described at:
  https://github.com/okbob/plpgsql_check/releases/tag/v2.7.15

* Wed Feb 5 2025 Devrim Gündüz <devrim@gunduz.org> 2.7.14-1PGDG
- Update to 2.7.14 per changes described at:
  https://github.com/okbob/plpgsql_check/releases/tag/v2.7.14
- Update LLVM dependencies.

* Tue Oct 15 2024 Devrim Gündüz <devrim@gunduz.org> 2.7.12-1PGDG
- Update to 2.7.12 per changes described at:
  https://github.com/okbob/plpgsql_check/releases/tag/v2.7.12

* Mon Sep 16 2024 Devrim Gündüz <devrim@gunduz.org> 2.7.11-1PGDG
- Update to 2.7.11 per changes described at:
  https://github.com/okbob/plpgsql_check/releases/tag/v2.7.11

* Mon Sep 16 2024 Devrim Gündüz <devrim@gunduz.org> 2.7.10-1PGDG
- Update to 2.7.10 per changes described at:
  https://github.com/okbob/plpgsql_check/releases/tag/v2.7.10

* Mon Sep 2 2024 Devrim Gündüz <devrim@gunduz.org> 2.7.9-1PGDG
- Update to 2.7.9 per changes described at:
  https://github.com/okbob/plpgsql_check/releases/tag/v2.7.9

* Tue Aug 6 2024 Devrim Gündüz <devrim@gunduz.org> 2.7.8-1PGDG
- Update to 2.7.8 per changes described at:
  https://github.com/okbob/plpgsql_check/releases/tag/v2.7.8

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> 2.7.7-2PGDG
- Update LLVM dependencies
- Fix changelog date
- Remove RHEL 7 support

* Tue Jun 25 2024 Devrim Gündüz <devrim@gunduz.org> 2.7.7-1PGDG
- Update to 2.7.7 per changes described at:
  https://github.com/okbob/plpgsql_check/releases/tag/v2.7.7

* Thu Jun 6 2024 Devrim Gündüz <devrim@gunduz.org> 2.7.6-1PGDG
- Update to 2.7.6 per changes described at:
  https://github.com/okbob/plpgsql_check/releases/tag/v2.7.6

* Sun Mar 31 2024 Devrim Gündüz <devrim@gunduz.org> 2.7.5-1PGDG
- Update to 2.7.5 per changes described at:
  https://github.com/okbob/plpgsql_check/releases/tag/v2.7.5

* Fri Mar 15 2024 Devrim Gündüz <devrim@gunduz.org> 2.7.4-1PGDG
- Update to 2.7.4 per changes described at:
  https://github.com/okbob/plpgsql_check/releases/tag/v2.7.4

* Tue Mar 12 2024 Devrim Gündüz <devrim@gunduz.org> 2.7.3-1PGDG
- Update to 2.7.3 per changes described at:
  https://github.com/okbob/plpgsql_check/releases/tag/v2.7.3

* Mon Feb 26 2024 Devrim Gündüz <devrim@gunduz.org> 2.7.2-2PGDG
- Enable -debug* subpackages

* Tue Jan 23 2024 Devrim Gündüz <devrim@gunduz.org> 2.7.2-1PGDG
- Update to 2.7.2 per changes described at:
  https://github.com/okbob/plpgsql_check/releases/tag/v2.7.2

* Thu Dec 21 2023 Devrim Gündüz <devrim@gunduz.org> 2.7.1-1PGDG
- Update to 2.7.1 per changes described at:
  https://github.com/okbob/plpgsql_check/releases/tag/v2.7.1

* Wed Dec 6 2023 Devrim Gündüz <devrim@gunduz.org> 2.7.0-1PGDG
- Update to 2.7.0 per changes described at:
  https://github.com/okbob/plpgsql_check/releases/tag/v2.7.0

* Tue Nov 28 2023 Devrim Gündüz <devrim@gunduz.org> 2.6.2-1PGDG
- Update to 2.6.2 per changes described at:
  https://github.com/okbob/plpgsql_check/releases/tag/v2.6.2

* Sun Nov 5 2023 Devrim Gündüz <devrim@gunduz.org> 2.6.1-1PGDG
- Update to 2.6.1 per changes described at:
  https://github.com/okbob/plpgsql_check/releases/tag/v2.6.1

* Wed Nov 1 2023 Devrim Gündüz <devrim@gunduz.org> 2.6.0-1PGDG
- Update to 2.6.0 per changes described at:
  https://github.com/okbob/plpgsql_check/releases/tag/v2.6.0

* Thu Oct 5 2023 Devrim Gündüz <devrim@gunduz.org> 2.5.3-1PGDG
- Update to 2.5.3

* Sat Sep 16 2023 Devrim Gündüz <devrim@gunduz.org> 2.5.1-1PGDG
- Update to 2.5.1

* Wed Sep 13 2023 Devrim Gündüz <devrim@gunduz.org> 2.5.0-1PGDG
- Update to 2.5.0

* Mon Aug 21 2023 Devrim Gündüz <devrim@gunduz.org> 2.4.0-2PGDG
- Remove RHEL 6 bits
- Fix rpmlint warnings

* Thu Aug 10 2023 Devrim Gündüz <devrim@gunduz.org> 2.4.0-1PGDG
- Update to 2.4.0
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 2.3.4-1.1
- Rebuild against LLVM 15 on SLES 15

* Tue Apr 18 2023 Devrim Gündüz <devrim@gunduz.org> 2.3.4-1
- Update to 2.3.4

* Sun Mar 12 2023 Devrim Gündüz <devrim@gunduz.org> 2.3.3-1
- Update to 2.3.3

* Wed Mar 1 2023 Devrim Gündüz <devrim@gunduz.org> 2.3.2-1
- Update to 2.3.2

* Tue Feb 21 2023 Devrim Gündüz <devrim@gunduz.org> 2.3.1-1
- Update to 2.3.1

* Wed Jan 11 2023 Devrim Gündüz <devrim@gunduz.org> 2.3.0-1
- Update to 2.3.0

* Thu Dec 22 2022 Devrim Gündüz <devrim@gunduz.org> 2.2.6-1
- Update to 2.2.6

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.2.5-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue Nov 29 2022 Devrim Gündüz <devrim@gunduz.org> 2.2.5-1
- Update to 2.2.5

* Tue Nov 22 2022 Devrim Gündüz <devrim@gunduz.org> 2.2.4-1
- Update to 2.2.4

* Mon Oct 24 2022 Devrim Gündüz <devrim@gunduz.org> 2.2.3-1
- Update to 2.2.3

* Thu Oct 6 2022 Devrim Gündüz <devrim@gunduz.org> 2.2.2-1
- Update to 2.2.2

* Mon Sep 26 2022 Devrim Gündüz <devrim@gunduz.org> 2.2.1-1
- Update to 2.2.1

* Wed Sep 7 2022 Devrim Gündüz <devrim@gunduz.org> 2.1.10-1
- Update to 2.1.10

* Mon Jul 25 2022 Devrim Gündüz <devrim@gunduz.org> 2.1.8-1
- Update to 2.1.8

* Sat Jun 4 2022 Devrim Gündüz <devrim@gunduz.org> 2.1.7-2
- Attempt to fix RHEL 8 - ppc64le builds.

* Sat Jun 4 2022 Devrim Gündüz <devrim@gunduz.org> 2.1.7-1
- Update to 2.1.7

* Sun May 8 2022 Devrim Gündüz <devrim@gunduz.org> 2.1.5-1
- Update to 2.1.5

* Thu May 5 2022 Devrim Gündüz <devrim@gunduz.org> 2.1.4-1
- Update to 2.1.4

* Thu Apr 7 2022 Devrim Gündüz <devrim@gunduz.org> 2.1.3-1
- Update to 2.1.3

* Tue Feb 1 2022 Devrim Gündüz <devrim@gunduz.org> 2.1.2-1
- Update to 2.1.2

* Tue Jan 4 2022 Devrim Gündüz <devrim@gunduz.org> 2.1.1-1
- Update to 2.1.1

* Thu Nov 4 2021 Devrim Gündüz <devrim@gunduz.org> 2.0.5-2
- Rebuild against LLVM 11 on SLES 15.
- Make sure that LLVM dependency versions are the same as
  PostgreSQL.

* Tue Oct 19 2021 Devrim Gündüz <devrim@gunduz.org> 2.0.5-1
- Update to 2.0.5

* Thu Sep 30 2021 Devrim Gündüz <devrim@gunduz.org> 2.0.3-1
- Update to 2.0.3

* Mon Jul 26 2021 Devrim Gündüz <devrim@gunduz.org> 1.17.1-1
- Update to 1.17.1

* Mon Jun 21 2021 Devrim Gündüz <devrim@gunduz.org> 1.17.0-1
- Update to 1.17.0

* Thu Mar 11 2021 Devrim Gündüz <devrim@gunduz.org> 1.16.0-1
- Update to 1.16.0

* Thu Feb 11 2021 Devrim Gündüz <devrim@gunduz.org> 1.15.3-2
- Split llvmjit into separate package

* Tue Feb 9 2021 Devrim Gündüz <devrim@gunduz.org> 1.15.3-1
- Update to 1.15.3

* Fri Feb 5 2021 Devrim Gündüz <devrim@gunduz.org> 1.15.2-1
- Update to 1.15.2

* Wed Jan 27 2021 Devrim Gündüz <devrim@gunduz.org> 1.15.1-2
- export PATH for pg_config, to get rid of patches.

* Tue Dec 22 2020 Devrim Gündüz <devrim@gunduz.org> 1.15.1-1
- Update to 1.15.1

* Wed Aug 19 2020 Devrim Gündüz <devrim@gunduz.org> 1.13.1-1
- Update to 1.13.1

* Wed Jul 29 2020 Devrim Gündüz <devrim@gunduz.org> 1.11.4-1
- Update to 1.11.4

* Wed May 13 2020 Devrim Gündüz <devrim@gunduz.org> 1.9.2-1
- Update to 1.9.2

* Tue Mar 31 2020 Devrim Gündüz <devrim@gunduz.org> 1.9.0-1
- Update to 1.9.0
- Switch to pgdg-srpm-macros

* Fri Jan 31 2020 Devrim Gündüz <devrim@gunduz.org> 1.8.2-1
- Update to 1.8.2

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Tue Sep 24 2019 Devrim Gündüz <devrim@gunduz.org> 1.7.6-1
- Update to 1.7.6

* Thu Aug 15 2019 Devrim Gündüz <devrim@gunduz.org> 1.7.4-1
- Update to 1.7.4

* Wed Jul 24 2019 Devrim Gündüz <devrim@gunduz.org> 1.7.3-1
- Update to 1.7.3

* Fri Apr 26 2019 Devrim Gündüz <devrim@gunduz.org> 1.7.1-1
- Update to 1.7.1

* Tue Jan 1 2019 Devrim Gündüz <devrim@gunduz.org> 1.4.2-1
- Update to 1.4.2

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.2.3-1.1
- Rebuild against PostgreSQL 11.0

* Tue Jun 19 2018 - Devrim Gündüz <devrim@gunduz.org> 1.2.3-1
- Update to 1.2.3

* Fri Sep 15 2017 - Devrim Gündüz <devrim@gunduz.org> 1.2.1-1
- Update to 1.2.1, per #2711

* Thu Jun 1 2017 - Devrim Gündüz <devrim@gunduz.org> 1.2.0-1
- Update to 1.2.0

* Sat Sep 17 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.6-1
- Update to 1.0.6

* Wed Jun 8 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.5-1
- Update to 1.0.5

* Tue Jan 26 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.4-1
- Update to 1.0.4

* Mon Jul 13 2015 - Devrim Gündüz <devrim@gunduz.org> 1.0.2-1
- Update to 1.0.2

* Tue Jan 20 2015 - Devrim Gündüz <devrim@gunduz.org> 0.9.3-1
- Update to 0.9.3

* Mon Aug 25 2014 - Pavel STEHULE <pavel.stehule@gmail.com> 0.9.2-1
- Initial packaging
