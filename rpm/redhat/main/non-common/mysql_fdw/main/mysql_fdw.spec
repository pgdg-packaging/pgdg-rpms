%global sname mysql_fdw
%global mysqlfdwmajver 2
%global mysqlfdwmidver 9
%global mysqlfdwminver 3

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL Foreign Data Wrapper (FDW) for the MySQL
Name:		%{sname}_%{pgmajorversion}
Version:	%{mysqlfdwmajver}.%{mysqlfdwmidver}.%{mysqlfdwminver}
Release:	3PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/EnterpriseDB/%{sname}/archive/REL-%{mysqlfdwmajver}_%{mysqlfdwmidver}_%{mysqlfdwminver}.tar.gz
URL:		https://github.com/EnterpriseDB/mysql_fdw
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros

Requires:	postgresql%{pgmajorversion}-server

%if 0%{?fedora} >= 40 || 0%{?rhel} >= 8
BuildRequires:	mariadb-devel
Requires:	mariadb-connector-c-devel
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	libmariadb-devel
Requires:	libmariadb-devel
%endif

%description
This PostgreSQL extension implements a Foreign Data Wrapper (FDW) for
the MySQL.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for mysql_fdw
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm => 19.0
%endif

%description llvmjit
This package provides JIT support for mysql_fdw
%endif

%prep
%setup -q -n %{sname}-REL-%{mysqlfdwmajver}_%{mysqlfdwmidver}_%{mysqlfdwminver}

%build
export LDFLAGS="-L%{_libdir}/mysql"

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 755 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(755,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}_pushdown.config

%if %llvm
 %{pginstdir}/lib/bitcode/%{sname}*.bc
 %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Tue Sep 30 2025 Devrim Gunduz <devrim@gunduz.org> - 2.9.3-1PGDG
- Update to 2.9.3 per changes described at:
  https://github.com/EnterpriseDB/mysql_fdw/releases/tag/REL-2_9_3

* Mon Jan 13 2025 Devrim Gündüz <devrim@gunduz.org> - 2.9.2-3PGDG
- Update LLVM dependencies
- Fix location of the README file.

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 2.9.2-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Fri Jul 12 2024 Devrim Gunduz <devrim@gunduz.org> - 2.9.2-1PGDG
- Update to 2.9.2 per changes described at:
  https://github.com/EnterpriseDB/mysql_fdw/releases/tag/REL-2_9_2

* Thu Feb 22 2024 Devrim Gunduz <devrim@gunduz.org> - 2.9.1-2PGDG
- Fix/update both BR and Requires.

* Thu Jul 20 2023 Devrim Gunduz <devrim@gunduz.org> - 2.9.1-1PGDG
- Update to 2.9.1
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 2.9.0-1.1
- Rebuild against LLVM 15 on SLES 15

* Wed Dec 21 2022 John Harvey <john.harvey@crunchydata.com> - 2.9.0-1
- Update to 2.9.0

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.8.0-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon May 30 2022 Devrim Gündüz <devrim@gunduz.org> - 2.8.0-1
- Update to 2.8.0

* Fri Feb 18 2022 John Harvey <john.harvey@crunchydata.com> - 2.7.0-2
- Update license to match source code

* Tue Jan 18 2022 Devrim Gündüz <devrim@gunduz.org> - 2.7.0-1
- Update to 2.7.0
- Remove the remaining RHEL 6 bit.

* Thu Sep 16 2021 Devrim Gündüz <devrim@gunduz.org> - 2.6.1-1
- Fix spec file for RHEL 8 / ppc64le. Per report from Aparna
 (I did not use her patch, though)

* Thu Sep 16 2021 Devrim Gündüz <devrim@gunduz.org> - 2.6.1-1
- Update to 2.6.1

* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> - 2.6.0-2
- Remove pgxs patches, and export PATH instead.

* Mon May 3 2021 Devrim Gündüz <devrim@gunduz.org> - 2.6.0-1
- Update to 2.6.0

* Wed Oct 21 2020 Devrim Gündüz <devrim@gunduz.org> - 2.5.5-1
- Update to 2.5.5

* Mon Aug 3 2020 Devrim Gündüz <devrim@gunduz.org> - 2.5.4-1
- Update to 2.5.4

* Sat Sep 28 2019 Devrim Gündüz <devrim@gunduz.org> - 2.5.3-1
- Update to 2.5.3

* Thu Oct 18 2018 Devrim Gündüz <devrim@gunduz.org> - 2.5.0-1
- Update to 2.5.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-1.1
- Rebuild against PostgreSQL 11.0

* Tue Mar 13 2018 - Devrim Gündüz <devrim@gunduz.org> 2.4.0-1
- Update to 2.4.0

* Fri Mar 9 2018 - Devrim Gündüz <devrim@gunduz.org> 2.3.0-3
- Add mariadb-devel as Requires, because it supplies versionless
  libmysqlclient.so as dependency.

* Wed Mar 7 2018 - Devrim Gündüz <devrim@gunduz.org> 2.3.0-2
- Add mariadb-libs dependency, per Fahar Abbas.

* Thu Oct 5 2017 - Devrim Gündüz <devrim@gunduz.org> 2.3.0-1
- Update to 2.3.0

* Thu Aug 24 2017 - Devrim Gündüz <devrim@gunduz.org> 2.2.0-2
- Attempt to link to mysqlclient available in the OS.

* Tue Jan 17 2017 - Devrim Gündüz <devrim@gunduz.org> 2.2.0-1
- Update to 2.2.0

* Tue Feb 23 2016 - Devrim Gündüz <devrim@gunduz.org> 2.1.2-1
- Update to 2.1.2

* Thu Feb 05 2015 - Devrim Gündüz <devrim@gunduz.org> 2.0.1-1
- Update to 2.0.1

* Fri Oct 10 2014 - Devrim Gündüz <devrim@gunduz.org> 1.0.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
