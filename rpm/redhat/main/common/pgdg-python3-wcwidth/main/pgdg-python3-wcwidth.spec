%pgdg_python3_setup

%global modname wcwidth

%global python3_sitelib %(%{__python3} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

Name:		python%{python3_pkgversion}-%{modname}
Version:	0.9.4
Release:	2PGDG%{?dist}
Summary:	Measures number of Terminal column cells of wide-character codes

# part of the code is under HPND-Markus-Kuhn
License:	MIT AND HPND-Markus-Kuhn
URL:		https://github.com/jquast/%{modname}
Source:		https://github.com/jquast/%{modname}/archive/refs/tags/%{version}.tar.gz#/%{modname}-%{version}.tar.gz
BuildArch:	noarch

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%if 0%{?suse_version} >= 1600
# SUSE's Python dependency generators. python3-devel pulls this in, but
# python%%{python3_pkgversion}-devel does not. On SLES 15 they come with
# the rpm package, and Leap 15.6 has no python-rpm-packaging.
BuildRequires:	python-rpm-packaging
%endif
%else
BuildRequires:	pyproject-rpm-macros
%endif
# python%%{python3_pkgversion}-devel is what pulls the Python RPM dependency
# generators into the buildroot; the macros packages alone do not. Without
# it, neither python(abi) nor pythonX.Ydist(...) get generated. Per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/228
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

%description
This API is mainly for Terminal Emulator implementors, or those writing programs
that expect to interpreted by a terminal emulator and wish to determine the
printable width of a string on a Terminal.

%prep
%setup -q -n %{modname}-%{version}
# skip coverage checks
sed -i -e 's|--cov[^[:space:]]*||g' tox.ini
# Classifiers are informational only; drop the Python 3.15 one, which older
# trove-classifiers releases do not know yet.
sed -i '/"Programming Language :: Python :: 3.15"/d' pyproject.toml

%build
# 0.9.0 and later ship an optional C extension. Skip it, so that the package
# stays noarch; the pure Python implementation is used at runtime.
export WCWIDTH_NO_EXTENSION=1
%pyproject_wheel

%install
%pyproject_install

%files
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{modname}-%{version}.dist-info/
%{python3_sitelib}/%{modname}/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 0.9.4-2PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 0.9.4-1PGDG
- Update to 0.9.4 per changes described at:
  https://github.com/jquast/wcwidth/releases/tag/0.9.4
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/447

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 0.9.3-2PGDG
- BuildRequire python-rpm-packaging on SLES 16 only: on SLES 15 the Python
  dependency generators come with the rpm package, and Leap 15.6 does not
  have python-rpm-packaging.

* Tue Oct 20 2026 Devrim Gunduz <devrim@gunduz.org> - 0.9.3-1PGDG
- Update to 0.9.3 per changes described at:
  https://github.com/jquast/wcwidth/releases/tag/0.9.3
- Upstream switched the build backend to setuptools: drop the flit-core
  workaround, and BuildRequire setuptools and wheel instead.
- Build without the optional C extension, which was added in 0.9.0, so
  that the package stays noarch.
- Use the GitHub tarball, as 0.9.3 is not on PyPI yet.
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/412

* Wed Sep 23 2026 Devrim Gunduz <devrim@gunduz.org> - 0.8.3-5PGDG
- Drop the explicit dist() Provides, which was python313dist(wcwidth) on
  SLES 16 instead of python3.13dist(wcwidth). The Python dependency
  generators now provide python3.Xdist(wcwidth) and python(abi) on all
  platforms.
- BuildRequire python-devel, hatchling and pip on SUSE as well, and
  python-rpm-packaging, which python313-devel does not pull in, so that
  the Python dependency generators run there.
- Drop the Python 3.15 classifier from pyproject.toml, which the hatchling
  on SLES 16 rejects.
- Build the python311 flavor on SLES 15. The SUSE pyproject macros built
  for the default python3 (3.6), so the build failed there. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226
- Build with flit-core instead of hatchling, and use the license table form
  in pyproject.toml: hatchling is not available on RHEL 8, and too old for
  the SPDX license expression and license-files on RHEL 9 and Amazon Linux
  2023.
- Add Amazon Linux 2023 support: prettytable 3.18.0 needs wcwidth >= 0.3.5.

* Mon Sep 14 2026 Devrim Gunduz <devrim@gunduz.org> - 0.8.3-4PGDG
- Package the whole %%{modname}/ directory instead of hand-picked globs

* Fri Sep 11 2026 Devrim Gunduz <devrim@gunduz.org> - 0.8.3-3PGDG
- Remove Fedora <= 42 support
- Add missing Fedora 44 pin (python3.14)

* Thu Sep 10 2026 Devrim Gunduz <devrim@gunduz.org> - 0.8.3-2PGDG
- Add missing BR

* Mon Aug 31 2026 Devrim Gunduz <devrim@gunduz.org> - 0.8.3-1PGDG
- Update to 0.8.3 per changes described at:
  https://pypi.org/project/wcwidth/0.8.3/

* Fri Aug 28 2026 Devrim Gunduz <devrim@gunduz.org> - 0.2.13-6PGDG
- Package the .dist-info directory itself instead of globbing only its
  contents (dist-info/*), so RHEL/Fedora's pythondist.attr generator
  (which is anchored on the .dist-info directory entry) actually fires
  and emits the correct runtime Requires. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226
- Add back python.5%%{python3_pkgversion}-devel as a BuildRequires on the
  non-SLES branch, needed to pull python3-rpm-generators into the
  buildroot for this pyproject build. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/228

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 0.2.13-5PGDG
- Also set __python3 (not just __ospython) for Amazon Linux 2023, so
  %%pyproject_wheel/%%pyproject_install actually build against python3.13
  instead of silently falling back to the system default python3.
  This one already had its own local sitelib override, so the
  mismatch was active (not just cosmetic): pip would install via 3.9
  while %%files looked for files under python3.13's site-packages.

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 0.2.13-4PGDG
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Mon Dec 29 2025 Devrim Gunduz <devrim@gunduz.org> - 0.2.13-3PGDG
- Add SLES support
- Switch to pyproject builds

* Tue Oct 7 2025 Devrim Gunduz <devrim@gunduz.org> - 0.2.13-2PGDG
- Provide dist(wcwidth). Needed at least on RHEL 9

* Mon Sep 22 2025 Devrim Gunduz <devrim@gunduz.org> - 0.2.13-1PGDG.1
- Add Fedora 43 support

* Tue May 20 2025 Devrim Gunduz <devrim@gunduz.org> - 0.2.3-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support Patroni
  on RHEL 9 and RHEL 8.
