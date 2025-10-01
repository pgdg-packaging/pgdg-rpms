%global sname	pg_hint_plan

%if %{pgmajorversion} == 18
%global pghintplanversion 1.8.0
%global git_tag	1_8_0
%endif
%if %{pgmajorversion} == 17
%global pghintplanversion 1.7.1
%global git_tag	1_7_1
%endif
%if %{pgmajorversion} == 16
%global pghintplanversion 1.6.2
%global git_tag	1_6_2
%endif
%if %{pgmajorversion} == 15
%global pghintplanversion 1.5.3
%global git_tag	1_5_3
%endif
%if %{pgmajorversion} == 14
%global pghintplanversion 1.4.4
%global git_tag	1_4_4
%endif
%if %{pgmajorversion} == 13
%global pghintplanversion 1.3.11
%global git_tag	1_3_11
%endif

%{!?llvm:%global llvm 1}

Summary:	Tweak PostgreSQL execution plans using so-called "hints" in SQL comments
Name:		%{sname}_%{pgmajorversion}
Version:	%{pghintplanversion}
Release:	1PGDG%{?dist}
License:	MIT
Source0:	https://github.com/ossc-db/pg_hint_plan/archive/refs/tags/REL%{pgmajorversion}_%{git_tag}.tar.gz
URL:		https://github.com/ossc-db/%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel flex
Requires:	postgresql%{pgmajorversion}-server

%description
pg_hint_plan makes it possible to tweak PostgreSQL execution plans using
so-called "hints" in SQL comments, like /*+ SeqScan(a) */.

PostgreSQL uses a cost-based optimizer, which utilizes data statistics,
not static rules. The planner (optimizer) esitimates costs of each possible
execution plans for a SQL statement then the execution plan with the lowest
cost finally be executed. The planner does its best to select the best best
execution plan, but is not always perfect, since it doesn't count some
properties of the data, for example, correlation between columns.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_hint_plan
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
This package provides JIT support for pg_hint_plan
%endif

%prep
%setup -q -n %{sname}-REL%{pgmajorversion}_%{git_tag}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
%if %{pgmajorversion} >= 14
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md
%endif

%files
%defattr(-,root,root,-)
%if %{pgmajorversion} >= 14
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%endif
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Mon Aug 18 2025 Devrim Gündüz <devrim@gunduz.org> - %{pghintplanversion}-1PGDG
- Update to 1.8.0 for PostgreSQL 18 per changes described at.:
  https://github.com/ossc-db/pg_hint_plan/releases/tag/REL18_1_8_0
- Update to 1.7.1 for PostgreSQL 17 per changes described at:
  https://github.com/ossc-db/pg_hint_plan/releases/tag/REL17_1_7_1
- Update to 1.6.2 for PostgreSQL 16 per changes described at:
  https://github.com/ossc-db/pg_hint_plan/releases/tag/REL16_1_6_2
- Update to 1.5.3 for PostgreSQL 15 per changes described at:
  https://github.com/ossc-db/pg_hint_plan/releases/tag/REL15_1_5_3
- Update to 1.4.4 for PostgreSQL 14 per changes described at:
  https://github.com/ossc-db/pg_hint_plan/releases/tag/REL14_1_4_4
- Update to 1.3.11 for PostgreSQL 13 per changes described at:
  https://github.com/ossc-db/pg_hint_plan/releases/tag/REL13_1_3_11

* Tue Feb 25 2025 Devrim Gündüz <devrim@gunduz.org> - %{pghintplanversion}-3PGDG
- Add missing BR

* Fri Feb 21 2025 Devrim Gündüz <devrim@gunduz.org> - %{pghintplanversion}-2PGDG
- Update LLVM dependencies
- Remove redundant BR and Requires

* Thu Aug 29 2024 Devrim Gündüz <devrim@gunduz.org> - %{pghintplanversion}-1PGDG
- Update to 1.7.0 for PostgreSQL 17 per changes described at:
  https://github.com/ossc-db/pg_hint_plan/releases/tag/REL17_1_7_0
- Update to 1.6.1 for PostgreSQL 16 per changes described at:
  https://github.com/ossc-db/pg_hint_plan/releases/tag/REL16_1_6_1
- Update to 1.5.2 for PostgreSQL 15 per changes described at:
  https://github.com/ossc-db/pg_hint_plan/releases/tag/REL15_1_5_2
- Update to 1.4.3 for PostgreSQL 14 per changes described at:
  https://github.com/ossc-db/pg_hint_plan/releases/tag/REL14_1_4_3
- Update to 1.3.10 for PostgreSQL 13 per changes described at:
  https://github.com/ossc-db/pg_hint_plan/releases/tag/REL13_1_3_10
- Update to 1.3.10 for PostgreSQL 12 per changes described at:
  https://github.com/ossc-db/pg_hint_plan/releases/tag/REL12_1_3_10

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - %{pghintplanversion}-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Tue Sep 12 2023 Devrim Gunduz <devrim@gunduz.org> - %{pghintplanversion}-1PGDG
- Initial packaging for the PostgreSQL RPM Repository
