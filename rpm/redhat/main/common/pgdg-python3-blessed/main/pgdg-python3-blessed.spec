%global	sname blessed

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
%global	python3_pkgversion 3.13
%endif
%if 0%{?suse_version} == 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
# Build the python311 flavor with the SUSE pyproject macros, instead of
# the default python3 (3.6):
%global	pythons python311
%endif
%if 0%{?suse_version} == 1600
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%global python3_sitelib %(%{__ospython} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

Name:		python%{python3_pkgversion}-%{sname}
Version:	1.39.0
Release:	3PGDG%{?dist}
Summary:	Easy, practical library for making terminal apps, by providing an elegant, well- documented interface to Colors, Keyboard input, and screen Positioning capabilities

License:	MIT
URL:		https://github.com/jquast/%{sname}
Source0:	https://files.pythonhosted.org/packages/source/b/%{sname}/%{sname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-flit-core
BuildRequires:	python%{python3_pkgversion}-six python%{python3_pkgversion}-wcwidth
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif
Requires:	python%{python3_pkgversion}
%if 0%{?suse_version}
# SUSE does not generate runtime Requires from the Python metadata by
# default; Fedora and RHEL do:
Requires:	python%{python3_pkgversion}-wcwidth >= 0.7
# SUSE ships the curses module of Python in a separate package:
Requires:	python%{python3_pkgversion}-curses
%endif

%description
Blessed is an easy, practical *library* for making *terminal* apps, by providing
an elegant, well-documented interface to Colors_, Keyboard_ input, and screen
position and Location_ capabilities... code-block:: python from blessed import
Terminal term Terminal() print(term.home + term.clear + term.move_y(term.height
// 2))...

%prep
%autosetup -n %{sname}-%{version}
# Remove bundled egg-info
%{__rm} -rf %{sname}.egg-info
# Upstream needs flit-core 3.11 or newer for the SPDX license expression
# and license-files, which are not available on all platforms (e.g. RHEL 10).
# Use the license table, which older flit-core versions understand:
%{__sed} -i -e "s|^license = 'MIT'$|license = { text = 'MIT' }|" \
	-e '/^license-files = /d' \
	-e "s|'flit_core >=3.11,<4'|'flit_core >=3.4,<4'|" pyproject.toml
grep -q "^license = { text = 'MIT' }$" pyproject.toml
if grep -q '^license-files' pyproject.toml; then exit 1; fi

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sname}-%{version}.dist-info/
%{python3_sitelib}/%{sname}

%changelog
* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 1.39.0-3PGDG
- Fix build on RHEL 10: use the license table form in pyproject.toml and
  remove license-files, as flit-core < 3.11 does not support the SPDX
  license expression. Also relax the flit_core >= 3.11 build requirement.
- Add SLES 16 support (python313), for pg_activity, and Require wcwidth
  and curses (a separate package there) on SUSE. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/427
- Add SLES 15 support (python311), for pg_activity. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/427

* Fri Sep 11 2026 Devrim Gunduz <devrim@gunduz.org> - 1.39.0-2PGDG
- Migrate %%python3_sitelib off the removed distutils.sysconfig module
  to sysconfig.get_path()
- Switch to pyproject builds
- Remove Fedora <= 42 support
- Add missing Fedora 44 pin (python3.14)

* Mon Aug 31 2026 Devrim Gündüz <devrim@gunduz.org> - 1.49.0-1PGDG
- Update to 1.49.0 per changes described at:
  https://pypi.org/project/blessed/1.49.0/

* Tue Aug 25 2026 Devrim Gündüz <devrim@gunduz.org> - 1.22.0-44PGDG
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Mon Oct 6 2025 Devrim Gündüz <devrim@gunduz.org> - 1.22.0-42PGDG
- Update to 1.22.0
- Use more macros and get rid of pypi_source macro.

* Mon Oct 6 2025 Devrim Gündüz <devrim@gunduz.org> - 1.19.1-42PGDG
- Initial packaging for the PostgreSQL RPM repository to satisfy
  pg_activity dependency. Package is for RHEL 8 only.

