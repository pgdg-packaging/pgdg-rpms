%pgdg_python3_setup

%global pypi_name attrs
%global sname attr
%{expand: %%global pyver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%global python3_sitelib %(%{__python3} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

Name:		python%{python3_pkgversion}-attrs
Version:	26.1.0
Release:	3PGDG%{?dist}
Summary:	Python attributes without boilerplate

License:	MIT
URL:		https://www.attrs.org/
BuildArch:	noarch
Source0:	https://github.com/python-attrs/%{pypi_name}/archive/refs/tags/%{version}.tar.gz

BuildRequires:	python%{python3_pkgversion}-devel python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-hatchling python%{python3_pkgversion}-hatch-vcs
BuildRequires:	python%{python3_pkgversion}-hatch-fancy-pypi-readme
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif
Requires:	python%{python3_pkgversion}

%description
attrs is an MIT-licensed Python package with class decorators that
ease the chores of implementing the most common attribute-related
object protocols.

%prep
%setup -q -n %{pypi_name}-%{version}
# The PEP 639 license-files list needs hatchling 1.27; RHEL 8 and 9 have our
# 1.25 (see python3.12-hatchling). Its default license file patterns pick
# up the same file:
%{__sed} -i '/^license-files = \["LICENSE"\]$/d' pyproject.toml
if grep -q '^license-files' pyproject.toml; then exit 1; fi

%build
# There is no git metadata in the tarball for hatch-vcs:
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/%{pypi_name}-%{version}.dist-info/
%{python3_sitelib}/%{sname}/*.py*
%{python3_sitelib}/%{sname}/py.typed
%{python3_sitelib}/%{sname}/__pycache__/*.pyc
%{python3_sitelib}/%{pypi_name}/*.py*
%{python3_sitelib}/%{pypi_name}/py.typed
%{python3_sitelib}/%{pypi_name}/__pycache__/*.pyc

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 26.1.0-3PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Fri Sep 11 2026 Devrim Gunduz <devrim@gunduz.org> - 26.1.0-2PGDG
- Migrate %%python3_sitelib off the removed distutils.sysconfig module
  to sysconfig.get_path()
- Switch to pyproject builds
- Remove Fedora <= 42 support
- Add missing Fedora 44 pin (python3.14)
- Remove the PEP 639 license-files list from pyproject.toml, which needs
  hatchling 1.27: RHEL 8 and 9 have 1.25. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
- Add Amazon Linux 2023 support (python3.13), for nagios-plugins-patroni.
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/427

* Mon Aug 31 2026 Devrim Gunduz <devrim@gunduz.org> - 26.1.0-1PGDG
- Update to 26.1.0 per changes described at:
  https://github.com/python-attrs/attrs/releases/tag/26.1.0

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 22.1.0-44PGDG
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Tue Jun 2 2026 Devrim Gunduz <devrim@gunduz.org> - 22.1.0-43PGDG
- Update URL in attempt to fix
  https://github.com/pgdg-packaging/pgdg-rpms/issues/202

* Mon Oct 6 2025 Devrim Gunduz <devrim@gunduz.org> - 22.1.0-42PGDG
- Initial packaging for the PostgreSQL RPM repository to satisfy
  pg_activity dependency. Package is for RHEL 8 only.
