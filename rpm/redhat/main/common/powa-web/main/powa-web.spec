%global __python %{_bindir}/python3
%global sname powa-web
%global swebname powa

%global	powawebdir  %{_datadir}/%{name}

%global __ospython %{_bindir}/python3
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 10
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif
%global python3_sitelib64 %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

Summary:	The user interface of PoWA
Name:		%{sname}
Version:	5.0.2
Release:	1PGDG%{?dist}
License:	BSD
Source0:	https://github.com/powa-team/powa-web/archive/refs/tags/%{version}.tar.gz
Source2:        %{sname}.service
URL:		https://powa.readthedocs.io/
Requires:	python3-tornado python3-sqlalchemy
# We require this to be present for %%{_prefix}/lib/tmpfiles.d
Requires:		systemd
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
Requires(post):		systemd-sysvinit
%endif
%else
Requires(post):		systemd-sysv
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
%endif

BuildRequires:	pgdg-srpm-macros

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
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install -O1 --skip-build --root %{buildroot}

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
%{python_sitelib}/powa_web-%{version}-py%{pyver}.egg-info/*
%{_sysconfdir}/powa-web.conf-dist
%{_unitdir}/%{sname}.service

%changelog
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
