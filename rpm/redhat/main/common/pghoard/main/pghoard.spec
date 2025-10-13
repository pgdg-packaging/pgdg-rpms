Summary:	PostgreSQL backup daemon and restore tooling for cloud object storage
Name:		pghoard
Version:	2.6.2
Release:	1PGDG%{?dist}
License:	BSD
Source0:	https://github.com/Aiven-Open/%{name}/archive/refs/tags/%{version}.tar.gz
URL:		https://github.com/Aiven-Open/%{name}
BuildArch:	noarch
BuildRequires:	python3-devel
Requires:	python3-snappy python3-cryptography python3-boto
Requires:	python3-rohmu

%description
pghoard is a PostgreSQL backup daemon and restore tooling for cloud
object storage.

Features:

 * Automatic periodic basebackups
 * Automatic transaction log (WAL/xlog) backups (using either
   pg_receivexlog, archive_command or experimental PG native
   replication protocol support with walreceiver)
 * Cloud object storage support (AWS S3, Google Cloud, OpenStack Swift,
   Azure, Ceph)
 * Backup restoration directly from object storage, compressed and
   encrypted
 * Point-in-time-recovery (PITR)
 * Initialize a new standby from object storage backups, automatically
   configured as a replicating hot-standby

%prep
%setup -q

%build
%{__make}

%install
%{__rm} -rf %{buildroot}
%__python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
sed -e "s@#!/bin/python@#!%{_bindir}/python@" -i %{buildroot}%{_bindir}/*
%{__install} -Dm0644 pghoard.unit %{buildroot}%{_unitdir}/pghoard.service
%{__mkdir_p} %{buildroot}%{_localstatedir}/lib/pghoard

%files
%defattr(-,root,root,-)
%doc README.rst pghoard.json
%attr (755,root,root) %{_bindir}/pghoard*
%attr(0755, postgres, postgres) %{_localstatedir}/lib/pghoard
%{_unitdir}/pghoard.service
%{python3_sitelib}/*
%license LICENSE

%changelog
* Mon Oct 13 2025 Devrim Gündüz <devrim@gunduz.org> - 2.6.2-1PGDG
- Update to 2.6.2

* Tue Feb 20 2024 Devrim Gündüz <devrim@gunduz.org> - 2.5.1-1PGDG
- Update to 2.5.1
- Add PGDG branding

* Mon Jan 23 2023 Devrim Gündüz <devrim@gunduz.org> - 2.2.2a-1
- Update to 2.2.2a

* Tue Nov 2 2021 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-2
- Remove deb-specific part.

* Mon Sep 13 2021 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-1
- Update to 2.2.1

* Thu Mar 11 2021 Devrim Gündüz <devrim@gunduz.org> - 2.1.1-1
- Update to 2.1.1

* Sat Feb 8 2020 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-1
- Update to 2.1.0

* Tue Apr 16 2019 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-1
- Update to 2.0.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-1.1
- Rebuild against PostgreSQL 11.0

* Mon Nov 7 2016 - Devrim Gündüz <devrim@gunduz.org> 1.4.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
