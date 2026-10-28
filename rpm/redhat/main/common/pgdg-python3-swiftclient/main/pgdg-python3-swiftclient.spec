%pgdg_python3_setup

# Built for the python3.13 alt-stack of Amazon Linux 2023 only, for
# the OpenStack Swift storage backend of rohmu (pghoard).

%global	modname swiftclient
%global	pymodname python_swiftclient

Name:		python%{python3_pkgversion}-%{modname}
Version:	4.11.0
Release:	2PGDG%{?dist}
Summary:	Client library for the OpenStack Swift API

License:	Apache-2.0
URL:		https://opendev.org/openstack/python-swiftclient
Source0:	https://files.pythonhosted.org/packages/source/p/python-swiftclient/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel
BuildRequires:	python%{python3_pkgversion}-pbr

%description
This is a Python client library for the OpenStack Swift object storage
API.

%prep
%autosetup -n %{pymodname}-%{version}

%build
export PBR_VERSION=%{version}
%pyproject_wheel

%install
export PBR_VERSION=%{version}
%pyproject_install
%pyproject_save_files -l swiftclient
# Only the library is needed; do not ship the swift command:
%{__rm} -f %{buildroot}%{_bindir}/swift %{buildroot}%{_mandir}/man1/swift.1*

%files -f %{pyproject_files}
%doc README.rst

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 4.11.0-2PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 4.11.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for
  the OpenStack Swift storage backend of rohmu (pghoard) on Amazon Linux 2023.
