%global sname pg_similarity
%global packagemajorver 1
%global packageminver 0

%{!?llvm:%global llvm 1}

Summary:	Set of functions and operators for executing similarity queries for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	%{packagemajorver}.%{packageminver}
Release:	3PGDG%{?dist}
URL:		https://github.com/eulerto/%{sname}
Source0:	https://github.com/eulerto/%{sname}/archive/refs/tags/%{sname}_%{packagemajorver}_%{packageminver}.tar.gz
Patch0:		%{sname}-hamming.patch
License:	BSD
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
pg_similarity is an extension to support similarity queries on PostgreSQL.
The implementation is tightly integrated in the RDBMS in the sense that it
defines operators so instead of the traditional operators (= and <>) you can
use ~~~ and ! (any of these operators represents a similarity function).

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_similarity
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
This packages provides JIT support for pg_similarity
%endif

%prep
%setup -q -n %{sname}-%{sname}_%{packagemajorver}_%{packageminver}
%patch -P 0 -p1

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} DESTDIR=%{buildroot} install

# Install sample config file under the PostgreSQL extension directory:
%{__cp} pg_similarity.conf.sample %{buildroot}%{pginstdir}/share/extension/

# Install README file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 755 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%config %{pginstdir}/share/extension/%{sname}.conf.sample
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Mon Jan 13 2025 Devrim Gündüz <devrim@gunduz.org> - 1.0-3PGDG
- Add a patch (from Debian) to fix builds against PostgreSQL 16+.
- Install README and sample config file.
- Update LLVM dependencies and package description

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.0-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Fri Apr 12 2024 Devrim Gunduz <devrim@gunduz.org> - 1.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository

