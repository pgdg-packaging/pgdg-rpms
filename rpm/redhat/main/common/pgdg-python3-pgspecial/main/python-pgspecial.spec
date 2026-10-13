%global sname pgspecial

%if 0%{?fedora} && 0%{?fedora} == 45
%global python3_pkgversion 3.15
%endif
%if 0%{?fedora} && 0%{?fedora} <= 44
%global python3_pkgversion 3.14
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global python3_pkgversion 3.12
%endif
%if 0%{?amzn} == 2023
%global __python3 %{_bindir}/python3.13
%global python3_pkgversion 3.13
%endif
%if 0%{?suse_version} == 1500
%global python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global python3_pkgversion 313
%endif

# SUSE only generates runtime Requires from the Python metadata when asked
# to; Fedora and RHEL do it by default.
%{?python_enable_dependency_generator}

Name:		python%{python3_pkgversion}-%{sname}
Version:	2.2.1
Release:	4PGDG%{?dist}
Epoch:		1
Summary:	Meta-commands handler for Postgres Database.

License:	BSD
URL:		https://pypi.python.org/pypi/pgspecial
Source0:	https://files.pythonhosted.org/packages/source/%(n=%{sname}; echo ${n:0:1})/%{sname}/%{sname}-%{version}.tar.gz

%if 0%{?fedora} || 0%{?rhel} == 10 || 0%{?suse_version} == 1600
# Up to 1:2.2.1-3 this package was named python3-pgspecial. On these
# platforms python3 is the same Python as above, so the old package installs
# the same files; replace it on upgrade.
Obsoletes:	python3-%{sname} < 1:2.2.1-4
%endif

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
# SUSE's Python dependency generators. python3-devel pulls this in, but
# python%%{python3_pkgversion}-devel does not.
BuildRequires:	python-rpm-packaging
%else
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-setuptools_scm
BuildRequires:	python%{python3_pkgversion}-wheel

BuildArch:	noarch

%description
This package provides an API to execute meta-commands (AKA “special”,
or “backslash commands”) on PostgreSQL.

%prep
%setup -q -n %{sname}-%{version}

%build
SETUPTOOLS_SCM_PRETEND_VERSION=%{version} %pyproject_wheel

%install
%pyproject_install

%files
%license License.txt
%doc README.rst
%{python3_sitelib}/%{sname}-%{version}.dist-info/
%{python3_sitelib}/%{sname}/

%changelog
* Wed Sep 23 2026 Devrim Gündüz <devrim@gunduz.org> - 1:2.2.1-4PGDG
- Enable the Python dependency generator, so that the runtime Requires
  (click, sqlparse, psycopg) are also generated on SUSE.
- Add missing python3-wheel BR, needed by the setuptools on RHEL 10.
- Rename package to python%%{python3_pkgversion}-pgspecial, using the same
  Python version mapping as pgcli, and obsolete python3-pgspecial where
  that is the same Python. Drop the local %%python3_sitelib override.
- BuildRequire python-rpm-packaging on SUSE, which python313-devel does
  not pull in, so that the Python dependency generators run there.

* Mon Sep 14 2026 Devrim Gündüz <devrim@gunduz.org> - 1:2.2.1-3PGDG
- Migrate %%python3_sitelib off the removed distutils.sysconfig module to
  sysconfig.get_path() (distutils is gone on Python 3.12+, e.g. Fedora's
  default python3.14)
- Switch to pyproject builds.
- Add SLES 16 support.

* Mon Aug 31 2026 Devrim Gündüz <devrim@gunduz.org> - 1:2.2.1-1PGDG
- Update to 2.2.1 per changes described at:
  https://pypi.org/project/pgspecial/2.2.1/

* Wed Dec 18 2024 Devrim Gündüz <devrim@gunduz.org> - 1:2.0.1-2PGDG
- Add RHEL 10 support
- Add PGDG branding

* Fri Sep 16 2022 Devrim Gündüz <devrim@gunduz.org> - 1:2.0.1-1
- Update to 2.0.1

* Thu Mar 11 2021 Devrim Gündüz <devrim@gunduz.org> - 1:1.12.1-1
- Update to 1.12.1
- Remove PY2 stuff.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1:1.8.0-1.1
- Rebuild against PostgreSQL 11.0

* Tue Jun 6 2017 Devrim Gündüz <devrim@gunduz.org> - 1:1.8.0-1
- Initial packaging for PostgreSQL YUM repo, to satisfy pgcli dependency.
