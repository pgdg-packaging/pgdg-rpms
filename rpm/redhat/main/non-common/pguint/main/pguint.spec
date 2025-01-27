%global sname pguint

%{!?llvm:%global llvm 1}

Summary:	Unsigned and other extra integer types for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.20231206
Release:	3PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/petere/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/petere/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} <= 1.20200704-2

%description
This extension provides additional integer types for PostgreSQL:

* int1 (signed 8-bit integer)
* uint1 (unsigned 8-bit integer)
* uint2 (unsigned 16-bit integer)
* uint4 (unsigned 32-bit integer)
* uint8 (unsigned 64-bit integer)

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pguint
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
This package provides JIT support for pguint
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%license LICENSE
%{pginstdir}/lib/uint.so
%{pginstdir}/share/extension/uint*

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/uint.index.bc
    %{pginstdir}/lib/bitcode/uint/*.bc
%endif

%changelog
* Sun Jan 19 2025 Devrim Gunduz <devrim@gunduz.org> - 1.20231206-3PGDG
- Update LLVM dependencies
- Install license file

* Mon Jul 29 2024 Devrim Gunduz <devrim@gunduz.org> - 1.20231206-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Sun Feb 25 2024 Devrim Gunduz <devrim@gunduz.org> - 1.20231206-1PGDG
- Update to 1.20231206
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.20220601-3.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.20220601-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Jun 1 2022 Devrim Gündüz <devrim@gunduz.org> - 1.20220601-2
- Split llvmjit into its own subpackage, which also will fix
  RHEL 8 - ppc64le builds.

* Wed Jun 1 2022 Devrim Gündüz <devrim@gunduz.org> - 1.20220601-1
- Update to 1.20220601

* Sat Jun 5 2021 Devrim Gündüz <devrim@gunduz.org> - 1.20200704-3
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.20200704-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Wed Aug 12 2020 Devrim Gündüz <devrim@gunduz.org> - 1.20200704-1
- Initial RPM packaging for PostgreSQL YUM Repository
