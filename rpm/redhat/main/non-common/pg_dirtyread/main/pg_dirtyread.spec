%global sname pg_dirtyread

%{!?llvm:%global llvm 1}

Summary:	Read dead but unvacuumed rows from a PostgreSQL relation
Name:		%{sname}_%{pgmajorversion}
Version:	2.7
Release:	5PGDG%{?dist}
License:	BSD
Source0:	https://github.com/df7cb/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/df7cb/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
The pg_dirtyread extension provides the ability to read dead but unvacuumed
rows from a relation.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_dirtyread
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
This packages provides JIT support for pg_dirtyread
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif


%changelog
* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 2.7-5PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Tue Feb 25 2025 Devrim Gündüz <devrim@gunduz.org> - 2.7-4PGDG
- Remove redundant BR

* Thu Jan 9 2025 Devrim Gündüz <devrim@gunduz.org> - 2.7-3PGDG
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 2.7-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Tue Jun 25 2024 Devrim Gündüz <devrim@gunduz.org> - 2.7-1PGDG
- Initial RPM packaging for PostgreSQL YUM Repository
