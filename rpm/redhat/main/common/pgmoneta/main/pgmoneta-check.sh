#  -*- Mode: sh; indent-tabs-mode: t -*-
#  shellcheck shell=bash
#
# Runs the pgmoneta test suite in %check. The spec sources this file after
# %pgdg_check_init, so the %check helpers of pgdg-srpm-macros are available,
# and sets PGDG_PGMAJORVERSION first.
#
# This is what upstream's test/check.sh does in its "ci" mode, without
# containers and sudo: a PostgreSQL server with the test users and WAL
# settings, and a pgmoneta in front of it, which test/pgmoneta-test runs its
# tests against.

pgdg_check_start main "listen_addresses = 'localhost'" "password_encryption = md5" \
	"wal_level = replica" "wal_log_hints = on" "summarize_wal = on" \
	"hot_standby = on" "max_wal_senders = 10"
psql -X -q -v ON_ERROR_STOP=1 -d postgres <<EOF
CREATE ROLE myuser WITH LOGIN PASSWORD 'mypass';
CREATE DATABASE mydb WITH OWNER myuser TEMPLATE template0 ENCODING UTF8;
CREATE ROLE repl WITH LOGIN REPLICATION PASSWORD 'replpass';
GRANT pg_checkpoint TO repl;
GRANT pg_read_server_files TO repl;
GRANT EXECUTE ON FUNCTION pg_catalog.pg_switch_wal() TO repl;
GRANT EXECUTE ON FUNCTION pg_read_binary_file(text, bigint, bigint, boolean) TO repl;
GRANT EXECUTE ON FUNCTION pg_stat_file(text, boolean) TO repl;
GRANT EXECUTE ON FUNCTION pg_backup_start(text, boolean) TO repl;
GRANT EXECUTE ON FUNCTION pg_backup_stop(boolean) TO repl;
EOF
# The authentication rules of upstream's test server
cat > "$PGDG_CHECK_DIR/main/pg_hba.conf" <<EOF
local	all		all			trust
local	replication	all			trust
host	all		myuser		127.0.0.1/32	trust
host	postgres	repl		127.0.0.1/32	md5
host	replication	repl		127.0.0.1/32	md5
EOF
psql -X -q -d postgres -c 'SELECT pg_reload_conf()'

# %cmake builds in a subdirectory of build/, whose name differs by distro
bin=$(dirname "$(find "$PWD/build" -type f -name pgmoneta-admin -path '*/src/*')")
tests=$(dirname "$(find "$PWD/build" -type f -name pgmoneta-test)")
root=$PWD/pgmoneta-test
base=$root/base
conf=$base/conf
mkdir -p "$root/log" "$root/retrospect" "$root/standby" "$base/restore" "$base/backup" \
	"$base/pgmoneta-workspace" "$base/pg_conf" "$conf"
cp -R test/resource "$base/"
cp -R test/postgresql/src/postgresql17/conf/* "$base/pg_conf/"
cat > "$conf/pgmoneta_cli.conf" <<EOF
unix_socket_dir = $PGHOST
log_type = file
log_level = info
log_path = $root/log/pgmoneta-cli.log
EOF
cat > "$conf/pgmoneta.conf" <<EOF
[pgmoneta]
host = localhost
metrics = 5001

base_dir = $base/backup

compression = zstd

encryption = aes-256-gcm

retention = 7
retention_interval = 3600

log_type = file
log_level = debug5
log_path = $root/log/pgmoneta.log

unix_socket_dir = $PGHOST
create_slot = yes
workspace = $base/pgmoneta-workspace/

[primary]
host = localhost
port = $PGPORT
user = repl
wal_slot = repl
hot_standby = $root/standby
hot_standby_overrides = $root/standby/overrides
EOF
cp "$conf/pgmoneta.conf" "$conf/pgmoneta.conf.sample"

# The master key goes into ~/.pgmoneta
export HOME=$root
"$bin/pgmoneta-admin" master-key -P replpass
"$bin/pgmoneta-admin" -f "$conf/pgmoneta_users.conf" -U repl -P replpass user add

# Stop pgmoneta before the %check helpers stop PostgreSQL, also on failure
pgmoneta_stop() {
	local rc=$?
	"$bin/pgmoneta-cli" -c "$conf/pgmoneta_cli.conf" shutdown >/dev/null 2>&1 || :
	[ $rc -eq 0 ] || tail -100 "$root/log/pgmoneta.log"
	# Hand the exit status on; (exit $rc) must not end the shell under -e
	set +e
	(exit $rc)
	pgdg_check_cleanup
}
trap pgmoneta_stop EXIT
"$bin/pgmoneta" -c "$conf/pgmoneta.conf" -u "$conf/pgmoneta_users.conf" -d
for _ in $(seq 30); do
	"$bin/pgmoneta-cli" -c "$conf/pgmoneta_cli.conf" status >/dev/null 2>&1 && break
	sleep 1
done

export PGMONETA_TEST_BASE_DIR=$base PGMONETA_TEST_EXECUTABLE_DIR=$bin \
	PGMONETA_TEST_CONF=$conf/pgmoneta.conf \
	PGMONETA_TEST_CONF_SAMPLE=$conf/pgmoneta.conf.sample \
	PGMONETA_TEST_USER_CONF=$conf/pgmoneta_users.conf \
	PGMONETA_TEST_RESTORE_DIR=$base/restore \
	PGMONETA_TEST_RETROSPECT_DIR=$root/retrospect \
	PGMONETA_TEST_HOT_STANDBY_DIR=$root/standby \
	TEST_PG_VERSION=$PGDG_PGMAJORVERSION
"$tests/pgmoneta-test"
