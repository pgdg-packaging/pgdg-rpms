%global sname topn

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL extension that returns the top values in a database
Name:		%{sname}_%{pgmajorversion}
Version:	2.7.0
Release:	4PGDG%{dist}
License:	AGPLv3
Source0:	https://github.com/citusdata/postgresql-%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/citusdata/postgresql-%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel libxml2-devel
Requires:	postgresql%{pgmajorversion}-server

%description
TopN is an open source PostgreSQL extension that returns the top values
in a database according to some criteria. TopN takes elements in a data
set, ranks them according to a given rule, and picks the top elements in
that data set. When doing this, TopN applies an approximation algorithm
to provide fast results using few compute and memory resources.

The TopN extension becomes useful when you want to materialize top
values, incrementally update these top values, and/or merge top values
from different time intervals. If you're familiar with the PostgreSQL
HLL extension, you can think of TopN as its cousin.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for topn
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
This package provides JIT support for topn
%endif

%prep
%setup -q -n postgresql-%{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %make_install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 2.7.0-4PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 2.7.0-3PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Tue Jan 28 2025 Devrim Gündüz <devrim@gunduz.org> - 2.7.0-2PGDG
- Update LLVM dependencies

* Sat Oct 19 2024 Devrim Gündüz <devrim@gunduz.org> - 2.7.0-1PGDG
- Update to 2.7.0

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 2.6.0-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Tue Sep 5 2023 Devrim Gündüz <devrim@gunduz.org> - 2.6.0-1PGDG
- Update to 2.6.0
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 2.4.0-3.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue Sep 20 2022 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-2
- Fix builds on RHEL 8 - ppc64le (switch to new LLVM scheme)

* Mon Sep 13 2021 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-1
- Update to 2.4.0

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> - 2.3.1-2
- Remove pgxs patches, and export PATH instead.

* Tue Dec 1 2020 Devrim Gündüz <devrim@gunduz.org> - 2.3.1-1
- Update to 2.3.1

* Wed Nov 6 2019 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-1
- Update to 2.3.0

* Fri Sep 6 2019 Devrim Gündüz <devrim@gunduz.org> - 2.2.2-1
- Update to 2.2.2

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Thu Aug 23 2018 - Devrim Gündüz <devrim@gunduz.org> 2.1.0-1
- Update to 2.1.0

* Sat Aug 11 2018 - Devrim Gündüz <devrim@gunduz.org> 2.0.2-2
- Ignore .bc files on PPC arch.

* Thu Mar 29 2018 - Devrim Gündüz <devrim@gunduz.org> 2.0.2-1
- Update to 2.0.2

* Tue Mar 27 2018 - Devrim Gündüz <devrim@gunduz.org> 2.0.1-1
- Initial RPM packaging for PostgreSQL RPM Repository.
