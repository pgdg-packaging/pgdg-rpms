%global sname address_standardizer

%{!?llvm:%global llvm 1}

Summary:	Postgres extension to parse a US street address string into its component parts.
Name:		%{sname}_%{pgmajorversion}
Version:	3.7.0
Release:	2PGDG%{?dist}
License:	MIT
Source0:	https://github.com/postgis/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/postgis/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server postgis3_%{pgmajorversion} >= 3.7

%description
This is a fork of the PAGC standardizer (http://www.pagcgeo.org) and single line
address parser. The code is built into a single PostgreSQL extension library.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for address_standardizer
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
This package provides JIT support for address_standardizer
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
%license COPYING
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%defattr(644,root,root,755)
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}_data_us.control
%{pginstdir}/lib/%{sname}.so

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 3.7.0-2PGDG
- Add Amazon Linux 2023 support.

* Mon Jul 13 2026 Devrim Gunduz <devrim@gunduz.org> - 3.7.0-1PGDG
- Initial RPM packaging for the PostgreSQL RPM Repository
