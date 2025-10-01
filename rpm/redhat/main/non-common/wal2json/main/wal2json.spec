%global sname wal2json
%global wal2json_rel 2_6

%{!?llvm:%global llvm 1}

Summary:	JSON output plugin for changeset extraction
Name:		%{sname}_%{pgmajorversion}
Version:	2.6
Release:	3PGDG%{?dist}
License:	BSD
Source0:	https://github.com/eulerto/%{sname}/archive/%{sname}_%{wal2json_rel}.tar.gz
URL:		https://github.com/eulerto/wal2json
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 2.3-3

%description
wal2json is an output plugin for logical decoding. It means that the
plugin have access to tuples produced by INSERT and UPDATE. Also,
UPDATE/DELETE old row versions can be accessed depending on the
configured replica identity. Changes can be consumed using the streaming
protocol (logical replication slots) or by a special SQL API.

The wal2json output plugin produces a JSON object per transaction. All
of the new/old tuples are available in the JSON object. Also, there are
options to include properties such as transaction timestamp,
schema-qualified, data types, and transaction ids.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for wal2json
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
This package provides JIT support for wal2json
%endif

%prep
%setup -q -n %{sname}-%{sname}_%{wal2json_rel}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %make_install DESTDIR=%{buildroot}
%{__install} -d %{buildroot}/%{pginstdir}/doc/extension/
%{__mv} README.md  %{buildroot}/%{pginstdir}/doc/extension/README-%{sname}.md

%postun -p /sbin/ldconfig
%post -p /sbin/ldconfig

%files
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so

%if %llvm
%files llvmjit
  %{pginstdir}/lib/bitcode/%{sname}*.bc
  %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Fri Feb 21 2025 Devrim Gündüz <devrim@gunduz.org> - 2.6-3PGDG
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 2.6-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Fri May 3 2024 - John Harvey <john.harvey@crunchydata.com> - 2.6-1PGDG
- Update to 2.6

* Mon Feb 26 2024 Devrim Gunduz <devrim@gunduz.org> - 2.5-4PGDG
- Add PGDG branding
- Update LLVM dependencies

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 2.5-3.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.5-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Fri Oct 14 2022 - John Harvey <john.harvey@crunchydata.com> 2.5-2
- Remove duplicated macros

* Tue Oct 11 2022 Devrim Gündüz <devrim@gunduz.org> 2.5-1
- Update to 2.5
- Split LLVM stuff into their own subpackage.

* Fri Sep 10 2021 Devrim Gündüz <devrim@gunduz.org> 2.4-1
- Update to 2.4

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> - 2.3-4
- Remove PGXS patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.3-3
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Tue Aug 11 2020 - John Harvey <john.harvey@crunchydata.com> 2.3-2
- Fix source pathing

* Tue Aug 11 2020 Devrim Gündüz <devrim@gunduz.org> 2.3-1
- Update to 2.3

* Mon Apr 27 2020 - John Harvey <john.harvey@crunchydata.com> 2.2-2
- Fix source pathing

* Fri Mar 27 2020 Devrim Gündüz <devrim@gunduz.org> 2.2-1
- Update to 2.2

* Mon Jan 6 2020 - John Harvey <john.harvey@crunchydata.com> 2.0-2
- fix source pathing

* Sun Jan 5 2020 Devrim Gündüz <devrim@gunduz.org> 2.0-1
- Update to 2.0

* Thu Jan 2 2020 - John Harvey <john.harvey@crunchydata.com> 1.0-4
- Update license type

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Wed Feb 13 2019 Devrim Gündüz <devrim@gunduz.org> 1.0-3
- Rebuild against PostgreSQL 11.2

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> 1.0.2.1
- Rebuild against PostgreSQL 11.0

* Sat Aug 11 2018 - Devrim Gündüz <devrim@gunduz.org> 1.0-2
- Ignore .bc files on PPC arch.

* Mon Jun 18 2018 - Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Initial RPM packaging for yum.postgresql.org
