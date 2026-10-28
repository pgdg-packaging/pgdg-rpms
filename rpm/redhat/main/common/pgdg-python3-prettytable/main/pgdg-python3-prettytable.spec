%pgdg_python3_setup

%global modname prettytable

%{expand: %%global pybasever %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%global python3_sitelib %(%{__python3} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

Name:		python%{python3_pkgversion}-%{modname}
Version:	3.18.0
Release:	3PGDG%{?dist}
Summary:	Python library to display tabular data in tables

License:	BSD-3-Clause
URL:		https://github.com/jazzband/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/p/prettytable/prettytable-3.18.0.tar.gz

BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-flit-core
BuildRequires:	python%{python3_pkgversion}-pip python%{python3_pkgversion}-wheel
BuildRequires:	pyproject-rpm-macros
BuildRequires:	sed

Provides:	python%{python3_pkgversion}dist(prettytable)

%description
PrettyTable is a simple Python library designed to make it quick and easy to
represent tabular data in visually appealing ASCII tables. It was inspired by
the ASCII tables used in the PostgreSQL shell psql. PrettyTable allows for
selection of which columns are to be printed, independent alignment of columns
(left or right justified or centred) and printing of "sub-tables" by specifying
a row range.

%prep
%autosetup -n %{modname}-%{version}
sed -i -e '/^*!\//, 1d' src/prettytable/*.py
# Upstream builds with hatchling >= 1.27 and hatch-vcs: hatchling is not
# available on RHEL 8, and older on RHEL 9. Build with flit-core instead,
# which is available everywhere, with the version written in pyproject.toml
# (the sdist already has src/prettytable/_version.py), and use the license
# table, which flit-core < 3.11 understands:
sed -i -e '/^\[build-system\]$/,/^\]$/d' \
	-e 's|^license = "BSD-3-Clause"$|license = { text = "BSD-3-Clause" }|' \
	-e '/^license-files = /d' \
	-e 's|^dynamic = \[ "version" \]$|version = "%{version}"|' pyproject.toml
cat >> pyproject.toml << 'BUILDSYSTEM'

[build-system]
build-backend = "flit_core.buildapi"
requires = [ "flit_core >=3.4,<4" ]
BUILDSYSTEM
grep -q '^license = { text = "BSD-3-Clause" }$' pyproject.toml
grep -q '^version = "%{version}"$' pyproject.toml
if grep -qE '^license-files|^dynamic|hatchling' pyproject.toml; then exit 1; fi

%build
%pyproject_wheel

%install
%pyproject_install
%if 0%{?amzn} == 2023
# AL2023's brp-python-bytecompile doesn't auto-discover the python3.13
# alt-stack site-packages dir the way Fedora/RHEL's does, so __pycache__
# never gets populated. Bytecompile explicitly instead.
%py_byte_compile %{__python3} %{buildroot}%{python3_sitelib}/%{modname}
%endif

%files
%doc README.md CHANGELOG.md
%license LICENSE
%{python3_sitelib}/%{modname}-%{version}.dist-info/
%{python3_sitelib}/%{modname}/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 3.18.0-3PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Fri Sep 11 2026 Devrim Gunduz <devrim@gunduz.org> - 3.18.0-2PGDG
- Remove Fedora <= 42 support
- Add missing Fedora 44 pin (python3.14)
- prettytable has no setup.py anymore. Build with the pyproject macros and
  flit-core instead of upstream's hatchling >= 1.27 and hatch-vcs, which
  are not available on RHEL 8 and 9, and use the license table form in
  pyproject.toml. Update the license file name. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226
- Needs wcwidth >= 0.3.5: build pgdg-python3-wcwidth 0.8.3 first.

* Mon Aug 31 2026 Devrim Gunduz <devrim@gunduz.org> - 3.18.0-1PGDG.1
- Update to 3.18.0 per changes described at:
  https://pypi.org/project/prettytable/3.18.0/

* Fri Aug 28 2026 Devrim Gunduz <devrim@gunduz.org> - 3.4.0-47PGDG.1
- Package the .egg-info directory itself instead of globbing only its
  contents (egg-info/*), so RHEL/Fedora's pythondist.attr generator
  (which is anchored on the .egg-info directory entry) actually fires
  and emits the wcwidth runtime Requires. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 3.4.0-46PGDG.1
- Explicitly bytecompile with %%py_byte_compile on Amazon Linux 2023.
  AL2023's brp-python-bytecompile doesn't auto-discover the python3.13
  alt-stack site-packages dir, so __pycache__ was never populated and
  the build failed with a missing-file error.

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 3.4.0-45PGDG.1
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Mon Sep 22 2025 Devrim Gunduz <devrim@gunduz.org> - 3.4.0-44PGDG.1
- Add Fedora 43 support

* Tue May 20 2025 Devrim Gunduz <devrim@gunduz.org> - 3.4.0-44PGDG
- Define python3_sitelib macro globally. For some reason it does not
  build on RHEL 8 - aarch64 without this.

* Tue May 20 2025 Devrim Gunduz <devrim@gunduz.org> - 3.4.0-43PGDG
- Add Provides:

* Tue May 20 2025 Devrim Gunduz <devrim@gunduz.org> - 3.4.0-42PGDG
- Initial packaging for the PostgreSQL RPM repository to support Patroni
  on RHEL 9 and RHEL 8.
