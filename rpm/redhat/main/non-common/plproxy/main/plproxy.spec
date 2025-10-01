%global sname plproxy

%{!?llvm:%global llvm 1}

Summary:	PL/Proxy is database partitioning system implemented as PL language.
Name:		%{sname}_%{pgmajorversion}
Version:	2.11.0
Release:	4PGDG%{?dist}
License:	ISC
URL:		https://plproxy.github.io
Source0:	https://github.com/%{sname}/%{sname}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel bison flex >= 2.5.4
Requires:	postgresql%{pgmajorversion}

Obsoletes:	%{sname}%{pgmajorversion} < 2.10.0-2

%description
PL/Proxy is database partitioning system implemented as PL language.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for plproxy
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
This package provides JIT support for plproxy
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%defattr(-,root,root,-)
%license COPYRIGHT
%doc README.md AUTHORS COPYRIGHT
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Wed Feb 26 2025 Devrim Gündüz <devrim@gunduz.org> - 2.11.0-4PGDG
- Add missing BR

* Mon Jan 27 2025 Devrim Gündüz <devrim@gunduz.org> - 2.11.0-3PGDG
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 2.11.0-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Sat Sep 16 2023 Devrim Gunduz <devrim@gunduz.org> - 2.11.0-1PGDG
- Update 2.11.0

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 2.10.0-4.1
- Remove RHEL 6 bits
- Add PGDG branding
- Fix rpmlint warnings

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 2.10.0-4.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.10.0-4
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> - 2.10.0-3
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.10.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Sun Sep 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.10.0-1
- Update to 2.10

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> 2.9-1.1
- Rebuild for PostgreSQL 12

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 2.9-1
- Update to 2.9

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.8-1.1
- Rebuild against PostgreSQL 11.0

* Mon Oct 9 2017 - Devrim Gündüz <devrim@gunduz.org> 2.8-1
- Update to 2.8

* Mon Jan 2 2017 - Devrim Gündüz <devrim@gunduz.org> 2.7-1
- Update to 2.7

* Fri Sep 11 2015 - Devrim Gündüz <devrim@gunduz.org> 2.6-1
- Update to 2.6

* Tue Jan 15 2013 - Devrim Gündüz <devrim@gunduz.org> 2.5-1
- Update to 2.5

* Fri Jul 27 2012 - Devrim Gündüz <devrim@gunduz.org> 2.4-1
- Update to 2.4
- Update download URL.

* Mon Feb 13 2012 - Devrim Gündüz <devrim@gunduz.org> 2.3-1
- Update to 2.3

* Tue Oct 12 2010 - Devrim Gündüz <devrim@gunduz.org> 2.1-2
- Apply 9.0 related changes to spec file.
- Get rid of ugly hacks in spec.

* Sat May 15 2010 - Devrim Gündüz <devrim@gunduz.org> 2.1-1
- Update to 2.1

* Wed Oct 28 2009 - Devrim Gündüz <devrim@gunduz.org> 2.0.9-1
- Update to 2.0.9

* Mon Feb 2 2009 - Devrim Gündüz <devrim@gunduz.org> 2.0.8-1
- Update to 2.0.8

* Tue Oct 7 2008 - Devrim Gündüz <devrim@gunduz.org> 2.0.7-1
- Update to 2.0.7

* Sat Sep 20 2008 - Devrim Gündüz <devrim@gunduz.org> 2.0.6-1
- Update to 2.0.6

* Sun Jun 15 2008 - Devrim Gündüz <devrim@gunduz.org> 2.0.5-1
- Update to 2.0.5
- Remove scanner.c and scanner.h, they are no longer needed.

* Tue Aug 28 2007 - Devrim Gündüz <devrim@gunduz.org> 2.0.2-2
- Add pre-generated scanner.c and scanner.h as sources. Only very
recent versions of flex can compile plproxy.

* Tue Aug 28 2007 - Devrim Gündüz <devrim@gunduz.org> 2.0.2-1
- Initial build 
