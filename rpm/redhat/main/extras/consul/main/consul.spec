%if 0%{?fedora} >= 40 || 0%{?rhel} >= 8
%global		debug_package %{nil}
%global		_missing_build_ids_terminate_build 0
%endif

# Consul does not provide tarballs for ppc64le:
ExcludeArch:	ppc64le

%ifarch x86_64
%global		tarballarch amd64
%endif
%ifarch aarch64
%global		tarballarch arm64
%endif

Name:		consul
Version:	1.21.0
Release:	1PGDG%{?dist}
Summary:	Consul is a tool for service discovery and configuration. Consul is distributed, highly available, and extremely scalable.

License:	MPLv2.0
URL:		http://www.consul.io
Source0:	https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_%{tarballarch}.zip
Source1:	%{name}.sysconfig
Source2:	%{name}.service
Source4:	%{name}.json
Source5:	%{name}.logrotate

BuildRequires:	systemd
Requires:	systemd
%if 0%{?fedora} >= 37 || 0%{?rhel} >= 7
Requires(pre):	shadow-utils
%endif
%if 0%{?suse_version} >= 1315
Requires(pre):	shadow
%endif

%description
Consul is a tool for service discovery and configuration. Consul is
distributed, highly available, and extremely scalable.

Consul provides several key features:
 - Service Discovery - Consul makes it simple for services to register
themselves and to discover other services via a DNS or HTTP interface.
External services such as SaaS providers can be registered as well.
 - Health Checking - Health Checking enables Consul to quickly alert
operators about any issues in a cluster. The integration with service
discovery prevents routing traffic to unhealthy hosts and enables service
level circuit breakers.
 - Key/Value Storage - A flexible key/value store enables storing dynamic
configuration, feature flagging, coordination, leader election and more.
The simple HTTP API makes it easy to use anywhere.
 - Multi-Datacenter - Consul is built to be datacenter aware, and can support
any number of regions without complex configuration.

%prep
%setup -q -c

%build

%install
%{__mkdir} -p %{buildroot}/%{_bindir}
%{__cp} consul %{buildroot}/%{_bindir}
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/%{name}.d
%{__cp} %{SOURCE4} %{buildroot}/%{_sysconfdir}/%{name}.d/consul.json-dist.hcl
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/sysconfig
%{__cp} %{SOURCE1} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
%{__mkdir} -p %{buildroot}/%{_sharedstatedir}/%{name}

%{__mkdir} -p %{buildroot}/%{_unitdir}
%{__cp} %{SOURCE2} %{buildroot}/%{_unitdir}/

%pre
getent group consul >/dev/null || groupadd -r consul
getent passwd consul >/dev/null || \
    useradd -r -g consul -d /var/lib/consul -s /sbin/nologin \
    -c "consul.io user" consul
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root,-)
%dir %attr(750, root, consul) %{_sysconfdir}/%{name}.d
%attr(640, root, consul) %{_sysconfdir}/%{name}.d/consul.json-dist.hcl
%dir %attr(750, consul, consul) %{_sharedstatedir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_unitdir}/%{name}.service
%attr(755, root, root) %{_bindir}/consul
%doc

%changelog
* Wed May 7 2025 Devrim Gündüz <devrim@gunduz.org> 1.21.0-1PGDG
- Update to 1.21.0 per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.21.0

* Mon Apr 28 2025 Devrim Gündüz <devrim@gunduz.org> 1.20.6-1PGDG
- Update to 1.20.6 per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.20.6

* Thu Mar 13 2025 Devrim Gündüz <devrim@gunduz.org> 1.20.5-1PGDG
- Update to 1.20.5 per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.20.5

* Thu Feb 20 2025 Devrim Gündüz <devrim@gunduz.org> 1.20.4-1PGDG
- Update to 1.20.4 per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.20.4

* Sun Feb 16 2025 Devrim Gündüz <devrim@gunduz.org> 1.20.3-1PGDG
- Update to 1.20.3 per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.20.3

* Mon Jan 6 2025 Devrim Gündüz <devrim@gunduz.org> 1.20.2-1PGDG
- Update to 1.20.2 per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.20.2

* Fri Nov 1 2024 Devrim Gündüz <devrim@gunduz.org> 1.20.1-1PGDG
- Update to 1.20.1 per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.20.1

* Tue Oct 15 2024 Devrim Gündüz <devrim@gunduz.org> 1.20.0-1PGDG
- Update to 1.20.0 per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.20.0

* Thu Aug 29 2024 Devrim Gündüz <devrim@gunduz.org> 1.19.2-1PGDG
- Update to 1.19.2 per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.19.2

* Fri Jul 12 2024 Devrim Gündüz <devrim@gunduz.org> 1.19.1-1PGDG
- Update to 1.19.1, per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.19.1

* Fri Jun 14 2024 Devrim Gündüz <devrim@gunduz.org> 1.19.0-1PGDG
- Update to 1.19.0, per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.19.0

* Mon May 20 2024 Devrim Gündüz <devrim@gunduz.org> 1.18.2-1PGDG
- Update to 1.18.2, per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.18.2

