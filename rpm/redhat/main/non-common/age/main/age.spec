%global sname	age

%{!?llvm:%global llvm 1}

Summary:	Graph database optimized for fast analysis and real-time data processing.
Name:		%{sname}_%{pgmajorversion}
Version:	1.7.0
Release:	rc0_2PGDG%{?dist}
License:	Apache 2.0
URL:		https://github.com/apache/%{sname}/
Source0:	https://github.com/apache/age/archive/refs/tags/PG%{pgmajorversion}/v%{version}-rc0.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
Apache AGE is an extension for PostgreSQL that enables users to leverage a
graph database on top of the existing relational databases. AGE is an acronym
for A Graph Extension and is inspired by Bitnine's AgensGraph, a multi-model
database fork of PostgreSQL. The basic principle of the project is to create
a single storage that handles both the relational and graph data model so that
the users can use the standard ANSI SQL along with openCypher, one of the most
popular graph query languages today. There is a strong need for cohesive,
easy-to-implement multi-model databases. As an extension of PostgreSQL, AGE
supports all the functionalities and features of PostgreSQL while also
offering a graph model to boot.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for age
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
This package provides JIT support for age
%endif

%prep
%setup -q -n %{sname}-PG%{pgmajorversion}-v%{version}-rc0/

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} INSTALL_PREFIX=%{buildroot} DESTDIR=%{buildroot} install

# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*
%endif

%changelog
* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 1.7.0-rc0-2PGDG
- Add Amazon Linux 2023 support.

* Fri Feb 13 2026 Devrim Gündüz <devrim@gunduz.org> - 1.7.0-rc0-1PGDG
- Update to 1.7.0-rc0 per changes described at:
  PostgreSQL 18: https://github.com/apache/age/releases/tag/PG18%2Fv1.7.0-rc0
  PostgreSQL 17: https://github.com/apache/age/releases/tag/PG17%2Fv1.7.0-rc0

* Thu Jan 15 2026 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-rc0-1PGDG
- Initial RPM packaging for the PostgreSQL RPM Repository.
