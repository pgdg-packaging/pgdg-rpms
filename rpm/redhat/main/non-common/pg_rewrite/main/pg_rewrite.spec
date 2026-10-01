%global sname pg_rewrite

%global pgrwmajver 2
%global pgrwmidver 2

%{!?llvm:%global llvm 1}
%{!?runselftest:%global runselftest 0}

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

Summary:	PostgreSQL tool to rewrite a table
Name:		%{sname}_%{pgmajorversion}
Version:	%{pgrwmajver}.%{pgrwmidver}
Release:	4PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/%{sname}/%{sname}
Source0:	https://github.com/cybertec-postgresql/pg_rewrite/archive/refs/tags/REL%{pgrwmajver}_%{pgrwmidver}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
%if %runselftest
BuildRequires:	postgresql%{pgmajorversion}-server pgdg-srpm-macros >= 2.0.0
# The tests also use pageinspect
BuildRequires:	postgresql%{pgmajorversion}-contrib
%endif

%description
pg_rewrite is a tool to rewrite table (i.e. to copy its data to a new file).
It allows both read and write access to the table during the rewriting.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_rewrite
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
This package provides JIT support for pg_rewrite
%endif

%prep
%setup -q -n %{sname}-REL%{pgrwmajver}_%{pgrwmidver}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} %{with_llvm_arg} install

%check
%if %runselftest
# The tests need pg_rewrite in shared_preload_libraries, and logical
# decoding. Recent PostgreSQL minor releases only allow the output plugins
# listed in output_plugin_libraries, so add pg_rewrite there when it exists.
%pgdg_check_init
opl=
if postgres --describe-config | grep -q '^output_plugin_libraries'; then
	opl="output_plugin_libraries = 'pgoutput, test_decoding, pg_rewrite'"
fi
pgdg_check_start main "shared_preload_libraries = 'pg_rewrite'" \
	"wal_level = logical" "max_replication_slots = 1" ${opl:+"$opl"}
pgdg_installcheck %{with_llvm_arg}
%endif

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/%{sname}.md
%{pginstdir}/lib/%{sname}*.*
%{pginstdir}/share/extension/%{sname}*.*

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}.index.bc
    %{pginstdir}/lib/bitcode/%{sname}/*bc
%endif

%changelog
* Thu Oct 1 2026 Devrim Gunduz <devrim@gunduz.org> - %{pgrwmajver}.%{pgrwmidver}-4PGDG
- Add %%check, running the regression tests with the %%check helpers
  from pgdg-srpm-macros 2.0.0. It is disabled by default; enable it
  with --define 'runselftest 1'.

* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - %{pgrwmajver}.%{pgrwmidver}-3PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51

* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 2.2-2PGDG
- Add Amazon Linux 2023 support.

* Mon Jul 13 2026 Devrim Gündüz <devrim@gunduz.org> - 2.2-1PGDG
- Update to 2.2 per changes described at:
  https://github.com/cybertec-postgresql/pg_rewrite/releases/tag/REL2_2

* Mon Feb 16 2026 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-1PGDG
- Update to 2.1.0 per changes described at:
  https://github.com/cybertec-postgresql/pg_rewrite/releases/tag/REL2_1_0

* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-3PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 2.0.0-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Tue Sep 2 2025 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-1PGDG
- Update to 2.0.0 per changes described at:
  https://github.com/cybertec-postgresql/pg_rewrite/releases/tag/REL2_0_0

* Wed Jul 30 2025 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1PGDG
- Initial packaging for the PostgreSQL RPM Repository
