%global		name perl-DBD-Oracle
%global		pkgname %(echo %{name}| sed 's/perl-//')
%{!?version:%global version 1.90_5}
%{!?oi_release:%global oi_release 23.7.0.25.01}
%global		release %{oi_release}PGDG%{dist}
%global		perl_vendorarch %(eval "$(%{__perl} -V:installvendorarch)"; echo $installvendorarch)
%global		_use_internal_dependency_generator 0
%global		custom_find_req %{_tmppath}/%{pkgname}-%{version}-find-requires
%global		__find_requires %{custom_find_req}
%global		__perl_requires %{custom_find_req}

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	DBD-Oracle - Oracle database driver for the DBI module
License:	GPL+ or Artistic
URL:		https://github.com/pythian/DBD-Oracle
Source0:	https://github.com/perl5-dbi/DBD-Oracle/archive/refs/tags/v%{version}.tar.gz
Requires:	libaio
Requires:	perl(:MODULE_COMPAT_%(eval "$(%{__perl} -V:version)"; echo $version))
Requires:	perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:	perl(DBI) >= 1.51 perl(ExtUtils::MakeMaker) >= 6.30
Requires:	perl(DBI) >= 1.51
Requires:	oracle-instantclient-basic = %{oi_release}
BuildRequires:	oracle-instantclient-devel = %{oi_release}
BuildRequires:	oracle-instantclient-sqlplus = %{oi_release}
Provides:	perl(DBD-Oracle) = %{version}
Provides:	perl(DBD::Oracle) = %{version}

%description
DBD::Oracle is a Perl module which works with the DBI module to provide
access to Oracle databases.

%prep
%setup -q -n %{pkgname}-%{version}
chmod -R u+w %{_builddir}/%{pkgname}-%{version}

%build
export ORACLE_HOME=$(dirname $(dirname $(rpm -ql oracle-instantclient-sqlplus | grep '/usr/lib/oracle/.*/sqlplus')))
export LD_LIBRARY_PATH=$ORACLE_HOME/lib
MKFILE=$(rpm -ql oracle-instantclient-devel | grep demo.mk)
%{__perl} Makefile.PL -m $MKFILE INSTALLDIRS="vendor" PREFIX=%{_prefix} -V %{oi_release}
%{__make} %{?_smp_mflags} OPTIMIZE="%{optflags}"

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
cat << 'EOF' > %{custom_find_req}
#!/bin/sh
/usr/lib/rpm/redhat/find-requires | grep -v -e 'libclntsh.so.' -e 'libocci.so.'
EOF
chmod 755 %{custom_find_req}
%{__make} PREFIX=%{buildroot}%{_prefix} pure_install
%{__rm} -f $(find %{buildroot} -type f -name perllocal.pod -o -name .packlist)

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
%{__rm} -f %{custom_find_req}

%files
%defattr(-,root,root)
%defattr(-,root,root)
%{perl_vendorarch}/auto/DBD/
%{perl_vendorarch}/DBD/
%{_mandir}/man3/*

%changelog
* Mon Feb 10 2025 Devrim Gündüz <devrim@gunduz.org> - 1.90_5-23.7.0.25.01
- Update Oracle instant client version to 23.7.0.25.01

* Thu Dec 19 2024 Devrim Gündüz <devrim@gunduz.org> - 1.90_5-23.6.0.24.10
- Update Oracle instant client version to 23.6.0.24.10
- Provide perl(DBD::Oracle) per report and patch from Sébastien Lardière:
  https://redmine.postgresql.org/issues/8074

* Fri Aug 2 2024 Devrim Gündüz <devrim@gunduz.org> - 1.90_5-23.5.0.24.07
- Update Oracle instant client version to 23.5.0.24.07

* Sat Mar 16 2024 Devrim Gündüz <devrim@gunduz.org> - 1.90_5-21.13.0.0.0
- Update Oracle instant client version to 21.13.0.0.0

* Mon Dec 18 2023 Devrim Gündüz <devrim@gunduz.org> - 1.90_5-21.12.0.0.0
- Update Oracle instant client version to 21.12.0.0.0

* Wed Sep 13 2023 Devrim Gündüz <devrim@gunduz.org> - 1.90_5-21.11.0.0.0
- Update Oracle instant client version to 21.11.0.0.0

* Mon Apr 24 2023 Devrim Gündüz <devrim@gunduz.org> - 1.90_5-21.10.0.0.0
- Update to 1.90_5
- Update Oracle instant client version to 21.10.0.0.0

* Fri Feb 3 2023 Devrim Gündüz <devrim@gunduz.org> - 1.90.4-3
- Update Oracle instant client version to 21.9.0.0.0

* Fri Oct 28 2022 Devrim Gündüz <devrim@gunduz.org> - 1.90.4-2
- Update Oracle instant client version to 21.8.0.0.0

* Sat Sep 10 2022 Devrim Gündüz <devrim@gunduz.org> - 1.90.4-1
- Update to 1.90_4
- Update Oracle instant client version to 21.7.0.0.0
- Remove patch0, no longer needed.

* Wed Apr 20 2022 Devrim Gündüz <devrim@gunduz.org> - 1.83-1
- Update to 1.83.0

* Tue Sep 7 2021 Devrim Gündüz <devrim@gunduz.org> - 1.80-5
- Rebuild for instant client 21.3.0.0.0

* Thu Mar 4 2021 Devrim Gündüz <devrim@gunduz.org> - 1.80-4
- Rebuild for instant client 21.1.0.0.0
- Add a temp patch until the next release of perl-DBD-Oracle,
  so that it recognizes the new packaging as of OIC 21.

* Thu Sep 24 2020 Devrim Gündüz <devrim@gunduz.org> - 1.80-3
- Rebuild for instant client 19.8.0.0.0

* Sat Jul 11 2020 Devrim Gündüz <devrim@gunduz.org> - 1.80-2
- Rebuild for instant client 19.6.0.0.0

* Fri Nov 15 2019 Devrim Gündüz <devrim@gunduz.org> - 1.80-1
- Initial packaging for PostgreSQL RPM repository.