* Fri Mar 29 2024 Devrim Gündüz <devrim@gunduz.org> 1.18.1-1PGDG
- Update to 1.18.1, per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.18.1

* Thu Feb 29 2024 Devrim Gündüz <devrim@gunduz.org> 1.18.0-1PGDG
- Update to 1.18.0, per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.18.0

* Wed Feb 21 2024 Devrim Gündüz <devrim@gunduz.org> 1.17.3-1PGDG
- Update to 1.17.3, per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.17.3
- Enable builds on SLES-15.

* Tue Jan 23 2024 Devrim Gündüz <devrim@gunduz.org> 1.17.2-1PGDG
- Update to 1.17.2, per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.17.2

* Fri Dec 15 2023 Devrim Gündüz <devrim@gunduz.org> 1.17.1-1PGDG
- Update to 1.17.1, per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.17.1

* Thu Nov 9 2023 Devrim Gündüz <devrim@gunduz.org> 1.17.0-1PGDG
- Update to 1.17.0, per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.17.0

* Thu Nov 2 2023 Devrim Gündüz <devrim@gunduz.org> 1.16.3-1PGDG
- Update to 1.16.3, per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.16.3

* Wed Sep 20 2023 Devrim Gündüz <devrim@gunduz.org> 1.16.2-1PGDG
- Update to 1.16.2, per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.16.2

* Wed Aug 9 2023 Devrim Gündüz <devrim@gunduz.org> 1.16.1-1PGDG
- Update to 1.16.1, per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.16.1

* Mon Jul 3 2023 Devrim Gündüz <devrim@gunduz.org> 1.16.0-1
- Update to 1.16.0, per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.16.0
- Add PGDG branding

* Fri Jun 2 2023 Devrim Gündüz <devrim@gunduz.org> 1.15.3-1
- Update to 1.15.3, per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.15.3
- Add SLES 15 support.

* Mon Apr 10 2023 Devrim Gündüz <devrim@gunduz.org> 1.15.2-1
- Update to 1.15.2, per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.15.2

* Sun Mar 12 2023 Devrim Gündüz <devrim@gunduz.org> 1.15.1-1
- Update to 1.15.1, per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.15.1

* Mon Feb 27 2023 Devrim Gündüz <devrim@gunduz.org> 1.15.0-1
- Update to 1.15.0, per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.15.0

* Mon Jan 30 2023 Devrim Gündüz <devrim@gunduz.org> 1.14.4-1
- Update to 1.14.4, per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.14.4

* Thu Dec 15 2022 Devrim Gündüz <devrim@gunduz.org> 1.14.3-1
- Update to 1.14.3, per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.14.3

* Wed Nov 23 2022 Devrim Gündüz <devrim@gunduz.org> 1.14.1-1
- Update to 1.14.1, per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.14.1

* Wed Nov 16 2022 Devrim Gündüz <devrim@gunduz.org> 1.14.0-1
- Update to 1.14.0, per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.14.0
- Remove RHEL 6 bits
- Enable builds on aarch64, and make sure that the package is
  not built on ppc64le.

* Fri Oct 21 2022 Devrim Gündüz <devrim@gunduz.org> 1.13.3-1
- Update to 1.13.3, per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.13.3

* Fri Sep 23 2022 Devrim Gündüz <devrim@gunduz.org> 1.13.2-1
- Update to 1.13.2, per changes described at:
  https://github.com/hashicorp/consul/releases/tag/v1.13.2

* Fri Aug 19 2022 Devrim Gündüz <devrim@gunduz.org> 1.13.1-1
- Update to 1.13.1

* Wed Jul 20 2022 Devrim Gündüz <devrim@gunduz.org> 1.12.3-1
- Update to 1.12.3

* Tue May 31 2022 Devrim Gündüz <devrim@gunduz.org> 1.12.1-1
- Update to 1.12.1

* Wed May 11 2022 Devrim Gündüz <devrim@gunduz.org> 1.12.0-1
- Update to 1.12.0

* Wed Apr 20 2022 Devrim Gündüz <devrim@gunduz.org> 1.11.5-1
- Update to 1.11.5

* Fri Mar 11 2022 Devrim Gündüz <devrim@gunduz.org> 1.11.4-1
- Update to 1.11.4

* Fri Oct 1 2021 Devrim Gündüz <devrim@gunduz.org> 1.30.3-1
- Update to 1.10.3

* Fri Oct 2 2020 Devrim Gündüz <devrim@gunduz.org> 1.8.4-1
- Update to 1.8.4

* Thu Aug 6 2020 Devrim Gündüz <devrim@gunduz.org> 1.8.1-1
- Update to 1.8.1
- Disable telemetry.
- Fix config file extension, per Hüseyin Sönmez
- Make sure that consul will restart after a failure, per gripe
  from Hüseyin Sönmez.

* Fri Mar 27 2020 Devrim Gündüz <devrim@gunduz.org> 1.7.2-1
- Update to 1.7.2

* Tue Sep 3 2019 Devrim Gündüz <devrim@gunduz.org> 1.6.0
- Initial packaging for PostgreSQL RPM Repository
