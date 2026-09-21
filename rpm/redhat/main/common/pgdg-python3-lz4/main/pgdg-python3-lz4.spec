%global srcname lz4

%if 0%{?fedora} && 0%{?fedora} == 44
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?fedora} && 0%{?fedora} == 43
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
%if 0%{?suse_version} >= 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif

%{expand: %%global pybasever %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%global python3_sitearch %(%{__ospython} -Esc "import sysconfig; print(sysconfig.get_path('platlib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

Name:		python%{python3_pkgversion}-%{srcname}
Version:	4.4.5
Release:	2PGDG%{?dist}.1
URL:		https://github.com/python-%{srcname}/python-%{srcname}
Summary:	LZ4 Bindings for Python
# Automatically converted from old format: BSD - review is highly recommended.
License:	LicenseRef-Callaway-BSD
Source:		https://files.pythonhosted.org/packages/source/l/%{srcname}/%{srcname}-%{version}.tar.gz
# Only applied on RHEL 8, RHEL 9 and AL 2023, where there is no pkgconfig module
# for the Python stack used here. It is listed on every distro, so that the SRPM
# always carries it.
Patch0:		lz4-drop-pkgconfig-setup-requires.patch

BuildRequires:	gcc python%{python3_pkgversion}-devel python%{python3_pkgversion}-setuptools
# Needed so setup.py's setup_requires (setuptools_scm, pkgconfig) are
# already satisfied locally; otherwise setup.py tries to pip-fetch them,
# which fails in a network-isolated mock build.
BuildRequires:	python%{python3_pkgversion}-setuptools_scm
%if 0%{?rhel} == 8 || 0%{?rhel} == 9 || 0%{?amzn} == 2023
# There is no pkgconfig module for the Python stack used here. setup.py only uses
# it to find a system liblz4, and falls back to the bundled lz4 without it, so
# the patch drops it from setup_requires (which would pip-fetch it from PyPI).
# This is what the published packages effectively were: built with the bundled lz4.
Provides:	bundled(lz4) = 1.9.4
%else
BuildRequires:	python%{python3_pkgversion}-pkgconfig
%endif
%if 0%{?rhel} && 0%{?rhel} >= 8
BuildRequires:	lz4-devel
%endif
%if 0%{?fedora} && 0%{?fedora} >= 41
BuildRequires:	lz4-devel
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	liblz4-devel
%endif

%description
Python 3 bindings for the lz4 compression library.

%prep
%setup -q -n %{srcname}-%{version}
%if 0%{?rhel} == 8 || 0%{?rhel} == 9 || 0%{?amzn} == 2023
%patch -P0 -p0
%endif

#rm lz4libs/lz4*.[ch]

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --no-compile --root %{buildroot}
%if 0%{?amzn} == 2023
# AL2023's brp-python-bytecompile doesn't auto-discover the python3.13
# alt-stack site-packages dir the way Fedora/RHEL's does, so __pycache__
# never gets populated. Bytecompile explicitly instead.
%py_byte_compile %{__ospython} %{buildroot}%{python3_sitearch}/%{srcname}
%endif

find %{buildroot}%{python3_sitearch} -name 'lz4*.so' \
	-exec chmod 0755 {} \;

%files
%license LICENSE
%doc README.rst
%{python3_sitearch}/%{srcname}-%{version}-py%{pybasever}.egg-info/
%{python3_sitearch}/%{srcname}/*.py*
%{python3_sitearch}/%{srcname}/*.so
%{python3_sitearch}/%{srcname}/block/*.py*
%{python3_sitearch}/%{srcname}/block/*.so
%{python3_sitearch}/%{srcname}/frame/*.py*
%{python3_sitearch}/%{srcname}/frame/*.so
%if 0%{?rhel} || 0%{?fedora}
%{python3_sitearch}/%{srcname}/__pycache__/*.py*
%{python3_sitearch}/%{srcname}/block/__pycache__/*.py*
%{python3_sitearch}/%{srcname}/frame/__pycache__/*.py*
%endif

%changelog
* Fri Sep 11 2026 Devrim Gunduz <devrim@gunduz.org> - 4.4.5-2PGDG
- On RHEL 8, RHEL 9 and AL 2023, drop pkgconfig from setup_requires with a patch, and
  do not BuildRequire python3.12-pkgconfig / python3.13-pkgconfig there: they do not
  exist. Without the module lz4 is built with its bundled lz4 1.9.4, as the published
  packages were (they got pkgconfig from PyPI at build time, which does not work in a
  network-isolated build). Add Provides: bundled(lz4).
- Add AL 2023 support (the AL-2023 directory).
- Migrate %%python3_sitearch off the removed distutils.sysconfig module
  to sysconfig.get_path()
- Add missing BR (python3-setuptools), needed by setup.py's own build
- Add missing BRs (python3-setuptools_scm, python3-pkgconfig), needed
  so setup.py's setup_requires are already satisfied locally instead of
  trying to pip-fetch them, which fails in a network-isolated mock build
- Remove Fedora <= 42 support
- Add missing Fedora 44 pin (python3.14)

* Mon Aug 31 2026 Devrim Gunduz <devrim@gunduz.org> - 4.4.5-1PGDG.1
- Update to 4.4.5 per changes described at:
  https://pypi.org/project/lz4/4.4.5/

* Fri Aug 28 2026 Devrim Gunduz <devrim@gunduz.org> - 4.3.3-46PGDG.1
- Package the .egg-info directory itself instead of globbing only its
  contents (egg-info/*), so RHEL/Fedora's pythondist.attr generator
  (which is anchored on the .egg-info directory entry) actually fires
  and emits the correct runtime Requires. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 4.3.3-45PGDG.1
- Explicitly bytecompile with %%py_byte_compile on Amazon Linux 2023.
  AL2023's brp-python-bytecompile doesn't auto-discover the python3.13
  alt-stack site-packages dir, so __pycache__ was never populated and
  the build failed with a missing-file error.

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 4.3.3-44PGDG.1
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Mon Sep 22 2025 Devrim Gunduz <devrim@gunduz.org> - 4.3.3-43PGDG.1
- Add Fedora 43 support

* Wed Jun 11 2025 Devrim Gunduz <devrim@gunduz.org> - 4.3.3-43PGDG
- Add SLES 15 support

* Tue May 27 2025 Devrim Gunduz <devrim@gunduz.org> - 4.3.3-42PGDG
- Initial packaging for the PostgreSQL RPM repository to support Barman
  on RHEL 9 and RHEL 8.
