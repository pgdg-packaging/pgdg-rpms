%pgdg_python3_setup

# Disable internal dependency generator.
# We will specify dependencies in the spec file.
%{?python_disable_dependency_generator}

%global debug_package %{nil}

Summary:	BigQuery Foreign Data Wrapper for PostgreSQL
Name:		bigquery_fdw
Version:	2.0
Release:	16PGDG%{?dist}
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
# interpreter that multicorn2 embeds. google-auth comes with them. Only the
# packages of that tree provide the pgdg-python3.X-<module> names (on SUSE,
# they are the package names); the distribution's python3.X-<module>
# packages may satisfy versioned Requires on the usual names with an Epoch:
Requires:	pgdg-python%{python3_pkgversion}-google-cloud-bigquery >= 3.46.1

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
import os as _os
import sys as _sys
_pgdg_sitelib = '/usr/lib/pgdg-python/python%d.%d/site-packages' % _sys.version_info[:2]
if _pgdg_sitelib not in _sys.path:
    _sys.path.insert(0, _pgdg_sitelib)
# setuptools "-nspkg.pth" files of the system packages (e.g. those of
# protobuf and google-cloud-core) may have created these namespace packages
# at startup, with a path that only has the directory of that .pth file,
# and that is not recalculated, as the private "google" is a regular
# package. Set their path to the private tree first, then the directories
# of all sys.path entries (e.g. /usr/lib64 and /usr/lib, where the system
# google-auth is), as pkgutil.extend_path() would:
for _name in ('google', 'google.cloud'):
    _mod = _sys.modules.get(_name)
    _dir = _os.path.join(_pgdg_sitelib, *_name.split('.'))
    if _mod is None or not _os.path.isdir(_dir):
        continue
    _path = [_dir]
    for _p in ([_os.path.join(_e, *_name.split('.')) for _e in _sys.path
                if isinstance(_e, str)] + list(getattr(_mod, '__path__', []))):
        if _p not in _path and _os.path.isdir(_p):
            _path.append(_p)
    _mod.__path__ = _path
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
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0-16PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Thu Oct 15 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0-15PGDG
- Fix "cannot import name 'bigquery' from 'google.cloud'" on Fedora and
  RHEL 10, when the distribution's Google Cloud packages are installed:
  their -nspkg.pth files create the google and google.cloud namespace
  packages at startup, and __init__.py did not add the private tree to
  their path in all cases.
- Require pgdg-python3.X-google-cloud-bigquery, which only the private
  tree provides, so that the distribution's packages (some have an Epoch)
  do not satisfy the dependencies of the stack. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/367

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
