%global sname pg_stat_monitor

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL Query Performance Monitoring Tool
Name:		%{sname}_%{pgmajorversion}
Version:	2.2.0
Release:	1PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/percona/%{sname}
Source0:	https://github.com/percona/%{sname}/archive/refs/tags/%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 2.1.3-2

%description
The pg_stat_monitor is a Query Performance Monitoring tool for PostgreSQL.
It attempts to provide a more holistic picture by providing much-needed query
performance insights in a single view.

pg_stat_monitor provides improved insights that allow database users to
understand query origins, execution, planning statistics and details, query
information, and metadata. This significantly improves observability, enabling
users to debug and tune query performance. pg_stat_monitor is developed on the
basis of pg_stat_statements as its more advanced replacement.

While pg_stat_statements provides ever-increasing metrics, pg_stat_monitor
aggregates the collected data, saving user efforts for doing it themselves.
pg_stat_monitor stores statistics in configurable time-based units – buckets.
This allows focusing on statistics generated for shorter time periods and
makes query timing information such as max/min/mean time more accurate.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_stat_monitor
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
This packages provides JIT support for pg_stat_monitor
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README
%{__install} -d %{buildroot}%{pginstdir}/doc/extension/
%{__install} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%license LICENSE
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
 %{pginstdir}/lib/bitcode/%{sname}*.bc
 %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Thu Jul 10 2025 - Devrim Gündüz <devrim@gunduz.org> - 2.2.0-1PGDG
- Update to 2.2.0 per changes described at:
  https://github.com/percona/pg_stat_monitor/releases/tag/2.2.0

* Mon Feb 24 2025 - Devrim Gündüz <devrim@gunduz.org> - 2.1.1-1PGDG
- Update to 2.1.1 per changes described at:
  https://github.com/percona/pg_stat_monitor/releases/tag/2.1.1

* Thu Jan 16 2025 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-2PGDG
- Update LLVM dependencies
- Update package description and install license file.

* Thu Aug 8 2024 - Devrim Gündüz <devrim@gunduz.org> - 2.1.0-1PGDG
- Update to 2.1.0 per changes described at:
  https://github.com/percona/pg_stat_monitor/releases/tag/2.1.0

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 2.0.4-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Sun Feb 25 2024 - Devrim Gündüz <devrim@gunduz.org> - 2.0.4-1PGDG
- Update to 2.0.4 per changes described at:
  https://github.com/percona/pg_stat_monitor/releases/tag/2.0.4

* Mon Dec 4 2023 - Devrim Gündüz <devrim@gunduz.org> - 2.0.3-1PGDG
- Update to 2.0.3

* Wed Sep 13 2023 - Devrim Gündüz <devrim@gunduz.org> - 2.0.2-1PGDG
- Update to 2.0.2
- Cleanup rpmlint warning

* Tue Jun 20 2023 - Devrim Gündüz <devrim@gunduz.org> - 2.0.1-1PGDG
- Update to 2.0.1
- Add PGDG suffix to the package.

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.1.0-2.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon Sep 19 2022 - Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1
- Update to 1.1.0

* Tue May 31 2022 - Devrim Gündüz <devrim@gunduz.org> - 1.0.1-1
- Update to 1.0.1

* Fri May 6 2022 - Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1
- Update to 1.0.0

* Tue Jan 4 2022 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-rc.1
- Update to 1.0.0-rc.1

* Fri Sep 24 2021 - Devrim Gündüz <devrim@gunduz.org> 0.9.2-beta1
- Update to 0.9.2 beta1

* Thu Apr 15 2021 - Devrim Gündüz <devrim@gunduz.org> 0.9.1-1
- Update to 0.9.1

* Thu Jan 28 2021 - Devrim Gündüz <devrim@gunduz.org> 0.7.2-2
- Fix distro part in RPM names.

* Thu Jan 21 2021 - Devrim Gündüz <devrim@gunduz.org> 0.7.2-1
- Initial RPM packaging for PostgreSQL RPM Repository
