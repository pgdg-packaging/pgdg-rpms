%global sname	pg_incremental

%{!?llvm:%global llvm 1}

Summary:	Incremental Data Processing in PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.0.0
Release:	1PGDG%{?dist}
License:	PostgreSQL
Group:		Applications/Databases
URL:		https://github.com/CrunchyData/%{sname}
Source0:	https://github.com/CrunchyData/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server pg_cron_%{pgmajorversion}

%description
pg_incremental is a simple extension that helps you do fast, reliable,
incremental batch processing in PostgreSQL.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_incremental
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
This packages provides JIT support for pg_incremental
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
%{__make} PG_CONFIG=%{pginstdir}/bin/pg_config USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} PG_CONFIG=%{pginstdir}/bin/pg_config USE_PGXS=1 %{?_smp_mflags} DESTDIR=%{buildroot} install
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__mv} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%defattr(-,root,root,-)
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}*.control

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Thu Jan 9 2025 - Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1PGDG
- Initial RPM packaging for the PostgreSQL RPM repository.
