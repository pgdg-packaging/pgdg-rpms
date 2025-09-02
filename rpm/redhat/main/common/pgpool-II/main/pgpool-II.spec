%global	_build_id_links none
%global pgpoolinstdir /usr
%global sname pgpool-II

Summary:		Pgpool is a connection pooling/replication server for PostgreSQL
Name:			%{sname}
Version:		4.6.3
Release:		2PGDG%{?dist}
License:		BSD
URL:			https://pgpool.net
Source0:		https://www.pgpool.net/mediawiki/images/%{sname}-%{version}.tar.gz
Source1:		%{sname}.service
Source2:		%{sname}.sysconfig
Patch1:			%{sname}-conf.sample.patch
Patch2:			%{sname}-gcc-15-c23.patch

BuildRequires:		postgresql%{pgmajorversion}-devel pam-devel
BuildRequires:		libmemcached-devel openssl-devel pgdg-srpm-macros

Requires:		libmemcached
Requires(pre):		/usr/sbin/useradd /usr/sbin/groupadd

BuildRequires:		systemd
# We require this to be present for %%{_prefix}/lib/tmpfiles.d
Requires:		systemd
%if 0%{?suse_version} && 0%{?suse_version} >= 1500
BuildRequires:		openldap2-devel
Requires(post):		systemd-sysvinit
%else
BuildRequires:		openldap-devel
Requires(post):		systemd-sysv
%endif
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd

%description
Pgpool-II is a middleware that works between PostgreSQL servers and a
PostgreSQL database client. It provides the following features:
 * Connection Pooling
 * Replication
 * Load Balancing
 * Limiting Exceeding Connections
 * Watchdog
 * In Memory Query Cache

%package devel
Summary:	The development files for pgpool-II
Requires:	%{name} = %{version}-%{release}

%description devel
Development headers and libraries for pgpool-II.

%package -n %{sname}-pcp
Summary:	PCP (Pgpool Control Protocol) files of Pgpool.

%description -n %{sname}-pcp
PCP (Pgpool Control Protocol) files of Pgpool, shared across
multiple Pgpool installations.

%prep
%setup -q -n %{sname}-%{version}
%patch -P 1 -p0
%patch -P 2 -p1

%build

# We need this flag on SLES so that pgpool can find libmemched.
# Otherwise, we get "libmemcached.so: undefined reference to `pthread_once'" error.
%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
	export LDFLAGS='-lpthread'
%endif
%endif
%ifarch ppc64 ppc64le
%configure --build=ppc64le \
%else
./configure \
%endif
	--prefix /usr \
	--libdir %{_libdir} \
	--disable-static \
	--sysconfdir=%{_sysconfdir}/%{name}/ \
	--with-ldap \
	--with-memcached=%{_includedir}/libmemcached \
	--with-openssl \
	--with-pam \
	--with-pgsql=%{pginstdir}

# https://fedoraproject.org/wiki/Packaging:Guidelines#Removing_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

export PATH=%{pginstdir}/bin/:$PATH
USE_PGXS=1 %{__make} %{?_smp_mflags}
USE_PGXS=1 %{__make} %{?_smp_mflags} -C src/sql/pgpool_adm
USE_PGXS=1 %{__make} %{?_smp_mflags} -C src/sql/pgpool-recovery
USE_PGXS=1 %{__make} %{?_smp_mflags} -C src/sql/pgpool-regclass

%install
export PATH=%{pginstdir}/bin/:$PATH
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install -C src/sql/pgpool_adm
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install -C src/sql/pgpool-recovery
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install -C src/sql/pgpool-regclass

%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 755 %{SOURCE1} %{buildroot}%{_unitdir}/%{sname}.service

# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}%{_tmpfilesdir}
cat > %{buildroot}%{_tmpfilesdir}/%{name}.conf <<EOF
d %{_rundir}/%{name} 0755 postgres postgres -
EOF

# Create the directory for the pid files (defined in pgpool.conf.sample)
%{__install} -d -m 755 %{buildroot}/run/%{name}

%{__install} -d %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# nuke libtool archive and static lib
%{__rm} -f %{buildroot}%{_libdir}/libpcp.{a,la}
# Remove bitcode files
%{__rm} -rf %{buildroot}%{pginstdir}/lib/bitcode/
# Remove extension subpackage files from main package.
# It is distributed as a separate one.
%{__rm} -f %{buildroot}%{pginstdir}/lib/pgpool*
%{__rm} -f %{buildroot}%{pginstdir}/share/extension/pgpool*

%pre
groupadd -g 26 -o -r postgres >/dev/null 2>&1 || :
useradd -M -g postgres -o -r -d /var/lib/pgsql -s /bin/bash \
	-c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || :

%post
/sbin/ldconfig
%systemd_post %{sname}.service

# Create log directory
%{__mkdir} -p /var/log/%{name}
%{__chown} postgres: /var/log/%{name}

%preun
%systemd_preun %{sname}.service

%postun
if [ "$1" -eq 0 ]
then
	/sbin/ldconfig
fi
/sbin/ldconfig

%systemd_postun_with_restart %{sname}.service

%files
%doc README TODO INSTALL AUTHORS ChangeLog NEWS
%license COPYING
%dir %{pgpoolinstdir}
%{_bindir}/pgpool
%{_bindir}/pg_enc
%{_bindir}/pgproto
%{_bindir}/pg_md5
%{_bindir}/pgpool_setup
%{_bindir}/watchdog_setup
%{_datadir}/pgpool-II/insert_lock.sql
%{_datadir}/pgpool-II/pgpool.pam
%{_sysconfdir}/%{name}/*.sample*

%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{sname}.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%attr(755,postgres,postgres) %dir /run/%{name}

%files devel
%{_includedir}/libpcp_ext.h
%{_includedir}/pcp.h
%{_includedir}/pool_process_reporting.h
%{_includedir}/pool_type.h

%files -n %{sname}-pcp
%{_bindir}/pcp_attach_node
%{_bindir}/pcp_detach_node
%{_bindir}/pcp_health_check_stats
%{_bindir}/pcp_invalidate_query_cache
%{_bindir}/pcp_log_rotate
%{_bindir}/pcp_node_count
%{_bindir}/pcp_node_info
%{_bindir}/pcp_pool_status
%{_bindir}/pcp_proc_count
%{_bindir}/pcp_proc_info
%{_bindir}/pcp_promote_node
%{_bindir}/pcp_recovery_node
%{_bindir}/pcp_reload_config
%{_bindir}/pcp_stop_pgpool
%{_bindir}/pcp_watchdog_info
%{_bindir}/wd_cli
%{_libdir}/libpcp.so*

%changelog
* Tue Sep 2 2025 Devrim Gündüz <devrim@gunduz.org> - 4.6.3-2PGDG
- Add a patch to fix compilation against GCC 15, per:
  https://github.com/pgpool/pgpool2/issues/124

* Sat Aug 23 2025 Devrim Gündüz <devrim@gunduz.org> - 4.6.3-1PGDG
- Update to 4.6.3 per changes described at:
  https://www.pgpool.net/docs/latest/en/html/release-4-6-3.html

* Wed Jun 4 2025 Devrim Gündüz <devrim@gunduz.org> - 4.6.2-1PGDG
- Update to 4.6.2 per changes described at:
  https://www.pgpool.net/docs/latest/en/html/release-4-6-2.html

* Mon May 26 2025 Devrim Gündüz <devrim@gunduz.org> - 4.6.1-1PGDG
- Update to 4.6.1 per changes described at:
  https://www.pgpool.net/docs/latest/en/html/release-4-6-1.html

* Mon Mar 3 2025 Devrim Gündüz <devrim@gunduz.org> - 4.6.0-1PGDG
- Update to 4.6.0 per changes described at:
  https://www.pgpool.net/docs/latest/en/html/release-4-6-0.html

* Mon Dec 16 2024 Devrim Gündüz <devrim@gunduz.org> - 4.5.5-1PGDG
- Update to 4.5.5 per changes described at:
  https://www.pgpool.net/docs/latest/en/html/release-4-5-5.html

* Mon Sep 9 2024 Devrim Gündüz <devrim@gunduz.org> - 4.5.4-1PGDG
- Update to 4.5.4 per changes described at:
  https://www.pgpool.net/docs/latest/en/html/release-4-5-4.html
  Fixes CVE-2024-45624.

* Fri Aug 16 2024 Devrim Gündüz <devrim@gunduz.org> - 4.5.3-1PGDG
- Update to 4.5.3 per changes described at:
  https://www.pgpool.net/docs/latest/en/html/release-4-5-3.html

* Sat Jul 13 2024 Devrim Gündüz <devrim@gunduz.org> - 4.5.2-1PGDG
- Update to 4.5.2 per changes described at:
  https://www.pgpool.net/docs/latest/en/html/release-4-5-2.html

* Thu Feb 29 2024 Devrim Gündüz <devrim@gunduz.org> - 4.5.1-1PGDG
- Update to 4.5.1

* Mon Jan 29 2024 Devrim Gündüz <devrim@gunduz.org> - 4.5.0-1PGDG
- Update to 4.5.0
- Add PGDG branding
- Spec file cleanup
- Fix rpmlint warnings

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 4.4.2-1.1
- Modernise %%patch usage, which has been deprecated in Fedora 38

* Mon Jan 23 2023 Devrim Gündüz <devrim@gunduz.org> - 4.4.2-1
- Update to 4.4.2

* Sun Dec 25 2022 Devrim Gündüz <devrim@gunduz.org> - 4.4.1-1
- Update to 4.4.1

* Tue Dec 20 2022 Devrim Gündüz <devrim@gunduz.org> - 4.4.0-1
- Update to 4.4.0

* Tue Dec 6 2022 Devrim Gündüz <devrim@gunduz.org> - 4.3.3-2
- Remove Advance Toolchain support from RHEL 7 - ppc64le.

* Fri Sep 9 2022 Devrim Gündüz <devrim@gunduz.org> - 4.3.3-1
- Update to 4.3.3
- Build with --with-ldap, per #7687 .

* Thu May 19 2022 Devrim Gündüz <devrim@gunduz.org> - 4.3.2-1
- Updare to 4.3.2

* Mon Feb 21 2022 Devrim Gündüz <devrim@gunduz.org> - 4.3.1-1
- Updare to 4.3.1

* Tue Dec 7 2021 Devrim Gündüz <devrim@gunduz.org> - 4.3.0-1
- Initial packaging for 4.3 series.

