%global sname sslutils

%{!?llvm:%global llvm 1}

Summary:	SSL Utils for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.4
Release:	2PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/EnterpriseDB/%{sname}
Source0:	https://github.com/EnterpriseDB/%{sname}/archive/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel, net-snmp-devel
Requires:	postgresql%{pgmajorversion}-server

%description
SSLUtils is a Postgres extension that provides SSL certicate generation
functions to Postgres.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for sslutils
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
This package provides JIT support for sslutils
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

# Install README-sslutils.txt
%{__install} -d -m 755 %{buildroot}%{pginstdir}/share/doc/extension
%{__cp} README.%{sname} %{buildroot}%{pginstdir}/share/doc/extension/README-%{sname}.txt

%ifarch ppc64 ppc64le
strip %{buildroot}%{pginstdir}/lib/*.so
%endif

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(644,root,root) %{pginstdir}/share/doc/extension/README-%{sname}.txt
%{pginstdir}/lib/sslutils.so
%{pginstdir}/share/extension/sslutils*.sql
%{pginstdir}/share/extension/uninstall_sslutils.sql
%{pginstdir}/share/extension/sslutils.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Wed Jan 29 2025 Devrim Gündüz <devrim@gunduz.org> - 1.4-2PGDG
- Update package description and LLVM dependencies.
- Remove redundant BR

* Mon Aug 12 2024 Devrim Gündüz <devrim@gunduz.org> - 1.4-1PGDG
- Update to 1.4

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.3-7PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.3-6PGDG
- Add PGDG branding
- Add SLES 15 support
- Update LLVM dependencies

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.3-5.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.3-5
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue Sep 21 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3-4
- Disable debug packages on ppc64le

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3-3
- Remove pgxs patches, and export PATH instead.

* Thu Apr 30 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3-2
- Switch to the new open source repo
- Switch to pgdg-srpm-macros

* Fri Sep 27 2019 Devrim Gündüz <devrim@gunduz.org> - 1.3-1
- Update to 1.3

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.2-1.1
- Rebuild against PostgreSQL 11.0

* Fri Feb 23 2018 - Devrim Gündüz <devrim@gunduz.org> 1.2-1
- Update to 1.2

* Thu Feb 22 2018 - Devrim Gündüz <devrim@gunduz.org> 1.1-1
- Initial packaging for PostgreSQL RPM repository
