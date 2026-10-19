%define		_build_id_links none
%global		debug_package %{nil}
%global		_missing_build_ids_terminate_build 0

# Upstream ships binaries for x86_64 and aarch64 only.
ExcludeArch:	ppc64le

%ifarch x86_64
%global		tarballarch amd64
%endif
%ifarch aarch64
%global		tarballarch aarch64
%endif

# The binaries are built on Ubuntu 24.04 and need glibc >= 2.34.
%global		ubuntuver 24.04

Name:		wal-g
Version:	3.0.9
Release:	1PGDG%{?dist}
Summary:	Archival and restoration tool for PostgreSQL
License:	Apache-2.0
URL:		https://github.com/%{name}/%{name}
Source0:	https://github.com/%{name}/%{name}/releases/download/v%{version}/%{name}-pg-%{ubuntuver}-%{tarballarch}.tar.gz
Source1:	https://raw.githubusercontent.com/%{name}/%{name}/v%{version}/LICENSE.md

%description
WAL-G is an archival and restoration tool for PostgreSQL. It takes base
backups and archives WAL files to cloud object storage (Amazon S3 and
compatible storage, Google Cloud Storage, Azure Blob Storage, Swift),
to SSH servers or to a file system, and restores them. It supports
compression (LZ4, LZMA, Zstandard, Brotli), encryption (libsodium,
OpenPGP), delta backups, parallel backup and WAL operations, backups
from standby servers, and point-in-time recovery.

This package contains the PostgreSQL build of WAL-G.

%prep
%setup -q -c -T
%{__tar} xzf %{SOURCE0}
%{__cp} %{SOURCE1} .

%build

%install
%{__install} -m 0755 -D %{name}-pg-%{ubuntuver}-%{tarballarch} %{buildroot}%{_bindir}/%{name}

%files
%defattr(-,root,root,-)
%license LICENSE.md
%attr(755, root, root) %{_bindir}/%{name}

%changelog
* Mon Oct 19 2026 Devrim Gündüz <devrim@gunduz.org> - 3.0.9-1PGDG
- Initial packaging for the PostgreSQL RPM repository.
