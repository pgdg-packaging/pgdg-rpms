%if 0%{?fedora} && 0%{?fedora} == 45
%global __ospython %{_bindir}/python3.15
%global python3_pkgversion 3.15
%endif
%if 0%{?fedora} && 0%{?fedora} <= 44
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?rhel} == 9
%global	__python3 %{_bindir}/python3.12
%endif
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?suse_version} == 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

%global	modname meson-python
%global	pymodname meson_python

Name:		python%{python3_pkgversion}-%{modname}
Version:	0.16.0
Release:	1PGDG%{?dist}
Summary:	Meson Python build backend (PEP 517)

License:	MIT
URL:		https://github.com/mesonbuild/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/m/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
%if ! 0%{?suse_version}
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-meson >= 1.2.3
BuildRequires:	python%{python3_pkgversion}-packaging
BuildRequires:	python%{python3_pkgversion}-pyproject-metadata
BuildRequires:	ninja-build

Requires:	python%{python3_pkgversion}-meson >= 1.2.3
Requires:	python%{python3_pkgversion}-packaging
Requires:	python%{python3_pkgversion}-pyproject-metadata
Requires:	ninja-build

%description
meson-python is a Python build backend built on top of the Meson build
system. It enables to use Meson for the configuration and build steps of
Python packages.

%prep
%autosetup -n %{pymodname}-%{version}

# Use our python%{python3_pkgversion}-meson by default, instead of the
# (older) meson package of the OS:
sed -i "s|meson = os.environ.get('MESON', meson or 'meson')|meson = os.environ.get('MESON', meson or 'meson-%{python3_pkgversion}')|" mesonpy/__init__.py
grep -q "'meson-%{python3_pkgversion}'" mesonpy/__init__.py

%build
export MESON=%{_bindir}/meson-%{python3_pkgversion}
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE LICENSES
%doc README.rst
%{python3_sitelib}/mesonpy/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Tue Oct 06 2026 Devrim Gunduz <devrim@gunduz.org> - 0.16.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  pg_statviz dependency on Amazon Linux 2023.
- Add RHEL 9 support (python3.12), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
