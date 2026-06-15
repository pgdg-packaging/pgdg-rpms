%global sname	biscuit

%{!?llvm:%global llvm 1}

Summary:	 High-Performance Pattern Matching Index for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	2.2.3
Release:	1PGDG%{?dist}
License:	MIT
URL:		https://github.com/crystallinecore//%{sname}/
Source0:	https://github.com/crystallinecore/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
Biscuit is a specialized PostgreSQL index access method (IAM) designed for
blazing-fast pattern matching on LIKE and ILIKE queries, with native support
for multi-column searches. It eliminates the recheck overhead of trigram
indexes while delivering significant performance improvements on wildcard-heavy
queries. It stands for Bitmap Indexed Searching with Comprehensive Union and
Intersection Techniques.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for biscuit
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
This package provides JIT support for biscuit
%endif

%prep
%setup -q -n Biscuit-%{version}

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
    %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Mon Jun 15 2026 Devrim Gündüz <devrim@gunduz.org> - 2.2.3-1PGDG
- Update to 2.2.3 per changes described at:
  https://github.com/CrystallineCore/Biscuit/releases/tag/v2.2.3

* Wed Jan 7 2026 Devrim Gündüz <devrim@gunduz.org> - 2.2.2-1PGDG
- Initial RPM packaging for the PostgreSQL RPM Repository.
