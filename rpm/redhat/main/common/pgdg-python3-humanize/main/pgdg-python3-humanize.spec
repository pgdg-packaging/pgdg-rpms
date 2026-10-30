%pgdg_python3_setup

%global sname humanize

%{expand: %%global pyver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:4])"`)}

%global python3_sitelib %(%{__python3} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

Name:		python%{python3_pkgversion}-%{sname}
Version:	4.16.0
Release:	45PGDG%{?dist}
Summary:	Turns dates in to human readable format, e.g '3 minutes ago'

License:	MIT
URL:		https://github.com/jmoiron/%{sname}
Source0:	https://files.pythonhosted.org/packages/source/h/%{sname}/%{sname}-%{version}.tar.gz
# Upstream computes the version dynamically via hatch-vcs from git metadata,
# which isn't available from this PyPI source tarball. Switch hatchling to
# read the version from the already-baked-in src/humanize/_version.py
# instead (same approach as pgdg-python3-urllib3).
Patch0:		%{sname}-pyproject.toml.patch

BuildArch:	noarch
BuildRequires:	python%{python3_pkgversion}-devel python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-hatchling
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif
Requires:	python%{python3_pkgversion}

%global _description\
This modest package contains various common humanization utilities, like turning\
a number into a fuzzy human readable duration ('3 minutes ago') or into a human\
readable size or throughput.\

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-humanize < %{version}-%{release}
%endif

%description %_description

%prep
%autosetup -n %{sname}-%{version}

# The hatchling we ship for RHEL 9 (1.25) is older than 1.27, and does not support
# the PEP 639 license-files list. Its default license file patterns
# include LICENCE anyway:
%{__sed} -i -e '/^license-files = /d' -e 's/"hatchling>=1.27"/"hatchling"/' pyproject.toml

%if 0%{?suse_version} || 0%{?amzn}
# Classifiers are informational only; drop the Python 3.15 one, which the
# trove-classifiers release of SLES 16 and Amazon Linux 2023 does not know
# yet:
%{__sed} -i '/"Programming Language :: Python :: 3.15"/d' pyproject.toml
%endif

# .gitignore lists src/*/_version.py, which hatch-vcs generates upstream,
# and hatchling 1.25 (RHEL 8, 9 and SLES 15) then leaves it out of the
# wheel, so humanize could not be imported. We ship it from the sdist:
%{__sed} -i '/^src\/\*\/_version\.py$/d' .gitignore
if grep -q '_version' .gitignore; then exit 1; fi

# Remove shebangs from libs.
for lib in src/humanize/time.py src/humanize/filesize.py src/humanize/number.py; do
 sed '1{\@^#!/usr/bin/env python@d}' $lib > $lib.new &&
 touch -r $lib $lib.new && mv $lib.new $lib
done

# Remove .po files
find -name '*.po' -delete

%build
%pyproject_wheel

%install
%pyproject_install

%files
%doc README.md
%license LICENCE
%{python3_sitelib}/%{sname}-%{version}.dist-info/
%{python3_sitelib}/%{sname}/*.py
%{python3_sitelib}/%{sname}/py.typed
%{python3_sitelib}/%{sname}/locale/*
%{python3_sitelib}/%{sname}/__pycache__/*.pyc

%changelog
* Fri Oct 30 2026 Devrim Gunduz <devrim@gunduz.org> - 4.16.0-45PGDG
- Add Amazon Linux 2023 support, for pg_activity. Drop the Python 3.15
  classifier there too: the hatchling of Amazon Linux 2023 rejects it.
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 4.16.0-44PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Tue Oct 27 2026 Devrim Gunduz <devrim@gunduz.org> - 4.16.0-43PGDG
- Ship src/humanize/_version.py: .gitignore lists it, and hatchling 1.25
  (RHEL 8, 9 and SLES 15) left it out of the wheel, so humanize could not
  be imported there.
- Add SLES 15 support (python311), for pg_activity. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/427

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 4.16.0-42PGDG
- Add RHEL 10 support, without EPEL, and obsolete the EPEL python3-humanize
  package there. Start the release from 42, so that our packages win over
  EPEL's. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422
- Add SLES 16 support (python313), for pg_activity. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/427

* Mon Oct 12 2026 Devrim Gunduz <devrim@gunduz.org> - 4.16.0-3PGDG
- Fix build on RHEL 9: remove the PEP 639 license-files list from
  pyproject.toml, which the hatchling there does not support.

* Fri Sep 11 2026 Devrim Gunduz <devrim@gunduz.org> - 4.16.0-2PGDG
- Migrate %%python3_sitelib off the removed distutils.sysconfig module
  to sysconfig.get_path()
- Migrate to pyproject builds.
- Remove Fedora <= 42 support
- Add missing Fedora 44 and Fedora 45 pins

* Mon Aug 31 2026 Devrim Gunduz <devrim@gunduz.org> - 4.16.0-1PGDG
- Update to 4.16.0 per changes described at:
  https://pypi.org/project/humanize/4.16.0/

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 3.13.1-45PGDG
- Fix a pre-existing typo: the sitelib macro was defined as
  "python_sitelib" but %%files referenced "python3_sitelib", so %%files
  was always resolving against the system default python3's
  site-packages rather than this spec's own __ospython-selected
  interpreter. Harmless on Fedora/RHEL/SUSE (where the chosen alt
  version always happens to match the true system default), but would
  have broken on Amazon Linux 2023, where it doesn't.

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 3.13.1-44PGDG
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Mon Oct 6 2025 Devrim Gunduz <devrim@gunduz.org> - 3.13.1-43PGDG
- Use more macros and get rid of pypi_source macro.

* Mon Oct 6 2025 Devrim Gunduz <devrim@gunduz.org> - 3.13.1-42PGDG
- Initial packaging for the PostgreSQL RPM repository to satisfy
  pg_activity dependency. Package is RHEL 8 only.
