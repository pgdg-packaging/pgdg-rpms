%global pypi_name kazoo

Name:		python3-%{pypi_name}
Version:	2.11.0
Release:	1%{?dist}
Summary:	Higher level Python Zookeeper client

License:	ASL 2.0
URL:		https://kazoo.readthedocs.org
Source0:	https://pypi.python.org/packages/source/k/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python3-sphinx

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

# generate html docs
sphinx-build docs html
# remove the sphinx-build leftovers
%{__rm} -rf html/.{doctrees,buildinfo}


%build
%py3_build

%install
%py3_install

#delete tests
%{__rm} -fr %{buildroot}%{python3_sitelib}/%{pypi_name}/tests/

%files -n python3-%{pypi_name}
%doc README.md LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info

%files doc
%doc html

%changelog
* Mon Aug 31 2026 Devrim Gündüz <devrim@gunduz.org> - 2.11.0-1
- Update to 2.11.0 per changes described at:
  https://pypi.org/project/kazoo/2.11.0/

* Wed Aug 5 2020 Devrim Gündüz <devrim@gunduz.org> - 2.8.0-1
- Initial packaging for the PostgreSQL RPM repository, to satisfy patroni
  dependency on RHEL 8, based on Fedora rawhide spec file.

