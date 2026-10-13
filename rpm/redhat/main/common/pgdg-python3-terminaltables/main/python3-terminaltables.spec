%global		sname terminaltables

Summary:	Generate tables in terminals from list of strings
Name:		python3-%{sname}
Version:	3.1.10
Release:	10%{?dist}
License:	MIT
URL:		https://pypi.python.org/pypi/%{sname}
Source:		https://files.pythonhosted.org/packages/source/t/%{sname}/%{sname}-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools

%description
Easily draw tables in terminal/console applications from a list of
lists of strings. Supports multi-line rows.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install -O1 --prefix=%{_prefix} --root=%{buildroot}

%files -n python3-%{sname}
%defattr(-,root,root)
%{python3_sitelib}/terminaltables*
%doc README.md PKG-INFO

%changelog
* Mon May 8 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.10-10
- Initial packaging for the PostgreSQL RPM repository to satisfy
  python3-cli-helpers on RHEL 8. Took spec file from EPEL 9
