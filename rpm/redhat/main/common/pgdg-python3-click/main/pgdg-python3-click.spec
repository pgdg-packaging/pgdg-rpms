%pgdg_python3_setup

%global modname click

%{expand: %%global pybasever %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%global pgdg_python3_sitearch %(%{__python3} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

Name:		python%{python3_pkgversion}-click
Version:	8.5.0
Release:	43PGDG%{?dist}
Summary:	Simple wrapper around optparse for powerful command line utilities

License:	BSD-3-Clause
URL:		https://github.com/pallets/%{modname}
Source0:	https://github.com/pallets/%{modname}/archive/%{version}/%{modname}-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-flit-core
BuildRequires:	python%{python3_pkgversion}-pip python%{python3_pkgversion}-wheel
BuildRequires:	pyproject-rpm-macros

Provides:	python%{python3_pkgversion}dist(click)

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-click < %{version}-%{release}
%endif

%description
click is a Python package for creating beautiful command line\
interfaces in a composable way with as little amount of code as necessary.\
It's the "Command Line Interface Creation Kit". It's highly configurable but\
comes with good defaults out of the box.

%prep
%autosetup -n click-%{version} -p1
# Upstream needs flit-core 3.11 or newer for the SPDX license expression
# and license-files, which are not available on these platforms. Use the
# license table, which older flit-core versions understand:
sed -i -e 's|^license = "BSD-3-Clause"$|license = { text = "BSD-3-Clause" }|' \
	-e '/^license-files = /d' \
	-e 's|"flit_core>=3.11,<4"|"flit_core>=3.4,<4"|' pyproject.toml
grep -q '^license = { text = "BSD-3-Clause" }$' pyproject.toml
if grep -q '^license-files' pyproject.toml; then exit 1; fi

%build
%pyproject_wheel

%install
%pyproject_install
%if 0%{?amzn} == 2023
# AL2023's brp-python-bytecompile doesn't auto-discover the python3.13
# alt-stack site-packages dir the way Fedora/RHEL's does, so __pycache__
# never gets populated. Bytecompile explicitly instead.
%py_byte_compile %{__python3} %{buildroot}%{pgdg_python3_sitearch}/%{modname}
%endif

%files
%license LICENSE.txt
%doc README.md CHANGES.md
%{pgdg_python3_sitearch}/%{modname}-%{version}.dist-info/
%{pgdg_python3_sitearch}/%{modname}/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 8.5.0-43PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 8.5.0-42PGDG
- Add RHEL 10 support, without EPEL, and obsolete the EPEL python3-click
  package there. Start the release from 42, so that our packages win over
  EPEL's. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Fri Sep 11 2026 Devrim Gunduz <devrim@gunduz.org> - 8.5.0-2PGDG
- Remove Fedora <= 42 support
- Add missing Fedora 44 pin (python3.14)
- Click has no setup.py since 8.2. Build with the pyproject macros and
  flit-core, and use the license table form in pyproject.toml, as flit-core
  3.11 is not available on these platforms. Update the doc file names. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226

* Mon Aug 31 2026 Devrim Gunduz <devrim@gunduz.org> - 8.5.0-1PGDG.1
- Update to 8.5.0 per changes described at:
  https://github.com/pallets/click/releases/tag/8.5.0

* Fri Aug 28 2026 Devrim Gunduz <devrim@gunduz.org> - 8.1.7-46PGDG.1
- Package the .egg-info directory itself instead of globbing only its
  contents (egg-info/*), so RHEL/Fedora's pythondist.attr generator
  (which is anchored on the .egg-info directory entry) actually fires
  and emits the correct runtime Requires. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 8.1.7-45PGDG.1
- Explicitly bytecompile with %%py_byte_compile on Amazon Linux 2023.
  AL2023's brp-python-bytecompile doesn't auto-discover the python3.13
  alt-stack site-packages dir, so __pycache__ was never populated and
  the build failed with a missing-file error.

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 8.1.7-44PGDG.1
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Mon Sep 22 2025 Devrim Gunduz <devrim@gunduz.org> - 8.1.7-43PGDG.1
- Add Fedora 43 support

* Tue May 20 2025 Devrim Gunduz <devrim@gunduz.org> - 8.1.7-43PGDG
- Add Provides:

* Tue May 20 2025 Devrim Gunduz <devrim@gunduz.org> - 8.1.7-42PGDG
- Initial packaging for the PostgreSQL RPM repository to support Patroni
  on RHEL 9 and 8.
