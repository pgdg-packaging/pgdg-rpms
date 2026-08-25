%global modname py_consul
%if 0%{?fedora} && 0%{?fedora} == 45
%global python3_pkgversion 3.15
%endif
%if 0%{?fedora} && 0%{?fedora} <= 44
%global python3_pkgversion 3.14
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	python3_pkgversion 3.12
%endif
%if 0%{?amzn} == 2023
%global	python3_pkgversion 3.13
%endif
%if 0%{?suse_version} == 1500
%global	python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global	python3_pkgversion 313
%endif

Name:		py-consul
Version:	1.7.1
Release:	43PGDG%{?dist}
Summary:	Python client for Consul
License:	MIT
URL:		https://github.com/criteo/%{name}
Source0:	https://github.com/criteo/%{name}/archive/refs/tags/v%{version}.tar.gz

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif

BuildArch:	noarch

Obsoletes:	python3-consul <= 1.1.0-42
Provides:	python%{python3_pkgversion}dist(%{name}) = %{version}-%{release}

%description
Python client for Consul

%prep
%setup -q -n %{name}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%{__rm} -rf %{buildroot}%{python3_sitelib}/docs
%{__rm} -f %{buildroot}/usr/*requirements*

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{python3_sitelib}/%{modname}-%{version}.dist-info/
%{python3_sitelib}/consul/*.py*
%{python3_sitelib}/consul/api/*.py*
%{python3_sitelib}/consul/api/acl/*.py*
%if 0%{?suse_version} == 1500
%{python3_sitelib}/docs/*.py
%endif
%if 0%{?rhel} || 0%{?fedora}
%{python3_sitelib}/consul/__pycache__/*.py*
%{python3_sitelib}/consul/api/__pycache__/*.py*
%{python3_sitelib}/consul/api/acl/__pycache__/*.py*
%endif

%changelog
* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 1.7.1-43PGDG
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Wed Aug 12 2026 Devrim Gunduz <devrim@gunduz.org> - 1.7.1-42PGDG
- Update to 1.7.1 per changes described at:
  https://github.com/criteo/py-consul/releases/tag/v1.7.1
  https://github.com/criteo/py-consul/releases/tag/v1.7.0
  https://github.com/criteo/py-consul/releases/tag/v1.6.1
- Switch to pyproject builds
- Add Fedora 45 support

* Mon Sep 22 2025 Devrim Gunduz <devrim@gunduz.org> - 1.6.0-44PGDG.1
- Add Fedora 43 support

* Sat Jun 7 2025 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-44PGDG
- Provide the correct Provides for python3Xdist(py-consul)

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
