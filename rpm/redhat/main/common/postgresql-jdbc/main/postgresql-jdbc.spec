
Summary:	JDBC driver for PostgreSQL
Name:		postgresql-jdbc
Version:	42.7.7
Release:	1PGDG%{?dist}
# ASL 2.0 applies only to postgresql-jdbc.pom file, the rest is BSD
License:	BSD and ASL 2.0
URL:		https://jdbc.postgresql.org/
Source0:	https://jdbc.postgresql.org/download/postgresql-jdbc-%{version}.src.tar.gz
Source1:	%{name}.pom
%if 0%{?rhel} == 8
Patch0:		%{name}-downgradeshade-rhel8.patch
%endif
BuildArch:	noarch

Requires:	jpackage-utils

%if 0%{?suse_version} >= 1500
# On SUSE/SLES, java-headless is Provided by java-11-openjdk-headless, which is version 0:11
Requires:	java-headless >= 8
%else
# On RHEL java-headless Provides 'java-headless = 1:1.8.0'
Requires:	java-headless
%endif

%if 0%{?rhel} == 8 || 0%{?fedora}
BuildRequires:	java-latest-openjdk-devel
%endif
%if 0%{?rhel} == 9
BuildRequires:	java-17-openjdk-devel
%endif
%if 0%{?rhel} == 10
BuildRequires:	java-21-openjdk-devel
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	java-11-openjdk-devel
%endif
BuildRequires:	maven javapackages-local

%description
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-jdbc package includes the .jar files needed for
Java programs to access a PostgreSQL database.

%package javadoc
Summary:	API docs for %{name}

%description javadoc
This package contains the API Documentation for %{name}.

%prep
%setup -q -n postgresql-%{version}-jdbc-src
%if 0%{?rhel} == 8
%patch -P 0 -p0
%endif

# remove any binary libs
find -name "*.jar" -or -name "*.class" | xargs %{__rm} -fr

# For compat reasons, make Maven artifact available under older coordinates.
%mvn_alias org.postgresql:postgresql postgresql:postgresql

# remove unmet dependency
%pom_remove_dep uk.org.webcompere:system-stubs-jupiter

# remove tests that depend on the system-stubs-jupiter
%{__rm} src/test/java/org/postgresql/test/jdbc2/DriverTest.java \
	src/test/java/org/postgresql/util/OSUtilTest.java \
	src/test/java/org/postgresql/jdbcurlresolver/PgServiceConfParserTest.java \
	src/test/java/org/postgresql/jdbcurlresolver/PgPassParserTest.java \
	src/test/java/org/postgresql/util/StubEnvironmentAndProperties.java

%build
%if 0%{?suse_version} >= 1500
export PATH=/usr/lib64/jvm/java-openjdk/bin:$PATH
%endif
%if 0%{?fedora} || 0%{?rhel}
export PATH=/usr/lib/jvm/java-openjdk/bin:$PATH
%endif

export CLASSPATH=
# Ideally we would run "sh update-translations.sh" here, but that results
# in inserting the build timestamp into the generated messages_*.class
# files, which makes rpmdiff complain about multilib conflicts if the
# different platforms don't build in the same minute. For now, rely on
# upstream to have updated the translations files before packaging.

mvn -DskipTests -Pjavadoc package

%install
%{__install} -d %{buildroot}%{_javadir}
# Per jpp conventions, jars have version-numbered names and we add
# versionless symlinks.
%{__install} -m 644 target/postgresql-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

pushd %{buildroot}%{_javadir}
# Also, for backwards compatibility with our old postgresql-jdbc packages,
# add these symlinks. (Probably only the jdbc3 symlink really makes sense?)
%{__ln_s} %{name}.jar postgresql-jdbc2.jar
%{__ln_s} %{name}.jar postgresql-jdbc2ee.jar
%{__ln_s} %{name}.jar postgresql-jdbc3.jar
popd

# Install the pom after inserting the correct version number
sed 's/UPSTREAM_VERSION/%{version}/g' %{SOURCE1} >JPP-%{name}.pom
%{__install} -d -m 755 %{buildroot}%{_mavenpomdir}/
%{__install} -m 644 JPP-%{name}.pom %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

