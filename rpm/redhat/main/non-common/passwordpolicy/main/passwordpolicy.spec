%global sname	passwordpolicy

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Summary:	PostgreSQL Passwordcheck Policy
Name:		%{sname}_%{pgmajorversion}
Version:	2.0.5
Release:	1PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/fmbiete/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/fmbiete/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel postgresql%{pgmajorversion}
BuildRequires: cracklib-devel
BuildRequires:	pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server
Requires: cracklib

%description
The PostgreSQL Passwordcheck Policy is like the regular passwordcheck module,
except that you can dynamically define the complexity requirements.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgdisablelogerror
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:  llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:  llvm13-devel clang13-devel
Requires:	llvm13
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm => 5.0
%endif

%description llvmjit
This packages provides JIT support for passwordpolicy
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
# Install README file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Sat Mar 21 2026 Francisco Miguel Biete Banon <fbiete@gmail.com> - 2.0.5
- New release

* Tue Dec 2 2025 Francisco Miguel Biete Banon <fbiete@gmail.com> - 2.0.4
- New release

* Sun Jun 29 2025 Francisco Miguel Biete Banon <fbiete@gmail.com> - 2.0.3
- New release

* Tue Feb 04 2025 Francisco Miguel Biete Banon <fbiete@gmail.com> - 2.0.2
- New release

* Sun Dec 15 2024 Francisco Miguel Biete Banon <fbiete@gmail.com> - 2.0.1
- New release

* Wed Jul 12 2023 Francisco Miguel Biete Banon <fbiete@gmail.com> - 1.1.0
- Initial RPM packaging
