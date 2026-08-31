%global sname	pljava
%global pljavamajver 1
%global pljavamidver 6
%global pljavaminver 10

%global relver %{pljavamajver}_%{pljavamidver}_%{pljavaminver}

# Every pljava version PGDG has ever shipped as an extension-packaged
# release (i.e. excluding pre-release betas, which never persisted as a
# real installed extension version string). Append the version being
# superseded here every time %%version is bumped for a new release --
# never remove or reorder entries. See %%install below for why.
%global pljava_old_versions 1.5.0 1.5.1 1.5.2 1.5.3 1.5.4 1.5.5 1.5.6 1.6.2 1.6.3 1.6.4 1.6.5 1.6.6 1.6.7 1.6.8 1.6.9

%if 0%{?suse_version} >= 1500
%else
%global debug_package %{nil}
%endif

%ifarch ppc64 ppc64le
%global archtag	ppc64le
%else
%global	archtag	amd64
%endif

Summary:	Java stored procedures, triggers, and functions for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	%{pljavamajver}.%{pljavamidver}.%{pljavaminver}
Release:	6PGDG%{?dist}
License:	BSD
URL:		http://tada.github.io/%{sname}/

Source0:	https://github.com/tada/%{sname}/archive/V%{relver}.tar.gz
Source1:	%{sname}.pom

%if 0%{?rhel} == 8
BuildRequires:	java-11-openjdk-devel
Requires:	java-11-openjdk
%else
%if 0%{?amzn} == 2023
BuildRequires:	java-25-amazon-corretto-devel
Requires:	java-25-amazon-corretto
%else
BuildRequires:	java-devel
Requires:	java
%endif
%endif

BuildRequires:	maven krb5-devel

%if 0%{?suse_version} >= 1500
Requires:	libopenssl3
BuildRequires:	libopenssl-3-devel
%endif
%if 0%{?fedora} >= 43 || 0%{?rhel} >= 8 || 0%{?amzn}
Requires:	openssl-libs >= 1.1.1k
BuildRequires:	openssl-devel
%endif
%description
PL/Java is a free open-source extension for PostgreSQL™ that allows
stored procedures, triggers, and functions to be written in the Java™
language and executed in the backend.

%prep
%setup -q -n %{sname}-%{relver}

%build
export CLASSPATH=

export PATH=%{pginstdir}/bin:$PATH
%ifarch ppc64 ppc64le
mvn clean install -Dso.debug=true -Psaxon-examples -Dnar.aolProperties=pljava-so/aol.%{archtag}-linux-gpp.properties
%else
%if 0%{?rhel} == 8
export JAVA_HOME=/etc/alternatives/java_sdk_11_openjdk
%endif
%if 0%{?fedora} || 0%{?rhel} >= 9
export JAVA_HOME=/usr/lib/jvm/java-openjdk/
%endif
%if 0%{?suse_version} >= 1500
export JAVA_HOME=/usr/lib64/jvm/java-openjdk/
%endif
%if 0%{?amzn} == 2023
export JAVA_HOME=/usr/lib/jvm/java-25-amazon-corretto.%{_arch}
%endif
# Common for all distros:
mvn clean install -Dso.debug=true -Psaxon-examples
%endif

%install
%{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{pginstdir}/lib
%{__cp} -f ./pljava-so/target/pljava-pgxs/libpljava-so-%{version}.so %{buildroot}%{pginstdir}/lib

%{__install} -d %{buildroot}%{pginstdir}/share/%{sname}
%{__cp} -f %{sname}/target/%{sname}-%{version}.jar %{buildroot}%{pginstdir}/share/%{sname}/
%{__cp} -f %{sname}-examples/target/%{sname}-examples-%{version}.jar %{buildroot}%{pginstdir}/share/%{sname}/
%{__cp} -f %{sname}-api/target/%{sname}-api-%{version}.jar %{buildroot}%{pginstdir}/share/%{sname}
%{__cp} -f %{sname}-packaging/target/classes/%{sname}.sql %{buildroot}%{pginstdir}/share/%{sname}/%{sname}--%{version}.sql
%{__cp} -f %{sname}-packaging/target/classes/%{sname}--unpackaged.sql %{buildroot}%{pginstdir}/share/%{sname}/%{sname}--unpackaged--%{version}.sql

# ALTER EXTENSION pljava UPDATE has no path to follow unless a
# %%sname--<old>--<new>.sql script exists for the hop. Provide a direct
# one-hop path from every version we've ever shipped straight to this
# one, so nobody is forced to DROP/CREATE the extension (which would
# CASCADE-drop the java/javau languages and every function written in
# them) just to move to a newer pljava. This is safe because the
# packaged SQL only contains idempotent CREATE OR REPLACE/DROP IF
# EXISTS DDL, so replaying it as an "upgrade" is equivalent to a fresh
# install. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/176
for oldver in %{pljava_old_versions}; do
  ln -sf %{sname}--%{version}.sql %{buildroot}%{pginstdir}/share/%{sname}/%{sname}--${oldver}--%{version}.sql
done

%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__cp} -f %{sname}-packaging/target/classes/%{sname}.control %{buildroot}%{pginstdir}/share/extension

%{__install} -d %{buildroot}%{_sysconfdir}/pgsql/
%{__cp} -f %{sname}-packaging/src/main/resources/pljava.policy %{buildroot}%{_sysconfdir}/pgsql/%{sname}_%{pgmajorversion}.policy

