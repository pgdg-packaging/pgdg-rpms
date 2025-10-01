%global sname pgmp

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL Multiple Precision Arithmetic Extension
Name:		%{sname}_%{pgmajorversion}
Version:	1.0.5
Release:	5PGDG%{?dist}
License:	LGPL
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
# Make sure that we use Python 3.
Patch1:		%{sname}-python3.patch
URL:		https://dvarrazzo.github.io/pgmp/
BuildRequires:	postgresql%{pgmajorversion}-devel gmp-devel pgdg-srpm-macros
%if 0%{?suse_version} >= 1500
Requires:	libgmp10
%else
Requires:	gmp
%endif

Obsoletes:	%{sname}%{pgmajorversion} < 1.0.4-3

%description
The pgmp extension adds PostgreSQL data types wrapping the high performance
integer and rational data types offered by the GMP library.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgmp
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
This packages provides JIT support for pgmp
%endif

%prep
%setup -q -n %{sname}-%{version}
%patch -P 1 -p0

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%defattr(644,root,root,755)
%doc README.rst
%license COPYING
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/%{sname}/%{sname}*.sql

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.0.5-5PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Thu Jan 9 2025 Devrim Gündüz <devrim@gunduz.org> - 1.0.5-4PGDG
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.0.5-3PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Mon Feb 26 2024 Devrim Gunduz <devrim@gunduz.org> - 1.0.5-2PGDG
- Add SLES 15 support

* Mon Sep 11 2023 Devrim Gunduz <devrim@gunduz.org> - 1.0.5-1PGDG
- Update to 1.0.5
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.0.4-5.2
- Rebuild against LLVM 15 on SLES 15

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 1.0.4-5.1
- Modernise %%patch usage, which has been deprecated in Fedora 38

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0.4-5
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0.4-4
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.4-3
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Wed Sep 23 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.4-2
- Make sure that we use Python 3.

* Tue Mar 31 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.4-1
- Update to 1.0.4

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0.2-1.1
- Rebuild against PostgreSQL 11.0

* Mon Jan 19 2015 - Devrim Gündüz <devrim@gunduz.org> 1.0.2-1
- Initial RPM packaging for PostgreSQL RPM Repository
