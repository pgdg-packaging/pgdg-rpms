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

%global	modname certifi
%global	pymodname certifi

Name:		python%{python3_pkgversion}-%{modname}
Version:	2026.7.22
Release:	1PGDG%{?dist}
Summary:	System CA bundle for Python

License:	MPL-2.0
URL:		https://github.com/certifi/python-certifi
Source0:	https://files.pythonhosted.org/packages/source/c/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

Requires:	ca-certificates

%description
Certifi provides the location of the CA bundle, for validating the
trustworthiness of SSL certificates while verifying the identity of TLS
hosts.

This package uses the CA bundle of the OS (ca-certificates), not the one
that upstream ships.

%prep
%autosetup -n %{pymodname}-%{version}

# Use the CA bundle of the OS, like Fedora and RHEL do:
cat > certifi/core.py <<'PYEOF2'
"""
certifi.py
~~~~~~~~~~

This module returns the installation location of the CA bundle of the OS or
its contents.
"""


def where() -> str:
    return "/etc/pki/tls/certs/ca-bundle.crt"


def contents() -> str:
    with open(where(), encoding="ascii") as data:
        return data.read()
PYEOF2

%build
%pyproject_wheel

%install
%pyproject_install
%{__rm} -f %{buildroot}%{python3_sitelib}/%{pymodname}/cacert.pem
%{__rm} -rf %{buildroot}%{python3_sitelib}/%{pymodname}/tests

%files
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 2026.7.22-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  httpx and requests dependency (for pg_statviz) on Amazon Linux 2023. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
