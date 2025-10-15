%if 0%{?fedora} && 0%{?fedora} == 43
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?fedora} && 0%{?fedora} <= 42
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
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

%global sname check_patroni

Name:		nagios-plugins-patroni
Version:	2.2.0
Release:	3PGDG%{dist}
Summary:	Patroni monitoring plugin for Nagios
License:	PostgreSQL
Url:		https://github.com/dalibo/%{sname}/
Source0:	https://github.com/dalibo/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildArch:	noarch
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif
Requires:	nagios-plugins
Provides:	%{sname} = %{version}

%description
check_patroni is a monitoring plugin of patroni for Nagios.

%prep
%setup -q -n %{sname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%defattr(-,root,root,0755)
%doc docs
%license LICENSE
%{_bindir}/%{sname}
%{python3_sitelib}/%{sname}/*.py
%{python3_sitelib}/%{sname}-%{version}.dist-info/
%{python3_sitelib}/%{sname}/__pycache__/*.pyc

%changelog
* Wed Oct 15 2025 Devrim Gündüz <devrim@gunduz.org> 2.2.0-3PGDG
- Fix builds on SLES

* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> 2.2.0-2PGDG
- Add SLES 16 support
- Use Python 3.1x on all platforms
- Switch to pyproject build

* Sun Apr 13 2025 Devrim Gündüz <devrim@gunduz.org> 2.2.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository
