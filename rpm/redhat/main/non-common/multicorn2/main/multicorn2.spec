%global sname multicorn2
%global pname multicorn

%{!?llvm:%global llvm 1}

%if 0%{?fedora} && 0%{?fedora} <= 42
%global	__ospython %{_bindir}/python3.13
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%endif
%if 0%{?suse_version} >= 1500
%global	__ospython %{_bindir}/python3.11
%endif

%if 0%{?fedora} >= 40 || 0%{?rhel} >= 10
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif

Summary:	Multicorn Python bindings for Postgres FDW
Name:		%{sname}_%{pgmajorversion}
Version:	3.1
Release:	1PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/pgsql-io/%{sname}/archive/refs/tags/v%{version}.tar.gz
Patch0:		%{sname}-Makefile-removepip.patch
URL:		https://github.com/pgsql-io/%{version}
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	python3-devel

Provides:	python3dist(multicorn)%{?_isa} = %{version}-%{release}
# Provide versionless multicorn. This will simplify using
# bigquery_fdw package.
Provides:	%{sname} = %{version}

%description
Multicorn2 Python3 Wrapper for Postgresql Foreign Data Wrapper. Tested
tested on Linux w/ Python 3.9-3.12 & Postgres 13-17.

The Multicorn Foreign Data Wrapper allows you to fetch foreign data in
Python in your PostgreSQL server.

Multicorn2 is distributed under the PostgreSQL license. See the LICENSE
file for details.The Multicorn Foreign Data Wrapper allows you to write
foreign data wrappers in Python.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for multicorn2
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
This package provides JIT support for multicorn2
%endif

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p0

%build
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install
# Install Python portions manually:
%{__mkdir} -p %{buildroot}%{python3_sitearch}/%{pname}
%{__cp} -rp python/multicorn/* %{buildroot}%{python3_sitearch}/%{pname}

%files
%defattr(644,root,root,755)
%doc README.md
%doc %{pginstdir}/doc/extension/%{pname}.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}*.sql
%{pginstdir}/share/extension/%{pname}.control
%{python3_sitearch}/%{pname}/*

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{pname}*.bc
    %{pginstdir}/lib/bitcode/%{pname}/src/*.bc
%endif

%changelog
* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Wed Aug 27 2025 Devrim Gündüz <devrim@gunduz.org> - 3.1-1PGDG
- Update to 3.1
- Build with Python 3.12 on RHEL 8 and 9.

* Fri Jan 3 2025 Devrim Gündüz <devrim@gunduz.org> - 3.0-2PGDG
- Add RHEL 10 support
- Update LLVM dependencies

* Wed Sep 25 2024 Devrim Gündüz <devrim@gunduz.org> - 3.0-1PGDG
- Update to 3.0
- Remove patch1, it is now in upstream tarball.

* Mon Sep 23 2024 Devrim Gündüz <devrim@gunduz.org> - 3.0beta1-3PGDG
- Add a (temporary) patch from upstream to fix builds against PostgreSQL 17.

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 3.0beta1-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Wed Jun 26 2024 Devrim Gündüz <devrim@gunduz.org> - 3.0beta1-1PGDG
- Update to 3.0 beta1
- Explicitly provide python module, per
  https://redmine.postgresql.org/issues/7811#note-3

* Mon Sep 25 2023 Devrim Gündüz <devrim@gunduz.org> - 2.5-1PGDG
- Update to 2.5
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 2.4-2.1
- Rebuild against LLVM 15 on SLES 15

* Mon May 22 2023 Devrim Gunduz <devrim@gunduz.org> - 2.4-2
- Install Python portions, per
  https://redmine.postgresql.org/issues/7811

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 2.4-1.1
- Modernise %%patch usage, which has been deprecated in Fedora 38

* Wed Apr 12 2023 Devrim Gündüz <devrim@gunduz.org> - 2.4-1
- Update to 2.4

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.3-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Sat Jun 11  2022 Devrim Gündüz <devrim@gunduz.org> 2.3-1
- Switch to new repo

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 1.4.0-4
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 1.4.0-3
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Tue May 19 2020 - Devrim Gündüz <devrim@gunduz.org> 1.4.0-2
- Provide versionless multicorn. This will simplify using
  bigquery_fdw package.

* Sat Mar 21 2020 - Devrim Gündüz <devrim@gunduz.org> 1.4.0-1
- Update to 1.4.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.3.5-1.1
- Rebuild against PostgreSQL 11.0

* Fri Jan 12 2018 - Devrim Gündüz <devrim@gunduz.org> 1.3.5-1
- Update to 1.3.5, per #2888 .

* Tue Nov 21 2017 - Devrim Gündüz <devrim@gunduz.org> 1.3.4-1
- Update to 1.3.4, per #2888 .

* Mon Mar 6 2017 - Devrim Gündüz <devrim@gunduz.org> 1.3.3-1
- Update to 1.3.3, per #2224 .

* Thu Mar 3 2016 - Devrim Gündüz <devrim@gunduz.org> 1.3.2-1
- Update to 1.3.2

* Mon Jan 18 2016 - Devrim Gündüz <devrim@gunduz.org> 1.3.1-1
- Update to 1.3.1

* Thu Dec 10 2015 - Devrim Gündüz <devrim@gunduz.org> 1.2.4-1
- Update to 1.2.4

* Wed Jan 21 2015 - Devrim Gündüz <devrim@gunduz.org> 1.2.3-1
- Initial packaging for PostgreSQL RPM Repository
