%global sname hll

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL extension adding HyperLogLog data structures as a native data type
Name:		%{sname}_%{pgmajorversion}
Version:	2.18
Release:	5PGDG%{dist}
License:	Apache
Source0:	https://github.com/citusdata/postgresql-%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/citusdata/postgresql-%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel libxml2-devel
Requires:	postgresql%{pgmajorversion}-server
Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

%description
This Postgres module introduces a new data type hll which is a
HyperLogLog data structure. HyperLogLog is a fixed-size, set-like
structure used for distinct value counting with tunable precision. For
example, in 1280 bytes hll can estimate the count of tens of billions of
distinct values with only a few percent error.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for hll
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
This package provides JIT support for hll
%endif


%prep
%setup -q -n postgresql-%{sname}-%{version}

%build
PG_CONFIG=%{pginstdir}/bin/pg_config %{__make} %{?_smp_mflags}

%install
PG_CONFIG=%{pginstdir}/bin/pg_config %make_install
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
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Sun Oct 5 2025 Devrim Gunduz <devrim@gunduz.org> - 2.18-5PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 2.18-4PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Thu Jan 2 2025 Devrim Gündüz <devrim@gunduz.org> - 2.18-3PGDG
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 2.18-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Sat Sep 16 2023 - Devrim Gündüz <devrim@gunduz.org> - 2.18-1PGDG
- Update to 2.18
- Add PGDG branding
- Cleanup rpmlint warnings

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 2.17-2.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.17-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Sep 21 2022 - Devrim Gündüz <devrim@gunduz.org> - 2.17-1
- Update to 2.17

* Mon Sep 13 2021 - Devrim Gündüz <devrim@gunduz.org> - 2.16-1
- Update to 2.16

* Wed Dec 16 2020 - Devrim Gündüz <devrim@gunduz.org> - 2.15.1-1
- Update to 2.15.1

* Mon Nov 30 2020 - Devrim Gündüz <devrim@gunduz.org> 2.15-1
- Update to 2.15

* Sun Jun 14 2020 - Devrim Gündüz <devrim@gunduz.org> 2.14-1
- Update to 2.14

* Wed Nov 6 2019 - Devrim Gündüz <devrim@gunduz.org> 2.13-1
- Update to 2.13

* Tue Apr 16 2019 - Devrim Gündüz <devrim@gunduz.org> 2.12-1
- Update to 2.12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Sun Aug 26 2018 - Devrim Gündüz <devrim@gunduz.org> 2.11-1
- Update to 2.11
- Install PostgreSQL 11+ bitcode files

* Tue Mar 27 2018 - Devrim Gündüz <devrim@gunduz.org> 2.10.2-1
- Initial RPM packaging for PostgreSQL RPM Repository.
