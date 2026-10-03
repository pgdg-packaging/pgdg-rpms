%{!?runselftest:%global runselftest 0}

Name:		pgagroal
Version:	2.1.0
Release:	5PGDG%{dist}
Summary:	High-performance connection pool for PostgreSQL
License:	BSD
URL:		https://github.com/agroal/%{name}
Source0:	https://github.com/agroal/%{name}/archive/%{version}.tar.gz
# Backport of upstream commit 8073ebc3c (#926): the port buffer of
# pgagroal_connect() was one byte short for backend ports >= 10000, which
# made pgagroal abort (and spin) with _FORTIFY_SOURCE.
Patch0:		%{name}-backend-port-buffer.patch

BuildRequires:	gcc cmake make python3-docutils
BuildRequires:	bzip2-devel liburing liburing-devel libzstd-devel lz4-devel
BuildRequires:	zlib-devel
BuildRequires:	libev libev-devel
BuildRequires:	systemd systemd-devel libatomic
Requires:	libev systemd
%if %runselftest
BuildRequires:	postgresql%{pgmajorversion}-server pgdg-srpm-macros >= 2.0.0
%endif

%if 0%{?suse_version} >= 1500
Requires:	libopenssl3
BuildRequires:	libopenssl-3-devel
%endif
%if 0%{?fedora} >= 42 || 0%{?rhel} >= 9 || 0%{?amzn}
Requires:	openssl-libs >= 1.1.1k
BuildRequires:	openssl-devel
%endif
%if 0%{?fedora} || 0%{?rhel} >= 9
Requires:	liburing
%else
Requires:	liburing2
%endif

%description
pgagroal is a high-performance connection pool for PostgreSQL.

%prep
%setup -q
%patch -P 0 -p0

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

%check
%if %runselftest
# What upstream's test/check.sh does in its "ci" mode, without containers and
# sudo: a PostgreSQL server with the test users and databases, pgbench tables,
# and a pgagroal in front of it, which test/pgagroal_test runs its tests
# against.
%pgdg_check_init
pgdg_check_start main "listen_addresses = 'localhost'" "password_encryption = 'scram-sha-256'"
# %%cmake builds in a subdirectory of build/, whose name differs by distro
bin=$(dirname $(find $PWD/build -type f -name pgagroal-admin -path '*/src/*'))
tests=$(dirname $(find $PWD/build -type f -name pgagroal_test))
# test/pgagroal_test reads its configuration from
# <project>/pgagroal-testsuite/conf, and writes to <project>/log
base=$PWD/pgagroal-testsuite
%{__mkdir} -p $PWD/log
conf=$base/conf
port=$((PGPORT + 1000))
export PG_USER_PASSWORD=yourpassword
export PG_UTF8_USER_PASSWORD='HelloПриветمرحبا你好नमस्तेสวัสดีこんにちは안녕하세요𠜎𡃁𩷶'
psql -X -q -v ON_ERROR_STOP=1 -d postgres <<EOF
CREATE ROLE myuser WITH LOGIN PASSWORD '$PG_USER_PASSWORD';
CREATE DATABASE mydb WITH OWNER myuser TEMPLATE template0 ENCODING UTF8;
CREATE ROLE utf8user WITH LOGIN PASSWORD '$PG_UTF8_USER_PASSWORD';
CREATE DATABASE utf8db WITH OWNER utf8user TEMPLATE template0 ENCODING UTF8;
EOF
# initdb trusted everyone; the tests log in with passwords, as upstream's do
sed -i 's/ trust$/ scram-sha-256/' $PGDG_CHECK_DIR/main/pg_hba.conf
# ... except postgres, as upstream's: the startup validation tests connect
# as health_check_user = postgres without a password
sed -i '1i local all postgres trust\nhost all postgres 127.0.0.1/32 trust' $PGDG_CHECK_DIR/main/pg_hba.conf
psql -X -q -d postgres -c 'SELECT pg_reload_conf()'
PGPASSWORD=$PG_USER_PASSWORD pgbench -i -s 1 -h localhost -U myuser mydb
PGPASSWORD=$PG_UTF8_USER_PASSWORD pgbench -i -s 1 -h localhost -U utf8user utf8db
%{__mkdir} -p $conf $base/log
%{__cp} -R test/resource $base/
cat > $conf/pgagroal.conf <<EOF
[pgagroal]
host = localhost
port = $port

