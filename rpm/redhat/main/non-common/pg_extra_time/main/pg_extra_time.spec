%global sname	pg_extra_time

%{!?runselftest:%global runselftest 0}

Summary:	Extra date time functions and operators for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	2.1.0
Release:	3PGDG%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		https://github.com/bigsmoke/%{sname}
Source0:	https://github.com/bigsmoke/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	make
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
%if %runselftest
%if %{pgmajorversion} >= 16
BuildRequires:	postgresql%{pgmajorversion}-server pgdg-srpm-macros >= 2.0.0
%endif
%endif
BuildArch:	noarch

%description
The pg_extra_time PostgreSQL extension contains some date time
functions and operators.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__make} PG_CONFIG=%{pginstdir}/bin/pg_config USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} PG_CONFIG=%{pginstdir}/bin/pg_config USE_PGXS=1 %{?_smp_mflags} DESTDIR=%{buildroot} install
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__mv} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%check
%if %runselftest
# The tests use the time zone form of generate_series(), which is new in
# PostgreSQL 16:
%if %{pgmajorversion} >= 16
# The test creates the extension with each of its entry versions, updates it to
# the newest one and runs its test procedures. The expected output has the
# versions in ascending order, but the Makefile lists them with $(wildcard),
# whose order is not guaranteed (older GNU make does not sort it), so pass
# them sorted:
%pgdg_check_installcheck EXTENSION_ENTRY_VERSIONS="$(ls sql/%{sname}--[0-9]*.[0-9]*.[0-9]*.sql | \
	sed -n 's|^sql/%{sname}--\([0-9.]*\)\.sql$|\1|p' | sort -V | paste -sd ' ')"
%endif
%endif

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENCE.txt
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}*.control

%changelog
* Mon Oct 12 2026 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-3PGDG
- Add %%check, running the regression tests with the %%check helpers
  from pgdg-srpm-macros 2.0.0, on PostgreSQL 16 and newer: the tests use
  the time zone form of generate_series(), which is new in PostgreSQL 16.
  It is disabled by default; enable it with --define 'runselftest 1'. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/165

* Thu Sep 10 2026 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-2PGDG
- Add missing BR

* Thu Jun 11 2026 - Devrim Gündüz <devrim@gunduz.org> - 2.1.0-1PGDG
- Update to 2.1.0 per changes described at:
  https://github.com/bigsmoke/pg_extra_time/releases/tag/v2.1.0
  https://github.com/bigsmoke/pg_extra_time/blob/v2.1.0/CHANGELOG.md

* Mon Jan 20 2025 - Devrim Gündüz <devrim@gunduz.org> - 2.0.0-1PGDG
- Update to 2.0.0 per changes described at:
  https://github.com/bigsmoke/pg_extra_time/releases/tag/v2.0.0
  https://github.com/bigsmoke/pg_extra_time/blob/v2.0.0/CHANGELOG.md

* Wed Jun 26 2024 - Devrim Gündüz <devrim@gunduz.org> - 1.1.3-1PGDG
- Update to 1.1.3 per changes described at:
  https://github.com/bigsmoke/pg_extra_time/releases/tag/v1.1.3

* Thu Dec 21 2023 - Devrim Gündüz <devrim@gunduz.org> - 1.1.2-1PGDG
- Initial RPM packaging for the PostgreSQL RPM repository.
