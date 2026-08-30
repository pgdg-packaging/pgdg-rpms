%global debug_package %{nil}
%global sname db2_fdw
%global db2_home "/opt/ibm/db2/V11.5/"

%global __requires_exclude libdb2.so.1


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

Summary:	PostgreSQL DB2 Foreign Data Wrapper
Name:		%{sname}_%{pgmajorversion}
Version:	18.2.0
Release:	2PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/Living-Mainframe/%{sname}/archive/refs/tags/%{version}.tar.gz
URL:		https://github.com/Living-Mainframe/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRequires:	libstdc++ pam

Obsoletes:	%{sname}%{pgmajorversion} < 4.0.0-2

%description
db2_fdw is a PostgreSQL extension that provides a Foreign Data Wrapper for
easy and efficient access to DB2 databases, including pushdown of WHERE
conditions and required columns as well as comprehensive EXPLAIN support.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for db2_fdw
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} == 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?suse_version} == 1600
BuildRequires:	llvm19-devel clang19-devel
Requires:	llvm19
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for db2_fdw
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
export DB2_HOME="%{db2_home}"
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} DESTDIR=%{buildroot} USE_PGXS=1 %{?_smp_mflags} %{with_llvm_arg} install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/*%{sname}.md
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/*%{sname}*.sql
%{pginstdir}/lib/%{sname}.so

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/source/*.bc
%endif

%changelog
* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - 18.2.0-2PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51

* Sun Jul 26 2026 - Devrim Gündüz <devrim@gunduz.org> 18.2.0-1PGDG
- Update to 18.2.0 per changes described at:
  https://github.com/Living-Mainframe/db2_fdw/releases/tag/18.2.0

* Wed May 6 2026 - Devrim Gündüz <devrim@gunduz.org> 18.1.2-1PGDG
- Update to 18.1.2 per changes described at:
  https://github.com/Living-Mainframe/db2_fdw/releases/tag/18.1.2

* Sat Feb 7 2026 - Devrim Gündüz <devrim@gunduz.org> 18.1.1-1PGDG
- Update to 18.1.1 per changes described at:
  https://github.com/Living-Mainframe/db2_fdw/releases/tag/18.1.1

* Mon Nov 24 2025 - Devrim Gündüz <devrim@gunduz.org> 18.1.0-1PGDG
- Update to 18.1.0 per changes described at:
  https://github.com/Living-Mainframe/db2_fdw/releases/tag/18.1.0

* Mon Nov 3 2025 - Devrim Gündüz <devrim@gunduz.org> 18.0.1-2PGDG
- Exclude libdb2.so.1 dependency. It is not installed via RPMs anyway.

* Sun Nov 2 2025 - Devrim Gündüz <devrim@gunduz.org> 18.0.1-1PGDG
- Update to 18.0.1 per changes described at:
  https://github.com/Living-Mainframe/db2_fdw/releases/tag/18.0.1
  https://github.com/Living-Mainframe/db2_fdw/releases/tag/18.0.0
  https://github.com/Living-Mainframe/db2_fdw/releases/tag/17.0.0

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 7.0.0-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Mon May 26 2025 - Devrim Gündüz <devrim@gunduz.org> 7.0.0-1PGDG
- Update to 7.0.0

* Fri Feb 21 2025 - Devrim Gündüz <devrim@gunduz.org> 6.0.1-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Fri Mar 29 2024 - Devrim Gündüz <devrim@gunduz.org> 6.0.1-1PGDG
- Update to 6.0.1

* Fri Sep 29 2023 - Devrim Gündüz <devrim@gunduz.org> 6.0.0-1PGDG
- Update to 6.0.0
- Add PGDG branding
- Modernise LLVM portion of the spec file
- Cleanup rpmlint warnings

* Thu Sep 8 2022 - Devrim Gündüz <devrim@gunduz.org> 5.0.0-1
- Update to 5.0.0
- Export PATH for pg_config, so get rid of patches.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 4.0.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 24 2020 - Devrim Gündüz <devrim@gunduz.org> 4.0.0-1
- Update to 4.0.0

* Mon Aug 17 2020 - Devrim Gündüz <devrim@gunduz.org> 3.0.3-1
- Update to 3.0.3

* Mon Aug 3 2020 - Devrim Gündüz <devrim@gunduz.org> 3.0.2-1
- Update to 3.0.2

* Tue Jul 28 2020 - Devrim Gündüz <devrim@gunduz.org> 3.0.1-1
- Update to 3.0.1

* Sun Mar 22 2020 - Devrim Gündüz <devrim@gunduz.org> 3.0.0-1
- Update to 3.0.0

* Sat Nov 23 2019 - Devrim Gündüz <devrim@gunduz.org> 2.0.1-1
- Initial packaging for PostgreSQL non-free RPM Repository
