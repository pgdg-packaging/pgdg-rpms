%if 0%{?fedora} && 0%{?fedora} == 45
%global __ospython %{_bindir}/python3.15
%global python3_pkgversion 3.15
%endif
%if 0%{?fedora} && 0%{?fedora} <= 44
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?suse_version} == 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
# Build the python311 flavor with the SUSE pyproject macros, instead of
# the default python3 (3.6):
%global	pythons python311
%global	python3_sitearch %{_libdir}/python3.11/site-packages
%endif
%if 0%{?suse_version} == 1600
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif
%global sname pglast

Name:		pglast
Version:	8.5
Release:	1PGDG%{?dist}
Summary:	PostgreSQL Languages AST and statements prettifier
License:	GPLv3+
Url:		https://github.com/lelit/%{sname}
# The GitHub tag archive does not include the libpg_query git submodule
# content that this package needs to build against, so we use the PyPI
# sdist instead, which bundles a private copy of the libpg_query sources.
Source0:	https://files.pythonhosted.org/packages/source/p/%{sname}/%{sname}-%{version}.tar.gz
# The pglast 8.x sdists miss the upb generated protobuf files and the upb
# port headers of the bundled libpg_query, as MANIFEST.in still lists the
# old protobuf-c files. Take them from the libpg_query release that the
# bundled copy is based on (pg_query.proto and upb are the same).
%global	pgqversion 18.1.0
Source1:	https://github.com/pganalyze/libpg_query/archive/refs/tags/%{pgqversion}.tar.gz#/libpg_query-%{pgqversion}.tar.gz
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

BuildRequires:	gcc libpg_query make

%description
pglast is a Python module able to parse PostgreSQL's SQL statements
and return their Abstract Syntax Tree, exposing it as a nested
structure of dataclass-like Python objects.

It builds on the low level PostgreSQL query parser extracted from the
actual PostgreSQL server source code (bundled here as libpg_query),
and can be used to programmatically inspect, rewrite or prettify SQL
code, as well as building tools such as pgspot.

%prep
%setup -q -n %{sname}-%{version} -a 1
# Only add the missing files, do not overwrite the bundled ones:
%{__cp} -rn libpg_query-%{pgqversion}/protobuf libpg_query-%{pgqversion}/vendor libpg_query/
%{__rm} -rf libpg_query-%{pgqversion}
# Upstream declares license as a bare PEP 639 SPDX string, which the
# setuptools shipped on RHEL 9/10 and Leap 16 is too old to validate
# ("project.license must be valid exactly by one definition"). Rewrite
# it to the older PEP 621 {text = ...} form, which every setuptools in
# our build matrix accepts.
sed -i 's/^license = "GPL-3.0-or-later"$/license = {text = "GPL-3.0-or-later"}/' pyproject.toml

%build
%pyproject_wheel

%install
%pyproject_install

%files
%defattr(-,root,root,0755)
%doc README.rst CHANGES.rst
%{_bindir}/pgpp
%{python3_sitearch}/%{sname}/
%{python3_sitearch}/%{sname}-%{version}.dist-info/

%changelog
* Sun Oct 18 2026 Devrim Gündüz <devrim@gunduz.org> - 8.5-1PGDG
- Update to 8.5, which targets the PostgreSQL 18 parser, per changes
  described at https://github.com/lelit/pglast/blob/v8/CHANGES.rst .
  pgspot 0.9.3 requires it.
- Add the upb generated protobuf files and the upb port headers that the
  sdist misses from the libpg_query 18.1.0 tarball, so that the bundled
  libpg_query builds.

* Sun Oct 11 2026 Devrim Gunduz <devrim@gunduz.org> - 7.11-2PGDG
- Build the python311 flavor on SLES 15. The SUSE pyproject macros built
  for the default python3 (3.6), so the build failed there. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226
- Set python3_sitearch to the python3.11 one on SLES 15, too: the SUSE macro
  points to the default python3 (3.6).

* Wed Sep 16 2026 Devrim Gunduz <devrim@gunduz.org> - 7.11-1PGDG
- Initial packaging for the PostgreSQL RPM repository
