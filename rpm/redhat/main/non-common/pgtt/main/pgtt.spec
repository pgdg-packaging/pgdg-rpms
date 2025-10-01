%global sname pgtt

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL Global Temporary Tables Extension
Name:		%{sname}_%{pgmajorversion}
Version:	4.4
Release:	1PGDG%{?dist}
License:	GPLv2
Source0:	https://github.com/darold/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/darold/%{sname}

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

%description
pgtt is a PostgreSQL extension to create, manage and use Oracle-style Global
Temporary Tables and the others RDBMS.

The objective of this extension it to propose an extension to provide the
Global Temporary Table feature waiting for an in core implementation. The
main interest of this extension is to mimic the Oracle behavior with GTT when
you can not or don't want to rewrite the application code when migrating to
PostgreSQL. In all other case best is to rewrite the code to use standard
PostgreSQL temporary tables.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgtt
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
This package provides JIT support for pgtt
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH USE_PGXS=1 %make_install install DESTDIR=%{buildroot}
# Install README and howto file under PostgreSQL installation directory with a better name:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}/%{pginstdir}/doc/extension/README.md

%files
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%doc %{pginstdir}/doc/extension/%{sname}.md
%license COPYING
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}*.sql

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Sun Aug 3 2025 Devrim Gündüz <devrim@gunduz.org> - 4.4-1PGDG
- Update to 4.4 per changes described at:
  https://github.com/darold/pgtt/releases/tag/v4.4

* Wed Jun 11 2025 Devrim Gündüz <devrim@gunduz.org> - 4.3-1PGDG
- Update to 4.3 per changes described at:
  https://github.com/darold/pgtt/releases/tag/v4.3
  https://github.com/darold/pgtt/releases/tag/v4.2

* Sat Mar 22 2025 Devrim Gündüz <devrim@gunduz.org> - 4.1-1PGDG
- Update to 4.1 per changes described at:
  https://github.com/darold/pgtt/releases/tag/v4.1

* Fri Feb 21 2025 Devrim Gündüz <devrim@gunduz.org> - 4.0-3PGDG
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 4.0-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Tue Jun 4 2024 Devrim Gündüz <devrim@gunduz.org> - 4.0-1PGDG
- Update to 4.0 per changes described at:
  https://github.com/darold/pgtt/releases/tag/v4.0

* Fri Apr 12 2024 Devrim Gündüz <devrim@gunduz.org> - 3.2-1PGDG
- Update to 3.2 per changes described at:
  https://github.com/darold/pgtt/releases/tag/v3.2

* Tue Dec 26 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1-1PGDG
- Update to 3.1

* Mon Sep 18 2023 Devrim Gündüz <devrim@gunduz.org> - 3.0-1PGDG
- Update to 3.0
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 2.10-1.1
- Rebuild against LLVM 15 on SLES 15

* Mon Feb 27 2023 Devrim Gündüz <devrim@gunduz.org> - 2.10-1
- Update to 2.10

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.9-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Fri Sep 16 2022 Devrim Gündüz <devrim@gunduz.org> - 2.9-1
- Update to 2.9

* Sat Jun 4 2022 Devrim Gündüz <devrim@gunduz.org> - 2.8-1
- Update to 2.8

* Fri Sep 24 2021 Devrim Gündüz <devrim@gunduz.org> - 2.6-1
- Update to 2.6

* Wed Sep 22 2021 Devrim Gündüz <devrim@gunduz.org> - 2.5-1
- Update to 2.5
- Fix RHEL 8 / ppc64le support.

* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> 2.4-1
- Update to 2.4

* Fri Apr 2 2021 Devrim Gündüz <devrim@gunduz.org> 2.3-1
- Update to 2.3
- Export PATH, and remove pgxs patches.

* Tue Nov 17 2020 Devrim Gündüz <devrim@gunduz.org> 2.2-1
- Initial packaging for PostgreSQL RPM repository
