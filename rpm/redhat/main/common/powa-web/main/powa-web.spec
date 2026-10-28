%pgdg_python3_setup

%global __python %{__python3}
%global sname powa-web
%global swebname powa

%global	powawebdir	%{_datadir}/%{name}

Summary:	The user interface of PoWA
Name:		%{sname}
Version:	5.3.0
Release:	6PGDG%{?dist}
License:	BSD
Source0:	https://github.com/powa-team/powa-web/archive/refs/tags/%{version}.tar.gz
Source2:	%{sname}.service
URL:		https://powa.readthedocs.io/
Requires:	python%{python3_pkgversion}-tornado python%{python3_pkgversion}-psycopg2

Requires:		systemd
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd

BuildRequires:	python%{python3_pkgversion}-devel python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools python%{python3_pkgversion}-wheel
BuildRequires:		systemd-rpm-macros

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif

BuildArch:	noarch

%description
PoWA is PostgreSQL Workload Analyzer that gathers performance stats and
provides real-time charts and graphs to help monitor and tune your PostgreSQL
servers.
It is similar to Oracle AWR or SQL Server MDW.

This is the user interface of POWA.

%prep
%setup -q -n %{sname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

# Install sample conf file
%{__mkdir} -p %{buildroot}%{_sysconfdir}
%{__install} powa-web.conf-dist %{buildroot}%{_sysconfdir}

# Install unit file:
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{sname}.service

%files
%defattr(-,root,root,-)
%{_bindir}/%{sname}
%dir %{python3_sitelib}/%{swebname}
%{python3_sitelib}/%{swebname}/*
%{python3_sitelib}/powa_web-%{version}.dist-info/
%{_sysconfdir}/powa-web.conf-dist
%{_unitdir}/%{sname}.service

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 5.3.0-6PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0, and build and run
  with its Python everywhere, not only on RHEL 8: require
  python%%{python3_pkgversion}-* instead of python3-*. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Fri Oct 23 2026 Devrim Gunduz <devrim@gunduz.org> - 5.3.0-5PGDG
- RHEL 8: BuildRequire the python3.12 packages, as the pyproject macros
  build with Python 3.12 there, not with the default python3 (3.6), and
  require the python3.12 tornado and psycopg2 packages there, as it runs
  with Python 3.12.
- Require psycopg2, which powa-web uses, and not SQLAlchemy, which it has not
  used since 5.0. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Sun Oct 11 2026 Devrim Gunduz <devrim@gunduz.org> - 5.3.0-4PGDG
- Use %%{python3_sitelib} in %%files: the pyproject macros install with
  %%{__python3} (python3.12 on RHEL 8), but %%{python_sitelib} pointed to
  the default python3 (3.6) there. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226
- Add python3-wheel BR.

* Thu Sep 10 2026 Devrim Gunduz <devrim@gunduz.org> - 5.3.0-3PGDG
- Add missing BR

* Fri Aug 28 2026 Devrim Gunduz <devrim@gunduz.org> - 5.3.0-2PGDG
- Package the .dist-info directory itself instead of globbing only its
  contents (dist-info/*), so RHEL/Fedora's pythondist.attr generator
  (which is anchored on the .dist-info directory entry) actually fires
  and emits the correct runtime Requires. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226

* Mon Aug 17 2026 Devrim Gunduz <devrim@gunduz.org> - 5.3.0-1PGDG
- Update to 5.3.0 for changes described at
  https://github.com/powa-team/powa-web/releases/tag/5.3.0

* Mon Jul 13 2026 Devrim Gunduz <devrim@gunduz.org> - 5.2.0-1PGDG
- Update to 5.2.0 for changes described at
  https://github.com/powa-team/powa-web/releases/tag/5.2.0

* Mon Mar 30 2026 Devrim Gunduz <devrim@gunduz.org> - 5.1.4-1PGDG
- Update to 5.1.4 for changes described at
  https://github.com/powa-team/powa-web/releases/tag/5.1.4
  https://github.com/powa-team/powa-web/releases/tag/5.1.3

* Mon Dec 15 2025 Devrim Gunduz <devrim@gunduz.org> - 5.1.2-1PGDG
- Update to 5.1.2 for changes described at
  https://github.com/powa-team/powa-web/releases/tag/5.1.2
- Switch to pyproject builds

* Tue Dec 2 2025 Devrim Gunduz <devrim@gunduz.org> - 5.1.1-1PGDG
- Update to 5.1.1 for changes described at
  https://github.com/powa-team/powa-web/releases/tag/5.1.1

* Mon Nov 24 2025 Devrim Gunduz <devrim@gunduz.org> - 5.1.0-1PGDG
- Update to 5.1.0 for changes described at
  https://github.com/powa-team/powa-web/releases/tag/5.1.0

* Tue Jul 15 2025 Devrim Gunduz <devrim@gunduz.org> - 5.0.2-1PGDG
- Update to 5.0.2 for changes described at
  https://github.com/powa-team/powa-web/releases/tag/5.0.2

* Tue Dec 17 2024 Devrim Gunduz <devrim@gunduz.org> - 5.0.1-2PGDG
- Add RHEL 10 support

* Mon Dec 9 2024 Devrim Gunduz <devrim@gunduz.org> - 5.0.1-1PGDG
- Update to 5.0.1 for changes described at
  https://github.com/powa-team/powa-web/releases/tag/5.0.1

* Tue Nov 12 2024 Devrim Gunduz <devrim@gunduz.org> - 5.0.0-1PGDG
- Update to 5.0.0 for changes described at
  https://github.com/powa-team/powa-web/releases/tag/5.0.0

* Wed Sep 20 2023 Devrim Gunduz <devrim@gunduz.org> - 4.2.0-1PGDG
- Update to 4.2.0
- Trim changelog
