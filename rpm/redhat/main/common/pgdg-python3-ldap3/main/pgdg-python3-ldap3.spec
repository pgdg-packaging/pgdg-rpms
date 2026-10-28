%pgdg_python3_setup

%global	modname ldap3
%global	pymodname ldap3

Name:		python%{python3_pkgversion}-%{modname}
Version:	2.9.1
Release:	43PGDG%{?dist}
Summary:	A strictly RFC 4511 conforming LDAP V3 pure Python client

License:	LGPL-3.0-or-later
URL:		https://github.com/cannatag/ldap3
Source0:	https://files.pythonhosted.org/packages/source/l/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

%if 0%{?rhel} == 8
# The python3.12 packages of RHEL 8 get no automatic python3.12dist()
# provides and requires:
Provides:	python%{python3_pkgversion}dist(%{pymodname}) = %{version}
Requires:	python%{python3_pkgversion}-pyasn1 >= 0.4.6
%endif

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-ldap3 < %{version}-%{release}
%endif

%description
ldap3 is a strictly RFC 4510 conforming LDAP V3 pure Python client
library. The same codebase runs in Python 2, Python 3, PyPy and PyPy3.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license COPYING.txt COPYING.LESSER.txt
%doc README.rst
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 2.9.1-43PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 2.9.1-42PGDG
- Initial packaging for the PostgreSQL RPM repository, for pgldapsync on
  RHEL 8, 9 and 10 and Amazon Linux 2023, without EPEL.
- RHEL 10: Obsolete the EPEL python3-ldap3 package. Start the release from
  42, so that our packages win over EPEL's. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
