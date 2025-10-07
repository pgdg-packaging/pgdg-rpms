%global	sname	periods

%{!?llvm:%global llvm 1}

Summary:	PERIODs and SYSTEM VERSIONING for PostgreSQL

Name:		%{sname}_%{pgmajorversion}
Version:	1.2.2
Release:	6PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/xocolatl/%{sname}
Source0:	https://github.com/xocolatl/%{sname}/archive/v%{version}.zip
BuildRequires:	postgresql%{pgmajorversion} postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}

%description
This extension recreates the behavior defined in SQL:2016 (originally in
SQL:2011) around periods and tables with SYSTEM VERSIONING. The idea is to
figure out all the rules that PostgreSQL would like to adopt (there are some
details missing in the standard) and to allow earlier versions of PostgreSQL
to simulate the behavior once the feature is finally integrated.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for periods
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
This package provides JIT support for periods
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md
%doc %{pginstdir}/doc/extension/README.periods
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Mon Oct 6 2025 Devrim Gunduz <devrim@gunduz.org> - 1.2.2-6PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.2.2-5PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Sat Jan 4 2025 Devrim Gündüz <devrim@gunduz.org> - 1.2.2-4PGDG
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.2.2-3PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Thu Feb 22 2024 Devrim Gunduz <devrim@gunduz.org> - 1.2.2-2PGDG
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.2.2-1.1
- Rebuild against LLVM 15 on SLES 15

* Wed Dec 14 2022 Devrim Gündüz <devrim@gunduz.org> - 1.2.2-1
- Update to 1.2.2

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.2-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed May 26 2021 Devrim Gündüz <devrim@gunduz.org> - 1.2-2
- Remove PGXS patches, and export PATH instead.

* Wed Sep 23 2020 Devrim Gündüz <devrim@gunduz.org> - 1.2-1
- Update to 1.2

* Wed Feb 5 2020 Devrim Gündüz <devrim@gunduz.org> - 1.1-2
- Add a patch to fix RHEL 7 builds, per Vik.

* Wed Feb 5 2020 Devrim Gündüz <devrim@gunduz.org> - 1.1-1
- Update to 1.1

* Sun Sep 1 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0-2
- Fix OS versions in Makefile, the distro name in the packages changed.

* Fri Aug 30 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
