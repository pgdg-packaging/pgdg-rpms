%global sname	pgspider_ext

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL extension to construct High-Performance SQL Cluster Engine for distributed big data
Name:		%{sname}_%{pgmajorversion}
Version:	1.3.0
Release:	3PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/pgspider/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/pgspider/%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
PGSpider Extension(pgspider_ext) is an extension to construct High-Performance
SQL Cluster Engine for distributed big data. pgspider_ext enables PostgreSQL
to access a number of data sources using Foreign Data Wrapper(FDW) and
retrieves the distributed data source vertically.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgspider_ext
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
This package provides JIT support for pgspider_ext
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
%license License
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/%{sname}*.bc
%endif

%changelog
* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-3PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.3.0-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Mon Mar 3 2025 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-1PGDG
- Initial packaging for the PostgreSQL RPM Repository
