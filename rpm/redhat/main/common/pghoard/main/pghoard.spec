# Amazon Linux 2023: build for Python 3.13, its default python3 (3.9) has no
# hatchling, and rohmu is built for 3.13 there.
%if 0%{?amzn} == 2023
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif

Summary:	PostgreSQL backup daemon and restore tooling for cloud object storage
Name:		pghoard
Version:	2.8.0
Release:	3PGDG%{?dist}
License:	Apache License 2.0
Source0:	https://github.com/Aiven-Open/%{name}/archive/refs/tags/%{version}.tar.gz
Patch0:		pghoard-pyproject.toml.patch
URL:		https://github.com/Aiven-Open/%{name}
BuildArch:	noarch
%if 0%{?amzn} == 2023
Requires:	python%{python3_pkgversion}-rohmu
BuildRequires:	python%{python3_pkgversion}-devel python%{python3_pkgversion}-hatchling
BuildRequires:	python%{python3_pkgversion}-pip
%else
Requires:	python3-snappy python3-cryptography
Requires:	python3-rohmu
%if 0%{?suse_version}
# SUSE does not generate requirements from the Python metadata:
Requires:	python3-packaging python3-psycopg2 python3-pydantic
Requires:	python3-python-dateutil python3-requests python3-systemd
Requires:	python3-zstandard
%endif
BuildRequires:	python3-devel python3-build python3-hatchling python3-pip
%endif
BuildRequires:	systemd-rpm-macros

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif

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
%patch -P 0 -p0
# pghoard reads its version from pghoard/version.py (pghoard.version.__version__),
# which hatch-vcs would generate. Write it here and let hatchling read the
# version from it.
echo "__version__ = '%{version}'" > pghoard/version.py
sed -i -e 's|^path = "pghoard/__init__.py"$|path = "pghoard/version.py"|' -e '/^pattern = "version = /d' pyproject.toml
# Use the distribution names of the packages that provide these modules:
# psycopg2 instead of psycopg2-binary, and systemd-python (python-systemd on
# PyPI is a different project).
sed -i -e 's/"psycopg2-binary /"psycopg2 /' -e 's/^\( *\)"python-systemd",/\1"systemd-python",/' pyproject.toml
# pghoard imports packaging, but does not list it:
sed -i 's/^\( *\)"pydantic",/\1"packaging",\n\1"pydantic",/' pyproject.toml

%build
SETUPTOOLS_SCM_PRETEND_VERSION=%{version} %pyproject_wheel

%install
%pyproject_install

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
* Fri Oct 16 2026 Devrim Gündüz <devrim@gunduz.org> - 2.8.0-3PGDG
- Fix the generated dependencies, which could not be satisfied: require
  psycopg2 instead of psycopg2-binary, and systemd-python instead of
  python-systemd. Add the missing packaging dependency. Remove the
  python3-boto dependency, pghoard does not use boto.
- Write pghoard/version.py, which pghoard imports its version from. The
  version line that was appended to pghoard/__init__.py instead shadowed
  that module, and pghoard failed to start.
- Build for Python 3.13 on Amazon Linux 2023, like rohmu.
- List the requirements on SUSE, which does not generate them from the
  Python metadata.

* Thu Sep 10 2026 Devrim Gündüz <devrim@gunduz.org> - 2.8.0-2PGDG
- Add missing BR

* Thu Jul 30 2026 Devrim Gündüz <devrim@gunduz.org> - 2.8.0-1PGDG
- Update to 2.8.0 per changes described at:
  https://github.com/Aiven-Open/pghoard/releases/tag/2.8.0

* Wed Jun 17 2026 Devrim Gündüz <devrim@gunduz.org> - 2.7.2-1PGDG
- Update to 2.7.2 per changes described at:
  https://github.com/Aiven-Open/pghoard/releases/tag/2.7.2
  https://github.com/Aiven-Open/pghoard/releases/tag/2.7.1
  Fixes CVE-2026-54711 and CVE-2026-63120

* Wed Jun 17 2026 Devrim Gündüz <devrim@gunduz.org> - 2.7.0-1PGDG
- Update to 2.7.0
- Switch to pyproject builds

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
