%global sname	pljava
%global pljavamajver 1
%global pljavamidver 6
%global pljavaminver 8

%global relver %{pljavamajver}_%{pljavamidver}_%{pljavaminver}

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
Release:	2PGDG%{?dist}
License:	BSD
URL:		http://tada.github.io/%{sname}/

Source0:	https://github.com/tada/%{sname}/archive/V%{relver}.tar.gz
Source1:	%{sname}.pom

BuildRequires:	java-devel
BuildRequires:	openssl-devel krb5-devel

BuildRequires:	maven java

Obsoletes:	%{sname}-%{pgmajorversion} < 1.5.6-2

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
%if 0%{?fedora} || 0%{?rhel} >= 8
export JAVA_HOME=/usr/lib/jvm/java-openjdk/
%endif
%if 0%{?suse_version} >= 1500
export JAVA_HOME=/usr/lib64/jvm/java-openjdk/
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
