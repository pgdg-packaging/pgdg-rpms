
%global __ospython3 %{_bindir}/python3
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 10
%{expand: %%global py3ver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global py3ver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif
%global python3_sitelib %(%{__ospython3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

%global sname pgspecial
%global srcname pgspecial

Name:		python3-%{sname}
Version:	2.2.1
Release:	1PGDG%{?dist}
Epoch:		1
Summary:	Meta-commands handler for Postgres Database.

License:	BSD
URL:		https://pypi.python.org/pypi/pgspecial
Source0:	https://files.pythonhosted.org/packages/source/%(n=%{srcname}; echo ${n:0:1})/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:	noarch

%description
This package provides an API to execute meta-commands (AKA “special”,
or “backslash commands”) on PostgreSQL.

%prep
%setup -q -n %{srcname}-%{version}

%build
CFLAGS="%{optflags}" %{__ospython3} setup.py build

%install
%{__ospython3} setup.py install --skip-build --root %{buildroot}


%files
%doc README.rst
%{python3_sitelib}/%{sname}-%{version}-py%{py3ver}.egg-info
%dir %{python3_sitelib}/%{sname}
%{python3_sitelib}/%{sname}/*

%changelog
* Mon Aug 31 2026 Devrim Gündüz <devrim@gunduz.org> - 1:2.2.1-1PGDG
- Update to 2.2.1 per changes described at:
  https://pypi.org/project/pgspecial/2.2.1/

* Wed Dec 18 2024 Devrim Gündüz <devrim@gunduz.org> - 1:2.0.1-2PGDG
- Add RHEL 10 support
- Add PGDG branding

* Fri Sep 16 2022 Devrim Gündüz <devrim@gunduz.org> - 1:2.0.1-1
- Update to 2.0.1

* Thu Mar 11 2021 Devrim Gündüz <devrim@gunduz.org> - 1:1.12.1-1
- Update to 1.12.1
- Remove PY2 stuff.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1:1.8.0-1.1
- Rebuild against PostgreSQL 11.0

* Tue Jun 6 2017 Devrim Gündüz <devrim@gunduz.org> - 1:1.8.0-1
- Initial packaging for PostgreSQL YUM repo, to satisfy pgcli dependency.
