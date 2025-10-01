%global sname	jsquery

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL json query language with GIN indexing support
Name:		%{sname}_%{pgmajorversion}
Version:	1.2
Release:	4PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/postgrespro/%{sname}/archive/ver_%{version}.tar.gz
URL:		https://github.com/postgrespro/%{sname}/

BuildRequires:	postgresql%{pgmajorversion} postgresql%{pgmajorversion}-devel
BuildRequires:	bison flex
Requires:	postgresql%{pgmajorversion}

%description
JsQuery – is a language to query jsonb data type.

It's primary goal is to provide an additional functionality to jsonb
(currently missing in PostgreSQL), such as a simple and effective way to
search in nested objects and arrays, more comparison operators with
indexes support. We hope, that jsquery will be eventually a part of
PostgreSQL.

Jsquery is released as jsquery data type (similar to tsquery) and @@
match operator for jsonb.

%package devel
Summary:	JsQuery development header files
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package includes the development headers for the jsquery extension.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for jsquery
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
This packages provides JIT support for jsquery

%endif

%prep
%setup -q -n %{sname}-ver_%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{pginstdir}/include/server
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%files devel
%defattr(-,root,root,-)
%{pginstdir}/include/server/jsquery*.h

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Mon Feb 24 2025 Devrim Gündüz <devrim@gunduz.org> - 1.2-4PGDG
- Add missing BRs

* Thu Jan 2 2025 Devrim Gündüz <devrim@gunduz.org> - 1.2-3PGDG
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.2-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Fri Oct 20 2023 Devrim Gunduz <devrim@gunduz.org> - 1.2-1PGDG
- Update to 1.2
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.1.1-3.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.1.1-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue May 5 2020 - Devrim Gündüz <devrim@gunduz.org> - 1.1.1-2
- Fix -devel package dependency, per report from Justin.

* Fri Sep 6 2019 - Devrim Gündüz <devrim@gunduz.org> - 1.1.1-1
- Update to 1.1.1

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-2
- Rebuild against PostgreSQL 11.0

* Thu Oct 5 2017 - Devrim Gündüz <devrim@gunduz.org> 1.1.0-1
- Update to 1.1.0

* Thu Oct 27 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-1
- Update to 1.0.0

* Fri Oct 21 2016 - Devrim Gündüz <devrim@gunduz.org> 0.0.4-1
- Initial RPM packaging for PostgreSQL RPM Repository
