Name:		pgexporter
Version:	0.8.0
Release:	1PGDG%{dist}
Summary:	Prometheus exporter for PostgreSQL
License:	BSD
URL:		https://github.com/%{name}/%{name}
Source0:	https://github.com/%{name}/%{name}/archive/%{version}.tar.gz

BuildRequires:	gcc cmake liburing-devel libyaml-devel make python3-docutils
BuildRequires:	libev libev-devel openssl openssl-devel systemd systemd-devel
Requires:	libev liburing libyaml openssl systemd

%description
Prometheus exporter for PostgreSQL

%prep
%setup -q

%build
%{__mkdir} build
pushd build
%cmake -DCMAKE_BUILD_TYPE=Release -DDOCS=OFF ..
%cmake_build
popd

%install
pushd build
%cmake_install
popd

# Some files require manual installation
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/shell_comp
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/etc/
%{__mkdir} -p %{buildroot}%{_sysconfdir}/%{name}
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/yaml
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/prometheus_scrape
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/grafana
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/grafana/provisioning/dashboards
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/grafana/provisioning/datasources
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/json/

%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/etc/%{name}.service %{buildroot}%{_docdir}/%{name}/etc/%{name}.service
%{__install} -m 644 %{_builddir}/%{name}-%{version}/contrib/shell_comp/pgexporter_comp.* %{buildroot}%{_docdir}/%{name}/shell_comp/
%{__install} -m 644 %{_builddir}/%{name}-%{version}/contrib/yaml/postgresql-*.yaml %{buildroot}%{_docdir}/%{name}/yaml/
%{__install} -m 644 %{_builddir}/%{name}-%{version}/contrib/prometheus_scrape/extra.info %{buildroot}%{_docdir}/%{name}/prometheus_scrape/extra.info
%{__install} -m 644 %{_builddir}/%{name}-%{version}/contrib/prometheus_scrape/prometheus.py %{buildroot}%{_docdir}/%{name}/prometheus_scrape/prometheus.py
%{__install} -m 644 %{_builddir}/%{name}-%{version}/contrib/prometheus_scrape/README.md %{buildroot}%{_docdir}/%{name}/prometheus_scrape/README.md
%{__mv} %{buildroot}/%{_docdir}/%{name}/etc/%{name}.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
%{__install} -m 644 %{_builddir}/%{name}-%{version}/contrib/grafana/*.json %{buildroot}%{_docdir}/%{name}/grafana/
%{__install} -m 644 %{_builddir}/%{name}-%{version}/contrib/grafana/*.yml %{buildroot}%{_docdir}/%{name}/grafana/
%{__install} -m 644 %{_builddir}/%{name}-%{version}/contrib/grafana/provisioning/dashboards/*.yml %{buildroot}%{_docdir}/%{name}/grafana/provisioning/dashboards/
%{__install} -m 644 %{_builddir}/%{name}-%{version}/contrib/grafana/provisioning/datasources/*.yml %{buildroot}%{_docdir}/%{name}/grafana/provisioning/datasources/
%{__install} -m 644 %{_builddir}/%{name}-%{version}/contrib/grafana/README.md %{buildroot}%{_docdir}/%{name}/grafana/README.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/contrib/grafana/TESTING.md %{buildroot}%{_docdir}/%{name}/grafana/TESTING.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/contrib/json/*.json %{buildroot}%{_docdir}/%{name}/json/

cd %{buildroot}%{_libdir}/
%{__ln_s} -f libpgexporter.so.%{version} libpgexporter.so.0
%{__ln_s} -f libpgexporter.so.0 libpgexporter.so

%files
%license LICENSE
%{_docdir}/%{name}/*.md
%{_docdir}/%{name}/etc/%{name}.service
%{_docdir}/%{name}/shell_comp/*
%{_docdir}/%{name}/yaml/postgresql-*.yaml
%{_docdir}/%{name}/prometheus_scrape/extra.info
%{_docdir}/%{name}/prometheus_scrape/prometheus.py
%{_docdir}/%{name}/prometheus_scrape/README.md
%{_docdir}/%{name}/json/
%{_docdir}/%{name}/grafana/
%{_datadir}/%{name}/extensions/*.yaml
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}-admin.1*
%{_mandir}/man1/%{name}-cli.1*
%{_mandir}/man5/%{name}.conf.5*
%config %{_sysconfdir}/%{name}/%{name}.conf
%{_bindir}/%{name}
%{_bindir}/%{name}-cli
%{_bindir}/%{name}-admin
%{_libdir}/libpgexporter.so
%{_libdir}/libpgexporter.so.0
%{_libdir}/libpgexporter.so.%{version}

%changelog
* Thu Apr 30 2026 - Devrim Gündüz <devrim@gunduz.org> 0.8.0-1PGDG
- Update to 0.8.0 per changes described at:
  https://github.com/pgexporter/pgexporter/releases/tag/0.8.0
  Fixes: https://github.com/pgdg-packaging/pgdg-rpms/issues/187

* Tue Apr 28 2026 - Devrim Gündüz <devrim@gunduz.org> 0.7.0-2PGDG
- Simplify build system
- Fix builds against CMake 4, per https://github.com/pgdg-packaging/pgdg-rpms/issues/167

* Thu Sep 11 2025 - Devrim Gündüz <devrim@gunduz.org> 0.7.0-1PGDG
- Update to 0.7.0 per changes described at:
  https://github.com/pgexporter/pgexporter/releases/tag/0.7.0
  Fixes: https://github.com/pgdg-packaging/pgdg-rpms/issues/79

* Tue Feb 11 2025 - Devrim Gündüz <devrim@gunduz.org> 0.6.1-1PGDG
- Update to 0.6.1 per changes described at:
  https://github.com/pgexporter/pgexporter/releases/tag/0.6.1

* Tue Feb 4 2025 - Devrim Gündüz <devrim@gunduz.org> 0.6.0-1PGDG
- Update to 0.6.0 per changes described at:
  https://github.com/pgexporter/pgexporter/releases/tag/0.6.0

* Tue Feb 13 2024 - Devrim Gündüz <devrim@gunduz.org> 0.5.0-1PGDG
- Update to 0.5.0 per changes described at:
  https://github.com/pgexporter/pgexporter/releases/tag/0.5.0

* Tue Jan 23 2024 - Devrim Gündüz <devrim@gunduz.org> 0.4.1-1PGDG
- Update to 0.4.1 per changes described at:
  https://github.com/pgexporter/pgexporter/releases/tag/0.4.1

* Thu Sep 7 2023 - Devrim Gündüz <devrim@gunduz.org> 0.4.0-1PGDG
- Update to 0.4.0
- Add PGDG branding

* Thu Jan 12 2023 - Devrim Gündüz <devrim@gunduz.org> 0.3.2-1
- Update to 0.3.2

* Thu Nov 3 2022 - Devrim Gündüz <devrim@gunduz.org> 0.3.1-1
- Update to 0.3.1

* Fri Sep 23 2022 - Devrim Gündüz <devrim@gunduz.org> 0.3.0-1
- Update to 0.3.0

* Fri May 27 2022 - Devrim Gündüz <devrim@gunduz.org> 0.2.3-1
- Update to 0.2.3

* Wed Apr 27 2022 - Devrim Gündüz <devrim@gunduz.org> 0.2.2-1
- Update to 0.2.2

* Mon Mar 21 2022 - Devrim Gündüz <devrim@gunduz.org> 0.2.1-1
- Update to 0.2.1

* Fri Oct 22 2021 - Devrim Gündüz <devrim@gunduz.org> 0.2.0-1
- Initial packaging for PostgreSQL RPM repository. Used upstream's
  spec file.

