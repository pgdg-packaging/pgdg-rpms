%global sname postgresql-unit

%{!?llvm:%global llvm 1}

Summary:	SI Units for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	7.10
Release:	6PGDG%{?dist}
License:	BSD
Source0:	https://github.com/ChristophBerg/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/ChristophBerg/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel flex
Requires:	postgresql%{pgmajorversion}-server

%description
postgresql-unit implements a PostgreSQL datatype for SI units, plus byte.
The base units can be combined to named and unnamed derived units using
operators defined in the PostgreSQL type system. SI prefixes are used for
input and output, and quantities can be converted to arbitrary scale.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for postgresql-unit
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
This package provides JIT support for postgresql-unit
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/unit.so
%{pginstdir}/share/extension/unit*.sql
%{pginstdir}/share/extension/unit.control
%{pginstdir}/share/extension/unit_prefixes.data
%{pginstdir}/share/extension/unit_units.data

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/uni*.bc
   %{pginstdir}/lib/bitcode/unit/*.bc
%endif

%changelog
* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 7.10-6PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 7.10-5PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Sat Sep 27 2025 Devrim Gündüz <devrim@gunduz.org> - 7.7-3PGDG
- Update LLVM dependencies

* Tue Feb 25 2025 Devrim Gündüz <devrim@gunduz.org> - 7.10-3PGDG
- Add missing BR

* Mon Jan 27 2025 Devrim Gündüz <devrim@gunduz.org> - 7.10-2PGDG
- Remove redundant BR

* Wed Dec 11 2024 Devrim Gündüz <devrim@gunduz.org> - 7.10-1PGDG
- Update to 7.10 per changes described at:
  https://github.com/df7cb/postgresql-unit/releases/tag/7.10

* Mon Sep 16 2024 Devrim Gündüz <devrim@gunduz.org> - 7.9-1PGDG
- Update to 7.9 per changes described at:
  https://github.com/df7cb/postgresql-unit/releases/tag/7.9
  https://github.com/df7cb/postgresql-unit/releases/tag/7.8

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 7.7-3PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Mon Feb 26 2024 Devrim Gündüz <devrim@gunduz.org> - 7.7-2PGDG
- Add PGDG branding
- Fix rpmlint warnings

* Mon Apr 24 2023 Devrim Gündüz <devrim@gunduz.org> - 7.7-1
- Update to 7.7

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org>- 7.4-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> - 7.4-1
- Update to 7.4
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 7.2-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>- 7.2-1.1
- Rebuild for PostgreSQL 12

* Thu Sep 5 2019 Devrim Gündüz <devrim@gunduz.org> 7.2-1
- Update to 7.2

* Thu Jul 25 2019 Devrim Gündüz <devrim@gunduz.org> 7.1-1
- Update to 7.1

* Tue Oct 23 2018 Devrim Gündüz <devrim@gunduz.org> 7.0-1
- Update to 7.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> 6.0-2.1
- Rebuild against PostgreSQL 11.0

* Thu Aug 23 2018 - Devrim Gündüz <devrim@gunduz.org> 6.0-2
- Add v11+ bitcode conditionals

* Thu Mar 22 2018 - Devrim Gündüz <devrim@gunduz.org> 6.0-1
- Update to 6.0

* Sun May 28 2017 - Devrim Gündüz <devrim@gunduz.org> 3.1-1
- Update to 3.1

* Thu Apr 27 2017 - Devrim Gündüz <devrim@gunduz.org> 3.0-1
- Update to 3.0
- Add support for Power RPMs.

* Tue Jan 10 2017 - Devrim Gündüz <devrim@gunduz.org> 2.0-1
- Update to 2.0

* Thu Sep 22 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Initial RPM packaging for PostgreSQL YUM Repository
