%global sname pldebugger

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	1.9
Release:	1PGDG%{?dist}
Summary:	PL/pgSQL debugger server-side code
License:	Artistic 2.0
URL:		https://github.com/EnterpriseDB/%{sname}
Source0:	https://github.com/EnterpriseDB/%{sname}/archive/v%{version}.tar.gz
Source1:	%{sname}.LICENSE

BuildRequires:	postgresql%{pgmajorversion}-devel openssl-devel krb5-devel
Requires:	postgresql%{pgmajorversion}-server

%description
This module is a set of shared libraries which implement an API for
debugging PL/pgSQL functions on PostgreSQL. The pgAdmin project
(https://www.pgadmin.org/) provides a client user interface.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pldebugger
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
This package provides JIT support for pldebugger
%endif

%prep
%setup -q -n %{sname}-%{version}

%{__cp} -p %{SOURCE1} ./LICENSE

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__install} -m 644 README-%{sname}.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%{pginstdir}/lib/plugin_debugger.so
%{pginstdir}/share/extension/pldbgapi*.sql
%{pginstdir}/share/extension/pldbgapi*.control

%if %llvm
%files llvmjit
 %{pginstdir}/lib/bitcode/plugin_debugger*.bc
 %{pginstdir}/lib/bitcode/plugin_debugger/*.bc
%endif

%changelog
* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Tue Sep 23 2025 Devrim Gunduz <devrim@gunduz.org> - 1.9-1PGDG
- Update to 1.9 per changes described at:
  https://github.com/EnterpriseDB/pldebugger/releases/tag/v1.9

* Wed Feb 26 2025 Devrim Gunduz <devrim@gunduz.org> - 1.8-3PGDG
- Add missing BRs and remove redundant BR

* Wed Jan 22 2025 Devrim Gunduz <devrim@gunduz.org> - 1.8-2PGDG
- Update LLVM dependencies and package description.

* Mon Jul 29 2024 Devrim Gunduz <devrim@gunduz.org> - 1.8-1PGDG
- Update to 1.8 per changes described at:
  https://github.com/EnterpriseDB/pldebugger/releases/tag/v1.8
  https://github.com/EnterpriseDB/pldebugger/releases/tag/v1.7
  https://github.com/EnterpriseDB/pldebugger/releases/tag/v1.6
- Update LLVM dependencies
- Remove RHEL 7 support


* Mon Aug 21 2023 Devrim Gunduz <devrim@gunduz.org> - 1.5-3PGDG
- Remove RHEL 6 bits
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.5-2.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.5-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu Oct 6 2022 Devrim Gündüz <devrim@gunduz.org> - 1.5-1
- Update to 1.5

* Tue Oct 12 2021 Devrim Gündüz <devrim@gunduz.org> - 1.4-2
- Provide non-underscore version as well, in order not to break
  upgrades and existing scripts. Per Dave Page and others.

* Thu Sep 23 2021 Devrim Gündüz <devrim@gunduz.org> - 1.4-1
- Update to 1.4

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3-3
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Wed Oct 21 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3-1
- Update to 1.3
- Switch to the new URL

* Thu Sep 24 2020 Devrim Gündüz <devrim@gunduz.org> - 1.2-1
- Update to 1.2

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Thu Dec 6 2018 Devrim Gündüz <devrim@gunduz.org> - 1.1-1
- Update to 1.1

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0-1.1
- Rebuild against PostgreSQL 11.0

* Mon Jun 5 2017 2017 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Initial packaging for PostgreSQL YUM repository.

