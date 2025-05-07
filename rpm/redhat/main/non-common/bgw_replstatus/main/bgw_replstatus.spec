%global sname bgw_replstatus

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.8
Release:	1PGDG%{?dist}
Summary:	PostgreSQL background worker to report wether a node is a replication master or standby
License:	PostgreSQL
URL:		https://github.com/mhagander/%{sname}
Source0:	https://github.com/mhagander/%{sname}/archive/%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.12
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 1.0.3-2

%description
bgw_replstatus is a tiny background worker to cheaply report the
replication status of a node. It's intended to be polled by a load
balancer such as haproxy.

When installed, a background worker will be started that listens on a
defined TCP port (configured bgw_replstatus.port). Any connection to
this port will get a TCP response back (no request necessary, response
will be sent immediately on connect) saying either MASTER or STANDBY
depending on the current state of the node. The connection is then
automatically closed.

Using a background worker like this will make polling a lot more light
weight than making a full PostgreSQL connection, logging in, and
checking the status.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for bgw_replstatus
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 17.0 clang-devel >= 17.0
Requires:	llvm => 17.0
%endif

%description llvmjit
This package provides JIT support for bgw_replstatus
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Wed May 7 2025 Devrim Gündüz <devrim@gunduz.org> - 1.0.8-1PGDG
- Update to 1.0.8 per changes described at:
  https://github.com/mhagander/bgw_replstatus/releases/tag/1.0.8
  https://github.com/mhagander/bgw_replstatus/releases/tag/1.0.7

* Fri Feb 21 2025 Devrim Gunduz <devrim@gunduz.org> - 1.0.6-5PGDG
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gunduz <devrim@gunduz.org> - 1.0.6-4PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Wed Feb 21 2024 Devrim Gunduz <devrim@gunduz.org> - 1.0.6-3PGDG
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.0.6-2.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0.6-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu Jul 28 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0.6-1
- Update to 1.0.6
- Split llvmjit package
- Remove superfluous %%clean section.

* Fri Jan 8 2021 Devrim Gündüz <devrim@gunduz.org> 1.0.3-3
- Use pgdg_set_llvm_variables macro for LLVM related files.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 1.0.3-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0.3-1
- Update to 1.0.3

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0.1-3
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0.1-2
- Rebuild against PostgreSQL 11.0

* Thu May 18 2017 Devrim Gündüz <devrim@gunduz.org> - 1.0.1-1
- Update to 1.0.1

* Fri Mar 31 2017 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1
- Initial packaging for PostgreSQL YUM repository.

