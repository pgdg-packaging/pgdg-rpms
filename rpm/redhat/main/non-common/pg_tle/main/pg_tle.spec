%global sname	pg_tle

%{!?llvm:%global llvm 1}

Summary:	Trusted Language Extensions for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.2.0
Release:	3PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/aws/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/aws/%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-libs

%description
Trusted Language Extensions (TLE) for PostgreSQL (pg_tle) is an open
source project that lets developers extend and deploy new PostgreSQL
functionality with lower administrative and technical overhead.
Developers can use Trusted Language Extensions for PostgreSQL to create
and install extensions on restricted filesystems and work with
PostgreSQL internals through a SQL API.
gives capability to users to launch

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_Tle
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
This package provides JIT support for pg_Tle
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(-,root,root,-)
%license LICENSE
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Fri Jan 17 2025 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-3PGDG
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Thu Apr 4 2024 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1PGDG
- Initial packaging for the PostgreSQL RPM Repository
