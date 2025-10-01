%global sname pgsodium

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL extension for high level cryptographic algorithms
Name:		%{sname}_%{pgmajorversion}
Version:	3.1.9
Release:	5PGDG%{dist}
License:	BSD
URL:		https://github.com/michelp/%{sname}/
Source0:	https://github.com/michelp/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel libsodium-devel
Requires:	postgresql%{pgmajorversion}-server

%if 0%{?fedora} || 0%{?rhel}
Requires:	libsodium
%endif
%if 0%{?suse_version} >= 1315
Requires:	libsodium23
%endif

%description
pgsodium is an encryption library extension for PostgreSQL using the
libsodium library for high level cryptographic algorithms.

pgsodium can be used a straight interface to libsodium, but it can also use
a powerful feature called Server Key Management where pgsodium loads an
external secret key into memory that is never accessible to SQL. This
inaccessible root key can then be used to derive sub-keys and keypairs by
key id. This id (type bigint) can then be stored instead of the derived key.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgsodium
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
This package provides JIT support for pgsodium
%endif

%prep
%setup -q -n %{sname}-%{version}

%build

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 3.1.9-5PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Fri Feb 21 2025 Devrim Gündüz <devrim@gunduz.org> - 3.1.9-4PGDG
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 3.1.9-3PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Fri Feb 23 2024 Devrim Gündüz <devrim@gunduz.org> - 3.1.9-2PGDG
- Fix rpmlint warnings

* Mon Nov 13 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.9-1PGDG
- Update to 3.1.9

* Wed Jul 19 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.8-1PGDG
- Update to 3.1.8
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 3.1.7-1.1
- Rebuild against LLVM 15 on SLES 15

* Mon May 29 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.7-1
- Update to 3.1.7

* Tue Apr 4 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.6-1
- Update to 3.1.6

* Wed Jan 4 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.5-1
- Update to 3.1.5

* Wed Dec 14 2022 Devrim Gündüz <devrim@gunduz.org> - 3.1.4-1
- Update to 3.1.4

* Tue Dec 13 2022 Devrim Gündüz <devrim@gunduz.org> - 3.1.1-1
- Update to 3.1.1

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 3.1.0-1
- Update to 3.1.0

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 3.0.6-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Sun Nov 13 2022 Devrim Gündüz <devrim@gunduz.org> 3.0.6-2
- Fix SLES dependency, per report from Tiago ANASTACIO.
  Fixes https://redmine.postgresql.org/issues/7739

* Sat Oct 22 2022 Devrim Gündüz <devrim@gunduz.org> 3.0.6-1
- Update to 3.0.6

* Tue Oct 18 2022 Devrim Gündüz <devrim@gunduz.org> 3.0.5-1
- Update to 3.0.5

* Thu Aug 25 2022 Devrim Gündüz <devrim@gunduz.org> 3.0.4-2
- Update SLES 15 dependencies for SP4.

* Mon Aug 22 2022 Devrim Gündüz <devrim@gunduz.org> 3.0.4-1
- Update to 3.0.4

* Tue Aug 9 2022 Devrim Gündüz <devrim@gunduz.org> 3.0.2-1
- Update to 3.0.2

* Mon Aug 8 2022 Devrim Gündüz <devrim@gunduz.org> 3.0.0-1
- Update to 3.0.0

* Tue Feb 15 2022 Devrim Gündüz <devrim@gunduz.org> 2.0.2-1
- Initial RPM packaging for the PostgreSQL RPM Repository.
