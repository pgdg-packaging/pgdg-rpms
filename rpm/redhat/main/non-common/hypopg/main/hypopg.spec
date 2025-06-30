%global sname	hypopg

%{!?llvm:%global llvm 1}

Summary:	Hypothetical Indexes support for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.4.2
Release:	1PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/HypoPG/hypopg/archive/%{version}.tar.gz
URL:		https://github.com/HypoPG/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-libs

%description
HypoPG is a PostgreSQL extension adding support for hypothetical indexes.

An hypothetical -- or virtual -- index is an index that doesn't really exists,
and thus doesn't cost CPU, disk or any resource to create. They're useful to
know if specific indexes can increase performance for problematic queries,
since you can know if PostgreSQL will use these indexes or not without having
to spend resources to create them.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for hypopg
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
This package provides JIT support for hypopg
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
   %{pginstdir}/lib/bitcode/%{sname}/import/*.bc
%endif

%changelog
* Mon Jun 30 2025 Devrim Gunduz <devrim@gunduz.org> - 1.4.2-1PGDG
- Update to 1.4.2 per changes described at:
  https://github.com/HypoPG/hypopg/releases/tag/1.4.2

* Thu Jan 2 2025 Devrim Gündüz <devrim@gunduz.org> - 1.4.1-3PGDG
- Update LLVM dependencies and improve description

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.4.1-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Sun Apr 28 2024 Devrim Gunduz <devrim@gunduz.org> - 1.4.1-1PGDG
- Update to 1.4.1 per changes described at:
  https://github.com/HypoPG/hypopg/releases/tag/1.4.1

* Tue Aug 1 2023 Devrim Gunduz <devrim@gunduz.org> - 1.4.0-2PGDG
- Cleanup rpmlint warnings
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.4.0-1.1
- Rebuild against LLVM 15 on SLES 15

* Mon May 29 2023 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-1
- Update to 1.4.0

* Wed Jan 11 2023 John Harvey <john.harvey@crunchydata.com> - 1.3.1-3
- Update license type

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Jun 23 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-1
- Update to 1.3.1

* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-1
- Update to 1.3.0

* Tue Mar 2 2021 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1
- Update to 1.2.0

* Thu Jul 9 2020 Devrim Gündüz <devrim@gunduz.org> - 1.1.4-1
- Update to 1.1.4

* Fri Mar 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.1.3-2
- Switch to using pgdg-srpm-macros dependency

* Fri Sep 6 2019 Devrim Gündüz <devrim@gunduz.org> - 1.1.3-1
- Update to 1.1.3

* Thu Dec 6 2018 Devrim Gündüz <devrim@gunduz.org> - 1.1.2-1
- Update to 1.1.2

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.1.1-1.1
- Rebuild against PostgreSQL 11.0

* Thu Mar 29 2018 - Devrim Gündüz <devrim@gunduz.org> 1.1.1-1
- Update to 1.1.1
- Update URLs

* Thu Oct 5 2017 - Devrim Gündüz <devrim@gunduz.org> 1.1.0-1
- Update to 1.1.0

* Thu Oct 27 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-1
- Update to 1.0.0

* Fri Oct 21 2016 - Devrim Gündüz <devrim@gunduz.org> 0.0.4-1
- Initial RPM packaging for PostgreSQL RPM Repository
