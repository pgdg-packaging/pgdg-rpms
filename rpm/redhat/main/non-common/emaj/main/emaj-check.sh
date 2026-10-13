#  shellcheck shell=bash
#
# Runs the E-Maj regression tests in %check, as upstream's tools/regress.sh
# and tools/create_cluster.sh do, against a server from the %check helpers of
# pgdg-srpm-macros. It is sourced from %check after %pgdg_check_init, with
# PGDG_PGMAJORVERSION and PGDG_EMAJ_VERSION set, in the top directory of the
# source tree.

PGVER=$PGDG_PGMAJORVERSION
srcdir=$(pwd)

# The tests connect over TCP, as upstream's do: the expected output has the
# client address of the sessions in the logged changes.
pgdg_check_start main \
	"listen_addresses = '127.0.0.1'" \
	"max_prepared_transactions = 5" \
	"track_functions = all" \
	"plpgsql.extra_warnings = all" \
	"wal_level = logical" || exit 1

# The tablespaces and the role that tools/create_cluster.sh creates. The
# standard test scenario expects tspemaj under the name it gets at the end of
# each run of the tests (cleanup.sql).
mkdir "$PGDG_CHECK_DIR/emaj_tblsp" "$PGDG_CHECK_DIR/tsplog1" "$PGDG_CHECK_DIR/tsplog2"
psql -X -q -v ON_ERROR_STOP=1 postgres <<EOF || exit 1
CREATE TABLESPACE tspemaj_renamed LOCATION '$PGDG_CHECK_DIR/emaj_tblsp';
CREATE TABLESPACE tsplog1 LOCATION '$PGDG_CHECK_DIR/tsplog1';
CREATE TABLESPACE "tsp log'2" LOCATION '$PGDG_CHECK_DIR/tsplog2';
CREATE ROLE myUser LOGIN PASSWORD '';
GRANT ALL ON DATABASE postgres TO myUser;
CREATE DATABASE regression TEMPLATE=template0 ENCODING='UTF8' LC_COLLATE='C' LC_CTYPE='C';
ALTER DATABASE regression SET lc_messages TO 'C';
ALTER DATABASE regression SET lc_monetary TO 'C';
ALTER DATABASE regression SET lc_numeric TO 'C';
ALTER DATABASE regression SET lc_time TO 'C';
ALTER DATABASE regression SET bytea_output TO 'hex';
ALTER DATABASE regression SET timezone_abbreviations TO 'Default';
EOF

# The expected output is written for the development version of E-Maj, which
# reports its version as <devel>. Install the packaged extension script as
# version "devel" too, with only the version strings changed.
sed -e "s/'$PGDG_EMAJ_VERSION'/'<devel>'/" -e "s/'E-Maj $PGDG_EMAJ_VERSION'/'E-Maj <devel>'/" \
	"$PGDG_CHECK_INSTDIR/share/emaj/emaj--$PGDG_EMAJ_VERSION.sql" \
	>"$PGDG_CHECK_INSTDIR/share/emaj/emaj--devel.sql"
testdir=$PGDG_CHECK_DIR/emaj_test
mkdir -p "$testdir/sql" "$testdir/expected" "$testdir/results"
cp -p test/sql/*.sql "$testdir/sql/"
sed -i "s/VERSION '$PGDG_EMAJ_VERSION'/VERSION 'devel'/" "$testdir/sql/install.sql"

# The standard test scenario of tools/regress.sh. It is not run on PG 17:
# upstream runs the psql install script scenario there, and its expected
# output for PG 17 is older than the release.
tests="install setup create_drop start_stop mark rollback stat misc verify alter alter_logging viewer adm1 adm2 adm3 client check cleanup"
cp -p test/"$PGVER"/expected/*.out "$testdir/expected/"

# The tests run the clients as $EMAJ_DIR/client/*.pl, pg_dump as
# $EMAJ_DIR/test/<version>/bin/pg_dump, and $EMAJ_DIR/tools/check_code.pl,
# which reads $EMAJ_DIR/sql/emaj--devel.sql. The clients run with the libpq
# of the OS first: DBD::Pg is built against it, and the libpq of an older
# PGDG PostgreSQL, which ld.so.conf.d puts first, may lack symbols it needs.
# The package is noarch, so %{_libdir} of the build is not the one of the OS.
libdir=$(rpm --eval '%{_libdir}')
EMAJ_DIR=$PGDG_CHECK_DIR/emaj_dir
mkdir -p "$EMAJ_DIR/client" "$EMAJ_DIR/sql" "$EMAJ_DIR/test/$PGVER/results"
ln -s "$srcdir/tools" "$EMAJ_DIR/tools"
cp -p "$PGDG_CHECK_INSTDIR/share/emaj/emaj--devel.sql" "$EMAJ_DIR/sql/"
for c in "$srcdir"/client/*.pl; do
	printf '#!/bin/sh\nLD_LIBRARY_PATH=%s exec /usr/bin/perl -w %s "$@"\n' \
		"$libdir" "$c" >"$EMAJ_DIR/client/${c##*/}"
	chmod 755 "$EMAJ_DIR/client/${c##*/}"
done
ln -s "$PGDG_CHECK_BINDIR" "$EMAJ_DIR/test/$PGVER/bin"
export PGVER EMAJ_DIR
rm -rf "/tmp/emaj_$PGVER"

failed=0
unset LC_COLLATE LC_CTYPE LC_MONETARY LC_NUMERIC LC_TIME LANG LANGUAGE LC_ALL
for t in $tests; do
	PGHOST=127.0.0.1 PGOPTIONS="-c intervalstyle=postgres_verbose" LC_MESSAGES=C \
		PGTZ=PST8PDT PGDATESTYLE="Postgres, MDY" psql regression -X -q --echo-all \
		<"$testdir/sql/$t.sql" >"$testdir/results/$t.out" 2>&1
	# The clients print their version, and emajStat.pl the port, which is
	# 54<PG major version> in upstream's expected output
	sed -i -e "s/ E-Maj (version $PGDG_EMAJ_VERSION) - / E-Maj (version <devel>) - /" \
		-e "s/(@127\.0\.0\.1:$PGPORT)/(@127.0.0.1:54$PGVER)/" "$testdir/results/$t.out"
	if diff -a -C3 "$testdir/expected/$t.out" "$testdir/results/$t.out" >>"$testdir/regression.diffs"; then
		echo "test $t ... ok"
	else
		echo "test $t ... FAILED"
		failed=$((failed + 1))
	fi
done
rm -rf "/tmp/emaj_$PGVER"

if [ $failed -ne 0 ]; then
	echo "$failed E-Maj regression tests failed:"
	cat "$testdir/regression.diffs"
	exit 1
fi
