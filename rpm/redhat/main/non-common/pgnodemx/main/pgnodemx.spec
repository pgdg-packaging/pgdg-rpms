%global sname pgnodemx

%{!?llvm:%global llvm 1}

Summary:	SQL functions that allow capture of node OS metrics from PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.7
Release:	1PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/CrunchyData/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/CrunchyData/%{sname}

BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-contrib

%description
pgnodemx includes SQL functions that allow capture of node OS metrics from
PostgreSQL.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgnodemx
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm => 19.0
%endif

%description llvmjit
This package provides JIT support for pgnodemx
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%defattr(644,root,root,755)
%license LICENSE.md
%doc %{pginstdir}/doc/extension/*%{sname}.md
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/pg_proctab*.sql
%{pginstdir}/share/extension/%{sname}*.control
%{pginstdir}/share/extension/pg_proctab*.control
%{pginstdir}/lib/%{sname}*.so

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}/*bc
    %{pginstdir}/lib/bitcode/%{sname}*bc
%endif

%changelog
* Thu Jul 10 2025 Devrim Gündüz <devrim@gunduz.org> 1.7-1PGDG
- Initial packaging for PostgreSQL RPM Repository
