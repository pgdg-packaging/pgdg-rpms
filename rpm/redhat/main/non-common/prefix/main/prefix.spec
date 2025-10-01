%global sname prefix

%{!?llvm:%global llvm 1}

Summary:	Prefix Range module for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.2.10
Release:	3PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/dimitri/%{sname}/archive/v%{version}.zip
URL:		https://github.com/dimitri/prefix
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 1.2.9-2

%description
The prefix project implements text prefix matches operator (prefix @>
text) and provide a GiST opclass for indexing support of prefix
searches.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for prefix
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
This package provides JIT support for prefix
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %make_install DESTDIR=%{buildroot}
# Rename docs to avoid conflict:
%{__mv} %{buildroot}%{pginstdir}/doc/extension/README.md %{buildroot}%{pginstdir}/doc/extension/README-prefix.md
%{__mv} %{buildroot}%{pginstdir}/doc/extension/TESTS.md %{buildroot}%{pginstdir}/doc/extension/TESTS-prefix.md

%postun -p /sbin/ldconfig
%post -p /sbin/ldconfig

%files
%doc %{pginstdir}/doc/extension/README-prefix.md
%doc %{pginstdir}/doc/extension/TESTS-prefix.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*

%if %llvm
%files llvmjit
 %{pginstdir}/lib/bitcode/%{sname}*.bc
 %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Wed Feb 5 2025 Devrim Gündüz <devrim@gunduz.org> - 1.2.10-3PGDG
- Update LLVM dependencies and remove redundant BR.

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.2.10-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Mon Jul 31 2023 Devrim Gunduz <devrim@gunduz.org> - 1.2.10-1PGDG
- Update to 1.2.10
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.2.9-4.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.2.9-4
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> 1.2.9-3
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.2.9-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 1.2.9-1.1
- Rebuild for PostgreSQL 12

* Thu Sep 26 2019 - Devrim Gündüz <devrim@gunduz.org> 1.2.9-1
- Update to 1.2.9

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Mon Jun 18 2018 - Devrim Gündüz <devrim@gunduz.org> 1.2.8-1
- Update to 1.2.8
- Add patches for all supported PostgreSQL releases
- Fix some rpmlint warnings

* Thu Mar 3 2016 - Devrim Gündüz <devrim@gunduz.org> 1.2.4-1
- Update to 1.2.4
- Put back Group: tag for RHEL 5.

* Mon Jan 12 2015 - Devrim Gündüz <devrim@gunduz.org> 1.2.3-1
- Omit deprecated Group: tags and %%clean section
- Use %%make_install macro
- No need to cleanup buildroot during %%install
- Remove %%defattr
- Run ldconfig
- Update URL

* Mon Jan 12 2015 - Devrim Gündüz <devrim@gunduz.org> 1.2.3-1
- Update to 1.2.3

* Mon Jan 7 2013 - Devrim Gündüz <devrim@gunduz.org> 1.2.0-1
- Update to 1.2.0
- Fix for PostgreSQL 9.0+ RPM layout.

* Fri Dec 11 2009 - Devrim Gündüz <devrim@gunduz.org> 1.1.0-1
- Update to 1.1.0

* Fri May 30 2008 - Devrim Gündüz <devrim@gunduz.org> 0.2-1
- Initial RPM packaging for yum.postgresql.org
