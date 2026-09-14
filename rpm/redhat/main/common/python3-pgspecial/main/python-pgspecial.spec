
%global __ospython3 %{_bindir}/python3
%global python3_sitelib %(%{__ospython3} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

%global sname pgspecial
%global srcname pgspecial

Name:		python3-%{sname}
Version:	2.2.1
Release:	3PGDG%{?dist}
Epoch:		1
Summary:	Meta-commands handler for Postgres Database.

License:	BSD
URL:		https://pypi.python.org/pypi/pgspecial
Source0:	https://files.pythonhosted.org/packages/source/%(n=%{srcname}; echo ${n:0:1})/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRequires:	python3-devel python3-pip python3-setuptools
BuildRequires:	python3-setuptools_scm pyproject-rpm-macros

BuildArch:	noarch

%description
This package provides an API to execute meta-commands (AKA “special”,
or “backslash commands”) on PostgreSQL.

%prep
%setup -q -n %{srcname}-%{version}

%build
SETUPTOOLS_SCM_PRETEND_VERSION=%{version} %pyproject_wheel

%install
%pyproject_install

%files
%license License.txt
%doc README.rst
%{python3_sitelib}/%{sname}-%{version}.dist-info/
%{python3_sitelib}/%{sname}/

%changelog
* Mon Sep 14 2026 Devrim Gündüz <devrim@gunduz.org> - 1:2.2.1-3PGDG
- Migrate %%python3_sitelib off the removed distutils.sysconfig module to
  sysconfig.get_path() (distutils is gone on Python 3.12+, e.g. Fedora's
  default python3.14)
- Switch to pyproject builds.

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
