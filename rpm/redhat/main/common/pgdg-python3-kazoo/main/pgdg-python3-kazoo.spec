%global modname kazoo
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
Version:	2.8.0
Release:	42PGDG%{?dist}
Summary:	Higher level Python Zookeeper client

License:	Apache-2.0
URL:		https://kazoo.readthedocs.org
Source0:	https://pypi.python.org/packages/source/k/%{modname}/%{modname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-setuptools

%description
Kazoo is a Python library designed to make working with Zookeeper a more\
hassle-free experience that is less prone to errors.

%prep
%setup -q -n %{modname}-%{version}

# Remove bundled egg-info
%{__rm} -rf %{modname}.egg-info

find . -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --no-compile --root %{buildroot}

#delete tests
%{__rm} -fr %{buildroot}%{python3_sitelib}/%{modname}/tests/

%files
%doc README.md LICENSE
%{python3_sitelib}/%{modname}
%{python3_sitelib}/%{modname}-%{version}-py%{pybasever}.egg-info

%changelog
* Tue May 20 2025 Devrim Gunduz <devrim@gunduz.org> - 2.8.0-42PGDG
- Initial packaging for the PostgreSQL RPM repository to support Patroni
  on RHEL 9 and 8 and SLES 15.