%{__install} -d -m 755 %{buildroot}%{_javadocdir}
%{__cp} -ra target/apidocs %{buildroot}%{_javadocdir}/%{name}
%{__install} -d target/apidocs docs/%{name}

%check
%if 0%{?runselftest}
# Note that this requires to have PostgreSQL properly configured; for this
# reason the testsuite is turned off by default (see org/postgresql/test/README)
test_log=test.log
# TODO: more reliable testing
mvn clean package 2>&1 | tee test.log | grep FAILED
test $? -eq 0 && { cat test.log ; exit 1 ; }
%endif

%if 0%{?suse_version} >= 1500
%files
%doc LICENSE README.md
%else
%files
%doc README.md
%license LICENSE
%{_javadir}/%{name}.jar
%endif

# ...and SLES locates .pom file somewhere else:
%if 0%{?suse_version} >= 1500
%{_javadir}/%{name}.jar
%{_datadir}/maven-poms/JPP-%{name}.pom
%endif
%if 0%{?rhel} && 0%{?rhel} >= 8
%{_datadir}/maven-poms/JPP-%{name}.pom
%endif
%if 0%{?fedora}
%{_datadir}/maven-poms/JPP-%{name}.pom
%endif
%{_javadir}/postgresql-jdbc2.jar
%{_javadir}/postgresql-jdbc2ee.jar
%{_javadir}/postgresql-jdbc3.jar
%files javadoc
%doc LICENSE
%doc %{_javadocdir}/%{name}

%changelog
* Wed Jun 11 2025 Devrim Gündüz <devrim@gunduz.org> - 42.7.7-1PGDG
- Update to 42.7.7 per changes described at:
  https://github.com/pgjdbc/pgjdbc/releases/tag/REL42.7.7

* Wed May 28 2025 Devrim Gündüz <devrim@gunduz.org> - 42.7.6-1PGDG
- Update to 42.7.6 per changes described at:
  https://github.com/pgjdbc/pgjdbc/releases/tag/REL42.7.6

* Wed Jan 15 2025 Devrim Gündüz <devrim@gunduz.org> - 42.7.5-2PGDG
- Do not remove shade plugin, just downgrade it for RHEL 8 to
  unbreak SCRAM auth.

* Tue Jan 14 2025 Devrim Gündüz <devrim@gunduz.org> - 42.7.5-1PGDG
- Update to 42.7.5 per changes described at:
  https://github.com/pgjdbc/pgjdbc/releases/tag/REL42.7.5
- Fix RHEL 10 dependency
- Disable shade plugin per https://github.com/pgjdbc/pgjdbc/issues/3480
- Merged some changes from Fedora spec file.

* Mon Dec 30 2024 Devrim Gündüz <devrim@gunduz.org> - 42.7.4-2PGDG
- Fix SLES 15 dependency and remove RHEL 7 and SLES 12 support.

* Fri Aug 23 2024 Devrim Gündüz <devrim@gunduz.org> - 42.7.4-1PGDG
- Update to 42.7.4 per changes described at:
  https://github.com/pgjdbc/pgjdbc/releases/tag/REL42.7.4

* Fri Mar 15 2024 Devrim Gündüz <devrim@gunduz.org> - 42.7.3-1PGDG
- Update to 42.7.3 per changes described at:
  https://jdbc.postgresql.org/changelogs/2024-03-14-42.7.3-release/

* Wed Feb 21 2024 Devrim Gündüz <devrim@gunduz.org> - 42.7.2-1PGDG
- Update to 42.7.2 per changes described at:
  https://jdbc.postgresql.org/changelogs/2024-02-21-42.7.2-release/

* Thu Dec 7 2023 Devrim Gündüz <devrim@gunduz.org> - 42.7.1-1PGDG
- Update to 42.7.1 per changes described at:
  https://jdbc.postgresql.org/changelogs/2023-12-06-42.7.1-release/

* Tue Nov 21 2023 Devrim Gündüz <devrim@gunduz.org> - 42.7.0-1PGDG
- Update to 42.7.0 per changes described at:
  https://jdbc.postgresql.org/changelogs/2023-11-20-42.7.0-release/
- Add PGDG branding

* Tue Mar 21 2023 Devrim Gündüz <devrim@gunduz.org> - 42.6.0-1
- Update to 42.6.0

