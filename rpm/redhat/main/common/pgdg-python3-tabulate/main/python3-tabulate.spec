%pgdg_python3_setup

%global sname tabulate

# Our consumers (pg_chameleon, cli-helpers) use python3.12 on RHEL 8 and 9
# and python3.13 on Amazon Linux 2023, not the system python3 (3.6, 3.9),
# so build that flavor there. Elsewhere the system python3 is already the
# one our consumers use, so keep the python3-tabulate name.
%global pyname python3
%if 0%{?rhel} == 8 || 0%{?rhel} == 9
%global pyname python3.12
%endif
%if 0%{?amzn} == 2023
%global pyname python3.13
%endif
%if "%{pyname}" != "python3"
%global python3_sitelib %(%{__python3} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")
%endif

Name:		%{pyname}-%{sname}
Version:	0.10.0
Release:	5PGDG%{?dist}
Summary:	Pretty-print tabular data in Python, a library and a command-line utility

License:	MIT
URL:		https://pypi.python.org/pypi/tabulate
Source:		https://files.pythonhosted.org/packages/46/58/8c37dea7bbf769b20d58e7ace7e5edfe65b849442b00ffcdd56be88697c6/%{sname}-%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	%{pyname}-devel
BuildRequires:	%{pyname}-pip
BuildRequires:	%{pyname}-wheel
BuildRequires:	%{pyname}-setuptools
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif
# widechars support
%{?python_extras_subpkg:Recommends: %{name}+widechars}
%{!?python_extras_subpkg:Recommends: python%{python3_version}dist(wcwidth)}

%{?python_extras_subpkg:%python_extras_subpkg -n %{name} -i %{python3_sitelib}/%{sname}-%{version}.dist-info widechars}

%description
The main use cases of the library are:

* printing small tables without hassle: just one function call, formatting is
  guided by the data itself
* authoring tabular data for lightweight plain-text markup: multiple output
  formats suitable for further editing or transformation
* readable presentation of mixed textual and numeric data: smart column
  alignment, configurable number formatting, alignment by a decimal point}

%prep
%autosetup -n %{sname}-%{version}

# This package's real target matrix spans setuptools versions from 53
# (EL9) through 69 (EL10); pyproject.toml's [project] table needs
# setuptools >= 61 just to be recognized at all (older setuptools
# silently produces an "UNKNOWN-0.0.0" package with no files), and its
# PEP 639 SPDX-string license field needs setuptools >= 77 (missing on
# SLES 15's 67.7.2 too). Replace it with a plain setup.py + a
# [build-system]-only pyproject.toml, which works identically
# regardless of the local setuptools vintage.
cat > setup.py <<'EOF'
from setuptools import setup

setup(
    name="tabulate",
    version="%{version}",
    packages=["tabulate"],
    license="MIT",
    entry_points={"console_scripts": ["tabulate=tabulate:_main"]},
    extras_require={"widechars": ["wcwidth"]},
)
EOF
cat > pyproject.toml <<'EOF'
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"
EOF

%build
%pyproject_wheel

%install
%pyproject_install
%if "%{pyname}" != "python3"
# Do not conflict with the system python3-tabulate:
%{__rm} -f %{buildroot}%{_bindir}/%{sname}
%endif

%files
%license LICENSE
%doc README README.md
%if "%{pyname}" == "python3"
%{_bindir}/%{sname}
%endif
%{python3_sitelib}/%{sname}-%{version}.dist-info/
%{python3_sitelib}/%{sname}/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 0.10.0-5PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Fri Oct 23 2026 Devrim Gunduz <devrim@gunduz.org> - 0.10.0-4PGDG
- Add RHEL 8 support (python3.12), for cli-helpers, so that it does not
  need EPEL. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Mon Oct 12 2026 Devrim Gunduz <devrim@gunduz.org> - 0.10.0-3PGDG
- Build the python3.12 flavor on RHEL 9 and the python3.13 flavor on
  Amazon Linux 2023, as python3.12-tabulate and python3.13-tabulate.
  The system python3 build did not provide the python3.12dist(tabulate)
  and python3.13dist(tabulate) that pg_chameleon and cli-helpers need.

* Mon Sep 14 2026 Devrim Gunduz <devrim@gunduz.org> - 0.10.0-2PGDG
- Update to 0.10.0 per changes described at:
  https://pypi.org/project/tabulate/0.10.0/
- Fix the same structural spec bug found in several other python3-*
  packages: BuildRequires/Recommends/the widechars extras-subpkg call
  sat *after* %%description with no section marker, so rpm's parser
  swallowed them as literal description prose instead of real tags.
- Switch to pyproject builds.
- Drop the unused "Test deps" BuildRequires (pytest, numpy, pandas,
  wcwidth) - there is no %%check section in this spec file
- Add PGDG branding

* Tue Jan 4 2022 Devrim Gündüz <devrim@gunduz.org> - 0.8.9-1
- Initial packaging to provide pg_chameleon dependency on SLES 15.
