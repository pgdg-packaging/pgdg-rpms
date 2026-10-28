%pgdg_python3_setup

%global	modname pyparsing

Name:		python%{python3_pkgversion}-%{modname}
Version:	3.1.4
Release:	2PGDG%{?dist}
Summary:	Python library for creating PEG parsers

License:	MIT
URL:		https://github.com/pyparsing/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/p/%{modname}/%{modname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-flit-core

%description
The pyparsing module is an alternative approach to creating and executing
simple grammars, vs. the traditional lex/yacc approach, or the use of
regular expressions.

This is 3.1.4: 3.2 and later need flit-core 3.11, RHEL 9 has 3.9.

%prep
%autosetup -n %{modname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.rst CHANGES
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}-%{version}.dist-info/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 3.1.4-2PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 3.1.4-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  matplotlib dependency (for pg_statviz) on RHEL 9 (python3.12). Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
