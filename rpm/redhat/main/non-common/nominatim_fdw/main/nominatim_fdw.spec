%global sname nominatim_fdw

%{!?llvm:%global llvm 1}

Summary:	Nominatim Foreign Data Wrapper for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.3
Release:	1PGDG%{?dist}
License:	MIT
URL:		https://github.com/jimjonesbr/%{sname}
Source0:	https://github.com/jimjonesbr/%{sname}/archive/%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel libcurl-devel libxml2-devel
Requires:	postgresql%{pgmajorversion}-server

%description
The nominatim_fdw is a PostgreSQL Foreign Data Wrapper to access data from
Nominatim servers using simple function calls.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for nominatim_fdw
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
This package provides JIT support for nominatim_fdw
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH USE_PGXS=1 %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension/
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Mon Apr 13 2026 Devrim Gunduz <devrim@gunduz.org> - 1.3-1PGDG
- Update to 1.3 per changes described at:
  https://github.com/jimjonesbr/nominatim_fdw/releases/tag/1.3

* Mon Apr 6 2026 Devrim Gunduz <devrim@gunduz.org> - 1.2-1PGDG
- Update to 1.2 per changes described at:
  https://github.com/jimjonesbr/nominatim_fdw/releases/tag/1.2

* Mon Jan 26 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1.0-1PGDG
- Initial packaging for the PostgreSQL RPM Repository.
