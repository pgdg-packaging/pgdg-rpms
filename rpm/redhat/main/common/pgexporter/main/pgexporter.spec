Name:		pgexporter
Version:	0.6.1
Release:	1PGDG%{dist}
Summary:	Prometheus exporter for PostgreSQL
License:	BSD
URL:		https://github.com/%{name}/%{name}
Source0:	https://github.com/%{name}/%{name}/archive/%{version}.tar.gz

BuildRequires:	gcc cmake3 make python3-docutils
BuildRequires:	libev libev-devel openssl openssl-devel systemd systemd-devel
BuildRequires:	libyaml-devel
Requires:	libev libyaml openssl systemd

%description
Prometheus exporter for PostgreSQL

%prep
%setup -q

%build
%{__mkdir} build
cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
%{__make}

%install

%{__mkdir} -p %{buildroot}%{_sysconfdir}
%{__mkdir} -p %{buildroot}%{_bindir}
%{__mkdir} -p %{buildroot}%{_libdir}
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/etc
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/shell_comp
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/tutorial
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/yaml
%{__mkdir} -p %{buildroot}%{_mandir}/man1
%{__mkdir} -p %{buildroot}%{_mandir}/man5
%{__mkdir} -p %{buildroot}%{_sysconfdir}/%{name}

%{__install} -m 644 %{_builddir}/%{name}-%{version}/LICENSE %{buildroot}%{_docdir}/%{name}/LICENSE
%{__install} -m 644 %{_builddir}/%{name}-%{version}/CODE_OF_CONDUCT.md %{buildroot}%{_docdir}/%{name}/CODE_OF_CONDUCT.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/README.md %{buildroot}%{_docdir}/%{name}/README.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/ARCHITECTURE.md %{buildroot}%{_docdir}/%{name}/ARCHITECTURE.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/CLI.md %{buildroot}%{_docdir}/%{name}/CLI.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/CONFIGURATION.md %{buildroot}%{_docdir}/%{name}/CONFIGURATION.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/GETTING_STARTED.md %{buildroot}%{_docdir}/%{name}/GETTING_STARTED.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/RPM.md %{buildroot}%{_docdir}/%{name}/RPM.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/YAML.md %{buildroot}%{_docdir}/%{name}/YAML.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/etc/%{name}.service %{buildroot}%{_docdir}/%{name}/etc/%{name}.service
%{__install} -m 644 %{_builddir}/%{name}-%{version}/contrib/shell_comp/pgexporter_comp.* %{buildroot}%{_docdir}/%{name}/shell_comp/
%{__install} -m 644 %{_builddir}/%{name}-%{version}/contrib/yaml/postgresql-*.yaml %{buildroot}%{_docdir}/%{name}/yaml/
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/tutorial/*.md %{buildroot}%{_docdir}/%{name}/tutorial/

%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/etc/%{name}.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf

%{__install} -m 644 %{_builddir}/%{name}-%{version}/build/doc/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
%{__install} -m 644 %{_builddir}/%{name}-%{version}/build/doc/%{name}-admin.1 %{buildroot}%{_mandir}/man1/%{name}-admin.1
%{__install} -m 644 %{_builddir}/%{name}-%{version}/build/doc/%{name}-cli.1 %{buildroot}%{_mandir}/man1/%{name}-cli.1
%{__install} -m 644 %{_builddir}/%{name}-%{version}/build/doc/%{name}.conf.5 %{buildroot}%{_mandir}/man5/%{name}.conf.5

%{__install} -m 755 %{_builddir}/%{name}-%{version}/build/src/%{name} %{buildroot}%{_bindir}/%{name}
%{__install} -m 755 %{_builddir}/%{name}-%{version}/build/src/%{name}-cli %{buildroot}%{_bindir}/%{name}-cli
%{__install} -m 755 %{_builddir}/%{name}-%{version}/build/src/%{name}-admin %{buildroot}%{_bindir}/%{name}-admin

%{__install} -m 755 %{_builddir}/%{name}-%{version}/build/src/libpgexporter.so.%{version} %{buildroot}%{_libdir}/libpgexporter.so.%{version}

chrpath -r %{_libdir} %{buildroot}%{_bindir}/%{name}
chrpath -r %{_libdir} %{buildroot}%{_bindir}/%{name}-cli
chrpath -r %{_libdir} %{buildroot}%{_bindir}/%{name}-admin

cd %{buildroot}%{_libdir}/
%{__ln_s} -f libpgexporter.so.%{version} libpgexporter.so.0
%{__ln_s} -f libpgexporter.so.0 libpgexporter.so

%files
%license %{_docdir}/%{name}/LICENSE
%{_docdir}/%{name}/*.md
%{_docdir}/%{name}/etc/%{name}.service
%{_docdir}/%{name}/shell_comp/*
%{_docdir}/%{name}/yaml/postgresql-*.yaml
%{_docdir}/%{name}/tutorial/*.md
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

