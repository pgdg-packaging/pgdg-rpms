%global sname humanize

%if 0%{?fedora} && 0%{?fedora} == 45
%global __ospython %{_bindir}/python3.15
%global python3_pkgversion 3.15
%endif
%if 0%{?fedora} && 0%{?fedora} <= 43
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?suse_version} == 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}

%global python3_sitelib %(%{__ospython} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

Name:		python%{python3_pkgversion}-%{sname}
Version:	4.16.0
Release:	2PGDG%{?dist}
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

%description %_description

%prep
%autosetup -n %{sname}-%{version}

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
