%global modname dateutil

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
%global pgdg_python3_sitearch %(%{__ospython} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

Name:		python%{python3_pkgversion}-%{modname}
Version:	3.0.0
Release:	1PGDG%{?dist}
Summary:	Powerful extensions to the standard datetime module
License:	(Apache-2.0 AND BSD-3-Clause) OR BSD-3-Clause
URL:		https://github.com/%{modname}/%{modname}
Source:		%{pypi_source python_dateutil}
# Allow setuptools-scm dependency greater than v8.0
Patch:		relax-setuptools_scm-requires.patch

BuildArch:	noarch
BuildRequires:	python%{python3_pkgversion}-devel python%{python3_pkgversion}-setuptools
# Needed so setuptools_scm's setup_requires is already satisfied locally;
# otherwise setup.py tries to pip-fetch it, which fails in a
# network-isolated mock build.
%if 0%{?rhel} != 8
BuildRequires:	python%{python3_pkgversion}-setuptools_scm
%endif
%if 0%{?rhel} && 0%{?rhel} <= 9
BuildRequires:	python%{python3_pkgversion}-pip
%endif
%if 0%{?rhel} && 0%{?rhel} == 10
BuildRequires:	python3-pip
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	python%{python3_pkgversion}-pip
%endif

# Time zone data is read from the system first:
Requires:	tzdata
# The dependency generator does not add these on RHEL 8. dateutil uses the
# tzdata module when a time zone is not found on the system, and for the
# deprecated dateutil.zoneinfo module:
Requires:	python%{python3_pkgversion}-six >= 1.6
Requires:	python%{python3_pkgversion}-tzdata

Provides:	python%{python3_pkgversion}dist(python-dateutil)

%description
The dateutil module provides powerful extensions to the standard datetime\
module available in Python.

%prep
%autosetup -p1 -n python_%{modname}-%{version}
%if 0%{?rhel} == 8
# There is no python3.12-setuptools_scm on RHEL 8. Give setup.py the version
# directly (the sdist already has src/dateutil/_version.py):
sed -i -e "/^      use_scm_version={$/,/^      },$/c\\      version='%{version}'," setup.py
sed -i -e '/^setup_requires = setuptools_scm$/d' setup.cfg
grep -q "^      version='%{version}',$" setup.py
if grep -q 'scm' setup.py setup.cfg; then exit 1; fi
%endif

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --no-compile --root %{buildroot}
%if 0%{?amzn} == 2023
# AL2023's brp-python-bytecompile doesn't auto-discover the python3.13
# alt-stack site-packages dir the way Fedora/RHEL's does, so __pycache__
# never gets populated. Bytecompile explicitly instead.
%py_byte_compile %{__ospython} %{buildroot}%{pgdg_python3_sitearch}/%{modname}
%endif


%files
%doc NEWS README.rst
%license LICENSE
%{pgdg_python3_sitearch}/%{modname}/*.py*
%{pgdg_python3_sitearch}/%{modname}/__pycache__/*.py*
%{pgdg_python3_sitearch}/%{modname}/parser/*.py*
%{pgdg_python3_sitearch}/%{modname}/parser/__pycache__/*.py*
%{pgdg_python3_sitearch}/%{modname}/tz/*.py*
%{pgdg_python3_sitearch}/%{modname}/tz/__pycache__/*.py*
%{pgdg_python3_sitearch}/%{modname}/zoneinfo/__pycache__/*.py*
%{pgdg_python3_sitearch}/%{modname}/zoneinfo/*.py*
%{pgdg_python3_sitearch}/python_dateutil-%{version}-py%{pybasever}.egg-info/

%changelog
* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 3.0.0-1PGDG
- Update to 3.0.0 per changes described at:
  https://github.com/dateutil/dateutil/releases/tag/3.0.0
- dateutil no longer ships its own copy of the time zone database, and
  uses the tzdata module instead when a time zone is not found on the
  system: Require python3-tzdata, and six >= 1.6.
- The sdist is now named python_dateutil.
- NEWS is UTF-8 now: do not convert it anymore.
- Refresh the setuptools_scm patch for the new pyproject.toml.
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/427

* Tue Oct 13 2026 Devrim Gunduz <devrim@gunduz.org> - 2.9.0.post0-7PGDG
- Add an explicit Requires on six: the dependency generator does not add
  it on RHEL 8, so dateutil could not be imported there. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/367

* Sun Oct 11 2026 Devrim Gunduz <devrim@gunduz.org> - 2.9.0.post0-6PGDG
- There is no python3.12-setuptools_scm on RHEL 8: do not BuildRequire it
  there, and give setup.py the version directly instead. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226

* Fri Sep 11 2026 Devrim Gunduz <devrim@gunduz.org> - 2.9.0.post0-5PGDG
- Remove Fedora <= 42 support
- Add missing Fedora 44 pin (python3.14)
- Add missing BR (python3-setuptools_scm), to avoid setup.py trying to pip-fetch it during a network-isolated mock build

* Fri Aug 28 2026 Devrim Gunduz <devrim@gunduz.org> - 2.9.0.post0-4PGDG.1
- Package the .egg-info directory itself instead of globbing only its
  contents (egg-info/*), so RHEL/Fedora's pythondist.attr generator
  (which is anchored on the .egg-info directory entry) actually fires
  and emits the six>=1.5 runtime Requires. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 2.9.0.post0-3PGDG.1
- Explicitly bytecompile with %%py_byte_compile on Amazon Linux 2023.
  AL2023's brp-python-bytecompile doesn't auto-discover the python3.13
  alt-stack site-packages dir, so __pycache__ was never populated and
  the build failed with a missing-file error.

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 2.9.0.post0-2PGDG.1
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Mon Sep 22 2025 Devrim Gunduz <devrim@gunduz.org> - 2.9.0.post0-1PGDG.1
- Add Fedora 43 support

* Sun May 18 2025 Devrim Gunduz <devrim@gunduz.org> - 2.9.0.post0-1PGDG
- Inıtial packaging for the PostgreSQL RPM repository to support Barman
  on RHEL 9 and RHEL 8.
