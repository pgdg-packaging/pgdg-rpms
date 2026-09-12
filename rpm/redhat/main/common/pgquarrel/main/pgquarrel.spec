%global sname pgquarrel
%global sversion 0_7_0

Summary:	Compares PostgreSQL database schemas (DDL)
Name:		%{sname}
Version:	0.7.0
Release:	5PGDG%{?dist}
License:	BSD
Source0:	https://github.com/eulerto/%{sname}/archive/%{sname}_%{sversion}.tar.gz
Patch0:		%{sname}-libminipath.patch
Patch1:		%{sname}-inccommon.patch
Patch2:		%{sname}-pg14-simple-prompt.patch
URL:		https://github.com/eulerto/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel cmake pgdg-srpm-macros
BuildRequires:	gcc
Requires:	postgresql-libs

%description
pgquarrel is a program that compares PostgreSQL database schemas (DDL).

Given two database connections, it output a file that represent the
difference between schemas. It means that if you run the output file into
the target database, it'll have the same schema as the source database.
The main use case is to deploy database changes into testing, staging or
production environment.

pgquarrel does not rely on another tool (such as pg_dump) instead it connects
directly to PostgreSQL server, obtain meta data from catalog, compare objects
and output the commands necessary to turn target database into source
database.

%prep
%setup -q -n %{sname}-%{sname}_%{sversion}
%patch -P 0 -p0
%patch -P 1 -p0
%patch -P 2 -p0

%build
cmake -DPGCONFIG_PATH=/usr/pgsql-%{pgmajorversion}/bin/pg_config \
	-DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
	-DCMAKE_INSTALL_PREFIX=/usr .

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} USE_PGXS=1 %{?_smp_mflags} install

%files
%defattr(644,root,root,755)
%doc README.md
%license LICENSE
%attr (755,root,root) %{_bindir}/%{sname}
%{_libdir}/libmini.so

%changelog
* Sat Sep 12 2026 Devrim Gunduz <devrim@gunduz.org> - 0.7.0-5PGDG
- Add -DCMAKE_POLICY_VERSION_MINIMUM=3.5: CMakeLists.txt's
  cmake_minimum_required is too old for CMake 4 ("Compatibility with
  CMake < 3.5 has been removed")
- Add missing BR (gcc)
- Add pgquarrel-pg14-simple-prompt.patch to fix builds against
  PostgreSQL 14+: src/quarrel.c called simple_prompt() with its old
  pre-PG14 3/4-argument signature without even including the header
  that declares it ("implicit declaration of function
  'simple_prompt'"). PG14+'s common/string.h declares it as
  simple_prompt(const char *prompt, bool echo) (2 args, allocates and
  returns the buffer itself). Add #include "common/string.h" and a
  PG_VERSION_NUM >= 140000 branch using the modern signature, alongside
  the existing >= 100000 and legacy branches

* Fri Sep 15 2023 Devrim Gunduz <devrim@gunduz.org> - 0.7.0-4PGDG
- Bump up release number after to reflect non-common -> common move.

* Mon Sep 11 2023 Devrim Gunduz <devrim@gunduz.org> - 0.7.0-3PGDG
- Add patch to fix builds against PostgreSQL 15 and 16, per
  https://github.com/eulerto/pgquarrel/issues/105 and
  https://github.com/eulerto/pgquarrel/commit/dac0a5527bd1ae48b5926a2b04fed5c01fb2c2c6
- Add PGDG branding

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 0.7.0-2.1
- Modernise %%patch usage, which has been deprecated in Fedora 38

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 0.7.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue Mar 31 2020 Devrim Gündüz <devrim@gunduz.org> - 0.7.0-1
- Update to 0.7.0
- Fix packaging

* Sat Nov 30 2019 Devrim Gündüz <devrim@gunduz.org> - 0.6.0-1
- Initial packaging for PostgreSQL RPM Repository
