%global sname parsy

%if 0%{?fedora} && 0%{?fedora} == 43
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?fedora} && 0%{?fedora} <= 42
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?suse_version} == 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

%{expand: %%global py3ver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}

Name:		python%{python3_pkgversion}-%{sname}
Version:	2.1
Release:	42PGDG%{dist}
Summary:	Easy and elegant way to parse text in Python
License:	MIT
URL:		https://github.com/python-%{sname}/%{sname}/
Source:		https://github.com/python-%{sname}/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	python3-devel python3-setuptools
BuildArch:	noarch

Provides:	python3-%{sname}%{?_isa} = %{version}-%{release}

%description
Parsy is an easy and elegant way to parse text in Python by combining small
parsers into complex, larger parsers. If it means anything to you, it's a
monadic parser combinator library for LL(infinity) grammars in the spirit
of Parsec, Parsnip, and Parsimmon. But don't worry, it has really good
documentation and it doesn't say things like that!

%prep
%setup -q -n %{sname}-%{version}

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --no-compile --root %{buildroot}

%files
%doc README.rst
%license LICENSE

%{python3_sitelib}/%{sname}-%{version}-py%{py3ver}.egg-info/*
%{python3_sitelib}/%{sname}/__init__.py
%{python3_sitelib}/%{sname}/__pycache__/__init__*

%changelog
* Sat Oct 25 2025 Devrim Gündüz <devrim@gunduz.org> - 2.1-42PGDG
- Add SLES 16 support and improve support for other supported OSes.

* Wed Jan 1 2025 Devrim Gündüz <devrim@gunduz.org> - 2.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support
  pg_chameleon.

