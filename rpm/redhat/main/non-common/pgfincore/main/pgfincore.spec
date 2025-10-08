%global sname pgfincore

%{!?llvm:%global llvm 1}

Summary:	PgFincore is a set of functions to manage blocks in memory
Name:		%{sname}_%{pgmajorversion}
Version:	1.3.1
Release:	6PGDG%{?dist}
License:	BSD
Source0:	https://github.com/klando/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/klando/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 1.2.2-2

%description
PgFincore is a set of functions to manage blocks in memory.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgfincore
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
This package provides JIT support for pgfincore
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p %{buildroot}%{pginstdir}/share/extension
%{__mkdir} -p %{buildroot}%{pginstdir}/share/%{sname}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 755 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/%{sname}/README.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%doc AUTHORS ChangeLog
%license COPYRIGHT
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/%{sname}/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Tue Oct 7 2025 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-6PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.3.1-5PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Thu Jan 9 2025 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-4PGDG
- Update LLVM dependencies
- Fix location of the README file.

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-3PGDG
- Update LLVM dependencies

* Wed Jul 17 2024 Devrim Gündüz <devrim@gunduz.org> 1.3.1-2PGDG
- Update LLVM dependencies

* Thu Sep 21 2023 Devrim Gündüz <devrim@gunduz.org> 1.3.1-1PGDG
- Update to 1.3.1
- Add PGDG branding
- Cleanup rpmlint warnings

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.2.4-2.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.2.4-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu Sep 29 2022 Devrim Gündüz <devrim@gunduz.org> 1.2.4-1
- Update to 1.2.4
- Remove RHEL 6 support
- Update LLVM code.

* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> 1.2.2-3
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 1.2.2-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Tue Sep 15 2020 Devrim Gündüz <devrim@gunduz.org> - 1.2.2-1
- Update to 1.2.2
- Remove patch1, now in upstream

* Fri Oct 4 2019 Devrim Gündüz <devrim@gunduz.org> - 1.2.1-1
- Update to 1.2.1
- Add a patch (from git master) to fix build issues.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.1.2-2.1
- Rebuild against PostgreSQL 11.0

* Tue Mar 10 2015 - Devrim Gündüz <devrim@gunduz.org> 1.1.2-2
- Fixes for Fedora 23 and PostgreSQL 9.5 doc layout.

* Tue Mar 10 2015 - Devrim Gündüz <devrim@gunduz.org> 1.1.2-1
- Update to 1.1.2
- Update project URL -- pgfoundry is dead.
- Update Source0 URL

* Mon Dec 19 2011 - Devrim Gündüz <devrim@gunduz.org> 1.1.1-1
- Update to 1.1.1, per changes described in
  http://pgfoundry.org/forum/forum.php?forum_id=1859

* Fri Aug 12 2011 - Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Update to 1.0, (#68), per changes described in
  http://pgfoundry.org/frs/shownotes.php?release_id=1872

* Wed Nov 10 2010 - Devrim Gündüz <devrim@gunduz.org> 0.4.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
