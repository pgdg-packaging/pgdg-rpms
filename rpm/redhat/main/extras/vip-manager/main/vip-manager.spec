%global		debug_package %{nil}
%global		_missing_build_ids_terminate_build 0

# Upstream does not provide tarballs for ppc64le:
ExcludeArch:	ppc64le

%ifarch x86_64
%global		tarballarch x86_64
%endif
%ifarch aarch64
%global		tarballarch arm64
%endif

Summary:	Manages a virtual IP for Patroni based on state kept in etcd or Consul
Name:		vip-manager
Version:	4.0.0
Release:	1PGDG%{?dist}
License:	BSD2
URL:		https://github.com/cybertec-postgresql/%{name}

Source0:	https://github.com/cybertec-postgresql/%{name}/releases/download/v%{version}/%{name}_%{version}_Linux_%{tarballarch}.tar.gz
Source2:	%{name}.service

BuildRequires:	systemd
Requires:	systemd


%description
Manages a virtual IP for Patroni based on state kept in etcd or Consul

%prep
%setup -q -n %{name}_%{version}_Linux_%{tarballarch}

%build

%install
%{__mkdir} -p %{buildroot}/%{_bindir}
%{__cp} %{name} %{buildroot}/%{_bindir}
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/%{name}/
%{__cp} %{name}.yml %{buildroot}/%{_sysconfdir}/%{name}/
%{__mkdir} -p %{buildroot}/%{_sharedstatedir}/%{name}

%{__mkdir} -p %{buildroot}/%{_unitdir}
%{__cp} %{SOURCE2} %{buildroot}/%{_unitdir}/

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root,-)
%dir %attr(750, root, root) %{_sysconfdir}/%{name}
%config(noreplace) %attr(640, root, root) %{_sysconfdir}/%{name}/*yml
%dir %attr(750, root, root) %{_sharedstatedir}/%{name}
%{_unitdir}/%{name}.service
%attr(755, root, root) %{_bindir}/%{name}
%doc

%changelog
* Wed Jun 18 2025 Devrim Gündüz <devrim@gunduz.org> 4.0.0-1PGDG
- Update to 4.0.0 per changes described at:
  https://github.com/cybertec-postgresql/vip-manager/releases/tag/v4.0.0

* Wed Dec 11 2024 Devrim Gündüz <devrim@gunduz.org> 3.0.0-1PGDG
- Update to 3.0.0 per changes described at:
  https://github.com/cybertec-postgresql/vip-manager/releases/tag/v3.0.0

* Mon Oct 28 2024 Devrim Gündüz <devrim@gunduz.org> 2.8.0-1PGDG
- Update to 2.8.0 per changes described at:
  https://github.com/cybertec-postgresql/vip-manager/releases/tag/v2.8.0

* Wed Sep 25 2024 Devrim Gündüz <devrim@gunduz.org> 2.7.0-1PGDG
- Update to 2.7.0 per changes described at:
  https://github.com/cybertec-postgresql/vip-manager/releases/tag/v2.7.0
- Make sure that config files is not overwritten during updates, per:
  https://redmine.postgresql.org/issues/8039

* Fri Jul 26 2024 Devrim Gündüz <devrim@gunduz.org> 2.6.0-1PGDG
- Update to 2.6.0 per changes described at:
  https://github.com/cybertec-postgresql/vip-manager/releases/tag/v2.6.0

* Mon May 20 2024 Devrim Gündüz <devrim@gunduz.org> 2.5.0-1PGDG
- Update to 2.5.0 per changes described at:
  https://github.com/cybertec-postgresql/vip-manager/releases/tag/v2.5.0

* Fri Apr 26 2024 Devrim Gündüz <devrim@gunduz.org> 2.4.0-1PGDG
- Update to 2.4.0 per changes described at:
  https://github.com/cybertec-postgresql/vip-manager/releases/tag/v2.4.0

* Mon Jan 22 2024 Devrim Gündüz <devrim@gunduz.org> 2.3.0-1PGDG
- Update to 2.3.0 per changes described at:
  https://github.com/cybertec-postgresql/vip-manager/releases/tag/v2.3.0

* Thu Jan 11 2024 Devrim Gündüz <devrim@gunduz.org> 2.2.0-1PGDG
- Update to 2.2.0 per changes described at:
  https://github.com/cybertec-postgresql/vip-manager/releases/tag/v2.2.0

* Tue Jun 20 2023 Devrim Gündüz <devrim@gunduz.org> 2.1.0-1PGDG
- Initial packaging for PostgreSQL RPM Repository
