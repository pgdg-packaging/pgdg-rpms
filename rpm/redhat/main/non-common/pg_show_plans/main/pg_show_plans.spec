%global sname pg_show_plans

%{!?llvm:%global llvm 1}

Summary:	A PostgreSQL extension that shows query plans of all the currently running SQL statements.
Name:		%{sname}_%{pgmajorversion}
Version:	2.1.6
Release:	1PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/cybertec-postgresql/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/cybertec-postgresql/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
PostgreSQL extension that shows query plans of all the currently running SQL
statements. Query plans can be shown in several formats, like JSON or YAML.

This extension creates a hash table within shared memory. The hash table is
not resizable, thus, no new plans can be added once it has been filled up.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_show_plans
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
This package provides JIT support for pg_show_plans
%endif

%prep
%setup -q -n %{sname}-%{version}

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

* Mon Jul 21 2025 Devrim Gündüz <devrim@gunduz.org> - 2.1.8-1PGDG
- Update to 2.1.8 per described at:
  https://github.com/cybertec-postgresql/pg_show_plans/releases/tag/v2.1.8

* Tue Apr 29 2025 Devrim Gündüz <devrim@gunduz.org> - 2.1.3-1PGDG
- Update to 2.1.3 per described at:
  https://github.com/cybertec-postgresql/pg_show_plans/releases/tag/v2.1.3

* Sat Jan 11 2025 Devrim Gündüz <devrim@gunduz.org> - 2.1.2-2PGDG
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 2.1.2-1PGDG
- Update to 2.1.2
- Update LLVM dependencies
- Remove RHEL 7 support

* Mon May 13 2024 Devrim Gunduz <devrim@gunduz.org> - 2.1.0-1PGDG
- Initial RPM packaging for PostgreSQL RPM Repository
