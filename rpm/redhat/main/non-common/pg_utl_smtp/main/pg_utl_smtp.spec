%global sname	pg_utl_smtp

%{!?runselftest:%global runselftest 0}

Summary:	PostgreSQL extension to add compatibility to Oracle UTL_SMTP package.
Name:		%{sname}_%{pgmajorversion}
Version:	2.0
Release:	1PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/hexacluster/%{sname}/
Source0:	https://github.com/hexacluster/%{sname}/archive/refs/tags/v%{version}.tar.gz
# Declare plperlu in the control file, so that CREATE EXTENSION ... CASCADE
# creates it. Sent upstream: https://github.com/HexaCluster/pg_utl_smtp/pull/3
Patch0:		%{sname}-control-requires-plperlu.patch
BuildRequires:	make
BuildRequires:	postgresql%{pgmajorversion}-devel
%if %runselftest
BuildRequires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-plperl
BuildRequires:	pgdg-srpm-macros >= 2.0.0
BuildRequires:	pg_dbms_job_%{pgmajorversion} >= 2.0
BuildRequires:	perl(Net::SMTP) perl(IO::Socket::SSL) perl(Test::Simple) perl(Test::Harness)
BuildRequires:	openssl
# For the test SMTP server. It is only available on Fedora and RHEL 9 and 10
# (EPEL), so the tests can only run there:
BuildRequires:	python3-aiosmtpd
%endif
Requires:	postgresql%{pgmajorversion}-plperl postgresql%{pgmajorversion}-server
Requires:	perl(Net::SMTP)
# For SSL/TLS connections:
Requires:	perl(IO::Socket::SSL) >= 2.007
# The asynchronous mode (pg_utl_smtp.asynchronous) sends the messages with
# pg_dbms_job jobs:
Suggests:	pg_dbms_job_%{pgmajorversion} >= 2.0

BuildArch:	noarch

%description
PostgreSQL extension to add compatibility to Oracle UTL_SMTP package.

This extension uses plperlu stored procedures based on the Net::SMTP
Perl module to provide the procedures of the UTL_SMTP package. Messages can
also be sent asynchronously, by pg_dbms_job jobs, only when the transaction
commits.

%prep
%autosetup -p0 -n %{sname}-%{version}

%build

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} INSTALL_PREFIX=%{buildroot} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%check
%if %runselftest
# The tests need a SMTP server on ports 25 and 465, which only root can
# listen on. Run the test server of upstream on ports 10025 and 10465
# instead, and make the tests use them:
sed -i -e 's/port=25)/port=10025)/' -e 's/port=465,/port=10465,/' test/smtp_test_server.py
grep -q 'port=10025)' test/smtp_test_server.py && grep -q 'port=10465,' test/smtp_test_server.py
sed -i -e "s/open_connection('localhost')/open_connection('localhost', 10025)/gI" \
	-e "s/open_connection('localhost', 465,/open_connection('localhost', 10465,/gI" test/sql/*.sql
if grep -iE "open_connection\('localhost'(\)|, 465,)" test/sql/*.sql; then exit 1; fi
# Keep the port printed by this query as in the expected output:
sed -i 's/^SELECT port, secure,/SELECT port %% 10000 AS port, secure,/' test/sql/send_smtp_async.sql
grep -q 'SELECT port %% 10000 AS port, secure,' test/sql/send_smtp_async.sql
sed -i 's/connection to localhost:465:/connection to localhost:10465:/' test/expected/sync_errors.out

# The certificate of the test server, and a CA that has not signed it:
mkdir -p tmp_check/certs
openssl req -x509 -newkey rsa:2048 -nodes -days 2 \
	-keyout tmp_check/certs/key.pem -out tmp_check/certs/cert.pem \
	-subj "/CN=localhost" -addext "subjectAltName=DNS:localhost" 2>/dev/null
openssl req -x509 -newkey rsa:2048 -nodes -days 2 \
	-keyout tmp_check/certs/other_key.pem -out tmp_check/certs/other_ca.pem \
	-subj "/CN=other" 2>/dev/null
export SMTPS_CA_FILE=$PWD/tmp_check/certs/cert.pem
export SMTPS_OTHER_CA_FILE=$PWD/tmp_check/certs/other_ca.pem
export SMTPS_HOST=localhost

%pgdg_check_init
%{__python3} test/smtp_test_server.py --cert tmp_check/certs/cert.pem \
	--key tmp_check/certs/key.pem --maildir tmp_check/mails > tmp_check/smtp_server.log 2>&1 &
SMTP_PID=$!
# Stop the test SMTP server too when %%check exits, keeping its exit status
# for pgdg_check_cleanup:
trap 'rc=$?; kill $SMTP_PID 2>/dev/null; (exit $rc); pgdg_check_cleanup' EXIT
for i in $(seq 1 50); do
	%{__python3} -c "import socket; [socket.create_connection(('127.0.0.1', p), 1).close() for p in (10025, 10465)]" 2>/dev/null && break
	sleep 0.2
done

# The asynchronous mode tests need the pg_dbms_job background worker:
pgdg_check_start main "shared_preload_libraries = 'pg_dbms_job'" \
	"pg_dbms_job.database = 'regress_utl_smtp'" "pg_dbms_job.username = 'postgres'" \
	"pg_dbms_job.job_queue_interval = 1"
pgdg_installcheck || { cat tmp_check/smtp_server.log; exit 1; }
%endif

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0-1PGDG
- Update to 2.0 per changes described at:
  https://github.com/HexaCluster/pg_utl_smtp/releases/tag/v2.0
- Require perl(Net::SMTP) instead of perl-Net-SNMP, which is a different
  module, and perl(IO::Socket::SSL) for the new SSL/TLS support.
- Suggest pg_dbms_job, used by the new asynchronous mode.
- Add a patch to declare plperlu in the control file, so that CREATE
  EXTENSION pg_utl_smtp CASCADE creates it:
  https://github.com/HexaCluster/pg_utl_smtp/pull/3
- Add %%check, running the regression tests with the test SMTP server of
  upstream and the %%check helpers from pgdg-srpm-macros 2.0.0. It is
  disabled by default; enable it with --define 'runselftest 1'.

* Thu Sep 10 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0-3PGDG
- Add missing BR

* Thu Jan 22 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0-2PGDG
- Fix plperl dependency

* Thu Jan 22 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0-1PGDG
- Initial RPM packaging for the PostgreSQL RPM Repository:
  https://github.com/HexaCluster/pg_utl_smtp/releases/tag/v1.0
