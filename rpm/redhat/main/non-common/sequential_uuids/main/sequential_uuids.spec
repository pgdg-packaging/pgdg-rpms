%global sname sequential-uuids
%global pname sequential_uuids

%{!?llvm:%global llvm 1}

Summary:	Sequential UUID generators for PostgreSQL
Name:		%{pname}_%{pgmajorversion}
Version:	1.0.3
Release:	1PGDG%{?dist}
License:	MIT
Source0:	https://github.com/tvondra/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/tvondra/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for sequential_uuids
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
This packages provides JIT support for sequential_uuids
%endif

%description
This PostgreSQL extension implements two UUID generators with sequential
patterns, which helps to reduce random I/O patterns associated with regular
entirely-random UUID.

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
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}*sql
%{pginstdir}/share/extension/%{pname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{pname}*.bc
   %{pginstdir}/lib/bitcode/%{pname}/*.bc
%endif

%changelog
* Mon Dec 23 2024 Devrim Gündüz <devrim@gunduz.org> - 1.0.3-1PGDG
- Update to 1.0.3 per changes described at:
  https://github.com/tvondra/sequential-uuids/releases/tag/v1.0.3

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.0.2-5PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Wed Sep 13 2023 Devrim Gunduz <devrim@gunduz.org> - 1.0.2-4PGDG
- Add PGDG branding
- Cleanup rpmlint warnings

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.0.2-3.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0.2-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu Sep 29 2022 Devrim Gündüz <devrim@gunduz.org> 1.0.2-2
- Fix builds on RHEL 8 - ppc64le (switch to new LLVM scheme)

* Thu Jan 20 2022 Devrim Gündüz <devrim@gunduz.org> 1.0.2-1
- Initial packaging for PostgreSQL RPM Repository
