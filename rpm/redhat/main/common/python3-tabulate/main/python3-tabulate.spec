%global sname tabulate

Name:		python3-%{sname}
Version:	0.10.0
Release:        1%{?dist}
Summary:	Pretty-print tabular data in Python, a library and a command-line utility

License:	MIT
URL:		https://pypi.python.org/pypi/tabulate
Source:		https://files.pythonhosted.org/packages/46/58/8c37dea7bbf769b20d58e7ace7e5edfe65b849442b00ffcdd56be88697c6/%{sname}-%{version}.tar.gz

BuildArch:	noarch

%description
The main use cases of the library are:

* printing small tables without hassle: just one function call, formatting is
  guided by the data itself
* authoring tabular data for lightweight plain-text markup: multiple output
  formats suitable for further editing or transformation
* readable presentation of mixed textual and numeric data: smart column
  alignment, configurable number formatting, alignment by a decimal point}


BuildRequires:	python3-devel
BuildRequires:	python3dist(setuptools)
# Test deps
BuildRequires:	python3dist(pytest)
BuildRequires:	python3dist(numpy)
BuildRequires:	python3dist(pandas)
BuildRequires:	python3dist(wcwidth)
# widechars support
%{?python_extras_subpkg:Recommends: python3-%{sname}+widechars}
%{!?python_extras_subpkg:Recommends: python%{python3_version}dist(wcwidth)}

%{?python_extras_subpkg:%python_extras_subpkg -n python3-%{sname} -i %{python3_sitelib}/%{sname}*.egg-info widechars}

%prep
%autosetup -n %{sname}-%{version}

%build
%py3_build

%install
%py3_install

%files
%license LICENSE
%doc README README.md
%{_bindir}/%{sname}
%{python3_sitelib}/%{sname}*.egg-info/
%{python3_sitelib}/%{sname}.py
%{python3_sitelib}/__pycache__/%{sname}.*

%changelog
* Mon Aug 31 2026 Devrim Gündüz <devrim@gunduz.org> - 0.10.0-1
- Update to 0.10.0 per changes described at:
  https://pypi.org/project/tabulate/0.10.0/

* Tue Jan 4 2022 Devrim Gündüz <devrim@gunduz.org> - 0.8.9-1
- Initial packaging to provide pg_chameleon dependency on SLES 15.