log_type = file
log_level = debug5
log_path = $base/log/pgagroal.log

max_connections = 8
idle_timeout = 600
validation = off
unix_socket_dir = $PGHOST
pipeline = 'performance'

[primary]
host = localhost
port = $PGPORT
EOF
echo 'host all all all trust' > $conf/pgagroal_hba.conf
cat > $conf/pgagroal_databases.conf <<EOF
mydb=pgalias1,pgalias2 myuser 6 6 1
utf8db utf8user 2 2 1
EOF
: > $conf/pgagroal_frontend_users.conf
# The master key goes into ~/.pgagroal
export HOME=$base
$bin/pgagroal-admin master-key -P $PG_USER_PASSWORD
$bin/pgagroal-admin -f $conf/pgagroal_users.conf -U myuser -P $PG_USER_PASSWORD user add
$bin/pgagroal-admin -f $conf/pgagroal_users.conf -U "$(id -un)" -P $PG_USER_PASSWORD user add
$bin/pgagroal-admin -f $conf/pgagroal_users.conf -U utf8user -P "$PG_UTF8_USER_PASSWORD" user add
# Stop pgagroal before the %%check helpers stop PostgreSQL, also on failure
pgagroal_stop() {
	local rc=$?
	$bin/pgagroal-cli -c $conf/pgagroal.conf shutdown >/dev/null 2>&1 || :
	[ $rc -eq 0 ] || cat $base/log/pgagroal.log
	# Hand the exit status on; (exit $rc) must not end the shell under -e
	set +e
	(exit $rc)
	pgdg_check_cleanup
}
trap pgagroal_stop EXIT
$bin/pgagroal -c $conf/pgagroal.conf -a $conf/pgagroal_hba.conf \
	-u $conf/pgagroal_users.conf -l $conf/pgagroal_databases.conf \
	-F $conf/pgagroal_frontend_users.conf -d
for i in $(seq 30); do
	$bin/pgagroal-cli -c $conf/pgagroal.conf status >/dev/null 2>&1 && break
	sleep 1
done
export PGAGROAL_TEST_BASE_DIR=$base PGAGROAL_TEST_CONF=$conf/pgagroal.conf
PGPASSWORD=$PG_USER_PASSWORD $tests/pgagroal_test $PWD myuser mydb
%endif

# Install some files manually
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/grafana
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/etc
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/images
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/prometheus_scrape
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/shell_comp
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/tutorial
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/valgrind

%{__mkdir} -p %{buildroot}%{_sysconfdir}/%{name}
%{__mkdir} -p %{buildroot}%{_docdir}/%{name}/manual/en/

