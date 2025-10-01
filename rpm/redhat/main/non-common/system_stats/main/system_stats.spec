%global sname system_stats

%{!?llvm:%global llvm 1}

Summary:	A Postgres extension for exposing system metrics such as CPU, memory and disk information
Name:		%{sname}_%{pgmajorversion}
Version:	3.2
Release:	2PGDG%{dist}
License:	PostgreSQL
URL:		https://github.com/EnterpriseDB/%{sname}
Source0:	https://github.com/EnterpriseDB/%{sname}/archive/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
system_stats is a Postgres extension that provides functions to access system
level statistics that can be used for monitoring. It supports Linux, macOS and
Windows.

Note that not all values are relevant on all operating systems. In such cases
NULL is returned for affected values.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for system_stats
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
This package provides JIT support for system_stats
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %make_install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/include/server/extension/%{sname}/%{sname}.h

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/*%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*/*.bc
%endif

%changelog
* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Wed Jan 29 2025 Devrim Gunduz <devrim@gunduz.org> - 3.2-2PGDG
- Update LLVM dependencies
- Remove redundant BR

* Wed Aug 28 2024 Devrim Gunduz <devrim@gunduz.org> - 3.2-1PGDG
- Update to 3.2 per changes described at:
  https://github.com/EnterpriseDB/system_stats/releases/tag/v3.2
  https://github.com/EnterpriseDB/system_stats/releases/tag/v3.1

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 3.0-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Tue Jul 9 2024 Devrim Gunduz <devrim@gunduz.org> - 3.0-1PGDG
- Update to 3.0 per changes described at:
  https://github.com/EnterpriseDB/system_stats/releases/tag/v3.0

* Mon Feb 26 2024 Devrim Gunduz <devrim@gunduz.org> - 2.1-1PGDG
- Update to 2.1
- Update LLVM dependencies

* Fri Sep 22 2023 Devrim Gunduz <devrim@gunduz.org> - 2.0-1PGDG
- Update to 2.0
- Add PGDG branding
- Cleanup rpmlint warning

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.0-3.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> 1.0-2
- Remove pgxs patches, and export PATH instead.

* Thu Jun 25 2020 Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
