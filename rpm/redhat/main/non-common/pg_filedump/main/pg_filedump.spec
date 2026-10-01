%global sname pg_filedump

%{!?runselftest:%global runselftest 0}

%global pg_fdmajorver 19
%global pg_fdminorver 0

%global sversion REL_%{pg_fdmajorver}_%{pg_fdminorver}

Summary:	PostgreSQL File Dump Utility
Name:		%{sname}_%{pgmajorversion}
Version:	%{pg_fdmajorver}.%{pg_fdminorver}
Release:	4PGDG%{?dist}
URL:		https://github.com/df7cb/%{sname}
Source0:	https://github.com/df7cb/%{sname}/archive/%{sversion}.tar.gz
Patch0:		%{sname}-makefile-rpm-gcc.patch
License:	GPLv2+
BuildRequires:	clang gcc make
BuildRequires:	postgresql%{pgmajorversion}-devel
# The static libraries (libpgcommon, libpgport) are in the -static subpackage
# as of PostgreSQL 19:
%if %{pgmajorversion} >= 19
BuildRequires:	postgresql%{pgmajorversion}-static
%endif
%if %runselftest
BuildRequires:	postgresql%{pgmajorversion}-server pgdg-srpm-macros >= 2.0.0
%endif
# lz4 dependency
%if 0%{?suse_version} >= 1500
BuildRequires:	liblz4-devel
Requires:	liblz4-1
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	lz4-devel
Requires:	lz4-libs
%endif

Obsoletes:	%{sname}17 <= 17.1 %{sname}16 <= 17.1 %{sname}15 <= 17.1
Obsoletes:	%{sname}14 <= 17.1 %{sname}13 <= 17.1

%description
Display formatted contents of a PostgreSQL heap/index/control file.

%prep
%setup -q -n %{sname}-%{sversion}
%patch -P0 -p0

%build
export CFLAGS="$RPM_OPT_FLAGS"

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__mkdir} -p %{buildroot}%{pginstdir}/bin
%{__install} -m 755 pg_filedump %{buildroot}%{pginstdir}/bin

%check
%if %runselftest
# Only the regression tests: the TAP test (t/001_basic.pl) dies halfway
# through (exit 29, no failed test) in the build environment.
%pgdg_check_installcheck TAP_TESTS=
%endif

%files
%defattr(-,root,root)
%{pginstdir}/bin/pg_filedump
%doc README.pg_filedump.md

%changelog
* Tue Sep 29 2026 Devrim Gündüz <devrim@gunduz.org> - 19.0-4PGDG
- Add %%check, running the regression tests with the %%check helpers
  from pgdg-srpm-macros 2.0.0. It is disabled by default; enable it
  with --define 'runselftest 1'.
- Add postgresqlNN-static to BuildRequires for PostgreSQL 19+: libpgcommon
  and libpgport static libraries are in that subpackage now.

* Thu Sep 10 2026 Devrim Gündüz <devrim@gunduz.org> - 19.0-3PGDG
- Add missing BR

* Thu Jul 23 2026 Devrim Gündüz <devrim@gunduz.org> - 19.0-2PGDG
- Add a patch to fix(?) intermittent build issues on Fedora.

* Thu Jul 23 2026 Devrim Gündüz <devrim@gunduz.org> - 19.0-1PGDG
- Update to 19.0 per changes described at:
  https://github.com/df7cb/pg_filedump/releases/tag/REL_19_0

* Sun Apr 20 2025 Devrim Gündüz <devrim@gunduz.org> - 17.4-1PGDG
- Update to 17.4 per changes described at:
  https://github.com/df7cb/pg_filedump/releases/tag/REL_17_4

* Wed Apr 16 2025 Devrim Gündüz <devrim@gunduz.org> - 17.3-1PGDG
- Update to 17.3 per changes described at:
  https://github.com/df7cb/pg_filedump/releases/tag/REL_17_3

* Tue Apr 15 2025 Devrim Gündüz <devrim@gunduz.org> - 17.2-1PGDG
- Update to 17.2 per changes described at:
  https://github.com/df7cb/pg_filedump/releases/tag/REL_17_2

* Tue Feb 25 2025 Devrim Gündüz <devrim@gunduz.org> - 17.1-2PGDG
- Add missing BRs and remove redundant BR

* Sat Nov 9 2024 Devrim Gündüz <devrim@gunduz.org> - 17.1-1PGDG
- Update to 17.1 per changes described at:
  https://github.com/df7cb/pg_filedump/releases/tag/REL_17_1

* Sat Sep 21 2024 Devrim Gündüz <devrim@gunduz.org> - 17.0-1PGDG
- Initial packaging for the PostgreSQL RPM Repository
