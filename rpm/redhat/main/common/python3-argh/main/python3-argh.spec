%global	pypi_name argh

Name:		python3-%{pypi_name}
Version:	0.31.3
Release:	1PGDG%{?dist}
Summary:	An unobtrusive argparse wrapper with natural syntax

License:	LGPLv3+
URL:		https://pypi.python.org/pypi/%{pypi_name}
Source0:	https://pypi.python.org/packages/source/a/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source1:	https://www.gnu.org/licenses/lgpl-3.0.txt
Source2:	https://www.gnu.org/licenses/gpl-3.0.txt
BuildArch:	noarch

%description
Building a command-line interface? Found yourself uttering “argh!” while struggling with the API of argparse? Don’t like the complexity but need the power?
Argh is a smart wrapper for argparse. Argparse is a very powerful tool; Argh just makes it easy to use.


BuildRequires:	python3-devel
BuildRequires:	python3-mock
BuildRequires:	python3-setuptools
BuildRequires:	glibc-langpack-en

%{?python_provide:%python_provide python3-%{pypi_name}}

%prep
%autosetup -n %{pypi_name}-%{version} -p 1

%{__install} -pm 0644 %{SOURCE1} COPYING
%{__install} -pm 0644 %{SOURCE2} .

%build
%py3_build

%install
%py3_install

%files -n python3-%{pypi_name}
%doc README.rst
%license COPYING gpl-3.0.txt
%{python3_sitelib}/argh*/

%changelog
* Mon Aug 31 2026 Devrim Gündüz <devrim@gunduz.org> - 0.31.3-1PGDG
- Update to 0.31.3 per changes described at:
  https://pypi.org/project/argh/0.31.3/

* Mon Jul 3 2023 Devrim Gündüz <devrim@gunduz.org> - 0.26.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support
  pg_statviz package.
