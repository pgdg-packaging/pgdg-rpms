%global sname extra_window_functions

%{!?llvm:%global llvm 1}

Summary:	Extra Window Functions for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.0
Release:	7PGDG%{dist}
License:	PostgreSQL
URL:		https://github.com/xocolatl/%{sname}
Source0:	https://github.com/xocolatl/%{sname}/archive/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server

%description
This extension provides additional window functions to PostgreSQL. Some of
them provide SQL Standard functionality but without the SQL Standard grammar,
others extend on the SQL Standard, and still others are novel and hopefully
useful to someone.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for extra_window_functions
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
This package provides JIT support for extra_window_functions
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %make_install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__mv} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.%{sname}

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/*%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
 %{pginstdir}/lib/bitcode/%{sname}*.bc
 %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.0-7PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Fri Feb 21 2025 Devrim Gunduz <devrim@gunduz.org> - 1.0-6PGDG
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gunduz <devrim@gunduz.org> - 1.0-5PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Thu Feb 22 2024 Devrim Gunduz <devrim@gunduz.org> - 1.0-4PGDG
- Add PGDG branding
- Fix rpmling warnings

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.0-3.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Sep 22 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0-2
- Remove pgxs patches, and export PATH instead.
- Add RHEL 8 / ppc64le support.

* Sat Jun 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
