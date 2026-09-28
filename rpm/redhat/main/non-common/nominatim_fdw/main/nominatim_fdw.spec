%global sname nominatim_fdw

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

Summary:	Nominatim Foreign Data Wrapper for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	2.3
Release:	1PGDG%{?dist}
License:	MIT
URL:		https://github.com/jimjonesbr/%{sname}
Source0:	https://github.com/jimjonesbr/%{sname}/archive/v%{version}.tar.gz
Patch0:		%{sname}-curl-nghttp2-version.patch
Patch1:		%{sname}-version-test-optional-components.patch

BuildRequires:	postgresql%{pgmajorversion}-devel libcurl-devel libxml2-devel
Requires:	postgresql%{pgmajorversion}-server
%if %runselftest
BuildRequires:	postgresql%{pgmajorversion}-server pgdg-srpm-macros
%endif

%description
The nominatim_fdw is a PostgreSQL Foreign Data Wrapper to access data from
Nominatim servers using simple function calls.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for nominatim_fdw
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
This package provides JIT support for nominatim_fdw
%endif

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p1
%patch -P 1 -p1

%build
PATH=%{pginstdir}/bin:$PATH USE_PGXS=1 %{__make} %{?_smp_mflags} %{with_llvm_arg}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH USE_PGXS=1 %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install %{with_llvm_arg}

%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension/
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%check
%if %runselftest
# The extension cannot be installed into %%{pginstdir} at build time, so run
# the regression tests against a copy of the PostgreSQL installation, with
# this package's files on top. PostgreSQL is relocatable, so pg_config and the
# server both pick up the copy. The expected output assumes the superuser is
# called postgres, hence a server of our own instead of pg_regress's
# --temp-instance. Only the tests that need no network access run by default.
# initdb refuses to run as root, so skip them then.
if [ x"`id -u`" = x0 ]; then
	echo "Skipping the regression tests, as initdb cannot be run as root."
else
	%{__rm} -rf tmp_pginst tmp_check
	%{__cp} -a %{pginstdir} tmp_pginst
	%{__cp} -a %{buildroot}%{pginstdir}/. tmp_pginst/
	sockdir=`mktemp -d`
	tmp_pginst/bin/initdb -D tmp_check/data -U postgres -A trust --no-sync >/dev/null
	tmp_pginst/bin/pg_ctl -D tmp_check/data -l tmp_check/postmaster.log -w \
		-o "-c listen_addresses='' -k $sockdir -p 54321" start
	rc=0
	PGHOST=$sockdir PGPORT=54321 PGUSER=postgres %{__make} installcheck USE_PGXS=1 \
		PG_CONFIG=$(pwd)/tmp_pginst/bin/pg_config %{with_llvm_arg} || rc=$?
	tmp_pginst/bin/pg_ctl -D tmp_check/data -m fast -w stop
	%{__rm} -rf $sockdir
	if [ $rc -ne 0 ]; then
		%{__cat} regression.diffs
		exit $rc
	fi
fi
%endif

%files
%defattr(644,root,root,755)
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
* Mon Sep 28 2026 Devrim Gunduz <devrim@gunduz.org> - 2.3-1PGDG
- Update to 2.3 per changes described at:
  https://github.com/jimjonesbr/nominatim_fdw/releases/tag/v2.3
- Add a patch to fix builds against curl < 7.66 (EL-8), which lacks
  nghttp2_version in curl_version_info_data.
- Add %%check, running the regression tests that need no network access.
  It is disabled by default; enable it with --define 'runselftest 1'.
  Add a patch to the version test, so that it does not expect the
  optional libcurl components (ssl, zlib, libSSH, nghttp2).

* Thu Sep 10 2026 Devrim Gunduz <devrim@gunduz.org> - 2.2-1PGDG
- Update to 2.2 per changes described at:
  https://github.com/jimjonesbr/nominatim_fdw/releases/tag/v2.2

* Mon Aug 31 2026 Devrim Gunduz <devrim@gunduz.org> - 2.1-1PGDG
- Update to 2.1 per changes described at:
  https://github.com/jimjonesbr/nominatim_fdw/releases/tag/v2.1

* Sun Aug 30 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0-3PGDG
- Make %%llvm actually control the build, not just packaging: pass
  with_llvm=no to make when %%llvm is 0, otherwise setting %%llvm 0 only
  dropped the llvm BuildRequires/subpackage/files while the build still
  invoked clang regardless, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/51

* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0-2PGDG
- Add Amazon Linux 2023 support.

* Tue Jul 7 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0-1PGDG
- Update to 2.0 per changes described at:
  https://github.com/jimjonesbr/nominatim_fdw/releases/tag/v2.0

* Tue Apr 14 2026 Devrim Gunduz <devrim@gunduz.org> - 1.3-2PGDG
- Rebuild because of a package signing issue

* Mon Apr 13 2026 Devrim Gunduz <devrim@gunduz.org> - 1.3-1PGDG
- Update to 1.3 per changes described at:
  https://github.com/jimjonesbr/nominatim_fdw/releases/tag/1.3

* Mon Apr 6 2026 Devrim Gunduz <devrim@gunduz.org> - 1.2-1PGDG
- Update to 1.2 per changes described at:
  https://github.com/jimjonesbr/nominatim_fdw/releases/tag/1.2

* Mon Jan 26 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1.0-1PGDG
- Initial packaging for the PostgreSQL RPM Repository.
