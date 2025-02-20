%global		debug_package %{nil}

%{expand: %%global py3ver %(python3 -c 'import sys;print(sys.version[0:3])')}
%global __ospython %{_bindir}/python3
%global python3_sitelib %(%{__ospython} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Summary:	A Template for PostgreSQL HA with ZooKeeper, etcd or Consul
Name:		patroni
Version:	4.0.5
Release:	1PGDG%{?dist}
License:	MIT
Source0:	https://github.com/patroni/%{name}/archive/v%{version}.tar.gz
Source1:	%{name}.service
URL:		https://github.com/patroni/%{name}

BuildArch:	noarch

BuildRequires:	python3-setuptools python3-psycopg2 >= 2.5.4

Requires:	python3-cdiff python3-psutil >= 2.0.0
Requires:	python3-psycopg2 >= 2.5.4
Requires:	python3-psutil >= 2.0.0
Requires:	python3-ydiff >= 1.2
Requires:	python3-ydiff <= 1.3

%if 0%{?fedora} >= 40 || 0%{?rhel} >= 8
Requires:	python3-click >= 4.1 python3-six >= 1.7
Requires:	python3-dateutil python3-prettytable >= 0.7
Requires:	python3-pyyaml python3-urllib3 >= 1.19.1
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1499
Requires:	python3-click >= 7.0 python3-six >= 1.7
Requires:	python3-PrettyTable >= 0.7 python3-PyYAML
Requires:	python3-python-dateutil python3-urllib3 >= 1.19.1
%endif
%endif

%description
Patroni is a template for you to create your own customized,
high-availability solution using Python and - for maximum accessibility - a
distributed configuration store like ZooKeeper, etcd, Consul or Kubernetes.
Database engineers, DBAs, DevOps engineers, and SREs who are looking to
quickly deploy HA PostgreSQL in the datacenter-or anywhere else-will
hopefully find it useful.

We call Patroni a "template" because it is far from being a
one-size-fits-all or plug-and-play replication system. It will have its own
caveats. Use wisely.

%package -n %{name}-consul
Summary:	Related components to use patroni with Consul
Requires:	%{name} = %{version}-%{release}
Requires:	consul python3-requests

%if 0%{?fedora} >= 40 || 0%{?rhel} >= 8
Requires:	python3-consul >= 0.7.1
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1499
Requires:	python3-python-consul
%endif
%endif

%description -n %{name}-consul
Meta package to pull consul related dependencies for patroni

%package -n %{name}-etcd
Summary:	Related components to use patroni with etcd
Requires:	%{name} = %{version}-%{release}
Requires:	python3-etcd >= 0.4.3

%if 0%{?fedora} >= 40 || 0%{?rhel} >= 8
Requires:	python3-dns python3-certifi
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1499
Requires:	python3-dnspython
%endif
%endif

%description -n %{name}-etcd
Meta package to pull etcd related dependencies for patroni

%package -n %{name}-aws
Summary:	Related components to use patroni on AWS
Requires:	%{name} = %{version}-%{release}
Requires:	python3-boto3

%description -n %{name}-aws
Meta package to pull AWS related dependencies for patroni

%package -n %{name}-zookeeper
Summary:	Related components to use patroni with Zookeeper
Requires:	%{name} = %{version}-%{release}
Requires:	python3-kazoo >= 1.3.1

%description -n %{name}-zookeeper
Meta package to pull zookeeper related dependencies for patroni

%prep
%setup -q
%build
%{__ospython} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__ospython} setup.py install --root %{buildroot} -O1 --skip-build

# Install sample yml files:
%{__mkdir} -p %{buildroot}%{docdir}/%{name}
%{__cp} postgres0.yml postgres1.yml %{buildroot}%{docdir}/%{name}

# Install unit file:
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

# We don't need to ship this file, per upstream:
%{__rm} -f %{buildroot}%{_bindir}/patroni_wale_restore

%post
%{__mkdir} -p /var/log/patroni
%{__mkdir} -p /etc/patroni/callbacks
touch /etc/patroni/callbacks/callbacks.sh
if [ $1 -eq 1 ] ; then
   /bin/systemctl daemon-reload >/dev/null 2>&1 || :
   %if 0%{?suse_version}
   %if 0%{?suse_version} >= 1315
   %service_add_pre %{name}.service
   %endif
   %else
   %systemd_post %{name}.service
   %endif