%files
%doc README.md
%license COPYRIGHT
%{_sysconfdir}/pgsql/%{sname}_%{pgmajorversion}.policy
%{pginstdir}/lib/libpljava-so-%{version}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/%{sname}/%{sname}--1*.sql
%{pginstdir}/share/%{sname}/%{sname}--unpackaged--%{version}.sql
%{pginstdir}/share/%{sname}/%{sname}-%{version}.jar
%{pginstdir}/share/%{sname}/%{sname}-examples-%{version}.jar
%{pginstdir}/share/%{sname}/%{sname}-api-%{version}.jar

%changelog
* Mon Aug 31 2026 Devrim Gündüz <devrim@gunduz.org> - 1.6.10-6PGDG
- Ship one-hop ALTER EXTENSION UPDATE paths (pljava--<old>--1.6.10.sql,
  symlinked to the plain install script) from every pljava version PGDG
  has ever shipped, so upgrading no longer requires an unsafe DROP/
  CREATE EXTENSION cycle. Fixes
  https://github.com/pgdg-packaging/pgdg-rpms/issues/176

* Thu Aug 27 2026 Devrim Gündüz <devrim@gunduz.org> - 1.6.10-5PGDG
- Add Amazon Linux 2023 support, using java-25-amazon-corretto-devel

* Mon Aug 24 2026 Devrim Gündüz <devrim@gunduz.org> - 1.6.10-4PGDG
- Fix OpenSSL dependency for Amazon Linux 2023

* Wed Nov 5 2025 Devrim Gündüz <devrim@gunduz.org> - 1.6.10-3PGDG
- Rebuild against OpenSSL 3 on SLES 15

* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 1.6.10-2PGDG
- Add SLES 16 support

* Mon Sep 29 2025 - Devrim Gündüz <devrim@gunduz.org> - 1.6.10-1PGDG
- Update to 1.6.10 per changes described at:
  https://github.com/tada/pljava/releases/tag/V1_6_10

* Mon Mar 24 2025 - Devrim Gündüz <devrim@gunduz.org> - 1.6.9-1PGDG
- Update to 1.6.9 per changes described at:
  https://github.com/tada/pljava/releases/tag/V1_6_9

* Thu Jan 2 2025 - Devrim Gündüz <devrim@gunduz.org> - 1.6.8-2PGDG
- Simplify Java BR and add Java Requires.
- Use proper JAVA_HOME on all distros
- Use macros for version numbers in the spec file to avoid accidents.

* Sun Oct 20 2024 - Devrim Gündüz <devrim@gunduz.org> - 1.6.8-1PGDG
- Update to 1.6.8 per changes described at:
  https://github.com/tada/pljava/releases/tag/V1_6_8
- Install pljava.policy file, per report from Chapman Flack.
- Remove RHEL 7 bits.

* Tue Apr 9 2024 - Devrim Gündüz <devrim@gunduz.org> - 1.6.7-1PGDG
- Update to 1.6.7

* Mon Feb 26 2024 - Devrim Gündüz <devrim@gunduz.org> - 1.6.6-2PGDG
- Update dependencies

* Tue Nov 21 2023 - Devrim Gündüz <devrim@gunduz.org> - 1.6.6-1PGDG
- Update to 1.6.6

* Mon Aug 21 2023 - Devrim Gündüz <devrim@gunduz.org> - 1.6.5-1PGDG
- Update to 1.6.5
- Add PGDG branding
- Fix rpmlint warning

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.6.4-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue Feb 15 2022 - Devrim Gündüz <devrim@gunduz.org> - 1.6.4-1
- Update to 1.6.4

* Mon Oct 11 2021 - Devrim Gündüz <devrim@gunduz.org> - 1.6.3-1
- Update to 1.6.3

* Tue Sep 21 2021 - Devrim Gündüz <devrim@gunduz.org> - 1.6.2-1
- Update to 1.6.2
- Remove patch0, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.5.6-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Tue Oct 6 2020 - Devrim Gündüz <devrim@gunduz.org> - 1.5.6-1
- Update to 1.5.6

* Fri Jul 10 2020 - Devrim Gündüz <devrim@gunduz.org> - 1.5.5-1
- Update to 1.5.5
- Add ppc64le support

* Tue Apr 28 2020 - John Harvey <john.harvey@crunchydata.com> - 1.5.4-1
- Update to 1.5.4

* Sat Oct 5 2019 Devrim Gündüz <devrim@gunduz.org> - 1.5.3-1
- Update to 1.5.3

* Wed Jan 2 2019 Devrim Gündüz <devrim@gunduz.org> - 1.5.2-2
- Create symlinks of .sql files for extension updates. Per Chapman.

* Tue Jan 1 2019 Devrim Gündüz <devrim@gunduz.org> - 1.5.2-1
- Update to 1.5.2

* Thu Oct 18 2018 Devrim Gündüz <devrim@gunduz.org> - 1.5.1-1
- Update to 1.5.1

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.5.1-b1_1.1
- Rebuild against PostgreSQL 11.0

* Tue Jun 20 2017 Devrim Gunduz <devrim@gunduz.org> 1.5.1-b1-1
- Update to 1.5.1 Beta 1

* Tue Mar 28 2017 Devrim Gunduz <devrim@gunduz.org> 1.5.0-2
- Fix packaging, per EnterpriseDB's spec file.

* Thu Jul 14 2016 Devrim Gunduz <devrim@gunduz.org> 1.5.0-1
- Update to 1.5.0

* Tue Feb 23 2016 Devrim Gunduz <devrim@gunduz.org> 1.5.0beta2-1
- Initial packaging for PostgreSQL RPM repository
