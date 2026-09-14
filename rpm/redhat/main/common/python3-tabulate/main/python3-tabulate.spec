%global sname tabulate

Name:		python3-%{sname}
Version:	0.10.0
Release:        2%{?dist}
Summary:	Pretty-print tabular data in Python, a library and a command-line utility

License:	MIT
URL:		https://pypi.python.org/pypi/tabulate
Source:		https://files.pythonhosted.org/packages/46/58/8c37dea7bbf769b20d58e7ace7e5edfe65b849442b00ffcdd56be88697c6/%{sname}-%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	python3-devel
BuildRequires:	python3-pip
BuildRequires:	python3-wheel
BuildRequires:	python3-setuptools
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif
# widechars support
%{?python_extras_subpkg:Recommends: python3-%{sname}+widechars}
%{!?python_extras_subpkg:Recommends: python%{python3_version}dist(wcwidth)}

%{?python_extras_subpkg:%python_extras_subpkg -n python3-%{sname} -i %{python3_sitelib}/%{sname}-%{version}.dist-info widechars}

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

%files
%license LICENSE
%doc README README.md
%{_bindir}/%{sname}
%{python3_sitelib}/%{sname}-%{version}.dist-info/
%{python3_sitelib}/%{sname}/

%changelog
* Mon Sep 14 2026 Devrim Gunduz <devrim@gunduz.org> - 0.10.0-2
- Update to 0.10.0 per changes described at:
  https://pypi.org/project/tabulate/0.10.0/

- Fix the same structural spec bug found in several other python3-*
  packages: BuildRequires/Recommends/the widechars extras-subpkg call
  sat *after* %%description with no section marker, so rpm's parser
  swallowed them as literal description prose instead of real tags.

- Switch to pyproject builds.

- Drop the unused "Test deps" BuildRequires (pytest, numpy, pandas,
  wcwidth) - there is no %%check section in this spec file

* Tue Jan 4 2022 Devrim Gündüz <devrim@gunduz.org> - 0.8.9-1
- Initial packaging to provide pg_chameleon dependency on SLES 15.
