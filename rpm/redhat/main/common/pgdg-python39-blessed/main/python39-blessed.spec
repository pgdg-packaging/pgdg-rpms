%global	pypi_name blessed
%global	pypi_version 1.19.1

%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Name:		python39-%{pypi_name}
Version:	%{pypi_version}
Release:	1%{?dist}
Summary:	Easy, practical library for making terminal apps, by providing an elegant, well- documented interface to Colors, Keyboard input, and screen Positioning capabilities

License:	MIT
URL:		https://github.com/jquast/blessed
Source0:	%{pypi_source}
BuildArch:	noarch

BuildRequires:	python39-devel
BuildRequires:	python39(setuptools)
BuildRequires:	python39(six) >= 1.9
BuildRequires:	python3dist(wcwidth) >= 0.1.4
BuildRequires:	python3dist(sphinx)

%description
Blessed is an easy, practical *library* for making *terminal* apps, by providing
an elegant, well-documented interface to Colors_, Keyboard_ input, and screen
position and Location_ capabilities... code-block:: python from blessed import
Terminal term Terminal() print(term.home + term.clear + term.move_y(term.height
// 2))...

%prep
%autosetup -n %{pypi_name}-%{pypi_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

%files
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{pyver}.egg-info

%changelog
* Mon Sep 26 2022 Devrim Gündüz <devrim@gunduz.org> - 1.19.1-1
- Initial packaging to satisfy pg_activity dependency on RHEL 8.
