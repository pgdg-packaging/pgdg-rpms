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
%{expand: %%global py3ver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:4])"`)}

%global sname pgspot

Name:		pgspot
Version:	0.9.2
Release:	1PGDG%{?dist}
Summary:	Spot vulnerabilities in PostgreSQL extension scripts
License:	PostgreSQL
Url:		https://github.com/timescale/%{sname}
Source0:	https://github.com/timescale/%{sname}/archive/refs/tags/%{version}.tar.gz
BuildArch:	noarch
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
# python%%{python3_pkgversion}-devel is what pulls python3-rpm-generators
# into the buildroot on RHEL/Fedora; pyproject-rpm-macros alone does not.
# Without it, neither python(abi) nor python%%{python3_pkgversion}dist(...)
# get generated. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/228
BuildRequires:	python%{python3_pkgversion}
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
%endif

%description
pgspot checks extension scripts for PostgreSQL security best practices.
In addition to checking extension scripts it can also be used to check
security definer functions or any other PostgreSQL SQL code.

pgspot checks for the following vulnerabilities:
- search_path-based attacks
- unsafe object creation

%prep
%setup -q -n %{sname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%defattr(-,root,root,0755)
%doc README.md CHANGELOG.md REFERENCE.md
%license LICENSE
%{_bindir}/%{sname}
%{python3_sitelib}/%{sname}/*.py
%{python3_sitelib}/%{sname}/__pycache__/*.pyc
%{python3_sitelib}/%{sname}/pg_catalog/*.py
%{python3_sitelib}/%{sname}/pg_catalog/__pycache__/*.pyc
%{python3_sitelib}/%{sname}-%{version}.dist-info/

%changelog
* Wed Sep 16 2026 Devrim Gunduz <devrim@gunduz.org> - 0.9.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository
