%global sname prioritize
%global pname pg_%{sname}

%{!?llvm:%global llvm 1}

Summary:	Get and set the nice priorities of PostgreSQL backends
Name:		%{pname}_%{pgmajorversion}
Version:	1.0.4
Release:	8PGDG%{?dist}
License:	PostgreSQL
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
URL:		https://github.com/schmiddy/%{pname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
This module implements an interface to getpriority() and setpriority()
for PostgreSQL backends, callable from SQL functions. Essentially,
this module allows users to `renice' their backends.

The priority values are used by getpriority() and setpriority(),
which you may be familiar with from the nice or renice programs.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_prioritize
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for pg_prioritize
%endif

%prep
%setup -q -n %{sname}-%{version}

%build

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__mv} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.*

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
   %{pginstdir}/lib/bitcode/%{sname}*.bc
%endif

%changelog
* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.0.4-8PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Fri Sep 5 2025 Devrim Gündüz <devrim@gunduz.org> - 1.0.4-7PGDG
- Update LLVM dependencies

* Fri Jan 10 2025 Devrim Gündüz <devrim@gunduz.org> - 1.0.4-7PGDG
- Update LLVM dependencies

* Fri Jan 10 2025 Devrim Gündüz <devrim@gunduz.org> - 1.0.4-6PGDG
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.0.4-5PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Fri Sep 8 2023 Devrim Gunduz <devrim@gunduz.org> - 1.0.4-4PGDG
- Add PGDG branding
- Cleanup rpmlint warnings

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.0.4-3.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0.4-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0.4-2
- Remove pgxs patches, and export PATH instead.

* Fri Sep 11 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.4-1
- Initial packaging for PostgreSQL RPM Repository
