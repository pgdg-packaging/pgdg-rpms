%global sname icu_ext

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	1.10.0
Release:	1PGDG%{?dist}
Summary:	PostgreSQL extension to expose functionality from ICU to PostgreSQL applications
License:	PostgreSQL
URL:		https://github.com/dverite/%{sname}
Source0:	https://github.com/dverite/%{sname}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel libxml2-devel
Requires:	postgresql%{pgmajorversion} libicu

%description
icu_ext is a PostgreSQL extension to expose functionality from ICU to
PostgreSQL applications.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for icu_ext
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
This package provides JIT support for icu_ext
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} DESTDIR=%{buildroot} install

%files
%defattr(644,root,root,755)
%doc README.md
%license LICENSE.md
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

* Thu Jun 26 2025 Devrim Gündüz <devrim@gunduz.org> 1.10.0-1PGDG
- Update to 1.10.0 per changes described at:
  https://github.com/dverite/icu_ext/releases/tag/v1.10.0

* Mon Apr 14 2025 Devrim Gündüz <devrim@gunduz.org> 1.9.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository
