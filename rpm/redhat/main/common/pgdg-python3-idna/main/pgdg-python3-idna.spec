%pgdg_python3_setup

%global	modname idna
%global	pymodname idna

Name:		python%{python3_pkgversion}-%{modname}
Version:	3.10
Release:	2PGDG%{?dist}
Summary:	Internationalized Domain Names in Applications (IDNA)

License:	BSD-3-Clause
URL:		https://github.com/kjd/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/i/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-flit-core

%description
Support for the Internationalized Domain Names in Applications (IDNA)
protocol as specified in RFC 5891.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE.md
%doc README.rst
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 3.10-2PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 3.10-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  httpx and requests dependency (for pg_statviz) on Amazon Linux 2023. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
