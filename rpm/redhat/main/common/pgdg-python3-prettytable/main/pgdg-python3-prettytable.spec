%global modname prettytable
%if 0%{?fedora} && 0%{?fedora} <= 42
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?suse_version} >= 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif

%{expand: %%global pybasever %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%global python3_sitelib %(%{__ospython} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

Name:		python%{python3_pkgversion}-%{modname}
Version:	3.4.0
Release:	43PGDG%{dist}
Summary:	Python library to display tabular data in tables

License:	BSD-3-Clause
URL:		https://github.com/jazzband/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/p/prettytable/prettytable-3.4.0.tar.gz

BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	sed

Provides:	python%{python3_pkgversion}dist(prettytable)

%description
PrettyTable is a simple Python library designed to make it quick and easy to
represent tabular data in visually appealing ASCII tables. It was inspired by
the ASCII tables used in the PostgreSQL shell psql. PrettyTable allows for
selection of which columns are to be printed, independent alignment of columns
(left or right justified or centred) and printing of "sub-tables" by specifying
a row range.

%prep
%autosetup -n %{modname}-%{version}
sed -i -e '/^*!\//, 1d' src/prettytable/*.py

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --no-compile --root %{buildroot}

%files
%doc README.md CHANGELOG.md
%license COPYING
%{python3_sitelib}/%{modname}-%{version}-py%{pybasever}.egg-info/*
%{python3_sitelib}/%{modname}/*.py*
%{python3_sitelib}/%{modname}/__pycache__/*.py*

%changelog
* Tue May 20 2025 Devrim Gunduz <devrim@gunduz.org> - 3.4.0-43PGDG
- Add Provides:

* Tue May 20 2025 Devrim Gunduz <devrim@gunduz.org> - 3.4.0-42PGDG
- Initial packaging for the PostgreSQL RPM repository to support Patroni
  on RHEL 9 and RHEL 8.
