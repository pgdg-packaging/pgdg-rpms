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

%global sname check_patroni

Name:		nagios-plugins-patroni
Version:	2.2.0
Release:	6PGDG%{dist}
Summary:	Patroni monitoring plugin for Nagios
License:	PostgreSQL
Url:		https://github.com/dalibo/%{sname}/
Source0:	https://github.com/dalibo/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildArch:	noarch
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
# python%%{python3_pkgversion}-devel is what pulls python3-rpm-generators
# into the buildroot on RHEL/Fedora; pyproject-rpm-macros alone does not.
# Without it, neither python(abi) nor python%%{python3_pkgversion}dist(...)
# get generated. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/228
BuildRequires:	python%{python3_pkgversion}-devel
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
* Fri Aug 28 2026 Devrim Gunduz <devrim@gunduz.org> - 2.2.0-6PGDG
- Add back python%{python3_pkgversion}-devel as a BuildRequires on the
  non-SLES branch, needed to pull python3-rpm-generators into the
  buildroot for this pyproject build. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/228

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 2.2.0-5PGDG
- Also set __python3 (not just __ospython) for Amazon Linux 2023, so
  %pyproject_wheel/%pyproject_install actually build against python3.13
  instead of silently falling back to the system default python3
  (__ospython only affects this repo's own macro computations, not
  RPM's own pyproject/site-packages macros).

* Tue Aug 25 2026 Devrim Gündüz <devrim@gunduz.org> 2.2.0-4PGDG
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Wed Oct 15 2025 Devrim Gündüz <devrim@gunduz.org> 2.2.0-3PGDG
- Fix builds on SLES

* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> 2.2.0-2PGDG
- Add SLES 16 support
- Use Python 3.1x on all platforms
- Switch to pyproject build

* Sun Apr 13 2025 Devrim Gündüz <devrim@gunduz.org> 2.2.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository
