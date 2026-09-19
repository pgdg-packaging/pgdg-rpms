%global sname sshtunnel

Name:		python3-%{sname}
Version:	0.4.0
Release:	1PGDG%{?dist}
Summary:	Pure Python SSH tunnels

License:	MIT
URL:		https://github.com/pahaz/%{sname}
Source0:	https://files.pythonhosted.org/packages/source/s/%{sname}/%{sname}-%{version}.tar.gz
BuildArch:	noarch

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python3-devel python3-pip python3-setuptools python3-wheel

Requires:	python3-paramiko >= 2.7.2

%description
sshtunnel is a pure Python library for creating SSH tunnels (port
forwarding) on top of Paramiko. It can be used both as a Python module
and as a command line tool.

%prep
%autosetup -n %{sname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.rst changelog.rst
%{_bindir}/%{sname}
%{python3_sitelib}/%{sname}.py
%{python3_sitelib}/__pycache__/%{sname}.*
%{python3_sitelib}/%{sname}-%{version}.dist-info/

%changelog
* Sat Sep 19 2026 Devrim Gündüz <devrim@gunduz.org> - 0.4.0-1PGDG
- Add back to the repository, to satisfy the pgcli dependency on
  platforms where the OS does not ship it (e.g. RHEL 10).
