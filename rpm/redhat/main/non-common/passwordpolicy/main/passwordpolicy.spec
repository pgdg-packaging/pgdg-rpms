%global sname	passwordpolicy
%{!?llvm:%global llvm 1}

Summary:	PostgreSQL Passwordcheck Policy
Name:		%{sname}_%{pgmajorversion}
Version:	2.0.6
Release:	2PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/fmbiete/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/fmbiete/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel postgresql%{pgmajorversion}
BuildRequires:	cracklib-devel
Requires:	postgresql%{pgmajorversion}-server
Requires:	cracklib

%description
The PostgreSQL Passwordcheck Policy is like the regular passwordcheck module,
except that you can dynamically define the complexity requirements.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for passwordpolicy
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
This package provides JIT support for passwordpolicy
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

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0.6-2PGDG
- Add Amazon Linux 2023 support.

* Wed Jul 8 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0.6-1PGDG
- Update to 2.0.6 per changes described at:
  https://github.com/fmbiete/passwordpolicy/releases/tag/v2.0.6

* Sat Mar 21 2026 Francisco Miguel Biete Banon <fbiete@gmail.com> - 2.0.5-1PGDG
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
