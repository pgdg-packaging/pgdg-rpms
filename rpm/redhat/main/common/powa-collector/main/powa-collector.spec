%global sname powa-collector
%global pname powa_collector

%global __ospython %{_bindir}/python3

Name:		powa-collector
Version:	1.3.1
Release:	2PGDG%{?dist}
Summary:	POWA data collector daemon
License:	PostgreSQL
URL:		https://github.com/powa-team/%{name}
Source0:	https://github.com/powa-team/%{name}/archive/%{version}.tar.gz
Source1:	%{name}.service
Source2:	%{sname}-tmpfiles.d

BuildRequires:	python3-devel python3-wheel
BuildRequires:	systemd-rpm-macros
Requires:	python3-psycopg2 systemd

BuildArch:	noarch

# We require this to be present for %%{_prefix}/lib/tmpfiles.d
Requires:		systemd
%if 0%{?suse_version} >= 1500
Requires(post):		systemd-sysvinit
%else
Requires(post):		systemd-sysv
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
%endif

%description
This is a simple multi-threaded python program that performs the
snapshots for all the remote servers configured in a powa repository
database (in the powa_servers table).

%prep
%setup -q -n %{name}-%{version}

%if 0%{?fedora} >= 40 || 0%{?rhel} >= 8
%generate_buildrequires
%pyproject_buildrequires -t
%endif

%build
%pyproject_wheel

%install
%pyproject_install

# Install sample config file:
%{__install} -d %{buildroot}%{_sysconfdir}
%{__install} -m 644 powa-collector.conf-dist %{buildroot}%{_sysconfdir}/

# Install unit file
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/

# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}/%{_tmpfilesdir}
%{__install} -m 0644 %{SOURCE2} %{buildroot}/%{_tmpfilesdir}/%{sname}.conf

%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1500
%service_add_pre %{name}.service
%endif
%else
%systemd_post %{name}.service
%endif

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{_bindir}/%{name}.py
%{_sysconfdir}/%{name}.conf-dist
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{sname}.conf
%{python3_sitelib}/%{pname}/*.py
%{python3_sitelib}/%{pname}/__pycache__/*.py*
%{python3_sitelib}/%{pname}-%{version}.dist-info/*

%changelog
* Mon Mar 24 2025 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-2PGDG
- Add missing BRs

* Sun Mar 23 2025 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-1PGDG
- Update to 1.3.1 per changes described at:
  https://github.com/powa-team/powa-collector/releases/tag/1.3.1

* Tue Dec 17 2024 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-2PGDG
- Add RHEL 10 support

* Sun Nov 3 2024 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-1PGDG
- Update to 1.3.0 per changes described at:
  https://github.com/powa-team/powa-collector/releases/tag/1.3.0

* Wed Sep 20 2023 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository
