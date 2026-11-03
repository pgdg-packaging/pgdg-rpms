# RHEL 8 only: the default python3 (3.6) flavor, for python3-faker, which
# postgresql_faker runs in plpython3. 4.1.1 is the last release that supports
# Python 3.6, so it cannot be built from pgdg-python3-typing-extensions.
%global __python3 /usr/bin/python3.6
%global	pymodname typing_extensions

Name:		python3-typing-extensions
Version:	4.1.1
Release:	1PGDG%{?dist}
Summary:	Backported and experimental type hints for Python 3

License:	Python-2.0.1
URL:		https://github.com/python/typing_extensions
Source0:	https://files.pythonhosted.org/packages/source/t/%{pymodname}/%{pymodname}-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python3-devel

%description
The typing_extensions module enables the use of new type system features on
older Python versions, and experimentation with new type system PEPs.

This is the flavor for the default python3 of RHEL 8, for python3-faker.

%prep
%autosetup -n %{pymodname}-%{version}

%build
# flit-core, which upstream builds with, does not support Python 3.6 anymore.
# This is a single module, so it is installed by hand.

%install
%{__install} -d %{buildroot}%{python3_sitelib}
%{__install} -m 644 src/%{pymodname}.py %{buildroot}%{python3_sitelib}/
%{__install} -m 644 PKG-INFO %{buildroot}%{python3_sitelib}/%{pymodname}-%{version}.egg-info
%py_byte_compile %{__python3} %{buildroot}%{python3_sitelib}

%files
%license LICENSE
%{python3_sitelib}/%{pymodname}.py
%{python3_sitelib}/%{pymodname}-%{version}.egg-info
%{python3_sitelib}/__pycache__/%{pymodname}.*

%changelog
* Tue Nov 3 2026 Devrim Gunduz <devrim@gunduz.org> - 4.1.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for python3-faker on
  RHEL 8, so that it does not need EPEL anymore.
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/513
