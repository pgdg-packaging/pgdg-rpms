%global sname	pgauditlogtofile

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL Audit Log To File Extension
Name:		%{sname}_%{pgmajorversion}
Version:	1.6.4
Release:	2PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/fmbiete/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/fmbiete/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel postgresql%{pgmajorversion}
Requires:	postgresql%{pgmajorversion}-server pgaudit_%{pgmajorversion}

%description
pgAudit Log to File is an addon to pgAudit than will redirect audit log lines
to an independent file, instead of using PostgreSQL server logger.

This will allow us to have an audit file that we can easily rotate without
polluting server logs with those messages.

Audit logs in heavily used systems can grow very fast. This extension allows
to automatically rotate the files based in a number of minutes.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgauditlogtofile
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
This packages provides JIT support for pgauditlogtofile
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Sat Jan 4 2025 Devrim Gunduz <devrim@gunduz.org> - 1.6.4-2PGDG
- Update package description and LLVM dependencies.

* Mon Dec 16 2024 Devrim Gunduz <devrim@gunduz.org> - 1.6.4-1PGDG
- Update to 1.6.4 per changes described at:
  https://github.com/fmbiete/pgauditlogtofile/releases/tag/v1.6.4

* Mon Oct 28 2024 Devrim Gunduz <devrim@gunduz.org> - 1.6.3-1PGDG
- Update to 1.6.3 per changes described at:
  https://github.com/fmbiete/pgauditlogtofile/releases/tag/v1.6.3

* Tue Sep 3 2024 Devrim Gunduz <devrim@gunduz.org> - 1.6.2-1PGDG
- Update to 1.6.2 per changes described at:
  https://github.com/fmbiete/pgauditlogtofile/releases/tag/v1.6.2
  https://github.com/fmbiete/pgauditlogtofile/releases/tag/v1.6.1

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-2PGDG
- Update LLVM dependencies

* Wed Jun 26 2024 Devrim Gunduz <devrim@gunduz.org> - 1.6.0-1PGDG
- Update to 1.6.0 per changes described at:
  https://github.com/fmbiete/pgauditlogtofile/releases/tag/v1.6.0

* Mon Jul 31 2023 Devrim Gunduz <devrim@gunduz.org> - 1.5.12-1PGDG
- Update to 1.5.12
- Add PGDG branding
- Update licence
- Fix rpmlint warnings

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.5.10-1.1
- Rebuild against LLVM 15 on SLES 15

* Tue Dec 13 2022 Devrim Gündüz <devrim@gunduz.org> - 1.5.10-1
- Update to 1.5.10

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.5.6-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon Oct 3 2022 Devrim Gündüz <devrim@gunduz.org> 1.5.6-2
- This package needs to require pgaudit17.

* Thu Sep 29 2022 Devrim Gündüz <devrim@gunduz.org> 1.5.6-1
- Update to 1.5.6

* Fri Sep 16 2022 Devrim Gündüz <devrim@gunduz.org> 1.5.5-1
- Update to 1.5.5

* Wed May 11 2022 Devrim Gündüz <devrim@gunduz.org> 1.5.1-1
- Update to 1.5.1

* Mon Oct 11 2021 Devrim Gündüz <devrim@gunduz.org> 1.4-1
- Update to 1.4

* Mon Sep 20 2021 Devrim Gündüz <devrim@gunduz.org> 1.3-1
- Update to 1.3

* Sat Jun 5 2021 Devrim Gündüz <devrim@gunduz.org> 1.2-1
- Update to 1.2
- Remove pgxs patches, and export PATH instead.

* Tue Nov 17 2020 Devrim Gündüz <devrim@gunduz.org> 1.1-1
- Update to 1.1

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 1.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Sat Jun 06 2020 Francisco Miguel Biete Banon <fbiete@gmail.com> - 1.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
