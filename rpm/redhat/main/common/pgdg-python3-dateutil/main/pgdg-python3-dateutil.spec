%global modname dateutil

%if 0%{?fedora} && 0%{?fedora} <= 42
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?rhel} && 0%{?rhel} < 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?suse_version} >= 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif

%{expand: %%global pybasever %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%global pgdg_python3_sitearch %(%{__ospython} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

Name:		pgdg-python3-%{modname}
Version:	2.9.0.post0
Release:	1PGDG%{?dist}
Summary:	Powerful extensions to the standard datetime module
License:	(Apache-2.0 AND BSD-3-Clause) OR BSD-3-Clause
URL:		https://github.com/%{modname}/%{modname}
Source:		%{pypi_source python-dateutil}
# Allow setuptools-scm dependency greater than v8.0
Patch:		relax-setuptools_scm-requires.patch

BuildArch:	noarch
BuildRequires:	python%{python3_pkgversion}-devel python%{python3_pkgversion}-setuptools

Requires:	tzdata

Provides:	python%{python3_pkgversion}dist(python-dateutil)

%description
The dateutil module provides powerful extensions to the standard datetime\
module available in Python.

%prep
%autosetup -p1 -n python-%{modname}-%{version}
iconv --from=ISO-8859-1 --to=UTF-8 NEWS > NEWS.new
%{__mv} NEWS.new NEWS

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --no-compile --root %{buildroot}


%files
%doc NEWS README.rst
%license LICENSE
%{pgdg_python3_sitearch}/%{modname}/*.py*
%{pgdg_python3_sitearch}/%{modname}/__pycache__/*.py*
%{pgdg_python3_sitearch}/%{modname}/parser/*.py*
%{pgdg_python3_sitearch}/%{modname}/parser/__pycache__/*.py*
%{pgdg_python3_sitearch}/%{modname}/tz/*.py*
%{pgdg_python3_sitearch}/%{modname}/tz/__pycache__/*.py*
%{pgdg_python3_sitearch}/%{modname}/zoneinfo/__pycache__/*.py*
%{pgdg_python3_sitearch}/%{modname}/zoneinfo/*.py*
%{pgdg_python3_sitearch}/%{modname}/zoneinfo/%{modname}-zoneinfo.tar.gz
%{pgdg_python3_sitearch}/python_dateutil-%{version}-py%{pybasever}.egg-info/*

%changelog
* Sun May 18 2025 Devrim Gunduz <devrim@gunduz.org> - 2.9.0.post0-1PGDG
- Inıtial packaging for the PostgreSQL RPM repository to support Barman
  on RHEL 8, RHEL 9 and SLES 15.
