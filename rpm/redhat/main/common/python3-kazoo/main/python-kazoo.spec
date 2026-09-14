%global pypi_name kazoo

Name:		python3-%{pypi_name}
Version:	2.11.0
Release:	2%{?dist}
Summary:	Higher level Python Zookeeper client

License:	ASL 2.0
URL:		https://kazoo.readthedocs.org
Source0:	https://pypi.python.org/packages/source/k/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python3-sphinx
BuildRequires:	python3-devel
BuildRequires:	python3-pip
BuildRequires:	python3-setuptools
BuildRequires:	python3-wheel
BuildRequires:	pyproject-rpm-macros

%description
Kazoo is a Python library designed to make working with Zookeeper a more\
hassle-free experience that is less prone to errors.

%package doc
Summary:	Documentation for %{name}
License:	ASL 2.0

%description doc
Kazoo is a Python library designed to make working with Zookeeper a more
hassle-free experience that is less prone to errors.

This package contains documentation in HTML format.

%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
%{__rm} -rf %{pypi_name}.egg-info

find . -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'

# sphinx_autodoc_typehints isn't packaged for our real targets (EL/AL2023);
# drop it, it only adds type-hint rendering to the docs
sed -i '/^\s*"sphinx_autodoc_typehints",\?\s*$/d' docs/conf.py

# generate html docs
sphinx-build docs html
# remove the sphinx-build leftovers
%{__rm} -rf html/.{doctrees,buildinfo}


%build
%pyproject_wheel

%install
%pyproject_install

#delete tests
%{__rm} -fr %{buildroot}%{python3_sitelib}/%{pypi_name}/tests/

%files -n python3-%{pypi_name}
%doc README.md LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}.dist-info/

%files doc
%doc html

%changelog
* Mon Sep 14 2026 Devrim Gündüz <devrim@gunduz.org> - 2.11.0-2
- Drop the sphinx_autodoc_typehints Sphinx extension from docs/conf.py in
  %%prep: it's not packaged for RHEL/AL2023, and docs build fail.
- Switch to pyproject builds

* Mon Aug 31 2026 Devrim Gündüz <devrim@gunduz.org> - 2.11.0-1
- Update to 2.11.0 per changes described at:
  https://pypi.org/project/kazoo/2.11.0/

* Wed Aug 5 2020 Devrim Gündüz <devrim@gunduz.org> - 2.8.0-1
- Initial packaging for the PostgreSQL RPM repository, to satisfy patroni
  dependency on RHEL 8, based on Fedora rawhide spec file.

