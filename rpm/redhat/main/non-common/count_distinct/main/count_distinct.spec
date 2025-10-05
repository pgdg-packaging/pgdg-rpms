%global sname count_distinct

%{!?llvm:%global llvm 1}

Summary:	A hash-table based alternative to COUNT(DISTINCT ...) aggregate in PostgreSQL.
Name:		%{sname}_%{pgmajorversion}
Version:	3.0.2
Release:	3PGDG%{?dist}
License:	BSD
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
URL:		https://github.com/tvondra/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 3.0.1-2

%description
This extension provides an alternative to COUNT(DISTINCT ...) which for large
amounts of data often ends in sorting and poor performance.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for count_distinct
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
This package provides JIT support for count_distinct
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install
%{__mkdir} -p %{buildroot}/%{pginstdir}/doc/extension/
%{__cp} README.md %{buildroot}/%{pginstdir}/doc/extension/README-%{sname}.md

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%{pginstdir}/lib/count_distinct.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Sun Oct 5 2025 Devrim Gunduz <devrim@gunduz.org> - 3.0.2-3PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 3.0.2-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Thu Jan 9 2025 Devrim Gunduz <devrim@gunduz.org> - 3.0.2-1PGDG
- Update to 3.0.2 per changes described at:
  https://github.com/tvondra/count_distinct/releases/tag/v3.0.2
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gunduz <devrim@gunduz.org> - 3.0.1-6PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 3.0.1-5.1
- Remove RHEL 6 bits
- Add PGDG branding
- Fix rpmlint warnings

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 3.0.1-4.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 3.0.1-4
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Fri May 21 2021 Devrim Gündüz <devrim@gunduz.org> 3.0.1-3
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 3.0.1-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Sun Nov 3 2019 Devrim Gündüz <devrim@gunduz.org> - 3.0.1-1
- Initial packaging for PostgreSQL RPM Repository
