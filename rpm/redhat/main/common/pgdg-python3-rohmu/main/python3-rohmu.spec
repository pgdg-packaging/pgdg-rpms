# Amazon Linux 2023: build for Python 3.13, its default python3 (3.9) has no
# hatchling, and the Python 3.13 packages of the storage backends' modules
# are in the PGDG repository.
%if 0%{?amzn} == 2023
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif

%global python3_sitelib %(%{__python3} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

%global sname rohmu

%if 0%{?amzn} == 2023
Name:		python%{python3_pkgversion}-%{sname}
%else
Name:		python3-%{sname}
%endif
Version:	2.8.2
Release:	5PGDG%{?dist}
Epoch:		1
Summary:	Python library for building backup tools for databases

License:	Apache 2.0
URL:		https://github.com/aiven/%{sname}
Source0:	https://github.com/aiven/%{sname}/archive/refs/tags/releases/%{version}.tar.gz

%if 0%{?amzn} == 2023
BuildRequires:	python%{python3_pkgversion}-devel python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-hatchling python%{python3_pkgversion}-hatch-vcs
%else
BuildRequires:	python3-devel python3-pip python3-hatchling python3-hatch-vcs
%endif
%if 0%{?suse_version}
# SUSE has no pyproject-rpm-macros; its pyproject macros are in
# python-rpm-macros, and its Python dependency generators in
# python-rpm-packaging:
BuildRequires:	python-rpm-macros python-rpm-packaging
%else
BuildRequires:	pyproject-rpm-macros
%endif

%if 0%{?amzn} == 2023
# The modules that only the Google Cloud storage backend needs are weak
# dependencies (see %%prep): google-api-python-client pulls in the private
# PGDG Python tree with its google-api-core. It is installed there, so it
# has no python3.13dist() provide:
Recommends:	pgdg-python%{python3_pkgversion}-google-api-python-client >= 2.201.0
Recommends:	python%{python3_pkgversion}-oauth2client
Recommends:	python%{python3_pkgversion}-httplib2
%endif
%if 0%{?suse_version}
# SUSE does not generate requirements from the Python metadata, so list
# them. Use the pythonX.Ydist() names, which both SUSE's and our packages of
# the same module provide (e.g. our python313-systemd, which patroni needs,
# does not provide SUSE's python3-<module> names):
Requires:	python%{python3_version}dist(cryptography)
Requires:	python%{python3_version}dist(pydantic)
Requires:	python%{python3_version}dist(python-dateutil)
Requires:	python%{python3_version}dist(requests)
Requires:	python%{python3_version}dist(typing-extensions)
Requires:	python%{python3_version}dist(zstandard)
%endif
%if ! 0%{?amzn}
# The modules of the storage backends are weak dependencies (see %%prep):
# rohmu only imports them when that backend is used, and the distributions
# do not have all of them (e.g. EPEL 9 has no azure-storage-blob,
# google-api-python-client and swiftclient, SUSE no azure-storage-blob,
# oauth2client and swiftclient).
Recommends:	python%{python3_version}dist(azure-common)
Recommends:	python%{python3_version}dist(azure-storage-blob)
Recommends:	python%{python3_version}dist(botocore)
Recommends:	python%{python3_version}dist(google-api-python-client)
Recommends:	python%{python3_version}dist(httplib2)
Recommends:	python%{python3_version}dist(oauth2client)
Recommends:	python%{python3_version}dist(paramiko)
Recommends:	python%{python3_version}dist(python-snappy)
Recommends:	python%{python3_version}dist(python-swiftclient)
%endif
BuildArch:	noarch

%description
Rohmu is a Python library for building backup tools for databases providing
functionality for compression, encryption and transferring data between the
database and an object storage. Rohmu supports main public clouds such as
GCP, AWS and Azure for backup storage. Rohmu is used in various backup tools
such as PGHhoard for PostgreSQL, MyHoard for MySQL and Astacus for M3 and
ClickHouse and other databases.

%prep
%setup -q -n %{sname}-releases-%{version}
# This GitHub tag-archive source has no git metadata for hatch-vcs to
# derive a version from; switch [tool.hatch.version] to hatchling's
# built-in "env" source instead, read from PGDG_PACKAGE_VERSION below
sed -i 's/^source = "vcs"$/source = "env"\nvariable = "PGDG_PACKAGE_VERSION"/' pyproject.toml
# rohmu imports typing_extensions on every Python version, but only requires
# it before Python 3.12:
sed -i "s/^\( *\)\"typing_extensions; python_version<'3.12'\",/\1\"typing_extensions\",/" pyproject.toml
# The pydantic.v1 of pydantic < 2.13 cannot infer the types of fields with
# defaults on Python 3.14, where annotations are evaluated lazily (e.g.
# Fedora 43 and 44, with pydantic 2.12). The other modules that define
# models already use postponed (string) annotations; do it in this one, too:
sed -i '1a from __future__ import annotations' rohmu/common/models.py
grep -q '^from __future__ import annotations' rohmu/common/models.py
%if ! 0%{?amzn} && ! 0%{?suse_version}
# Make the modules of the storage backends weak dependencies (Recommends
# above) instead of generated requirements:
sed -i -E '/^ *"(azure-common|azure-storage-blob|botocore|google-api-python-client|httplib2|oauth2client|paramiko|python-snappy|python-swiftclient)[ ",]/d' pyproject.toml
%endif
%if 0%{?rhel} == 9
# EPEL 9 has pydantic 1.10.14, which is the v1 API itself: the pydantic.v1
# namespace rohmu imports was added in 1.10.17. Import pydantic there, and
# require a 1.x version:
sed -i 's/^\( *\)"pydantic >= 1.10.17",/\1"pydantic >= 1.10.14, < 2",/' pyproject.toml
grep -q '"pydantic >= 1.10.14, < 2"' pyproject.toml
sed -i -e 's/^import pydantic\.v1 as pyd$/import pydantic as pyd/' -e 's/^from pydantic\.v1 import /from pydantic import /' \
	rohmu/common/models.py rohmu/common/statsd.py rohmu/delta/common.py rohmu/object_storage/config.py
! grep -rq 'pydantic\.v1' rohmu
%endif
%if 0%{?amzn} == 2023
# google-api-python-client needs a newer google-api-core than the
# distribution has. On Amazon Linux 2023 both are in the private PGDG Python
# tree, which also holds the bigquery_fdw stack. Make the modules that only
# the Google Cloud backend imports weak dependencies (Recommends above)
# instead of generated requirements, and make that backend add the private
# tree to sys.path before it imports googleapiclient:
sed -i -E '/^ *"(google-api-python-client|oauth2client|httplib2)",$/d' pyproject.toml
%{__cat} > rohmu/object_storage/_pgdg_google_path.py << 'EOF'
# Added by the PGDG RPM packaging: google-api-python-client and the
# google-api-core it needs are in the private PGDG Python tree.
import os as _os
import sys as _sys

_pgdg_sitelib = "/usr/lib/pgdg-python/python%%d.%%d/site-packages" %% _sys.version_info[:2]
if _pgdg_sitelib not in _sys.path:
    _sys.path.insert(0, _pgdg_sitelib)
import google as _google  # noqa: E402

# "google" is a namespace package, and its parts are in both trees (e.g.
# google.auth in the system site-packages, google.api_core in the private
# one). Its path may have been computed before the private tree was added,
# so recompute it, private tree first:
_path = []
for _p in [_os.path.join(_e, "google") for _e in _sys.path if isinstance(_e, str)] + list(
    getattr(_google, "__path__", [])
):
    if _p not in _path and _os.path.isdir(_p):
        _path.append(_p)
_google.__path__ = _path
EOF
sed -i 's/^from __future__ import annotations$/&\n\nfrom rohmu.object_storage import _pgdg_google_path  # noqa: F401  # PGDG: private tree/' rohmu/object_storage/google.py
grep -q '_pgdg_google_path' rohmu/object_storage/google.py
%endif

%build
export PGDG_PACKAGE_VERSION=%{version}
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sname}-%{version}.dist-info/
%{python3_sitelib}/%{sname}/

