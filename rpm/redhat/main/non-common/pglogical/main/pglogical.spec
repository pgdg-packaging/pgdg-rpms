%global sname pglogical

%global pglogicalmajver 2
%global pglogicalmidver 4
%global pglogicalminver 6

%{!?llvm:%global llvm 1}

Summary:	Logical Replication extension for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	%{pglogicalmajver}.%{pglogicalmidver}.%{pglogicalminver}
Release:	4PGDG%{dist}
License:	PostgreSQL
URL:		https://github.com/2ndQuadrant/%{sname}
Source0:	https://github.com/2ndQuadrant/%{sname}/archive/REL%{pglogicalmajver}_%{pglogicalmidver}_%{pglogicalminver}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel
# lz4 dependency
%if 0%{?suse_version} >= 1500
BuildRequires:	liblz4-devel
Requires:	liblz4-1
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	lz4-devel
Requires:	lz4-libs
# zstd dependency
%if 0%{?suse_version} >= 1500
BuildRequires:	libzstd-devel >= 1.4.0
Requires:	libzstd1 >= 1.4.0
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	libzstd-devel >= 1.4.0
Requires:	libzstd >= 1.4.0
%endif
%endif
%if 0%{?suse_version} >= 1500
Requires:	libopenssl3
BuildRequires:	libopenssl-3-devel
%endif
%if 0%{?fedora} >= 41 || 0%{?rhel} >= 8
Requires:	openssl-libs >= 1.1.1k
BuildRequires:	openssl-devel
%endif
BuildRequires:	libxml2-devel libxslt-devel pam-devel
BuildRequires:	krb5-devel zlib-devel

Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}_%{pgmajorversion} < 2.3.3-2

%description
pglogical is a logical replication system implemented entirely as a PostgreSQL
extension. Fully integrated, it requires no triggers or external programs.
This alternative to physical replication is a highly efficient method of
replicating data using a publish/subscribe model for selective replication.

This extension provides logical streaming replication for
PostgreSQL, using a publish/subscribe model.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pglogical
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
This package provides JIT support for pglogical
%endif

%prep
%setup -q -n %{sname}-REL%{pglogicalmajver}_%{pglogicalmidver}_%{pglogicalminver}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
PATH=%{pginstdir}/bin:$PATH %make_install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%defattr(-,root,root,-)
%license COPYRIGHT
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/bin/%{sname}_create_subscriber
%{pginstdir}/lib/%{sname}_output.so
%{pginstdir}/share/extension/%{sname}_origin--1.0.0.sql
%{pginstdir}/share/extension/%{sname}_origin.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}_output/*.bc
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/compat%{pgmajorversion}/*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc*
%endif

%changelog
* Wed Nov 5 2025 Devrim Gündüz <devrim@gunduz.org> - 2.4.6-4PGDG
- Rebuild against OpenSSL 3 on SLES 15

* Tue Oct 7 2025 Devrim Gündüz <devrim@gunduz.org> - 2.4.6-3PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 2.4.6-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Wed Aug 27 2025 Devrim Gündüz <devrim@gunduz.org> - 2.4.6-1PGDG
- Update to 2.4.6 per changes described at:
  https://github.com/2ndQuadrant/pglogical/releases/tag/REL2_4_6

* Tue Feb 25 2025 Devrim Gündüz <devrim@gunduz.org> - 2.4.5-3PGDG
- Add missing BRs

* Thu Jan 9 2025 Devrim Gündüz <devrim@gunduz.org> - 2.4.5-2PGDG
- Update LLVM dependencies

* Mon Sep 23 2024 Devrim Gündüz <devrim@gunduz.org> - 2.4.5-1PGDG
- Update to 2.4.5 per changes described at:
  https://github.com/2ndQuadrant/pglogical/releases/tag/REL2_4_5

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 2.4.4-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Wed Oct 4 2023 - Devrim Gündüz <devrim@gunduz.org> - 2.4.4-1PGDG
- Update to 2.4.4

* Mon Aug 21 2023 Devrim Gunduz <devrim@gunduz.org> - 2.4.3-2PGDG
- Remove RHEL 6 bits
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 2.4.3-1.1
- Rebuild against LLVM 15 on SLES 15

* Tue May 30 2023 - Devrim Gündüz <devrim@gunduz.org> - 2.4.3-1
- Update to 2.4.3

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.4.2-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Fri Oct 21 2022 - John Harvey <john.harvey@crunchydata.com> - 2.4.2-1
- Update to 2.4.2

* Thu Aug 25 2022 Devrim Gündüz <devrim@gunduz.org> - 2.4.1-2
- Update SLES 15 dependencies for SP4.

* Wed Mar 30 2022 Devrim Gündüz <devrim@gunduz.org> - 2.4.1-1
- Update to 2.4.1

* Thu Nov 4 2021 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-2
- Rebuild against LLVM 11 on SLES 15.
- Make sure that LLVM dependency versions are the same as
  PostgreSQL.

* Tue Aug 17 2021 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-1
- Update to 2.4.0
* Tue Aug 17 2021 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-1
- Update to 2.4.0
- Split llvmjit bits into a separate package

* Mon Jun 7 2021 Devrim Gündüz <devrim@gunduz.org> 2.3.4-1
- Update to 2.3.4

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 2.3.3-1
- Update to 2.3.3
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Sun May 3 2020 Devrim Gündüz <devrim@gunduz.org> 2.3.1-1
- Initial RPM packaging for PostgreSQL RPM Repository,
