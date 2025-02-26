pgdg-mock-configs
=================

mock is a 'simple' chroot build environment manager for building RPMs: https://github.com/rpm-software-management/mock

This package includes mock configuration files for the PGDG RPM packages.

Usage:
------

- Building package on Fedora 41 and against PostgreSQL 17: sudo mock -r pgdg-fedora-41-pg17-x86_64 package.src.rpm
- Building package on Rocky 9 and against PostgreSQL 16: sudo mock -r pgdg-rocky-9-pg16-x86_64 package.src.rpm

