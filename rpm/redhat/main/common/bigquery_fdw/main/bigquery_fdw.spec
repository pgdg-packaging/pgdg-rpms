# Disable internal dependency generator.
# We will specify dependencies in the spec file.
%{?python_disable_dependency_generator}

%if 0%{?fedora} && 0%{?fedora} == 45
%global __python3 %{_bindir}/python3.15
%global python3_pkgversion 3.15
%endif
%if 0%{?fedora} && 0%{?fedora} <= 44
%global __python3 %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__python3 %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?amzn} == 2023
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?suse_version} == 1500
%global	__python3 %{_bindir}/python3.11
%global	python3_pkgversion 311
# Build the python311 flavor with the SUSE pyproject macros, instead of
# the default python3 (3.6):
%global	pythons python311
%global	python3_sitelib %{_prefix}/lib/python3.11/site-packages
%endif
%if 0%{?suse_version} == 1600
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

%global debug_package %{nil}

Summary:	BigQuery Foreign Data Wrapper for PostgreSQL
Name:		bigquery_fdw
Version:	2.0
Release:	14PGDG%{?dist}
# The exceptions allow linking to OpenSSL and PostgreSQL's libpq
License:	LGPLv3+ with exceptions
Url:		https://github.com/gabfl/%{name}/
Source0:	https://github.com/gabfl/%{name}/archive/%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-packaging
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%endif
%if ! 0%{?suse_version} && 0%{?rhel} != 8
BuildRequires:	pyproject-rpm-macros
%endif

Requires:	multicorn2
# The Google Cloud libraries live in the private PGDG Python tree, for the
# interpreter that multicorn2 embeds. google-auth comes with them:
%if 0%{?suse_version}
# On SUSE, the private stack has distinct package names, as SUSE ships
# older copies of these modules under the usual ones:
Requires:	pgdg-python%{python3_pkgversion}-google-cloud-bigquery >= 3.46.1
%else
Requires:	python%{python3_pkgversion}-google-cloud-bigquery >= 3.46.1
%endif

%description
bigquery_fdw is a BigQuery foreign data wrapper for PostgreSQL using
Multicorn2.

It allows to write queries in PostgreSQL SQL syntax using a foreign table. It
supports most of BigQuery's data types and operators.

%prep
%setup -q -n %{name}-%{version}
# Make bigquery_fdw use the private PGDG Python tree, which has the Google
# Cloud libraries it needs, ahead of the system site-packages. The package
# is always imported before its submodules, both by multicorn2 and by
# bq_client_test. Upstream's __init__.py is empty:
test ! -s src/__init__.py
%{__cat} > src/__init__.py << 'EOF'
# Added by the PGDG RPM packaging: use the private PGDG Python tree, which
# has the Google Cloud libraries bigquery_fdw needs.
import importlib as _importlib
import os as _os
import sys as _sys
_pgdg_sitelib = '/usr/lib/pgdg-python/python%d.%d/site-packages' % _sys.version_info[:2]
if _pgdg_sitelib not in _sys.path:
    _sys.path.insert(0, _pgdg_sitelib)
# A setuptools "-nspkg.pth" file (e.g. that of an older system protobuf)
# may have created these namespace packages at startup, with a fixed path
# that does not include the private tree:
for _name in ('google', 'google.cloud'):
    _mod = _sys.modules.get(_name)
    _dir = _os.path.join(_pgdg_sitelib, *_name.split('.'))
    if (_mod is None or not _os.path.isdir(_dir)
            or _dir in list(getattr(_mod, '__path__', []))):
        continue
    if isinstance(_mod.__path__, list):
        _mod.__path__.insert(0, _dir)
    elif not any(_k.startswith(_name + '.') for _k in _sys.modules):
        # Nothing was imported from it yet, so re-create it from sys.path:
        del _sys.modules[_name]
        _importlib.import_module(_name)
EOF

%build
# Change /usr/bin/python to /usr/bin/python2 in the scripts:
for i in `find . -iname "*.py"`; do sed -i "s/\/usr\/bin\/env python/\/usr\/bin\/env python3/g" $i; done
%if 0%{?rhel} == 8
# There are no pyproject-rpm-macros on RHEL 8:
%{__python3} -m pip wheel --no-deps --no-build-isolation --no-index \
	--disable-pip-version-check -w pgdg-dist .
