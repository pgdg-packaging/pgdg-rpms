%global sname pgl_ddl_deploy

%{!?llvm:%global llvm 1}

Summary:	Transparent Logical DDL Replication (pgl_ddl_deploy)
Name:		%{sname}_%{pgmajorversion}
Version:	2.2.1
Release:	3PGDG%{?dist}
License:	MIT
Source0:	https://github.com/enova/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/enova/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
Transparent DDL replication for both pglogical and native logical
replication.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgl_ddl_deploy
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
This packages provides JIT support for pgl_ddl_deploy
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%defattr(644,root,root,755)
%{pginstdir}/share/extension/%{sname}*sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/lib/ddl_deparse.so
%{pginstdir}/lib/%{sname}.so

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
    %{pginstdir}/lib/bitcode/ddl_deparse*.bc
    %{pginstdir}/lib/bitcode/ddl_deparse/*.bc
%endif

%changelog
* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Thu Jan 9 2025 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-3PGDG
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-2PGDG
- Update LLVM dependencies

* Thu Jul 18 2024 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-1PGDG
- Update to 2.2.1
- Remove RHEL 7 support
- Update LLVM dependencies

* Tue Oct 24 2023 Devrim Gündüz <devrim@gunduz.org> - 2.2.0-1PGDG
- Initial RPM packaging for the PostgreSQL RPM Repository
