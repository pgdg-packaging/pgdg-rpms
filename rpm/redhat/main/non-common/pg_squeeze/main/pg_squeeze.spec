%global sname pg_squeeze

%global squeezemajver 1
%global squeezemidver 9
%global squeezeminver 1

%{!?llvm:%global llvm 1}

Summary:	A PostgreSQL extension for automatic bloat cleanup
Name:		%{sname}_%{pgmajorversion}
Version:	%{squeezemajver}.%{squeezemidver}.%{squeezeminver}
Release:	1PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/cybertec-postgresql/%{sname}/archive/REL%{squeezemajver}_%{squeezemidver}_%{squeezeminver}.tar.gz
URL:		https://github.com/cybertec-postgresql/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
pg_squeeze is an extension that removes unused space from a table and
optionally sorts tuples according to particular index (as if CLUSTER
command was executed concurrently with regular reads / writes).

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_squeeze
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
This packages provides JIT support for pg_squeeze
%endif

%prep
%setup -q -n %{sname}-REL%{squeezemajver}_%{squeezemidver}_%{squeezeminver}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension/
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/%{sname}.md

%files
%license LICENSE
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%defattr(644,root,root,755)
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/lib/%{sname}.so


%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Mon Sep 15 2025 Devrim Gündüz <devrim@gunduz.org> - 1.9.1-1PGDG
- Update to 1.9.1 per changes described at:
  https://github.com/cybertec-postgresql/pg_squeeze/releases/tag/REL1_9_1

* Mon Aug 4 2025 Devrim Gündüz <devrim@gunduz.org> - 1.9.0-1PGDG
- Update to 1.9.0 per changes described at:
  https://github.com/cybertec-postgresql/pg_squeeze/releases/tag/REL1_9_0

* Sun Jan 26 2025 Devrim Gündüz <devrim@gunduz.org> - 1.8.0-1PGDG
- Update to 1.8.0 per changes described at:
  https://github.com/cybertec-postgresql/pg_squeeze/releases/tag/REL1_8_0

* Mon Jan 13 2025 Devrim Gündüz <devrim@gunduz.org> - 1.7.0-2PGDG
- Update LLVM dependencies

* Tue Sep 24 2024 Devrim Gündüz <devrim@gunduz.org> - 1.7.0-1PGDG
- Update to 1.7.0

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.6.2-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Fri Feb 23 2024 Devrim Gunduz <devrim@gunduz.org> - 1.6.2-1PGDG
- Update to 1.6.2

* Mon Sep 11 2023 Devrim Gunduz <devrim@gunduz.org> - 1.6.1-1PGDG
- Update to 1.6.1
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.5.0-2.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.5.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu Oct 6 2022 Devrim Gündüz <devrim@gunduz.org> - 1.5.0-1
- Update to 1.5.0
- Split llvmjit into its own subpackage.

* Fri Feb 18 2022 John Harvey <john.harvey@crunchydata.com> - 1.4.1-2
- Update license to match source code

* Fri Sep 24 2021 Devrim Gündüz <devrim@gunduz.org> - 1.4.1-1
- Update to 1.4.1

* Mon Sep 13 2021 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-1
- Update to 1.4.0

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-1
- Update to 1.3.1
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Sat Sep 26 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-1
- Update to 1.3.0

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1.1
- Rebuild for PostgreSQL 12

* Mon Aug 26 2019 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1
- Update to 1.2.0

* Mon Nov 5 2018 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
