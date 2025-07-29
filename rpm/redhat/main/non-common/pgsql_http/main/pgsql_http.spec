%global pname pgsql_http
%global sname pgsql-http

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL HTTP client
Name:		%{pname}_%{pgmajorversion}
Version:	1.7.0
Release:	1PGDG%{?dist}
URL:		https://github.com/pramsey/%{sname}
Source0:	https://github.com/pramsey/%{sname}/archive/refs/tags/v%{version}.tar.gz
License:	MIT
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	libcurl-devel
Requires:	postgresql%{pgmajorversion}-server

%description
pgsql_http allows users to be able to write a trigger that calls a
web service either to get back a result, or to poke that service into
refreshing itself against the new state of the database.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgsql_http
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
This packages provides JIT support for pgsql_http
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} DESTDIR=%{buildroot} install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{pginstdir}/lib/http.so
%{pginstdir}/share/extension/http*.sql
%{pginstdir}/share/extension/http*.control

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/http.index*.bc
    %{pginstdir}/lib/bitcode/http/*.bc
%endif

%changelog
* Mon Jul 28 2025 Devrim Gündüz <devrim@gunduz.org> - 1.7.0-1PGDG
- Update to 1.7.0 per changes described at:
  https://github.com/pramsey/pgsql-http/releases/tag/v1.7.0

* Wed Feb 26 2025 Devrim Gündüz <devrim@gunduz.org> - 1.6.3-2PGDG
- Simplify libcurl dependency. The package name is the same on all
  supported distros.

* Fri Jan 24 2025 Devrim Gündüz <devrim@gunduz.org> - 1.6.3-1PGDG
- Update to 1.6.3 per changes described at:
  https://github.com/pramsey/pgsql-http/releases/tag/v1.6.3

* Tue Jan 14 2025 Devrim Gündüz <devrim@gunduz.org> - 1.6.2-1PGDG
- Update to 1.6.2 per changes described at:
  https://github.com/pramsey/pgsql-http/releases/tag/v1.6.2

* Mon Jan 13 2025 Devrim Gündüz <devrim@gunduz.org> - 1.6.1-2PGDG
- Update LLVM dependencies

* Thu Oct 10 2024 Devrim Gündüz <devrim@gunduz.org> - 1.6.1-1PGDG
- Update to 1.6.1 per changes described at:
  https://github.com/pramsey/pgsql-http/releases/tag/v1.6.1

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Fri Apr 5 2024 Devrim Gunduz <devrim@gunduz.org> - 1.6.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository

