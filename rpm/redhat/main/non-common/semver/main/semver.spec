%global sname semver

%{!?llvm:%global llvm 1}

Summary:	A semantic version data type for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	0.40.0
Release:	1PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/theory/pg-%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/theory/pg-%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 0.31.0-2

%description
This library contains a single PostgreSQL extension, a data type called "semver".
It's an implementation of the version number format specified by the Semantic
Versioning 2.0.0 Specification.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for semver
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
This package provides JIT support for semver
%endif

%prep
%setup -q -n pg-%{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/%{sname}/%{sname}.mmd
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/%{sname}/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/src/%{sname}*.bc
   %{pginstdir}/lib/bitcode/src/%{sname}/src/*.bc
%endif

%changelog
* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Wed Jan 29 2025 Devrim Gunduz <devrim@gunduz.org> - 0.40.0-1PGDG
- Update to 0.40.0 per changes described at:
  https://github.com/theory/pg-semver/releases/tag/v0.40.0
- Remove RHEL 7 and SLES 15 support

* Wed Aug 2 2023 Devrim Gunduz <devrim@gunduz.org> - 0.32.1-1PGDG
- Update to 0.32.1
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 0.32.0-2.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 0.32.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon Oct 24 2022 Devrim Gündüz <devrim@gunduz.org> - 0.32.0-1
- Update to 0.32.0

* Wed Sep 29 2021 Devrim Gündüz <devrim@gunduz.org> - 0.31.2-1
- Update to 0.31.2

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> - 0.31.1-2
- Remove pgxs patches, and export PATH instead.

* Tue Apr 27 2021 Devrim Gündüz <devrim@gunduz.org> - 0.31.1-1
- Update to 0.31.1

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 0.31.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Mon Oct 19 2020 Devrim Gündüz <devrim@gunduz.org> - 0.31.0-1
- Update to 0.31.0

* Mon Jun 1 2020 Devrim Gündüz <devrim@gunduz.org> - 0.30.0-1
- Update to 0.30.0

* Sat Apr 4 2020 Devrim Gündüz <devrim@gunduz.org> - 0.22.0-1
- Update to 0.22.0

* Wed Mar 25 2020 Devrim Gündüz <devrim@gunduz.org> - 0.21.0-1
- Initial packaging for PostgreSQL RPM Repository
