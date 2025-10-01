%global sname postgresql_anonymizer

%{!?llvm:%global llvm 1}

Summary:	Anonymization & Data Masking for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.3.2
Release:	4PGDG%{?dist}
License:	PostgreSQL
Source0:	https://gitlab.com/dalibo/%{sname}/-/archive/%{version}/%{sname}-%{version}.tar.gz
URL:		https://gitlab.com/dalibo/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-contrib
Requires:	ddlx_%{pgmajorversion}

%if 0%{?suse_version} >= 1315
Requires:	python3-Faker
%else
Requires:	python3-faker
%endif
Obsoletes:	%{sname}%{pgmajorversion} < 0.7.1-2

%description
postgresql_anonymizer is an extension to mask or replace personally
identifiable information (PII) or commercially sensitive data from a
PostgreSQL database.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for postgresql_anonymizer
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
This package provides JIT support for postgresql_anonymizer
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension/
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%license LICENSE.md
%defattr(644,root,root,755)
%{pginstdir}/bin/pg_dump_anon.sh
%{pginstdir}/lib/anon.so
%{pginstdir}/share/extension/anon/*
%{pginstdir}/share/extension/anon.control
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%doc docs/*

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/anon*.bc
   %{pginstdir}/lib/bitcode/anon/*.bc
%endif

%changelog
* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.3.2-4PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Fri Feb 21 2025 Devrim Gündüz <devrim@gunduz.org> - 1.3.2-3PGDG
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.3.2-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Tue Apr 2 2024 Devrim Gündüz <devrim@gunduz.org> - 1.3.2-1PGDG
- Update to 1.3.2

* Mon Mar 4 2024 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-1PGDG
- Update to 1.3.1

* Tue Jan 23 2024 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1PGDG
- Update to 1.2.0

* Tue Oct 24 2023 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-5PGDG
- Install documentation along with the main package, per report
  from Seda Yavuz.

* Fri Sep 22 2023 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-4PGDG
- Fix LLVM dependency on SLES 15

* Mon Aug 21 2023 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-3PGDG
- Remove RHEL 6 bits
- Add PGDG branding
- Fix rpmlint warnings

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu Sep 29 2022 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1
- Update to 1.1.0

* Thu May 19 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1
- Update to 1.0.0

* Mon Apr 11 2022 Devrim Gündüz <devrim@gunduz.org> - 0.12.0-1
- Update to 0.12.0

* Thu Mar 31 2022 Devrim Gündüz <devrim@gunduz.org> - 0.11.0-1
- Update to 0.11.0

* Mon Mar 14 2022 Devrim Gündüz <devrim@gunduz.org> - 0.10.0-1
- Update to 0.10.0

* Thu Dec 23 2021 Devrim Gündüz <devrim@gunduz.org> - 0.9.0-3
- Fix SLES dependency name

* Thu Nov 4 2021 Devrim Gündüz <devrim@gunduz.org> - 0.9.0-2
- Add SLES support.

* Sun Jul 4 2021 Devrim Gündüz <devrim@gunduz.org> - 0.9.0-1
- Update to 0.9.0

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> - 0.8.1-2
- Remove pgxs patches, and export PATH instead.

* Tue Feb 9 2021 Devrim Gündüz <devrim@gunduz.org> - 0.8.1-1
- Update to 0.8.1

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 0.7.1-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Tue Sep 29 2020 Devrim Gündüz <devrim@gunduz.org> 0.7.1-1
- Update to 0.7.1

* Tue Mar 10 2020 Devrim Gündüz <devrim@gunduz.org> 0.6.0-1
- Update to 0.6.0

* Sat Nov 9 2019 Devrim Gündüz <devrim@gunduz.org> 0.5.0-1
- Update to 0.5.0

* Sun Nov 3 2019 Devrim Gündüz <devrim@gunduz.org> 0.4.1-2
- Require -contrib subpackage for tsm_system_rows extension. Per
  Damien: https://redmine.postgresql.org/issues/4861

* Thu Oct 17 2019 Devrim Gündüz <devrim@gunduz.org> 0.4.1-1
- Update to 0.4.1

* Sat Oct 12 2019 Devrim Gündüz <devrim@gunduz.org> 0.4.0-1
- Update to 0.4.0

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 0.3.1-1.1
- Rebuild for PostgreSQL 12

* Tue Sep 24 2019 Devrim Gündüz <devrim@gunduz.org> 0.3.1-1
- Update to 0.3.1

* Wed Aug 14 2019 Devrim Gündüz <devrim@gunduz.org> 0.3.0-1
- Update to 0.3.0
- Add ddlx dependency

* Tue Nov 6 2018 Devrim Gündüz <devrim@gunduz.org> 0.2.1-1
- Initial packaging for PostgreSQL RPM Repository