* Tue Feb 21 2023 Devrim Gündüz <devrim@gunduz.org> - 42.5.4-1
- Update to 42.5.4

* Mon Feb 13 2023 Devrim Gündüz <devrim@gunduz.org> - 42.5.3-1
- Update to 42.5.3

* Wed Nov 23 2022 Devrim Gündüz <devrim@gunduz.org> - 42.5.1-1
- Update to 42.5.1

* Fri Aug 26 2022 Devrim Gündüz <devrim@gunduz.org> - 42.5.0-1
- Update to 42.5.0

* Tue Aug 9 2022 Devrim Gündüz <devrim@gunduz.org> - 42.4.1-1
- Update to 42.4.1

* Mon May 30 2022 Devrim Gündüz <devrim@gunduz.org> - 42.3.6-1
- Update to 42.3.6

* Thu May 5 2022 Devrim Gündüz <devrim@gunduz.org> - 42.3.5-1
- Update to 42.3.5

* Sun Apr 17 2022 Devrim Gündüz <devrim@gunduz.org> - 42.3.4-1
- Update to 42.3.4

* Mon Feb 28 2022 Devrim Gündüz <devrim@gunduz.org> - 42.3.3-1
- Update to 42.3.3

* Mon Feb 7 2022 - John Harvey <john.harvey@crunchydata.com> 42.3.2-2
- Fix SLES15 java-headless dependency

* Wed Feb 2 2022 Devrim Gündüz <devrim@gunduz.org> - 42.3.2-1
- Update to 42.3.2, per changes described at:
  https://jdbc.postgresql.org/documentation/changelog.html#version_42.3.2

* Fri Nov 26 2021 Devrim Gündüz <devrim@gunduz.org> - 42.3.1-2
- Add RHEL 9 support

* Mon Nov 1 2021 Devrim Gündüz <devrim@gunduz.org> - 42.3.1-1
- Update to 42.3.1, per changes described at:
  https://jdbc.postgresql.org/documentation/changelog.html#version_42.3.1

* Mon Oct 25 2021 Devrim Gündüz <devrim@gunduz.org> - 42.3.0-1
- Update to 42.3.0

* Mon Sep 27 2021 Devrim Gündüz <devrim@gunduz.org> - 42.2.24-1
- Update to 42.2.24

* Wed Jul 7 2021 Devrim Gündüz <devrim@gunduz.org> - 42.2.23-1
- Update to 42.2.23

* Fri Jun 18 2021 Devrim Gündüz <devrim@gunduz.org> - 42.2.22-2
- Fix SLES packaging, remove RHEL 6 support, update Fedora dependency.

* Fri Jun 18 2021 Devrim Gündüz <devrim@gunduz.org> - 42.2.22-1
- Update to 42.2.22

* Fri Jun 11 2021 Devrim Gündüz <devrim@gunduz.org> - 42.2.21-1
- Update to 42.2.21

* Fri Apr 23 2021 Devrim Gündüz <devrim@gunduz.org> - 42.2.20-1
- Update to 42.2.20

* Mon Feb 22 2021 - John Harvey <john.harvey@crunchydata.com> 42.2.19-2
- Add maven profile for javadoc and restore javadoc package

* Fri Feb 19 2021 Devrim Gündüz <devrim@gunduz.org> - 42.2.19-1
- Update to 42.2.19
- Remove javadoc package -- upstream removed its contents

* Sun Oct 18 2020 Devrim Gündüz <devrim@gunduz.org> - 42.2.18-1
- Update to 42.2.18

* Mon Oct 12 2020 Devrim Gündüz <devrim@gunduz.org> - 42.2.17-1
- Update to 42.2.17

* Fri Aug 28 2020 Devrim Gündüz <devrim@gunduz.org> - 42.2.16-2
- Clarify maven dependencies

* Fri Aug 28 2020 Devrim Gündüz <devrim@gunduz.org> - 42.2.16-1
- Update to 42.2.16

* Wed Jun 10 2020 Devrim Gündüz <devrim@gunduz.org> - 42.2.14-1
- Update to 42.2.14

* Wed Apr 1 2020 Devrim Gündüz <devrim@gunduz.org> - 42.2.12-1
- Update to 42.2.12