%changelog
* Fri Oct 16 2026 Devrim Gündüz <devrim@gunduz.org> - 1:2.8.2-5PGDG
- Make the modules of the storage backends weak dependencies on all
  distributions but Amazon Linux 2023: they do not all exist there (EPEL
  has no azure-storage-blob, google-api-python-client and swiftclient for
  RHEL 9, for instance), and rohmu only imports them when that backend is
  used. Do not require azure-storage-blob any more.
- On SUSE, require the pythonX.Ydist() names, which both SUSE's and our
  packages provide.
- Use the pydantic 1.10.14 of EPEL 9 on RHEL 9: it has no pydantic.v1
  namespace, but is the v1 API itself.
- Use postponed annotations in rohmu/common/models.py, like in rohmu's
  other modules with pydantic models: rohmu failed to start on Python 3.14
  with pydantic < 2.13 (Fedora 43 and 44).

* Fri Oct 16 2026 Devrim Gündüz <devrim@gunduz.org> - 1:2.8.2-4PGDG
- Build for Python 3.13 on Amazon Linux 2023 (python3.13-rohmu), whose
  default python3 has no hatchling. The Python 3.13 packages of the cloud
  storage SDKs are new in the PGDG repository there; google-api-python-client
  is installed into the private PGDG Python tree, with the google-api-core
  it needs, and the Google Cloud backend adds that tree to sys.path. The
  modules that only that backend needs are weak dependencies there.
- Stop building on RHEL 8 and SLES 15: their python3 (3.6) has no
  hatchling either, and rohmu needs Python >= 3.8.
- Require typing_extensions on all Python versions, rohmu imports it
  unconditionally.
- BuildRequire python-rpm-macros and python-rpm-packaging on SUSE, which
  has no pyproject-rpm-macros.
- List the requirements on SUSE, which does not generate them from the
  Python metadata: the core ones as Requires, the modules of the storage
  backends as Recommends. Do not require azure-storage-blob there, SUSE
  does not have it.

* Mon Sep 14 2026 Devrim Gündüz <devrim@gunduz.org> - 1:2.8.2-3PGDG
- Migrate %%python3_sitelib off the removed distutils.sysconfig module to
  sysconfig.get_path() (distutils is gone on Python 3.12+, e.g. Fedora's
  default python3.14)
- Switch to pyproject builds.

* Mon Aug 31 2026 Devrim Gündüz <devrim@gunduz.org> - 1:2.8.2-1PGDG
- Update to 2.8.2 per changes described at:
  https://github.com/aiven/rohmu/releases/tag/releases/2.8.2

* Tue Dec 17 2024 Devrim Gündüz <devrim@gunduz.org> - 1:1.0.9-2PGDG
- Add RHEL 10 support
- Add PGDG branding

* Mon Jan 23 2023 Devrim Gündüz <devrim@gunduz.org> - 1:1.0.9-1
- Initial packaging for PostgreSQL YUM repo, to satisfy pghoard dependency.
