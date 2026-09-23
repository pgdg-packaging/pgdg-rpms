%global pypi_name cli_helpers

%if 0%{?fedora} && 0%{?fedora} == 45
%global python3_pkgversion 3.15
%global pybasever 3.15
%endif
%if 0%{?fedora} && 0%{?fedora} <= 44
%global python3_pkgversion 3.14
%global pybasever 3.14
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global python3_pkgversion 3.12
%global pybasever 3.12
%endif
%if 0%{?amzn} == 2023
%global __python3 %{_bindir}/python3.13
%global python3_pkgversion 3.13
%global pybasever 3.13
%endif
%if 0%{?suse_version} == 1500
%global python3_pkgversion 311
%global pybasever 3.11
%endif
%if 0%{?suse_version} == 1600
%global python3_pkgversion 313
%global pybasever 3.13
%endif

Summary:	Python helpers for common CLI tasks
Name:		python%{python3_pkgversion}-cli-helpers
Version:	2.15.1
Release:	4PGDG%{?dist}
License:	BSD-3-Clause
URL:		https://github.com/dbcli/cli_helpers
Source0:	https://github.com/dbcli/cli_helpers/archive/refs/tags/v%{version}.tar.gz
BuildArch:	noarch

%if 0%{?fedora} || 0%{?rhel} == 10 || 0%{?suse_version} == 1600
# Up to 2.15.1-2 this package was named python3-cli-helpers. On these
# platforms python3 is the same Python as above, so the old package installs
# the same files; replace it on upgrade.
Obsoletes:	python3-cli-helpers < 2.15.1-3
Obsoletes:	python3-cli-helpers+styles < 2.15.1-3
%endif

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
# SUSE's Python dependency generators. python3-devel pulls this in, but
# python%%{python3_pkgversion}-devel does not.
BuildRequires:	python-rpm-packaging
%else
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

Requires:	python%{python3_pkgversion}-configobj >= 5.0.5
# Our python3-tabulate is not renamed, as SUSE ships its own (older)
# python313-tabulate, so require it through the dist() name.
Requires:	python%{pybasever}dist(tabulate) >= 0.10
# Require wcwidth by name: on SLES 16 PGDG and SUSE both ship a
# python313-wcwidth, and only SUSE's provides python3-wcwidth.
Requires:	python%{python3_pkgversion}-wcwidth

%description
CLI Helpers is a Python package that makes it easy to perform common
tasks when building command-line apps. It is a helper library for
command-line interfaces.

%{?python_extras_subpkg:%python_extras_subpkg -n python%{python3_pkgversion}-cli-helpers -i %{python3_sitelib}/%{pypi_name}-%{version}.dist-info styles}

%prep
%autosetup -n %{pypi_name}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files -n python%{python3_pkgversion}-cli-helpers
%license LICENSE
%doc AUTHORS CHANGELOG README.rst
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-%{version}.dist-info/

%changelog
* Wed Sep 23 2026 Devrim Gündüz <devrim@gunduz.org> - 2.15.1-4PGDG
- BuildRequire python-rpm-packaging on SUSE, which python313-devel does
  not pull in, so that the Python dependency generators run there.

* Wed Sep 23 2026 Devrim Gündüz <devrim@gunduz.org> - 2.15.1-3PGDG
- Rename package to python%%{python3_pkgversion}-cli-helpers, using the same
  Python version mapping as pgcli, and obsolete python3-cli-helpers where
  that is the same Python.
- Require wcwidth by its python%%{python3_pkgversion}- name. On SLES 16 the
  PGDG python313-wcwidth does not provide python3-wcwidth, so zypper could
  not install pgcli without a vendor change.
- Require tabulate through its dist() name.

* Sat Sep 19 2026 Devrim Gündüz <devrim@gunduz.org> - 2.15.1-2PGDG
- Modernise the spec file and switch to pyproject builds
- Drop obsoleted BRs
- Require python3-tabulate >= 0.10, matching upstream's ~= 0.10.0 pin.
- Fix the License tag to use the SPDX identifier, and stop the
  %%description text from ending in stray backslashes.
- Remove the unneeded egg-info cleanup in %%prep, and use %%autosetup.
- Add PGDG branding

* Mon Aug 31 2026 Devrim Gündüz <devrim@gunduz.org> - 2.15.1-1
- Update to 2.15.1 per changes described at:
  https://github.com/dbcli/cli_helpers/releases/tag/v2.15.1

* Mon May 8 2023 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-2
- Spec file cleanup: Remove non-python3 portions.

* Tue Feb 8 2022 Devrim Gündüz <devrim@gunduz.org> - 2.2.1-1
- Initial packaging for the PostgreSQL RPM repository to satisfy pgcli dependency.
