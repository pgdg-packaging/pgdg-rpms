#  -*- Mode: sh; indent-tabs-mode: t -*-
#  shellcheck shell=bash
#
# Runs the pgagroal test suite in %check. The spec sources this file after
# %pgdg_check_init, so the %check helpers of pgdg-srpm-macros are available.
#
# This is what upstream's test/check.sh does in its "ci" mode, without
# containers and sudo: a PostgreSQL server with the test users and
# databases, pgbench tables, and a pgagroal in front of it, which
# test/pgagroal_test runs its tests against.

pgdg_check_start main "listen_addresses = 'localhost'" "password_encryption = 'scram-sha-256'"

# %cmake builds in a subdirectory of build/, whose name differs by distro
bin=$(dirname "$(find "$PWD/build" -type f -name pgagroal-admin -path '*/src/*')")
tests=$(dirname "$(find "$PWD/build" -type f -name pgagroal_test)")
# test/pgagroal_test reads its configuration from
# <project>/pgagroal-testsuite/conf, and writes to <project>/log
base=$PWD/pgagroal-testsuite
conf=$base/conf
port=$((PGPORT + 1000))
mkdir -p "$PWD/log" "$conf" "$base/log"

export PG_USER_PASSWORD=yourpassword
export PG_UTF8_USER_PASSWORD='HelloПриветمرحبا你好नमस्तेสวัสดีこんにちは안녕하세요𠜎𡃁𩷶'
psql -X -q -v ON_ERROR_STOP=1 -d postgres <<EOF
CREATE ROLE myuser WITH LOGIN PASSWORD '$PG_USER_PASSWORD';
CREATE DATABASE mydb WITH OWNER myuser TEMPLATE template0 ENCODING UTF8;
CREATE ROLE utf8user WITH LOGIN PASSWORD '$PG_UTF8_USER_PASSWORD';
CREATE DATABASE utf8db WITH OWNER utf8user TEMPLATE template0 ENCODING UTF8;
EOF
# initdb trusted everyone; the tests log in with passwords, as upstream's do
sed -i 's/ trust$/ scram-sha-256/' "$PGDG_CHECK_DIR/main/pg_hba.conf"
# ... except postgres, as upstream's: the startup validation tests connect
# as health_check_user = postgres without a password
sed -i '1i local all postgres trust\nhost all postgres 127.0.0.1/32 trust' "$PGDG_CHECK_DIR/main/pg_hba.conf"
psql -X -q -d postgres -c 'SELECT pg_reload_conf()'
PGPASSWORD=$PG_USER_PASSWORD pgbench -i -s 1 -h localhost -U myuser mydb
PGPASSWORD=$PG_UTF8_USER_PASSWORD pgbench -i -s 1 -h localhost -U utf8user utf8db

cp -R test/resource "$base/"
cat > "$conf/pgagroal.conf" <<EOF
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
echo 'host all all all trust' > "$conf/pgagroal_hba.conf"
cat > "$conf/pgagroal_databases.conf" <<EOF
mydb=pgalias1,pgalias2 myuser 6 6 1
utf8db utf8user 2 2 1
EOF
: > "$conf/pgagroal_frontend_users.conf"

# The master key goes into ~/.pgagroal
export HOME=$base
"$bin/pgagroal-admin" master-key -P "$PG_USER_PASSWORD"
"$bin/pgagroal-admin" -f "$conf/pgagroal_users.conf" -U myuser -P "$PG_USER_PASSWORD" user add
"$bin/pgagroal-admin" -f "$conf/pgagroal_users.conf" -U "$(id -un)" -P "$PG_USER_PASSWORD" user add
"$bin/pgagroal-admin" -f "$conf/pgagroal_users.conf" -U utf8user -P "$PG_UTF8_USER_PASSWORD" user add

# Stop pgagroal before the %check helpers stop PostgreSQL, also on failure
pgagroal_stop() {
	local rc=$?
	"$bin/pgagroal-cli" -c "$conf/pgagroal.conf" shutdown >/dev/null 2>&1 || :
	[ $rc -eq 0 ] || cat "$base/log/pgagroal.log"
	# Hand the exit status on; (exit $rc) must not end the shell under -e
	set +e
	(exit $rc)
	pgdg_check_cleanup
}
trap pgagroal_stop EXIT
"$bin/pgagroal" -c "$conf/pgagroal.conf" -a "$conf/pgagroal_hba.conf" \
	-u "$conf/pgagroal_users.conf" -l "$conf/pgagroal_databases.conf" \
	-F "$conf/pgagroal_frontend_users.conf" -d
for _ in $(seq 30); do
	"$bin/pgagroal-cli" -c "$conf/pgagroal.conf" status >/dev/null 2>&1 && break
	sleep 1
done

export PGAGROAL_TEST_BASE_DIR=$base PGAGROAL_TEST_CONF=$conf/pgagroal.conf
PGPASSWORD=$PG_USER_PASSWORD "$tests/pgagroal_test" "$PWD" myuser mydb
