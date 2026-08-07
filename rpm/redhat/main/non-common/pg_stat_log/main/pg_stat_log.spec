%global sname pg_stat_log

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL extension that uses the Custom Cumulative Stats API to track log messages
Name:		%{sname}_%{pgmajorversion}
Version:	0.1
Release:	2PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/fabriziomello/%{sname}
Source0:	https://github.com/fabriziomello/%{sname}/archive/refs/tags/%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
Cumulative statistics about PostgreSQL log messages, built on the Custom
Cumulative Stats API introduced in PostgreSQL 18.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_stat_log
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} == 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?suse_version} == 1600
BuildRequires:	llvm19-devel clang19-devel
Requires:	llvm19
%endif
%if 0%{?amzn}
BuildRequires:	llvm-devel >= 15.0 clang-devel >= 15.0
Requires:	llvm >= 15.0
%endif
%if ( 0%{?fedora} || 0%{?rhel} >= 8 ) && !0%{?amzn}
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm >= 19.0
%endif

%description llvmjit
This packages provides JIT support for pg_stat_log
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README
%{__install} -d %{buildroot}%{pginstdir}/doc/extension/
%{__install} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%license LICENSE
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
 %{pginstdir}/lib/bitcode/%{sname}*.bc
 %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 0.1-2PGDG
- Add Amazon Linux 2023 support.

* Sun Jun 7 2026 - Devrim Gündüz <devrim@gunduz.org> - 0.1-1PGDG
- Initial RPM packaging for PostgreSQL RPM Repository
