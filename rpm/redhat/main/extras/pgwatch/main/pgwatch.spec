%define		_build_id_links none
%global		debug_package %{nil}
%global		_missing_build_ids_terminate_build 0

# pgwatch does not provide tarballs for ppc64le:
ExclusiveArch:	x86_64 aarch64

%ifarch x86_64
%global		tarballarch x86_64
%endif
%ifarch aarch64
%global		tarballarch arm64
%endif

Name:		pgwatch
Version:	6.0.0
Release:	1PGDG%{?dist}
Summary:	PostgreSQL monitoring metrics collector
License:	BSD-3-Clause
URL:		https://github.com/cybertec-postgresql/%{name}
# The upstream tarball names do not contain the version, so rename them:
Source0:	https://github.com/cybertec-postgresql/%{name}/releases/download/v%{version}/%{name}_Linux_%{tarballarch}.tar.gz#/%{name}-%{version}-Linux-%{tarballarch}.tar.gz
Source1:	https://raw.githubusercontent.com/cybertec-postgresql/%{name}/v%{version}/LICENSE#/%{name}-%{version}-LICENSE
Source2:	%{name}.service
Source3:	%{name}.conf
Source4:	%{name}-sources.yaml
Source6:	%{name}-sysusers.conf
Source7:	%{name}-tmpfiles.d

BuildRequires:	systemd-rpm-macros systemd
Requires:	systemd

Provides:	user(pgwatch) group(pgwatch)

%description
pgwatch is a flexible PostgreSQL-specific monitoring solution. It collects
metrics from PostgreSQL, PgBouncer, Pgpool-II and Patroni using SQL based
metric definitions, and stores them in PostgreSQL, Prometheus or JSON sinks.
Grafana dashboards for visualizing the metrics are included.

%prep
%setup -q -n %{name}_Linux_%{tarballarch}
%{__cp} -p %{SOURCE1} LICENSE

%build

%install
%{__install} -m 0755 -D %{name} %{buildroot}%{_bindir}/%{name}

%{__mkdir} -p %{buildroot}%{_sysconfdir}/%{name}
%{__install} -m 0640 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
%{__install} -m 0640 %{SOURCE4} %{buildroot}%{_sysconfdir}/%{name}/sources.yaml

%{__mkdir} -p %{buildroot}%{_datadir}/%{name}
%{__cp} -pr grafana %{buildroot}%{_datadir}/%{name}/
%{__install} -m 0644 metrics.yaml %{buildroot}%{_datadir}/%{name}/

%{__install} -m 0644 -D %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service

%{__mkdir} -p %{buildroot}%{_sharedstatedir}/%{name}

%{__install} -m 0644 -D %{SOURCE6} %{buildroot}%{_sysusersdir}/%{name}-pgdg.conf

%{__mkdir} -p %{buildroot}%{_tmpfilesdir}
%{__install} -m 0644 %{SOURCE7} %{buildroot}%{_tmpfilesdir}/%{name}.conf

%pre
%sysusers_create_package %{name} %SOURCE6

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root,-)
%doc README.md sample.sources.yaml
%license LICENSE
%dir %attr(750, pgwatch, pgwatch) %{_sysconfdir}/%{name}
%config(noreplace) %attr(640, root, pgwatch) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %attr(640, pgwatch, pgwatch) %{_sysconfdir}/%{name}/sources.yaml
%dir %attr(700, pgwatch, pgwatch) %{_sharedstatedir}/%{name}
%attr(755, root, root) %{_bindir}/%{name}
%{_datadir}/%{name}
%{_sysusersdir}/%{name}-pgdg.conf
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{name}.service

%changelog
* Mon Oct 12 2026 Devrim Gündüz <devrim@gunduz.org> - 6.0.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/360
