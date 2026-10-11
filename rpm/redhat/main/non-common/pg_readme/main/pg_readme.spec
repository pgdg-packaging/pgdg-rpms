%global sname	pg_readme

%{!?runselftest:%global runselftest 0}
# The tests use the \getenv command of psql, which is new in PostgreSQL 15:
%if 0%{?pgmajorversion} && 0%{?pgmajorversion} < 15
%global runselftest 0
%endif

Summary:	PostgreSQL extension to generate a README.md document for a database extension or schema
Name:		%{sname}_%{pgmajorversion}
Version:	0.7.1
Release:	3PGDG%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		https://github.com/bigsmoke/%{sname}
Source0:	https://github.com/bigsmoke/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	make
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
%if %runselftest
BuildRequires:	postgresql%{pgmajorversion}-server pgdg-srpm-macros >= 2.0.0
# For hstore, which pg_readme requires:
BuildRequires:	postgresql%{pgmajorversion}-contrib
%endif
BuildArch:	noarch

%description
The pg_readme PostgreSQL extension provides functions to generate a README.md
document for a database extension or schema, based on COMMENT objects found
in the pg_description system catalog.

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
# The test creates the extension with each of its entry versions, updates it to
# the newest one and runs its test procedures. The expected output has the
# versions in ascending order, but the Makefile lists them with $(wildcard),
# whose order is not guaranteed (older GNU make does not sort it), so pass
# them sorted:
%pgdg_check_installcheck EXTENSION_ENTRY_VERSIONS="$(ls sql/%{sname}--[0-9]*.[0-9]*.[0-9]*.sql | \
	sed -n 's|^sql/%{sname}--\([0-9.]*\)\.sql$|\1|p' | sort -V | paste -sd ' ')"
%endif

%files
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENCE.txt
%defattr(-,root,root,-)
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}*.control

%changelog
* Mon Oct 12 2026 Devrim Gündüz <devrim@gunduz.org> - 0.7.1-3PGDG
- Add %%check, running the regression tests with the %%check helpers
  from pgdg-srpm-macros 2.0.0, on PostgreSQL 15 and newer: the tests use
  the \getenv command of psql, which is new in PostgreSQL 15. It is
  disabled by default; enable it with --define 'runselftest 1'. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/165

* Thu Sep 10 2026 Devrim Gündüz <devrim@gunduz.org> - 0.7.1-2PGDG
- Add missing BR

* Mon Aug 31 2026 - Devrim Gündüz <devrim@gunduz.org> - 0.7.1-1PGDG
- Update to 0.7.1 per changes described at:
  https://github.com/bigsmoke/pg_readme/releases/tag/v0.7.1

* Tue Sep 3 2024 - Devrim Gündüz <devrim@gunduz.org> - 0.7.0-1PGDG
- Initial RPM packaging for the PostgreSQL RPM repository.
