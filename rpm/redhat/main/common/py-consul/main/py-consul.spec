%global pname py_consul

Name:		py-consul
Version:	1.6.0
Release:	2PGDG%{?dist}
Summary:	Python client for Consul
License:	MIT
URL:		https://github.com/criteo/%{name}
Source0:	https://github.com/criteo/%{name}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:	python3-devel python3-wheel

%if 0%{?rhel} == 8
BuildRequires:	python39-wheel
%endif
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 9
BuildRequires:	pyproject-rpm-macros
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%endif

BuildArch:	noarch

Obsoletes:	python3-consul <= 1.1.0-42

%description
Python client for Consul

%prep
%setup -q -n %{name}-%{version}

%if 0%{?fedora} >= 40 || 0%{?rhel} >= 9 || 0%{?suse_version} >= 1500
%generate_buildrequires
%pyproject_buildrequires
%endif

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
%{python3_sitelib}/%{pname}-%{version}.dist-info/*
%{python3_sitelib}/consul/*.py*
%{python3_sitelib}/consul/__pycache__/*.py*
%{python3_sitelib}/consul/api/*.py*
%{python3_sitelib}/consul/api/__pycache__/*.py*
%{python3_sitelib}/consul/api/acl/*.py*
%{python3_sitelib}/consul/api/acl/__pycache__/*.py*

%changelog
* Thu May 15 2025 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-2PGDG
- Rebuild on RHEL 8 against Python 3.6 . Apparently previous release was built
  against Python 3.9 accidentally, breaking new installs.
  Per report from Seda Yavuz.

* Thu Apr 17 2025 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository
