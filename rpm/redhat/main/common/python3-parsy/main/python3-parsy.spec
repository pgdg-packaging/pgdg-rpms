%global sname parsy

%if 0%{?fedora} >= 40 || 0%{?rhel} >= 10
%{expand: %%global py3ver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global py3ver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif

Name:		python3-%{sname}
Version:	2.1
Release:	1PGDG%{dist}
Summary:	Easy and elegant way to parse text in Python
License:	MIT
URL:		https://github.com/python-%{sname}/%{sname}/
Source:		https://github.com/python-%{sname}/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	python3-devel python3-setuptools
BuildArch:	noarch

%description
Parsy is an easy and elegant way to parse text in Python by combining small
parsers into complex, larger parsers. If it means anything to you, it's a
monadic parser combinator library for LL(infinity) grammars in the spirit
of Parsec, Parsnip, and Parsimmon. But don't worry, it has really good
documentation and it doesn't say things like that!

%prep
%setup -q -n %{sname}-%{version}

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --no-compile --root %{buildroot}

%files
%doc README.rst
%license LICENSE

%{python3_sitelib}/%{sname}-%{version}-py%{py3ver}.egg-info/*
%{python3_sitelib}/%{sname}/__init__.py
%{python3_sitelib}/%{sname}/__pycache__/__init__*

%changelog
* Wed Jan 1 2025 Devrim Gündüz <devrim@gunduz.org> - 2.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support
  pg_chameleon.
