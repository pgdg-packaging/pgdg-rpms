%global sname	passwordcheck_cracklib

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	3.1.0
Release:	3PGDG%{?dist}
Summary:	PostgreSQL passwordcheck extension, built with cracklib.
License:	BSD
URL:		https://github.com/devrimgunduz/%{sname}/
Source0:	https://github.com/devrimgunduz/%{sname}/archive/%{version}.tar.gz
Requires:	postgresql%{pgmajorversion} cracklib
%if 0%{?suse_version} >= 1500
Requires:	cracklib-dict-full
%else
Requires:	cracklib-dicts
%endif

BuildRequires:	cracklib-devel postgresql%{pgmajorversion}-devel

%description
This is the regular PostgreSQL passwordcheck extension, built with cracklib.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for passwordcheck_cracklib
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
This packages provides JIT support for passwordcheck_cracklib
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%files
%defattr(-,root,root,-)
%{pginstdir}/lib/%{sname}.so

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 3.1.0-3PGDG
- Update LLVM dependencies
- Remove SLES 12 support

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 3.1.0-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Fri Apr 26 2024 Devrim Gunduz <devrim@gunduz.org> - 3.1.0-1PGDG
- Update to 3.1.0 per changes described at:
  https://github.com/devrimgunduz/passwordcheck_cracklib/releases/tag/3.1.0

* Mon Feb 26 2024 Devrim Gunduz <devrim@gunduz.org> - 3.0.0-3PGDG
- Add SLES 15 support

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 3.0.0-2PGDG
- Add PGDG branding
- Clean up rpmlint warnings

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 3.0.0-1.1
- Rebuild against LLVM 15 on SLES 15

* Thu Jan 12 2023 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-1
- Update to 3.0.0

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu Jan 27 2022 Devrim Gündüz <devrim@gunduz.org> 2.0.0-1
- Update to 2.0.0
- Remove PGXS patches, and use PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 1.0.2-3
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Wed Aug 22 2018 - Devrim Gündüz <devrim@gunduz.org> 1.0.2-2
- Add v11 code to spec file

* Tue May 30 2017 - Devrim Gündüz <devrim@gunduz.org> 1.0.2-1
- Initial packaging
