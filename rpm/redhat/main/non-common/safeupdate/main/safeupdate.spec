%global	sname	safeupdate

%{!?llvm:%global llvm 1}

Summary:	A simple extension to PostgreSQL that requires criteria for UPDATE and DELETE
Name:		%{sname}_%{pgmajorversion}
Version:	1.5
Release:	4PGDG%{?dist}
License:	ISC
URL:		https://github.com/eradman/pg-safeupdate
Source0:	https://github.com/eradman/pg-safeupdate/archive/refs/tags/%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion} postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}

%description
safeupdate is a simple extension to PostgreSQL that raises an error if UPDATE
and DELETE are executed without specifying conditions. This extension was
initially designed to protect data from accidental obliteration of data that
is writable by PostgREST.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for safeupdate
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
This package provides JIT support for safeupdate
%endif

%prep
%setup -q -n pg-%{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}
%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 1.5-4PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.5-3PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Wed Jan 29 2025 Devrim Gunduz <devrim@gunduz.org> - 1.5-2PGDG
- Update LLVM dependencies
- Remove redundant BR

* Mon Jul 29 2024 Devrim Gunduz <devrim@gunduz.org> - 1.5-1PGDG
- Update to 1.5 per changes described at:
  https://github.com/eradman/pg-safeupdate/releases/tag/1.5
- Update LLVM dependencies

* Wed Sep 13 2023 Devrim Gunduz <devrim@gunduz.org> - 1.4.2-2PGDG
- Add PGDG branding
- Cleanup rpmlint warning

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.4.2-1.1
- Rebuild against LLVM 15 on SLES 15

* Sat Dec 31 2022 Devrim Gündüz <devrim@gunduz.org> - 1.4.2-1
- Update to 1.4.2

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.4.-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu Jun 3 2021 Devrim Gündüz <devrim@gunduz.org> - 1.4-1
- Update to 1.4

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> 1.3-2
- Remove pgxs patches, and export PATH instead.

* Wed Aug 12 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3-1
- Update to 1.3

* Fri Aug 30 2019 Devrim Gündüz <devrim@gunduz.org> - 1.2-1
- Initial RPM packaging for PostgreSQL RPM Repository
