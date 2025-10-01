%global sname tds_fdw

%{!?llvm:%global llvm 1}

Summary:	TDS Foreign Data Wrapper for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	2.0.5
Release:	2PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/tds-fdw/%{sname}/archive/v%{version}.zip
URL:		https://github.com/tds-fdw/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel freetds-devel
Requires:	postgresql%{pgmajorversion}-server freetds

Obsoletes:	%{sname}%{pgmajorversion} < 2.0.2-2

%description
This is a PostgreSQL foreign data wrapper that can connect to databases that
use the Tabular Data Stream (TDS) protocol, such as Sybase databases and
Microsoft SQL server.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for tds_fdw
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
This package provides JIT support for tds_fdw
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install

# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__install} -m 644 ForeignSchemaImporting.md %{buildroot}%{pginstdir}/doc/extension/ForeignSchemaImporting-%{sname}.md
%{__install} -m 644 ForeignServerCreation.md %{buildroot}%{pginstdir}/doc/extension/ForeignServerCreation-%{sname}.md
%{__install} -m 644 ForeignTableCreation.md %{buildroot}%{pginstdir}/doc/extension/ForeignTableCreation-%{sname}.md
%{__install} -m 644 UserMappingCreation.md %{buildroot}%{pginstdir}/doc/extension/UserMappingCreation-%{sname}.md
%{__install} -m 644 Variables.md %{buildroot}%{pginstdir}/doc/extension/Variables-%{sname}.md
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%{__rm} -f %{buildroot}/%{pginstdir}/doc/extension/README.%{sname}.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/*%{sname}.md
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/lib/%{sname}.so

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 2.0.5-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Thu Sep 18 2025 John Harvey <john.harvey@crunchydata.com> - 2.0.5-1PGDG
- Update to 2.0.5 per changes described at:
  https://github.com/tds-fdw/tds_fdw/releases

* Tue Jan 28 2025 Devrim Gündüz <devrim@gunduz.org> - 2.0.4-2PGDG
- Update LLVM dependencies and remove redundant BR

* Tue Sep 17 2024 Devrim Gündüz <devrim@gunduz.org> - 2.0.4-1PGDG
- Update to 2.0.4 per changes described at:
  https://github.com/tds-fdw/tds_fdw/releases

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 2.0.3-5PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Thu Sep 14 2023 Devrim Gündüz <devrim@gunduz.org> - 2.0.3-4PGDG
- Update LLVM dependency for SLES 15.
- Add PGDG branding
- Cleanup rpmlint warnings

* Wed Jan 11 2023 John Harvey <john.harvey@crunchydata.com> - 2.0.3-3
- Update license type

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.0.3-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Sat Oct 22 2022 Devrim Gündüz <devrim@gunduz.org> - 2.0.3-1
- Update to 2.0.3
- Split llvm stuff into its own subpackage.

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> - 2.0.2-3
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.2-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Sun Sep 27 2020 - Devrim Gündüz <devrim@gunduz.org> 2.0.2-1
- Update to 2.0.2

* Wed Dec 4 2019 - Devrim Gündüz <devrim@gunduz.org> 2.0.1-1
- Update to 2.0.1

* Sat Jan 19 2019 - Devrim Gündüz <devrim@gunduz.org> 2.0.0-alpha.3
- Update to 2.0.0-alpha.3 for testing repo only.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-alpha.2_1.1
- Rebuild against PostgreSQL 11.0

* Tue Jul 31 2018 - Devrim Gündüz <devrim@gunduz.org> 2.0.0-alpha.2
- Update to 2.0.0-alpha.2 for testing repo only.

* Fri Oct 28 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.8-1
- Update to 1.0.8
- Change links to point to github.

* Thu Jan 7 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.7-1
- Update to 1.0.7
- Apply 9.5 doc layout.

* Mon Jan 4 2016 - Devrim Gündüz <devrim@gunduz.org> 1.0.6-1
- Update to 1.0.6

* Fri Sep 25 2015  - Devrim Gündüz <devrim@gunduz.org> 1.0.5-1
- Initial packaging for PostgreSQL RPM Repository
