%undefine _package_note_file
%global sname pgcopydb

Summary:	Automate pg_dump | pg_restore between two running Postgres servers
Name:		%{sname}
Version:	0.17
Release:	3PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/dimitri/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/dimitri/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel openssl-devel gc-devel
BuildRequires:	krb5-devel bison flex sqlite-devel
# zstd dependency
%if 0%{?suse_version} >= 1500
BuildRequires:	libzstd-devel >= 1.4.0
Requires:	libzstd1 >= 1.4.0
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	libzstd-devel >= 1.4.0
Requires:	libzstd >= 1.4.0
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
BuildRequires:	libxml2-devel libxslt-devel pam-devel
BuildRequires:	readline-devel zlib-devel
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 8
Requires:	gc
%endif
%if 0%{?suse_version} >= 1500
Requires:	libgc1
%endif
Requires:	postgresql%{pgmajorversion}

%description
pgcopydb is a tool that automates running pg_dump | pg_restore between
two running Postgres servers. To make a copy of a database to another
server as quickly as possible, one would like to use the parallel
options of pg_dump and still be able to stream the data to as many
pg_restore jobs.

%prep
%setup -q -n %{sname}-%{version}

USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%files
%license LICENSE
%doc README.md
%{pginstdir}/bin/pgcopydb

%changelog
* Tue Feb 25 2025 Devrim Gündüz <devrim@gunduz.org> - 0.17-3PGDG
- Add missing BRs

* Fri Feb 21 2025 Devrim Gündüz <devrim@gunduz.org> - 0.17-2PGDG
- Remove redundant BR

* Mon Aug 19 2024 Devrim Gündüz <devrim@gunduz.org> - 0.17-1PGDG
- Update to 0.17 per changes described at:
  https://github.com/dimitri/pgcopydb/releases/tag/v0.17
  https://github.com/dimitri/pgcopydb/releases/tag/v0.16
- Fix permissions of the binary file. Fixes
  https://redmine.postgresql.org/issues/7899

* Mon Feb 5 2024 Devrim Gündüz <devrim@gunduz.org> - 0.15-1PGDG
- Update to 0.15

* Fri Sep 8 2023 Devrim Gündüz <devrim@gunduz.org> - 0.13-1PGDG
- Update to 0.13

* Sun Jul 23 2023 Devrim Gündüz <devrim@gunduz.org> - 0.12-1PGDG
- Update to 0.12
- Add PGDG branding

* Mon May 22 2023 Devrim Gündüz <devrim@gunduz.org> - 0.11-1
- Update to 0.11

* Wed Dec 14 2022 Devrim Gündüz <devrim@gunduz.org> - 0.10-1
- Update to 0.10

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 0.9-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon Oct 3 2022 - Devrim Gündüz <devrim@gunduz.org> 0.9.0-1
- Initial packaging for the PostgreSQL RPM repository
