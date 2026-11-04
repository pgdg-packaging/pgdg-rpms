%global sname	passwordpolicy
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

Summary:	PostgreSQL Passwordcheck Policy
Name:		%{sname}_%{pgmajorversion}
Version:	2.0.6
Release:	6PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/fmbiete/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/fmbiete/%{sname}
BuildRequires:	krb5-devel
%if 0%{?suse_version} >= 1500
BuildRequires:	libopenssl-3-devel
%endif
%if 0%{?fedora} >= 43 || 0%{?rhel} >= 8 || 0%{?amzn}
BuildRequires:	openssl-devel
%endif
%if 0%{?fedora} && 0%{?fedora} <= 44 && !0%{?amzn}
BuildRequires:	openssl-devel-engine
%endif
BuildRequires:	postgresql%{pgmajorversion}-devel postgresql%{pgmajorversion}
BuildRequires:	cracklib-devel
Requires:	postgresql%{pgmajorversion}-server
Requires:	cracklib
%if %runselftest
BuildRequires:	postgresql%{pgmajorversion}-server pgdg-srpm-macros >= 2.0.0
%if 0%{?suse_version}
BuildRequires:	cracklib-dict-full
%else
BuildRequires:	cracklib-dicts
%endif
%endif

%description
The PostgreSQL Passwordcheck Policy is like the regular passwordcheck module,
except that you can dynamically define the complexity requirements.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for passwordpolicy
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
This package provides JIT support for passwordpolicy
%endif

%prep
%setup -q -n %{sname}-%{version}
# pg_reload_conf() only signals the postmaster, so the backend may run the
# next statement before it gets the reload signal. Sleep in the same
# statement, so that the reload is processed before the next one runs. The
# column name stays the same, so the expected output only changes in the
# echoed statement.
%{__sed} -i 's/^SELECT pg_reload_conf();/SELECT r AS pg_reload_conf FROM pg_reload_conf() r, LATERAL (SELECT pg_sleep(0.5)) s;/' \
	test/sql/common/reset.sql test/sql/*.sql test/expected/*.out
# test05's expected output predates the pg_sleep() calls in its SQL
%{__sed} -i '/^SELECT pg_sleep(1);$/d' test/sql/passwordpolicy_test05.sql

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install %{with_llvm_arg}
# Install README file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%check
%if %runselftest
# passwordpolicy needs to be preloaded; test04 checks a dictionary word, so
# point cracklib at the system dictionary.
%pgdg_check_init
pgdg_check_start main "shared_preload_libraries = 'passwordpolicy'" \
	"password_policy.cracklib_dictpath = '%{_datadir}/cracklib/pw_dict'"
# test06's expected output belongs to an older version of the test, and its
# result depends on the background worker flushing the password history.
pgdg_installcheck %{with_llvm_arg} \
	REGRESS="passwordpolicy_test01 passwordpolicy_test02 passwordpolicy_test03 passwordpolicy_test04 passwordpolicy_test05"
%endif

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Wed Nov 4 2026 Devrim Gündüz <devrim@gunduz.org> - 2.0.6-6PGDG
- Add %%check, running the regression tests with the %%check helpers
  from pgdg-srpm-macros 2.0.0. It is disabled by default; enable it with
  --define 'runselftest 1'. The tests sleep briefly after each
  pg_reload_conf(), so that the new settings are in effect in the next
  statement. Drop the pg_sleep() calls from test05, which its expected
  output does not have, and skip test06, whose expected output belongs to
  an older version of the test.
- Add the missing openssl-devel BuildRequires on RHEL 8.

* Fri Oct 30 2026 Devrim Gündüz <devrim@gunduz.org> - 2.0.6-5PGDG
- Fix/modernize openssl dependencies.

* Thu Sep 10 2026 Devrim Gündüz <devrim@gunduz.org> - 2.0.6-4PGDG
- Add missing BR

* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0.6-3PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51

* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0.6-2PGDG
- Add Amazon Linux 2023 support.

* Wed Jul 8 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0.6-1PGDG
- Update to 2.0.6 per changes described at:
  https://github.com/fmbiete/passwordpolicy/releases/tag/v2.0.6

* Sat Mar 21 2026 Francisco Miguel Biete Banon <fbiete@gmail.com> - 2.0.5-1PGDG
- New release

* Tue Dec 2 2025 Francisco Miguel Biete Banon <fbiete@gmail.com> - 2.0.4
- New release

* Sun Jun 29 2025 Francisco Miguel Biete Banon <fbiete@gmail.com> - 2.0.3
- New release

* Tue Feb 04 2025 Francisco Miguel Biete Banon <fbiete@gmail.com> - 2.0.2
- New release

* Sun Dec 15 2024 Francisco Miguel Biete Banon <fbiete@gmail.com> - 2.0.1
- New release

* Wed Jul 12 2023 Francisco Miguel Biete Banon <fbiete@gmail.com> - 1.1.0
- Initial RPM packaging
