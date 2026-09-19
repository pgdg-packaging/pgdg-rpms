%global pypi_name cli_helpers

Summary:	Python helpers for common CLI tasks
Name:		python3-cli-helpers
Version:	2.15.1
Release:	2PGDG%{?dist}
License:	BSD-3-Clause
URL:		https://github.com/dbcli/cli_helpers
Source0:	https://github.com/dbcli/cli_helpers/archive/refs/tags/v%{version}.tar.gz
BuildArch:	noarch

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python3-devel
BuildRequires:	python3-pip
BuildRequires:	python3-setuptools
BuildRequires:	python3-wheel

Requires:	python3-configobj >= 5.0.5
Requires:	python3-tabulate >= 0.10
Requires:	python3-wcwidth

%description
CLI Helpers is a Python package that makes it easy to perform common
tasks when building command-line apps. It is a helper library for
command-line interfaces.

%{?python_extras_subpkg:%python_extras_subpkg -n python3-cli-helpers -i %{python3_sitelib}/%{pypi_name}-%{version}.dist-info styles}

%prep
%autosetup -n %{pypi_name}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files -n python3-cli-helpers
%license LICENSE
%doc AUTHORS CHANGELOG README.rst
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-%{version}.dist-info/

%changelog
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
