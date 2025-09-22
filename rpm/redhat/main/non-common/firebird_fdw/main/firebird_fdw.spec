%global sname firebird_fdw

%{!?llvm:%global llvm 1}

Summary:	A PostgreSQL foreign data wrapper (FDW) for Firebird
Name:		%{sname}_%{pgmajorversion}
Version:	1.4.1
Release:	1PGDG%{dist}
Source0:	https://github.com/ibarwick/%{sname}/archive/refs/tags/%{version}.tar.gz
URL:		https://github.com/ibarwick/%{sname}
License:	PostgreSQL
BuildRequires:	postgresql%{pgmajorversion}-devel firebird-devel
BuildRequires:	libfq >= 0.6.1
Requires:	postgresql%{pgmajorversion}-server

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for firebird_fdw
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm => 19.0
%endif

%description llvmjit
This package provides JIT support for firebird_fdw
%endif

%description
This is a foreign data wrapper (FDW) to connect PostgreSQL to Firebird.
It provides both read (SELECT) and write (INSERT/UPDATE/DELETE)
support, WHERE-clause pushdowns, connection caching and Firebird transaction
support.

This code is very much work-in-progress; USE AT YOUR OWN RISK.

%prep
%setup -q -n %{sname}-%{version}

%build
export PG_CONFIG=%{pginstdir}/bin/pg_config
PG_CPPFLAGS="-I%{_includedir}/firebird" USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
export PG_CONFIG=%{pginstdir}/bin/pg_config
USE_PGXS=1 %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%files
%defattr(-, root, root)
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Mon Sep 22 2025 Devrim Gündüz <devrim@gunduz.org> - 1.4.1-1PGDG
- Update to 1.4.1 per changes described at
  https://github.com/ibarwick/firebird_fdw/releases/tag/1.4.1

* Fri Feb 21 2025 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-4PGDG
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-3PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Tue May 28 2024 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-2PGDG
- Rebuild against libfq 0.6.1

* Thu May 23 2024 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-1PGDG
- Update to 1.4.0 per changes described at
  https://github.com/ibarwick/firebird_fdw/releases/tag/1.4.0

* Thu Jun 22 2023 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-1PGDG
- Update to 1.3.1
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.3.0-1.1
- Rebuild against LLVM 15 on SLES 15

* Sat Dec 31 2022 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-1
- Update to 1.3.0

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.2.3-4
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu Aug 25 2022 Devrim Gündüz <devrim@gunduz.org> - 1.2.3-3
- Update SLES 15 dependencies for SP4.

* Mon Feb 21 2022 Devrim Gündüz <devrim@gunduz.org> - 1.2.3-2
- Rebuild against libfq 0.4.3

* Mon Feb 21 2022 Devrim Gündüz <devrim@gunduz.org> - 1.2.3-1
- Update to 1.2.3

* Mon Sep 20 2021 Devrim Gündüz <devrim@gunduz.org> - 1.2.2-1
- Update to 1.2.2

* Wed Oct 21 2020 Devrim Gündüz <devrim@gunduz.org> - 1.2.1-1
- Update to 1.2.1
- Add support for Power.

* Tue Oct 20 2020 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1
- Initial packaging for the PostgreSQL RPM repository. This is
  an improved version of the upstream spec file.