%{__install} -m 644 %{_builddir}/%{name}-%{version}/LICENSE %{buildroot}%{_docdir}/%{name}/LICENSE
%{__install} -m 644 %{_builddir}/%{name}-%{version}/CODE_OF_CONDUCT.md %{buildroot}%{_docdir}/%{name}/CODE_OF_CONDUCT.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/README.md %{buildroot}%{_docdir}/%{name}/README.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/contrib/grafana/*.json %{buildroot}%{_docdir}/%{name}/grafana/
%{__cp} -r %{_builddir}/%{name}-%{version}/contrib/grafana/provisioning/ %{buildroot}%{_docdir}/%{name}/grafana/provisioning
%{__install} -m 644 %{_builddir}/%{name}-%{version}/contrib/grafana/README.md %{buildroot}%{_docdir}/%{name}/grafana/README.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/contrib/shell_comp/pgagroal_comp.bash %{buildroot}%{_docdir}/%{name}/shell_comp/pgagroal_comp.bash
%{__install} -m 644 %{_builddir}/%{name}-%{version}/contrib/shell_comp/pgagroal_comp.zsh %{buildroot}%{_docdir}/%{name}/shell_comp/pgagroal_comp.zsh

%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/etc/%{name}.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/etc/%{name}_hba.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}_hba.conf

%{__install} -m 644 %{_builddir}/%{name}-%{version}/contrib/prometheus_scrape/* %{buildroot}%{_docdir}/%{name}/prometheus_scrape/
%{__install} -m 644 %{_builddir}/%{name}-%{version}/contrib/valgrind/pgagroal.supp %{buildroot}%{_docdir}/%{name}/valgrind/pgagroal.supp
%{__install} -m 644 %{_builddir}/%{name}-%{version}/contrib/valgrind/README.md %{buildroot}%{_docdir}/%{name}/valgrind/README.md
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/manual/en/*.md %{buildroot}%{_docdir}/%{name}/manual/en/

# Install unit file
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/etc/%{name}.service %{buildroot}%{_unitdir}/
%{__install} -m 644 %{_builddir}/%{name}-%{version}/doc/etc/%{name}.socket %{buildroot}%{_unitdir}/
# ... and make a tmpfiles script to recreate it at reboot.
%{__mkdir} -p %{buildroot}%{_tmpfilesdir}
cat > %{buildroot}%{_tmpfilesdir}/%{name}.conf <<EOF
d %{_rundir}/%{sname} 0755 root root -
EOF

cd %{buildroot}%{_libdir}/
%{__ln_s} -f libpgagroal.so.%{version} libpgagroal.so.1
%{__ln_s} -f libpgagroal.so.1 libpgagroal.so

%post
if [ $1 -eq 1 ] ; then
%systemd_post %{name}.service
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
%license %{_docdir}/%{name}/LICENSE
%{_docdir}/%{name}/*.md
%{_docdir}/%{name}/etc/*.conf
%{_docdir}/%{name}/images/*.png
%{_docdir}/%{name}/grafana/provisioning
%{_docdir}/%{name}/grafana/*.json
%{_docdir}/%{name}/grafana/README.md
%{_docdir}/%{name}/manual/en/*.md
%{_docdir}/%{name}/prometheus_scrape/*
%{_docdir}/%{name}/shell_comp/pgagroal_comp.bash
%{_docdir}/%{name}/shell_comp/pgagroal_comp.zsh
%{_docdir}/%{name}/tutorial/08_tls_enforced.md
%{_docdir}/%{name}/valgrind/pgagroal.supp
%{_docdir}/%{name}/valgrind/README.md

%{_mandir}/man1/%{name}*
%{_mandir}/man5/%{name}*
%config %{_sysconfdir}/%{name}/%{name}.conf
%config %{_sysconfdir}/%{name}/%{name}_hba.conf
%{_bindir}/%{name}
%{_bindir}/%{name}-cli
%{_bindir}/%{name}-config
%{_bindir}/%{name}-admin
%{_bindir}/%{name}-vault
%{_libdir}/libpgagroal.so*
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.socket

%changelog
* Sat Oct 3 2026 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-5PGDG
- Add a patch from upstream (8073ebc3c, #926) to fix a buffer overflow
  when connecting to a backend whose port is 10000 or higher: pgagroal
  aborted, or spun at 100%% CPU, as it is built with _FORTIFY_SOURCE.
- Add %%check, running the upstream tests (test/pgagroal_test) against a
  PostgreSQL server from the %%check helpers of pgdg-srpm-macros 2.0.0.
  It is disabled by default; enable it with --define 'runselftest 1'.

* Thu Sep 10 2026 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-4PGDG
- Add missing BR

* Mon Aug 24 2026 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-3PGDG
- Fix OpenSSL dependency for Amazon Linux 2023

* Thu Apr 30 2026 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-2PGDG
- Simplify the spec file.
- Install some missing files, per:
  https://github.com/pgdg-packaging/pgdg-rpms/issues/185

* Wed Apr 29 2026 Devrim Gündüz <devrim@gunduz.org> - 2.1.0-1PGDG
- Update to 2.1.0 per changes described at:
  https://github.com/agroal/pgagroal/releases/tag/2.1.0

* Wed Feb 25 2026 Devrim Gündüz <devrim@gunduz.org> - 2.0.2-1PGDG
- Update to 2.0.2 per changes described at:
  https://github.com/agroal/pgagroal/releases/tag/2.0.2
- Drop RHEL 8 support

* Wed Feb 18 2026 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-1PGDG
- Update to 2.0.1 per changes described at:
  https://github.com/agroal/pgagroal/releases/tag/2.0.1

* Thu Jan 29 2026 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-1PGDG
- Update to 2.0.0 per changes described at:
  https://github.com/agroal/pgagroal/releases/tag/2.0.0

* Fri Feb 23 2024 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-1PGDG
- Update to 1.6.0 per changes described at:
  https://github.com/agroal/pgagroal/releases/tag/1.6.0
- Add PGDG branding

* Wed Jan 11 2023 Devrim Gündüz <devrim@gunduz.org> - 1.5.1-1
- Update to 1.5.1

* Thu Sep 8 2022 Devrim Gündüz <devrim@gunduz.org> - 1.5.0-1
- Update to 1.5.0

* Mon Mar 21 2022 Devrim Gündüz <devrim@gunduz.org> - 1.4.2-1
- Update to 1.4.2

* Mon Mar 21 2022 Devrim Gündüz <devrim@gunduz.org> - 1.4.1-1
- Update to 1.4.1

* Tue Jan 11 2022 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-1
- Update to 1.4.0

* Fri Nov 26 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3.3-1
- Update to 1.3.3

* Fri Oct 22 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3.2-1
- Update to 1.3.2

* Sat Oct 16 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-1
- Update to 1.3.1

* Tue Sep 7 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-1
- Update to 1.3.0

* Wed Jun 30 2021 Devrim Gündüz <devrim@gunduz.org> - 1.2.2-1
- Update to 1.2.2

* Tue Mar 23 2021 Devrim Gündüz <devrim@gunduz.org> - 1.2.1-1
- Update to 1.2.1

* Fri Feb 26 2021 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1
- Update to 1.2.0

* Wed Jan 06 2021 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1
- Update to 1.1.0

* Tue Dec 22 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.2-1
- Update to 1.0.2

* Tue Nov 24 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1
- Update to 1.0.0

* Thu Nov 12 2020 Devrim Gündüz <devrim@gunduz.org> - 0.9.2-1
- Update to 0.9.2

* Wed Oct 14 2020 Devrim Gündüz <devrim@gunduz.org> - 0.9.1-1
- Update to 0.9.1

* Tue Sep 29 2020 Devrim Gündüz <devrim@gunduz.org> - 0.9.0-2
- Install systemd related files under their actual directory,
  and improve systemd support.
- Use macros more.

* Tue Sep 22 2020 Devrim Gündüz <devrim@gunduz.org> - 0.9.0-1
- Update to 0.9.0

* Wed Sep 2 2020 Devrim Gündüz <devrim@gunduz.org> - 0.8.2-1
- Update to 0.8.2

* Fri Aug 28 2020 Devrim Gündüz <devrim@gunduz.org> - 0.8.1-1
- Update to 0.8.1

* Tue Aug 4 2020 Devrim Gündüz <devrim@gunduz.org> - 0.8.0-1
- Update to 0.8.0

* Tue Jul 28 2020 Devrim Gündüz <devrim@gunduz.org> - 0.7.3-1
- Update to 0.7.3

* Wed Jun 10 2020 Devrim Gündüz <devrim@gunduz.org> - 0.7.1-1
- Update to 0.7.1

* Wed May 27 2020 Devrim Gündüz <devrim@gunduz.org> - 0.7.0-1
- Update to 0.7.0

* Fri May 1 2020 Devrim Gündüz <devrim@gunduz.org> - 0.6.0-1
- Update to 0.6.0

* Fri Apr 17 2020 Devrim Gündüz <devrim@gunduz.org> - 0.5.1-1
- Update to 0.5.1

* Tue Mar 24 2020 Devrim Gündüz <devrim@gunduz.org> - 0.5.0-1
- Initial packaging for PostgreSQL RPM repository, per upstream spec.
