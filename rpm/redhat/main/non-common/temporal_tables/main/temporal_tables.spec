%global sname temporal_tables

%{!?llvm:%global llvm 1}

Summary:	Temporal tables extension for PostgreQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.2.2
Release:	7PGDG%{dist}
Source0:	https://github.com/arkhipov/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/arkhipov/%{sname}
License:	BSD
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for temporal_tables
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
This package provides JIT support for temporal_tables
%endif

%description
A temporal table is a table that records the period of time when a row
is valid. There are two types of periods: the application period (also
known as valid-time or business-time) and the system period (also known
as transaction-time).

Currently, Temporal Tables Extension supports the system-period
temporal tables only.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%{__mv} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(-, root, root)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%if %llvm
%files llvmjit
	%{pginstdir}/lib/bitcode/%{sname}*.bc
	%{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 1.2.2-7PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.2.2-6PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Tue Jan 28 2025 Devrim Gündüz <devrim@gunduz.org> - 1.2.2-5PGDG
- Update LLVM dependencies and remove redundant BR

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.2.2-4PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Mon Feb 26 2024 Devrim Gündüz <devrim@gunduz.org> - 1.2.2-3PGDG
- Update LLVM dependencies

* Thu Jan 18 2024 Devrim Gündüz <devrim@gunduz.org> - 1.2.2-2PGDG
- Remove LLVM conditionals. Future updates will all have LLVM enabled
  anyway. This actually fixes RHEL 8 builds, where *for some reason* spectool
  cannot download sources when llvm macro is around just for this spec file.
  This does not fix PostgreSQL bug #18289 in full:
  https://www.postgresql.org/message-id/18289-cc1b88346b51af93%40postgresql.org
  but at least we provide user the RPM.

* Mon Sep 25 2023 Devrim Gündüz <devrim@gunduz.org> - 1.2.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository.

