%global __python %{_bindir}/python3
%global sname powa

# Powa archivist version
%global powamajorversion 5
%global powamidversion 0
%global powaminorversion 3

%global __ospython %{_bindir}/python3
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 10
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL Workload Analyzer Archivist
Name:		%{sname}-archivist_%{pgmajorversion}
Version:	%{powamajorversion}.%{powamidversion}.%{powaminorversion}
Release:	2PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/powa-team/powa-archivist/archive/REL_%{powamajorversion}_%{powamidversion}_%{powaminorversion}.tar.gz
URL:		https://powa.readthedocs.io/
BuildRequires:	postgresql%{pgmajorversion}-devel

%description
PoWA is PostgreSQL Workload Analyzer that gathers performance stats and
provides real-time charts and graphs to help monitor and tune your PostgreSQL
servers.

It is similar to Oracle AWR or SQL Server MDW.

This is the core extension of the PoWA project, a PostgreSQL Workload Analyzer
that gathers performance stats and provides real-time charts and graphs to help
monitor and tune your PostgreSQL servers.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for powa-archivist
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm => 19.0
%endif

%description llvmjit
This package provides JIT support for powa-archivist
%endif

%prep
%setup -q -n %{sname}-archivist-REL_%{powamajorversion}_%{powamidversion}_%{powaminorversion}

%build
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
# Move powa docs into their own subdirectory:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension/%{sname}
%{__install} INSTALL.md LICENSE.md PL_funcs.md README.md %{buildroot}%{pginstdir}/doc/extension/%{sname}

%files
%defattr(-,root,root,-)
%dir %{pginstdir}/doc/extension/%{sname}
%doc %{pginstdir}/doc/extension/%{sname}/INSTALL.md
%doc %{pginstdir}/doc/extension/%{sname}/PL_funcs.md
%doc %{pginstdir}/doc/extension/%{sname}/README.md
%license %{pginstdir}/doc/extension/%{sname}/LICENSE.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Thu Sep 205 2025 Devrim Gündüz <devrim@gunduz.org> - 5.0.3-2PGDG
- Rebuild

* Sat Jun 7 2025 Devrim Gündüz <devrim@gunduz.org> - 5.0.3-1PGDG
- Update 5.0.3 per changes described at:
  https://github.com/powa-team/powa-archivist/releases/tag/REL_5_0_3

* Sun Apr 13 2025 Devrim Gündüz <devrim@gunduz.org> - 5.0.2-1PGDG
- Update 5.0.2 per changes described at:
  https://github.com/powa-team/powa-archivist/releases/tag/REL_5_0_2

* Sun Jan 5 2025 Devrim Gündüz <devrim@gunduz.org> - 5.0.1-1PGDG
- Update 5.0.1 per changes described at:
  https://github.com/powa-team/powa-archivist/releases/tag/REL_5_0_1

* Mon Dec 9 2024 Devrim Gündüz <devrim@gunduz.org> - 5.0.0-1PGDG
- Update 5.0.0 per changes described at:
  https://github.com/powa-team/powa-archivist/releases/tag/REL_5_0_0

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 4.2.2-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Tue Nov 28 2023 Devrim Gunduz <devrim@gunduz.org> - 4.2.2-1PGDG
- Update to 4.2.2 per changes described at:
  https://github.com/powa-team/powa-archivist/releases/tag/REL_4_2_2

* Mon Oct 30 2023 Devrim Gunduz <devrim@gunduz.org> - 4.2.1-1PGDG
- Update to 4.2.1

* Thu Sep 21 2023 Devrim Gunduz <devrim@gunduz.org> - 4.2.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository

