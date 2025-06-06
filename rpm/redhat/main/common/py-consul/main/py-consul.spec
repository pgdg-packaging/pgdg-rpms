%global modname py_consul

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
%global pgdg_python3_sitelib %(%{__ospython} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

Name:		py-consul
Version:	1.6.0
Release:	43PGDG%{?dist}
Summary:	Python client for Consul
License:	MIT
URL:		https://github.com/criteo/%{name}
Source0:	https://github.com/criteo/%{name}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-setuptools

BuildArch:	noarch

Obsoletes:	python3-consul <= 1.1.0-42
Provides:	python%{python3_pkgversion}dist(%{name})%{?_isa} = %{version}-%{release}

%description
Python client for Consul

%prep
%setup -q -n %{name}-%{version}

%build
%{__ospython} setup.py build

%install
%{__ospython} setup.py install --no-compile --root %{buildroot}

%{__rm} -rf %{buildroot}%{python3_sitelib}/docs
%{__rm} -f %{buildroot}/usr/*requirements*

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{pgdg_python3_sitelib}/%{modname}-%{version}-py%{pybasever}.egg-info/*
%{pgdg_python3_sitelib}/consul/*.py*
%{pgdg_python3_sitelib}/consul/__pycache__/*.py*
%{pgdg_python3_sitelib}/consul/api/*.py*
%{pgdg_python3_sitelib}/consul/api/__pycache__/*.py*
%{pgdg_python3_sitelib}/consul/api/acl/*.py*
%{pgdg_python3_sitelib}/consul/api/acl/__pycache__/*.py*

%changelog
* Fri Jun 6 2025 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-43PGDG
- Provide python3Xdist(py-consul) to satisfy patroni dependency
  introduced in 4.0.6

* Tue May 20 2025 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-42PGDG
- Rebuild on RHEL 8

* Mon May 19 2025 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-3PGDG
- Build the package with Python 3.12 on RHEL 9 & 8 and Python 3.11 on SLES
  15. For the other distros (Fedora and RHEL 10) use OS'd default Python
  version.
  https://github.com/pgdg-packaging/pgdg-rpms/issues/16

* Thu May 15 2025 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-2PGDG
- Rebuild on RHEL 8 against Python 3.6 . Apparently previous release was built
  against Python 3.9 accidentally, breaking new installs.
  Per report from Seda Yavuz.

* Thu Apr 17 2025 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository
