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

%global	modname httpx
%global	pymodname httpx

Name:		python%{python3_pkgversion}-%{modname}
Version:	0.28.1
Release:	1PGDG%{?dist}
Summary:	The next generation HTTP client

License:	BSD-3-Clause
URL:		https://github.com/encode/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/h/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-hatchling
BuildRequires:	python%{python3_pkgversion}-hatch-fancy-pypi-readme

Requires:	python%{python3_pkgversion}-anyio
Requires:	python%{python3_pkgversion}-certifi
Requires:	python%{python3_pkgversion}-httpcore >= 1.0
Requires:	python%{python3_pkgversion}-idna

%description
HTTPX is a fully featured HTTP client library for Python 3, which provides
sync and async APIs, and support for both HTTP/1.1 and HTTP/2.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
# Remove the command line tool, it needs the cli extra (click, rich):
%{__rm} -rf %{buildroot}%{_bindir}

%files
%license LICENSE.md
%doc README.md
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 0.28.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  anthropic and ollama dependency (for pg_statviz) on Amazon Linux 2023. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
