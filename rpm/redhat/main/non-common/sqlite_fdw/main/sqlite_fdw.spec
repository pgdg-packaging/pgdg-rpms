%global sname	sqlite_fdw

%{!?llvm:%global llvm 1}

Summary:	SQLite Foreign Data Wrapper for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	2.5.0
Release:	2PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/pgspider/%{sname}
Source0:	https://github.com/pgspider/%{sname}/archive/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	postgresql%{pgmajorversion}-server sqlite-devel
Requires:	postgresql%{pgmajorversion}-server
%if 0%{?suse_version} >= 1500
# Unfortunately SLES 15 ships the libraries with -devel subpackage:
Requires:	sqlite3-devel >= 3.7
%else
# All other sane distributions have a separate -libs subpackage:
Requires:	sqlite-libs >= 3.7
%endif

%description
This PostgreSQL extension is a Foreign Data Wrapper for SQLite.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for sqlite_fdw
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
This package provides JIT support for sqlite_fdw
%endif

%prep
%setup -q -n %{sname}-%{version}

%build

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(-,root,root,-)
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.sql
%{pginstdir}/share/extension/*.control
%{pginstdir}/doc/extension/README-%{sname}.md

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Wed Jan 29 2025 Devrim Gündüz <devrim@gunduz.org> - 2.5.0-2PGDG
- Update LLVM dependencies
- Remove redundant BR

* Wed Dec 11 2024 Devrim Gündüz <devrim@gunduz.org> - 2.5.0-1PGDG
- Update to 2.5.0 per changes described at:
  https://github.com/pgspider/sqlite_fdw/releases/tag/v2.5.0
- Remove the patch added in 2.4.0-4, now in upstream.

* Mon Sep 23 2024 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-4PGDG
- Add a patch to fix builds on PostgreSQL 17.

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-3PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Mon Feb 26 2024 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-2PGDG
- Add SLES 15 support

* Wed Sep 27 2023 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-1PGDG
- Update to 2.4.0
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 2.3.0-1.1
- Rebuild against LLVM 15 on SLES 15

* Fri Jan 20 2023 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-1
- Update to 2.3.0

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.2.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue Sep 27 2022 Devrim Gündüz <devrim@gunduz.org> - 2.2.0-1
- Update to 2.2.0

* Wed Dec 22 2021 Devrim Gündüz <devrim@gunduz.org> - 2.1.1-1
- Update to 2.1.1

* Fri Sep 24 2021 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-1
- Update to 2.1.0

* Wed May 26 2021 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-1
- Update to 2.0.0

* Thu Jan 21 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-1
- Update to 1.3.1

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Oct 1 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-1
- Update to 1.3.0

* Fri Aug 28 2020 Devrim Gündüz <devrim@gunduz.org> - 1.2.1-1
- Update to 1.2.1

* Tue Oct 1 2019 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1
- Update to 1.2.0

* Wed Oct 31 2018 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1
- Update to 1.1.0

* Tue Oct 23 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1
- Initial packaging for PostgreSQL RPM repositories
