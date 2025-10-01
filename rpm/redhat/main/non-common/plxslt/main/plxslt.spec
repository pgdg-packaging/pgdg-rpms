%global sname plxslt

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	0.20140221
Release:	1PGDG%{?dist}
Summary:	PL/XSLT Procedural Language Handler for PostgreSQL
License:	GPLv2
URL:		https://github.com/petere/%{sname}
Source0:	https://github.com/petere/%{sname}/archive/refs/tags/%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel libxslt-devel
Requires:	postgresql%{pgmajorversion}

%description
PL/XSLT is a procedural language handler for PostgreSQL that allows
you to write stored procedures in XSLT.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for plxslt
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
This package provides JIT support for plxslt
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} DESTDIR=%{buildroot} install
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__mv} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license COPYING
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Tue Apr 15 2025 Devrim Gündüz <devrim@gunduz.org> 0.20140221-1PGDG
- Initial packaging for the PostgreSQL RPM repository
