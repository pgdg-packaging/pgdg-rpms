%global __python %{_bindir}/python3
%global sname powa-web
%global swebname powa

%global	powawebdir	%{_datadir}/%{name}

%global __ospython %{_bindir}/python3
%if 0%{?fedora} >= 42 || 0%{?rhel} >= 10 || 0%{?suse_version} == 1600
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif

Summary:	The user interface of PoWA
Name:		%{sname}
Version:	5.3.0
Release:	2PGDG%{?dist}
License:	BSD
Source0:	https://github.com/powa-team/powa-web/archive/refs/tags/%{version}.tar.gz
Source2:	%{sname}.service
URL:		https://powa.readthedocs.io/
Requires:	python3-tornado python3-sqlalchemy

Requires:		systemd
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd

BuildRequires:		python3-devel

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
%dir %{python_sitelib}/%{swebname}
%{python_sitelib}/%{swebname}/*
%{python_sitelib}/powa_web-%{version}.dist-info/
%{_sysconfdir}/powa-web.conf-dist
%{_unitdir}/%{sname}.service

%changelog
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