%else
%pyproject_wheel
%endif

%install
%if 0%{?rhel} == 8
%{__python3} -m pip install --no-deps --no-index --no-compile \
	--disable-pip-version-check --ignore-installed \
	--root %{buildroot} --prefix %{_prefix} pgdg-dist/*.whl
%{__rm} -f %{buildroot}%{python3_sitelib}/*.dist-info/direct_url.json
echo rpm > $(echo %{buildroot}%{python3_sitelib}/*.dist-info)/INSTALLER
%else
%pyproject_install
%endif

%files
%defattr(-,root,root)
%doc docs/ README.md
%license LICENSE
%{_bindir}/bq_client_test
%{python3_sitelib}/%{name}/*.py
%{python3_sitelib}/%{name}/__pycache__/*.pyc
%{python3_sitelib}/%{name}-%{version}.dist-info

%changelog
* Tue Oct 13 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0-14PGDG
- Use the new private Python stack (google-cloud-bigquery 3.46.1 and its
  dependencies, in /usr/lib/pgdg-python), built for the interpreter that
  multicorn2 embeds. The python3-google-* packages were built for the
  default python3, which bigquery_fdw could not import on most distros.
- Drop the dependency on google-oauthlib, which bigquery_fdw does not use.
- Build with pip on RHEL 8, which has no pyproject-rpm-macros.
- Per https://github.com/pgdg-packaging/pgdg-rpms/issues/367

* Sun Oct 11 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0-13PGDG
- Build the python311 flavor on SLES 15. The SUSE pyproject macros built
  for the default python3 (3.6), so the build failed there. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226
- Set python3_sitelib to the python3.11 one on SLES 15, too: the SUSE macro
  points to the default python3 (3.6).

* Mon Sep 14 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0-12PGDG
- Refresh the stale, hardcoded exact-version Requires on
  python3-google-auth (was = 1.14.3), python3-google-oauthlib (was =
  0.4.1) and python3-google-cloud-bigquery (was = 1.24) 
- Switch to pyproject builds.
- Enable pycache everywhere
- Remove Fedora <= 42 support

* Thu Sep 10 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0-10PGDG
- Add missing BR

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0-9PGDG
- Also set __python3 (not just __ospython) for Amazon Linux 2023, so
  %pyproject_wheel/%pyproject_install actually build against python3.13
  instead of silently falling back to the system default python3
  (__ospython only affects this repo's own macro computations, not
  RPM's own pyproject/site-packages macros).

* Tue Aug 25 2026 Devrim Gündüz <devrim@gunduz.org> - 2.0-8PGDG
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Thu May 7 2026 Devrim Gündüz <devrim@gunduz.org> - 2.0-7PGDG
- Add missing BR

* Tue Apr 28 2026 Devrim Gündüz <devrim@gunduz.org> - 2.0-6PGDG
- Use Python 3.14 on Fedora 44. Many BRs and Requires are not ready
  for 3.15.

* Tue Apr 28 2026 Devrim Gündüz <devrim@gunduz.org> - 2.0-5PGDG
- Switch to pyproject builds
- Add Fedora 44 support

* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 2.0-4PGDG
- Use multicorn2 instead of deprecated multicorn package.
- Add SLES 16 support

* Sun Mar 9 2025 Devrim Gündüz <devrim@gunduz.org> - 2.0-3PGDG
- Add RHEL 10 dependency
- Remove redundant BR

* Fri Feb 16 2024 Devrim Gündüz <devrim@gunduz.org> - 2.0-2PGDG
- Fix SLES 15 builds
- Add PGDG branding
- Fix rpmlint warning

* Tue Dec 6 2022 Devrim Gündüz <devrim@gunduz.org> - 2.0-1
- Update to 2.0

* Tue Dec 6 2022 Devrim Gündüz <devrim@gunduz.org> - 1.6-3
- Remove Advance Toolchain support from RHEL 7 - ppc64le.

* Mon Mar 28 2022 Devrim Gündüz <devrim@gunduz.org> - 1.6-2
- Add Fedora 35+ support.

* Mon May 18 2020 Devrim Gündüz <devrim@gunduz.org> - 1.6-1
- Update to 1.6

* Mon May 4 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.2-1
- Initial packaging for PostgreSQL YUM repository
