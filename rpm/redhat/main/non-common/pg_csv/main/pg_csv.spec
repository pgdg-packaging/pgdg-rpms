%global sname	pg_csv

%{!?llvm:%global llvm 1}

Summary:	Flexible CSV processing as a solution for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.0.1
Release:	1PGDG%{?dist}
License:	MIT
URL:		https://github.com/PostgREST/%{sname}/
Source0:	https://github.com/PostgREST/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
pg_csv offers flexible CSV processing as a solution.
 - Includes a CSV aggregate that composes with SQL expressions.
 - Native C extension, x2 times faster than SQL queries that try to output CSV
   (see our CI results).
 - No dependencies except Postgres.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_csv
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
This packages provides JIT support for pg_csv
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} INSTALL_PREFIX=%{buildroot} DESTDIR=%{buildroot} install

%files
%defattr(-,root,root,-)
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
    %{pginstdir}/lib/bitcode/%{sname}*.bc
%endif

%changelog
* Thu Sep 11 2025 Devrim Gündüz <devrim@gunduz.org> - 1.0.1-1PGDG
- Initial RPM packaging for the PostgreSQL RPM Repository per:
  https://github.com/pgdg-packaging/pgdg-rpms/issues/78
