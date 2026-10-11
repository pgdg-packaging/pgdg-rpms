%global sname	pgpdf

%{!?llvm:%global llvm 1}
%{!?runselftest:%global runselftest 0}
# The expected output of the tests has the text that poppler extracts from the
# test PDF, which the older poppler of RHEL 8 and 9 extracts differently:
%if 0%{?rhel} && 0%{?rhel} <= 9
%global runselftest 0
%endif

# Propagate %%llvm into the actual build: PGXS decides whether to invoke
# clang/llvm-config based on with_llvm from the installed postgresql*-devel's
# Makefile.global, not from this spec's %%llvm. Without passing with_llvm=no
# through to make, setting %%llvm 0 here only drops the llvm BuildRequires/
# subpackage/files, while the build still tries to run clang regardless.
%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif


Summary:	pdf type for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	0.1.0
Release:	8PGDG%{?dist}
License:	GPLv2
URL:		https://github.com/Florents-Tselai/%{sname}/
Source0:	https://github.com/Florents-Tselai/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel
%if 0%{?suse_version} == 1500
BuildRequires:	libpoppler-glib-devel
Requires:	libpoppler135 libpoppler-glib8
%endif
%if 0%{?suse_version} == 1600
BuildRequires:	libpoppler-glib-devel
Requires:	libpoppler148 libpoppler-glib8
%endif
%if 0%{?fedora} >= 42 || 0%{?rhel} >= 8  || 0%{?amzn}
BuildRequires:	poppler-glib-devel
Requires:	poppler
%endif
Requires:	postgresql%{pgmajorversion}-server
%if %runselftest
BuildRequires:	postgresql%{pgmajorversion}-server pgdg-srpm-macros >= 2.0.0
BuildRequires:	wget
%endif

%description
This extension for PostgreSQL provides a pdf data type and assorted functions.

You can create a pdf type, by casting either a text filepath or bytea column.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgpdf
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} == 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?suse_version} == 1600
BuildRequires:	llvm19-devel clang19-devel
Requires:	llvm19
%endif
%if 0%{?amzn}
BuildRequires:	llvm-devel >= 15.0 clang-devel >= 15.0
Requires:	llvm >= 15.0
%endif
%if ( 0%{?fedora} || 0%{?rhel} >= 8 ) && !0%{?amzn}
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for pgpdf
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg} INSTALL_PREFIX=%{buildroot} DESTDIR=%{buildroot} install

%check
%if %runselftest
# The tests read PDF files from /tmp, which the installcheck target creates
# (big.pdf is downloaded from www.postgresql.org, so the tests need internet
# access). Put them in the data directory of the test server instead, so that
# builds running side by side do not share them, and use paths relative to it
# in the tests, which keeps the queries short enough to be shown in full in
# the error messages of the expected output:
%pgdg_check_init
pgdg_check_start main
datadir=$(psql -XAt -d postgres -c "SHOW data_directory")
mkdir "$datadir/pgpdf"
sed -i "s|/tmp/|$datadir/pgpdf/|g" Makefile
sed -i "s|'/tmp/|'pgpdf/|g" test/sql/pgpdf.sql test/expected/pgpdf.out
grep -qF "$datadir/pgpdf/big.pdf" Makefile
grep -qF "'pgpdf/pgintro.pdf'" test/sql/pgpdf.sql
if grep -q "/tmp/" test/sql/pgpdf.sql test/expected/pgpdf.out; then exit 1; fi
pgdg_installcheck %{with_llvm_arg}
%endif

%files
%defattr(-,root,root,-)
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Mon Oct 12 2026 Devrim Gunduz <devrim@gunduz.org> - 0.1.0-8PGDG
- Add %%check, running the regression tests with the %%check helpers
  from pgdg-srpm-macros 2.0.0. The tests need internet access, and cannot
  run on RHEL 8 and 9, whose older poppler extracts the text of the test
  PDF differently. It is disabled by default; enable it with
  --define 'runselftest 1'. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/165

* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - 0.1.0-7PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51

* Thu Aug 27 2026 Devrim Gunduz <devrim@gunduz.org> - 0.1.0-6PGDG
- Fix Amazon Linux 2023 support.

* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 0.1.0-5PGDG
- Add Amazon Linux 2023 support.

* Wed Mar 25 2026 Devrim Gündüz <devrim@gunduz.org> - 0.1.0-4PGDG
- Fix SLES 16 support

* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 0.1.0-3PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 0.1.0-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Thu Feb 20 2025 Devrim Gündüz <devrim@gunduz.org> - 0.1.0-1PGDG
- Initial RPM packaging for the PostgreSQL RPM Repository.
