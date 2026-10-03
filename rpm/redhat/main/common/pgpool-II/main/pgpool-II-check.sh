#  -*- Mode: sh; indent-tabs-mode: t -*-
#  shellcheck shell=bash
#
# Runs upstream's regression suite (src/test/regression/regress.sh) in
# %check. The spec sources this file after %pgdg_check_init, so the %check
# helpers of pgdg-srpm-macros are available, and sets these first:
#   PGDG_PGINSTDIR    %{pginstdir}
#   PGPOOL_PREFIX     %{_prefix}
#   PGPOOL_BINDIR     %{_bindir}
#   PGPOOL_CONFDIR    %{_sysconfdir}/%{name}
#   PGPOOL_LIBDIR     %{_libdir}
#
# regress.sh builds pgpool clusters of its own with pgpool_setup. It uses
# fixed ports from 11000 up, so do not run two of these builds on one host
# at a time.

# pgpool_setup installs pgpool_recovery, pgpool_regclass and pgpool_adm into
# the clusters it creates, so put them into the copy of PostgreSQL.
for d in pgpool_adm pgpool-recovery pgpool-regclass; do
	USE_PGXS=1 make -C src/sql/$d install DESTDIR="$PWD/pgext" PG_CONFIG="$PGDG_PGINSTDIR/bin/pg_config"
done
cp -a "pgext$PGDG_PGINSTDIR/." "$PGDG_CHECK_INSTDIR/"

# regress.sh's own "make install prefix=..." cannot work with the absolute
# sysconfdir of this package, so install pgpool into a scratch directory.
inst=$PWD/pgpool-inst
make install DESTDIR="$inst"
install -m 755 src/test/pgpool_setup src/test/watchdog_setup "$inst$PGPOOL_BINDIR/"
# The script that starts a recovered standby runs pg_ctl over "ssh -T
# localhost", which needs passwordless ssh; run pg_ctl directly instead.
# shellcheck disable=SC2016
sed -i 's/^ssh -T \$DEST \$PGCTL /$PGCTL /' "$inst$PGPOOL_BINDIR/pgpool_setup"
if grep -q '^ssh -T' "$inst$PGPOOL_BINDIR/pgpool_setup"; then
	echo "pgpool_setup still uses ssh"
	exit 1
fi
export PGPOOLDIR=$inst$PGPOOL_CONFDIR
export LD_LIBRARY_PATH=$inst$PGPOOL_LIBDIR

# pgpool_setup creates its own clusters, as the build user, with the copy
# of PostgreSQL; it must not inherit the libpq settings of the helpers. The
# tests run psql without -h, and our libpq looks in /run/postgresql by
# default, so point it at the socket directory given to regress.sh.
unset PGUSER PGPORT
export PGHOST=/tmp
cd src/test/regression || exit 1
# 007.memqcache-memcached expects a memcached on the default port
memcached -d -l 127.0.0.1 -p 11211 -P "$PWD/memcached.pid"

# Skipped tests:
# - 028.watchdog_enable_consensus_with_half_votes: shutting down its four
#   watchdog nodes does not finish in a build environment.
# - 036.trusted_servers: the watchdog cannot ping the trusted servers there.
# regress.sh empties log/ on each run, so run the tests one at a time and
# show the logs of each failure right away. Now and then pgpool does not
# stop at the end of a test, which then times out; retry those once.
pgpool_test() {
	./regress.sh -m noinstall -i "$inst$PGPOOL_PREFIX" -p "$PGDG_CHECK_BINDIR" -s /tmp -t 300 \
		-j /usr/share/java/postgresql-jdbc.jar "^$1\$" > regress.out 2>&1
	# regress.sh always exits 0. Its verdict is coloured by tput, whose
	# escape sequences (and a trailing SI) are stripped here.
	sed -E 's/\x1b[^a-zA-Z]*[a-zA-Z]//g; s/[[:cntrl:]]//g' regress.out | grep -a "^testing $1\.\.\." || :
}
failed=
for d in tests/[0-9][0-9][0-9].*/; do
	t=$(basename "$d")
	case "$t" in 028.*|036.*) continue ;; esac
	r=$(pgpool_test "$t")
	case "$r" in
	*...timeout.)
		echo "$r, retrying once"
		r=$(pgpool_test "$t")
		;;
	esac
	echo "$r"
	case "$r" in
	*...ok.) ;;
	*)
		failed="$failed $t"
		echo "===== log/$t"; tail -60 "log/$t"
		for f in tests/"$t"/testdir/log/pgpool.log tests/"$t"/testdir/data*/log/*; do
			[ -f "$f" ] && { echo "===== $f"; tail -30 "$f"; }
		done
		;;
	esac
done
kill "$(cat memcached.pid)"
cd ../../.. || exit 1
if [ -n "$failed" ]; then
	echo "pgpool-II regression tests failed:$failed"
	exit 1
fi
