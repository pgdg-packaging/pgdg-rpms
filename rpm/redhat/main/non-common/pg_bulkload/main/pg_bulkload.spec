%global sname pg_bulkload

%global pgbulkloadmajver 3
%global pgbulkloadmidver 1
%global pgbulkloadminver 22
%global	pgbulkloadpackagever %{pgbulkloadmajver}_%{pgbulkloadmidver}_%{pgbulkloadminver}

%{!?llvm:%global llvm 1}

Summary:	High speed data loading utility for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	%{pgbulkloadmajver}.%{pgbulkloadmidver}.%{pgbulkloadminver}
Release:	5PGDG%{?dist}
URL:		https://github.com/ossc-db/%{sname}
Source0:	https://github.com/ossc-db/%{sname}/archive/VERSION%{pgbulkloadpackagever}.tar.gz
License:	BSD
BuildRequires:	postgresql%{pgmajorversion}-devel openssl-devel pam-devel
BuildRequires:	libsepol-devel readline-devel krb5-devel zlib-devel

# lz4 dependency
%if 0%{?suse_version} >= 1500
BuildRequires:	liblz4-devel
Requires:	liblz4-1
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	lz4-devel
Requires:	lz4-libs
%endif

# zstd dependency
%if 0%{?suse_version} >= 1500
BuildRequires:	libzstd-devel >= 1.4.0
Requires:	libzstd1 >= 1.4.0
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	libzstd-devel >= 1.4.0
Requires:	libzstd >= 1.4.0
%endif
Requires:	postgresql%{pgmajorversion}-server %{sname}_%{pgmajorversion}-client

%description
pg_bulkload is a high speed data loading tool for PostgreSQL.

pg_bulkload is designed to load huge amount of data to a database. You can
load data to table bypassing PostgreSQL shared buffers.

pg_bulkload also has some ETL features; input data validation and data
transformation.

%package client
Summary:	High speed data loading utility for PostgreSQL
Requires:	postgresql%{pgmajorversion}-libs

%description client
pg_bulkload client subpackage provides client-only tools.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_bulkload
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
This package provides JIT support for pg_bulkload
%endif

%prep
%setup -q -n %{sname}-VERSION%{pgbulkloadpackagever}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} DESTDIR=%{buildroot} install

# Strip .so files to produce -debug* packages properly on SLES.
%{__strip} %{buildroot}%{pginstdir}/lib/*.so

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/lib/pg_timestamp.so
%{pginstdir}/share/contrib/pg_timestamp.sql
%{pginstdir}/share/contrib/uninstall_pg_timestamp.sql
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%files client
%defattr(-,root,root)
%{pginstdir}/bin/%{sname}
%{pginstdir}/bin/postgresql

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
   %{pginstdir}/lib/bitcode/%{sname}/pgut/*.bc
   %{pginstdir}/lib/bitcode/pg_timestamp*.bc
   %{pginstdir}/lib/bitcode/pg_timestamp/*.bc
%endif

%changelog
* Sat Nov 8 2025 Devrim Gündüz <devrim@gunduz.org> - 3.1.22-4PGDG
- Fix SLES support

* Tue Oct 7 2025 Devrim Gündüz <devrim@gunduz.org> - 3.1.22-3PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 3.1.22-3PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Tue Feb 25 2025 Devrim Gunduz <devrim@gunduz.org> - 3.1.21-2PGDG
- Add missing BRs

* Mon Jan 27 2025 Devrim Gunduz <devrim@gunduz.org> - 3.1.21-1PGDG
- Update to 3.1.22 per changes described at:
  https://github.com/ossc-db/pg_bulkload/releases/tag/VERSION3_1_22

* Thu Jan 9 2025  Devrim Gündüz <devrim@gunduz.org> - 3.1.21-4PGDG
- Update LLVM dependencies and package description

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 3.1.21-3PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Fri Feb 23 2024 Devrim Gunduz <devrim@gunduz.org> - 3.1.21-2PGDG
- Strip .so files to produce -debug* packages properly on SLES.

* Thu Jan 18 2024 Devrim Gunduz <devrim@gunduz.org> - 3.1.21-1PGDG
- Update to 3.1.21
- Update LLVM dependencies
- Fix rpmlint warnings
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 3.1.20-1.1
- Rebuild against LLVM 15 on SLES 15

* Mon Jan 16 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.20-1
- Update to 3.1.20

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 3.1.19-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Apr 27 2022 Devrim Gündüz <devrim@gunduz.org> - 3.1.19-2
- Split llvmjit into its own subpackage.

* Tue Oct 19 2021 Devrim Gündüz <devrim@gunduz.org> - 3.1.19-1
- Update to 3.1.19

* Thu Jun 24 2021 Devrim Gündüz <devrim@gunduz.org> - 3.1.18-2
- Unbreak pg_bulkload installation.

* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> - 3.1.18-1
- Update to 3.1.18

* Thu Apr 15 2021 Devrim Gündüz <devrim@gunduz.org> - 3.1.17-1
- Update to 3.1.17
- Export PATH, and remove pgxs patches.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 3.1.16-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Mon Jan 27 2020 Devrim Gündüz <devrim@gunduz.org> - 3.1.16-1
- Update to 3.1.16

* Tue Jan 22 2019 Devrim Gündüz <devrim@gunduz.org> - 3.1.15-1
- Update to 3.1.15

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 3.1.14-2.1
- Rebuild against PostgreSQL 11.0

* Sun Mar 4 2018 Devrim Gündüz <devrim@gunduz.org> 3.1.14-2
- Split client tools into a separate subpackage, per #3165

* Mon Nov 13 2017 Devrim Gündüz <devrim@gunduz.org> 3.1.14-1
- Update to 3.1.14

* Thu May 18 2017 Devrim Gündüz <devrim@gunduz.org> 3.1.13-1
- Update to 3.1.13

* Thu Sep 29 2016 Devrim Gündüz <devrim@gunduz.org> 3.1.10-1
- Update to 3.1.10

* Thu Feb 11 2016 Devrim Gündüz <devrim@gunduz.org> 3.1.9-1
- Update to 3.1.9

* Sun Jan 24 2016 Devrim Gündüz <devrim@gunduz.org> 3.1.8-1
- Update to 3.1.8
- Update URL

* Thu May 29 2014 Devrim Gündüz <devrim@gunduz.org> 3.1.6-1
- Update to 3.1.6
- Simplify install section

* Fri Jan 22 2010 Devrim Gündüz <devrim@gunduz.org> 3.0a2-1
- Update to 3.0a2

* Fri Apr 18 2008 Devrim Gündüz <devrim@gunduz.org> 2.3.0-1
- Initial packaging for PGDG Repository