fi

%preun
if [ $1 -eq 0 ] ; then
	# Package removal, not upgrade
	/bin/systemctl --no-reload disable %{name}.service >/dev/null 2>&1 || :
	/bin/systemctl stop %{name}.service >/dev/null 2>&1 || :
fi

%postun
 /bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
	# Package upgrade, not uninstall
	/bin/systemctl try-restart %{name}.service >/dev/null 2>&1 || :
fi

%files
%defattr(644,root,root,755)
%license LICENSE
%doc docs README.rst postgres0.yml postgres1.yml
%attr (755,root,root) %{_bindir}/patroni
%attr (755,root,root) %{_bindir}/patronictl
%attr (755,root,root) %{_bindir}/patroni_barman
%attr (755,root,root) %{_bindir}/patroni_raft_controller
%{_unitdir}/%{name}.service
%{python3_sitelib}/%{name}*.egg-info
%dir %{python3_sitelib}/%{name}/
%{python3_sitelib}/%{name}/*

%files -n %{name}-aws
%attr (755,root,root) %{_bindir}/patroni_aws

%files -n %{name}-consul

%files -n %{name}-etcd

%files -n %{name}-zookeeper

%changelog
* Thu Feb 20 2025 Devrim Gündüz <devrim@gunduz.org> - 4.0.5-1PGDG
- Update to 4.0.5, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-405

* Mon Dec 16 2024 Devrim Gündüz <devrim@gunduz.org> - 4.0.4-2PGDG
- Update URL

* Fri Nov 22 2024 Devrim Gündüz <devrim@gunduz.org> - 4.0.4-1PGDG
- Update to 4.0.4, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-404

* Sat Oct 19 2024 Devrim Gündüz <devrim@gunduz.org> - 4.0.3-1PGDG
- Update to 4.0.3, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-403

* Tue Sep 17 2024 Devrim Gündüz <devrim@gunduz.org> - 4.0.2-1PGDG
- Update to 4.0.2, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-402

* Fri Aug 30 2024 Devrim Gündüz <devrim@gunduz.org> - 4.0.1-1PGDG
- Update to 4.0.1, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-401
- Fix boto3 dependency for the aws subpackage.

* Fri Aug 30 2024 Devrim Gündüz <devrim@gunduz.org> - 4.0.0-1PGDG
- Update to 4.0.0, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-400

* Fri Jul 12 2024 Devrim Gündüz <devrim@gunduz.org> - 3.3.2-1PGDG
- Update to 3.3.2, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-332

* Tue Jun 25 2024 Devrim Gündüz <devrim@gunduz.org> - 3.3.1-1PGDG
- Update to 3.3.1, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-331

* Fri Apr 5 2024 Devrim Gündüz <devrim@gunduz.org> - 3.3.0-1PGDG
- Update to 3.3.0, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-330

* Fri Jan 19 2024 Devrim Gündüz <devrim@gunduz.org> - 3.2.2-1PGDG
- Update to 3.2.2, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-322

* Mon Dec 4 2023 Devrim Gündüz <devrim@gunduz.org> - 3.2.1-1PGDG
- Update to 3.2.1, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-321

* Thu Oct 26 2023 Devrim Gündüz <devrim@gunduz.org> - 3.2.0-1PGDG
- Update to 3.2.0, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-320

* Wed Oct 4 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.2-1PGDG
- Update to 3.1.2, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-312

* Wed Sep 20 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.1-1PGDG
- Update to 3.1.1, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-311

* Fri Aug 4 2023 Devrim Gündüz <devrim@gunduz.org> - 3.1.0-1PGDG
- Update to 3.1.0, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-310
- Build package as noarch, per request and patch from Matt Baker:
  https://redmine.postgresql.org/issues/7833

* Thu Jul 20 2023 Devrim Gündüz <devrim@gunduz.org> - 3.0.4-1PGDG
- Update to 3.0.4, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-304

* Fri Jun 30 2023 Devrim Gündüz <devrim@gunduz.org> - 3.0.3-2PGDG
- Go back to psycopg2. There are some issues with psycopg3 (could be
  our package). Per report from Magnus Hagander.

* Tue Jun 27 2023 Devrim Gündüz <devrim@gunduz.org> - 3.0.3-1PGDG
- Update to 3.0.3, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-303
- Switch to psycopg3
- Add PGDG branding

* Fri Mar 31 2023 Devrim Gündüz <devrim@gunduz.org> - 3.0.2-1
- Update to 3.0.2, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-302

* Fri Mar 24 2023 Devrim Gündüz <devrim@gunduz.org> - 3.0.1-2
- Move urllib3 dependency to main package, per report from Matt Baker.
  Fixes https://redmine.postgresql.org/issues/7782 .

* Tue Feb 28 2023 Devrim Gündüz <devrim@gunduz.org> - 3.0.1-1
- Update to 3.0.1, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-301

* Wed Feb 15 2023 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-2
- Fix post section, use actual directory names.

* Thu Feb 9 2023 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-1
- Update to 3.0.0, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-300

* Thu Jan 5 2023 Devrim Gündüz <devrim@gunduz.org> - 2.1.7-2
- Add SLES 15 support

* Wed Jan 4 2023 Devrim Gündüz <devrim@gunduz.org> - 2.1.7-1
- Update to 2.1.7, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-217
- Remove etcd dependency from patroni-etcd subpackage, per:
  https://github.com/zalando/patroni/issues/2477

* Wed Nov 30 2022 Devrim Gündüz <devrim@gunduz.org> - 2.1.5-1
- Update to 2.1.5, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-215

* Sun Sep 4 2022 Devrim Gündüz <devrim@gunduz.org> - 2.1.4-2
- Now that we have etcd package in PGDG RHEL extras repo, patroni-etcd
  subpackage will pull it.

* Wed Jun 1 2022 Devrim Gündüz <devrim@gunduz.org> - 2.1.4-1
- Update to 2.1.4, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-214

* Mon Feb 28 2022 Devrim Gündüz <devrim@gunduz.org> - 2.1.3-1
- Update to 2.1.3, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-213

* Mon Dec 6 2021 Devrim Gündüz <devrim@gunduz.org> - 2.1.2-1
- Update to 2.1.2, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-212

* Fri Oct 1 2021 Devrim Gündüz <devrim@gunduz.org> - 2.1.1-2
- Create log directory, per Seda Halaçlı.

* Wed Sep 1 2021 Devrim Gündüz <devrim@gunduz.org> - 2.1.1-1
- Update to 2.1.1, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-211

* Tue Jul 6 2021 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-1
- Update to 2.1.0, per changes described at:
  https://github.com/zalando/patroni/blob/master/docs/releases.rst#version-210

* Wed May 26 2021 Devrim Gündüz <devrim@gunduz.org> - 2.0.2-2
- Specify absolute path in WorkingDirectory in the unit file, per:
  https://github.com/zalando/patroni/issues/1688
  https://redmine.postgresql.org/issues/6490

* Mon Feb 22 2021 Devrim Gündüz <devrim@gunduz.org> - 2.0.2-1
- Update to 2.0.2

* Mon Oct 12 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-4
- Add python3-requests dependency, per Julian Markwort

* Thu Oct 1 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-3
- Make sure that we require ydiff >= 1.2.

* Thu Oct 1 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-2
- Add another missing dependency

* Thu Oct 1 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-1
- Update to 2.0.1

* Mon Sep 7 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-2
- Fix another missing dependency (needed by urllib3)

* Mon Sep 7 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-1
- Update to 2.0.0
- Fix missing dependencies, per Alexandre Pereira

* Thu Aug 6 2020 Devrim Gündüz <devrim@gunduz.org> - 1.6.5-4
- Fix RHEL 7 dependencies

* Thu Aug 6 2020 Devrim Gündüz <devrim@gunduz.org> - 1.6.5-3
- Add unit file, per Hüseyin.
- Install sample config files, per Hüseyin.
- Fix BR and Requires, per Alexander.

* Thu Aug 6 2020 Devrim Gündüz <devrim@gunduz.org> - 1.6.5-2
- Add missing requires, per Hüseyin Sönmez.
- Create (meta) subpacakges for consul, etcd, aws and zookeeper,
  per discussion with Hüseyin.

* Wed Aug 5 2020 Devrim Gündüz <devrim@gunduz.org> - 1.6.5-1
- Initial packaging for PostgreSQL RPM repository
