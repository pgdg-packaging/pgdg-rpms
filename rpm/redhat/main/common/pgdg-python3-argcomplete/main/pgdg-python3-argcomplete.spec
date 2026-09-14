%global modname argcomplete

%if 0%{?fedora} && 0%{?fedora} == 45
%global __ospython %{_bindir}/python3.15
%global python3_pkgversion 3.15
%endif
%if 0%{?fedora} && 0%{?fedora} <= 44
%global __ospython %{_bindir}/python3.14
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
%if 0%{?suse_version} >= 1500
%global	__python3 %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif

Name:		python%{python3_pkgversion}-%{modname}
Summary:	Bash tab completion for argparse
Version:	3.7.2
Release:	3PGDG%{dist}.1
License:	Apache-2.0
URL:		https://github.com/kislyuk/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/a/%{modname}/%{modname}-%{version}.tar.gz

# hatchling/hatch-vcs (upstream's real build-system) aren't packaged for
# every alt-interpreter stack this spec targets (e.g. python3.12 on
# RHEL 9/10); drop the [build-system]/[tool.hatch.version] tables so
# this falls back to the PEP 517 default (setuptools+wheel, always
# available), which is enough since the PyPI sdist already ships a
# frozen PKG-INFO with the correct version.
Patch0:		pgdg-python3-argcomplete-removehatchling.patch

BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: python%{python3_pkgversion}-setuptools
BuildRequires: python%{python3_pkgversion}-pip
BuildRequires: python%{python3_pkgversion}-wheel
BuildRequires: pyproject-rpm-macros
BuildArch:     noarch

%description
Tab complete all the things!

Argcomplete provides easy, extensible command line tab completion of
arguments for your Python application.

It makes two assumptions:

 - You're using bash or zsh as your shell
 - You're using argparse to manage your command line arguments/options

Argcomplete is particularly useful if your program has lots of options
or subparsers, and if your program can dynamically suggest completions
for your argument/option values (for example, if the user is browsing
resources over the network).}

%prep
%autosetup -n argcomplete-%{version} -p0
# Without hatch-vcs, dynamic=["version"] has nothing to resolve it from
# and setuptools silently falls back to "0.0.0"; pin it statically since
# the PyPI sdist's frozen PKG-INFO already confirms this is %{version}.
sed -i 's/^dynamic = \["version"\]$/version = "%{version}"/' pyproject.toml
# Remove useless BRs (aka linters)
sed -i -r -e '/test = /s/"(coverage|ruff|mypy)"[, ]*//g' pyproject.toml

# https://github.com/kislyuk/argcomplete/issues/255
# https://github.com/kislyuk/argcomplete/issues/256
sed -i -e "1s|#!.*python.*|#!%{__python3}|" test/prog argcomplete/scripts/*
sed -i -e "s|python |python3 |" test/test.py

# Remove shebang from installed scripts
sed -i '/^#!/d' argcomplete/scripts/*.py

%build
%pyproject_wheel

%install
%pyproject_install
%{__rm} %{buildroot}%{_bindir}/*

%files
%license LICENSE.rst
%doc README.rst
%{python3_sitelib}/%{modname}-%{version}.dist-info/
%{python3_sitelib}/argcomplete/*.py*
%{python3_sitelib}/argcomplete/__pycache__/*.py*
%{python3_sitelib}/argcomplete/bash_completion.d/_python-argcomplete
%{python3_sitelib}/argcomplete/packages/*.py*
%{python3_sitelib}/argcomplete/packages/__pycache__/*.py*
%{python3_sitelib}/argcomplete/py.typed
%{python3_sitelib}/argcomplete/scripts/*.py*
%{python3_sitelib}/argcomplete/scripts/__pycache__/*.py*

%changelog
* Mon Sep 14 2026 Devrim Gunduz <devrim@gunduz.org> - 3.7.2-3PGDG
- Drop hotfix-bz2359689.patch: the fix it carried
  (argcomplete/bash_completion.d/_python-argcomplete's python*/pypy*
  interpreter guard) is already present upstream as of 3.7.2, so the
  patch no longer applies and is redundant.
- Add pgdg-python3-argcomplete-removehatchling.patch: upstream's real
  build-system (hatchling+hatch-vcs) isn't packaged for every
  alt-interpreter stack this spec targets (e.g. python3.12dist(hatchling)
  doesn't exist on RHEL 9/10), so drop it in favor of plain setuptools,
  which is universally available and works fine since the PyPI sdist
  ships a frozen PKG-INFO with the version.
- Switch from %%generate_buildrequires/%%pyproject_buildrequires (which
  requires a real setup.py once there's no [build-system] table) to
  static BuildRequires (setuptools, pip, pyproject-rpm-macros).
- Add [tool.setuptools.packages.find] to the same patch, scoping package
  discovery to argcomplete* - without it, setuptools' flat-layout
  auto-discovery also picks up the top-level contrib/ directory
  (README.rst only, no code) as a bogus second package and refuses to
  build.
- Pin the version statically in %%prep (dynamic=["version"] has no
  resolver left without hatch-vcs and silently becomes "0.0.0").
- Add missing BuildRequires: python%%{python3_pkgversion}-wheel
  (needed for the "bdist_wheel" setuptools command).
- Add [tool.setuptools.package-data] to the patch to explicitly include
  argcomplete/py.typed - hatchling packaged it automatically, but
  setuptools only auto-includes files also listed in MANIFEST.in, which
  never mentions py.typed.

* Fri Sep 11 2026 Devrim Gunduz <devrim@gunduz.org> - 3.7.2-2PGDG
- Remove Fedora <= 42 support
- Add missing Fedora 44 pin (python3.14)

* Mon Aug 31 2026 Devrim Gunduz <devrim@gunduz.org> - 3.7.2-1PGDG.1
- Update to 3.7.2 per changes described at:
  https://pypi.org/project/argcomplete/3.7.2/

* Fri Aug 28 2026 Devrim Gunduz <devrim@gunduz.org> - 3.6.2-3PGDG.1
- Package the .dist-info directory itself instead of globbing only its
  contents (dist-info/*), so RHEL/Fedora's pythondist.attr generator
  (which is anchored on the .dist-info directory entry) actually fires
  and emits the correct runtime Requires. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 3.6.2-2PGDG.1
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Mon Sep 22 2025 Devrim Gunduz <devrim@gunduz.org> - 3.6.2-1PGDG.1
- Add Fedora 43 support

* Mon May 19 2025 Devrim Gunduz <devrim@gunduz.org> - 3.6.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support Barman
  on RHEL 9 and RHEL 8. Modified Fedora rawhide spec file.
