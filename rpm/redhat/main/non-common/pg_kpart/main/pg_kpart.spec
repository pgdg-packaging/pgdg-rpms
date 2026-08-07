%global sname pg_kpart

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	1.0
Release:	2PGDG%{?dist}
Summary:	PostgreSQL username/password checks
License:	PostgreSQL
URL:		https://github.com/HexaCluster/%{sname}
Source0:	https://github.com/HexaCluster/%{sname}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
A PostgreSQL extension that rejects queries which would scan every partition
of a partitioned table without a usable predicate on the partition key. It
prevents accidental full-hierarchy scans caused by missing WHERE/JOIN
conditions on the partition key.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_kpart
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
This package provides JIT support for pg_kpart
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension//%{sname}.control
%{pginstdir}/share/extension/%{sname}*sql
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 1.0-2PGDG
- Add Amazon Linux 2023 support.

* Tue Jun 16 2026 Devrim Gunduz <devrim@gunduz.org> - 1.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository.

