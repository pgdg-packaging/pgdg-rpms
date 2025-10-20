%global sname	pg_dbms_errlog

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL extension which enables DML error logging
Name:		%{sname}_%{pgmajorversion}
Version:	2.2
Release:	1PGDG%{?dist}
License:	ISC
Source0:	https://github.com/HexaCluster/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/HexaCluster/%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel make
Requires:	postgresql%{pgmajorversion}-server pg_statement_rollback_%{pgmajorversion}

%description
The pg_dbms_errlog extension provides the infrastructure that enables you to
create an error logging table so that DML operations can continue after
encountering errors rather than abort and roll back.

It requires the use of the pg_statement_rollback extension or to fully manage
the SAVEPOINT in the DML script.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_dbms_errlog
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
This package provides JIT support for pg_dbms_errlog
%endif


%prep
%setup -q -n %{sname}-%{version}

%build

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} INSTALL_PREFIX=%{buildroot} DESTDIR=%{buildroot} install

# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}*.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Mon Oct 20 2025 Devrim Gündüz <devrim@gunduz.org> - 2.2-1PGDG
- Initial packaging for the PostgreSQL RPM Repository.
