%global sname pgldapsync

%if 0%{?fedora} && 0%{?fedora} == 44
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
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

%if 0%{?fedora} >= 42 || 0%{?rhel} >= 8 || 0%{?suse_version} == 1600 || 0%{?amzn} == 2023
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif

Summary:	A tool for syncing LDAP users to Postgres Roles
Name:		%{sname}
Version:	1.0.0
Release:	12PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/enterprisedb/%{sname}
Source0:	https://github.com/EnterpriseDB/%{sname}/archive/refs/tags/%{sname}-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python3-devel >= 3.5 pgdg-srpm-macros >= 1.0.17

Requires:	libpq5 >= 10.0 python3-psycopg2
Requires:	python3-ldap3

%description
This Python module allows you to synchronise Postgres login roles with users
in an LDAP directory.

pgldapsync requires Python 3.5 or later.

%prep
%setup -q -n %{sname}-%{sname}-%{version}

%build

# Change /usr/bin/python to /usr/bin/python3 in the scripts:
for i in `find . -iname "*.py"`; do sed -i "s/\/usr\/bin\/env python/\/usr\/bin\/env python3/g" $i; done

%{__python3} setup.py build

%install
%{__python3} setup.py install --no-compile --root %{buildroot}
%{__install} -d %{buildroot}%{_sysconfdir}/%{sname}
%{__cp} %{sname}/config_default.ini %{sname}/config.ini.example %{buildroot}%{_sysconfdir}/%{sname}

# Create __pycache__ directories and their contents in SLES and
# Amazon Linux 2023 *too*, since the automatic RPM Python bytecompile
# doesn't reliably compile against the python3.13 alt-stack there:
%if 0%{?suse_version} || 0%{?amzn} == 2023
%py3_compile %{buildroot}%{python3_sitelib}
%endif

%files
%defattr(-,root,root)
%doc README.md
%{_sysconfdir}/%{sname}/*
%{_bindir}/%{sname}
%{python3_sitelib}/%{sname}-%{version}-py%{pyver}.egg-info/*
%{python3_sitelib}/%{sname}/*.py
%{python3_sitelib}/%{sname}/config.ini.example
%{python3_sitelib}/%{sname}/config_default.ini
%{python3_sitelib}/%{sname}/ldaputils/*.py*
%{python3_sitelib}/%{sname}/pgutils/*.py
%{python3_sitelib}/%{sname}/__pycache__/*.pyc
%{python3_sitelib}/%{sname}/ldaputils/__pycache__/*.py*
%{python3_sitelib}/%{sname}/pgutils/__pycache__/*.py*

%changelog
* Thu Aug 27 2026 Devrim Gunduz <devrim@gunduz.org> - 1.0.0-12PGDG
- Explicitly run %py3_compile on Amazon Linux 2023, too, so the
  __pycache__/*.pyc files listed in %files actually exist in the
  buildroot when building against the python3.13 alt-stack.

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 1.0.0-11PGDG
- Also set __python3 (not just __ospython) for Amazon Linux 2023, so
  %pyproject_wheel/%pyproject_install actually build against python3.13
  instead of silently falling back to the system default python3
  (__ospython only affects this repo's own macro computations, not
  RPM's own pyproject/site-packages macros).

* Tue Aug 25 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-10PGDG
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Thu May 7 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-9PGDG
- Now that we use Python 3.1X on all RHEL platforms, updated the
  conditional to fix builds on RHEL 8 and 9.

* Tue Apr 28 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-8PGDG
- Use Python 3.14 on Fedora 44. Many BRs and Requires are not ready
  for 3.15.

* Mon Mar 23 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-7PGDG
- Add SLES 16 and Fedora 44 support

* Tue Dec 17 2024 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-6PGDG
- Add RHEL 10 support and remove RHEL 7 support

* Tue Feb 20 2024 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-5PGDG
- Force creation of __pycache__ directories and their contents in
  SLES *too*.
- Add PGDG branding

* Tue Feb 14 2023 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-4
- Add missing dependencies, per report from Troels Arvin.
  Fixes https://redmine.postgresql.org/issues/7772
- Install sample config files.

* Tue Dec 6 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-3
- Remove Advance Toolchain support from RHEL 7 - ppc64le.

* Tue Nov 2 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-2
- Add Fedora 35 support

* Wed Sep 1 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1
- Initial packaging for the PostgreSQL RPM repository.