* Tue Mar 17 2020 Devrim Gündüz <devrim@gunduz.org> - 42.2.11-1
- Update to 42.2.11

* Fri Feb 7 2020 Devrim Gündüz <devrim@gunduz.org> - 42.2.10-1
- Update to 42.2.10

* Tue Dec 10 2019 Devrim Gündüz <devrim@gunduz.org> - 42.2.9-1
- Update to 42.2.9

* Tue Oct 1 2019 Devrim Gündüz <devrim@gunduz.org> - 42.2.8-1
- Update to 42.2.8

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 42.2.7-1.1
- Rebuild for PostgreSQL 12

* Wed Sep 11 2019 Devrim Gündüz <devrim@gunduz.org> - 42.2.7
- Update to 42.2.7

* Thu Jun 27 2019 Devrim Gündüz <devrim@gunduz.org> - 42.2.6-1
- Update to 42.2.6

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 42.2.5-1.1
- Rebuild against PostgreSQL 11.0

* Mon Aug 27 2018 Devrim Gündüz <devrim@gunduz.org> - 42.2.5-1
- Update to 42.2.5, which fixes CVE-2018-10936

* Sun Jul 15 2018 Devrim Gündüz <devrim@gunduz.org> - 42.2.4-1
- Update to 42.2.4

* Sat Mar 17 2018 Devrim Gündüz <devrim@gunduz.org> - 42.2.2-2
- Fix SLES builds

* Fri Mar 16 2018 Devrim Gündüz <devrim@gunduz.org> - 42.2.2-1
- Update to 42.2.2, per changes described at
  https://jdbc.postgresql.org/documentation/changelog.html#version_42.2.2

* Sat Jan 27 2018 Devrim Gündüz <devrim@gunduz.org> - 42.2.1-1
- Update to 42.2.1, per changes described at
  https://jdbc.postgresql.org/documentation/changelog.html#version_42.2.1

* Thu Jan 18 2018 Devrim Gündüz <devrim@gunduz.org> - 42.2.0-1
- Update to 42.2.0, per changes described at
  https://jdbc.postgresql.org/documentation/changelog.html#version_42.2.0

* Sat Jul 15 2017 Devrim Gündüz <devrim@gunduz.org> - 42.1.4-1
- Update to 42.1.4, per changes described at
  https://jdbc.postgresql.org/documentation/changelog.html#version_42.1.4

* Sat Jul 15 2017 Devrim Gündüz <devrim@gunduz.org> - 42.1.3-1
- Update to 42.1.3

* Thu Jul 13 2017 Devrim Gündüz <devrim@gunduz.org> - 42.1.2-1
- Update to 42.1.2

* Wed May 10 2017 Devrim Gündüz <devrim@gunduz.org> - 42.1.1-1
- Update to 42.1.1

* Mon Feb 20 2017 Devrim Gündüz <devrim@gunduz.org> - 42.0.0-1
- Update to 42.0.0

* Thu Nov 17 2016 Devrim Gündüz <devrim@gunduz.org> - 9.4.1212-1
- Update to 9.4.1212

* Mon Sep 19 2016 Devrim Gündüz <devrim@gunduz.org> - 9.4.1211-1
- Update to 9.4.1211

* Tue Mar 15 2016 Devrim Gündüz <devrim@gunduz.org> - 9.4.1208-1
- Update to 9.4.1208, per #1034.
- Use more macros, per John Harvey. Closes #1017.

* Wed Feb 10 2016 Devrim Gündüz <devrim@gunduz.org> - 9.4.1207-3
- Remove pgmajorversion from spec file, because this package does not
  depend on PostgreSQL version.
- Add more conditionals for unified spec file.
- Remove some BRs, per John Harvey.
- Specify maven version, per John Harvey.

* Wed Feb 10 2016 John Harvey <john.harvey@crunchydata.com> - 9.4.1207-2
- Fix broken links to jar files.
- Trim changelog (Devrim)

* Tue Jan 5 2016 John Harvey <john.harvey@crunchydata.com> - 9.4.1207-1
- Update to 9.4 build 1207 (maven support)
- Use some more macros, where appropriate (Devrim)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.4.1200-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 04 2015 Pavel Raiskup <praiskup@redhat.com> - 9.4.1200-1
- rebase to most recent version (#1188827)
