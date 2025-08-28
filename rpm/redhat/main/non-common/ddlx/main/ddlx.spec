%global sname ddlx
%global pname pgddl

Summary:	DDL eXtractor functions for PostgreSQL (ddlx)
Name:		%{sname}_%{pgmajorversion}
Version:	0.30
Release:	1PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/lacanoid/%{pname}/archive/%{version}.tar.gz
URL:		https://github.com/lacanoid/%{pname}
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
BuildArch:	noarch
Requires:	postgresql%{pgmajorversion}-server

%description
This is an SQL-only extension for PostgreSQL that provides uniform functions
for generating SQL Data Definition Language (DDL) scripts for objects created
in a database. It contains a bunch of SQL functions to convert PostgreSQL
system catalogs to nicely formatted snippets of SQL DDL, such as CREATE TABLE.

%prep
%setup -q -n %{pname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension/
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%license LICENSE.md
%defattr(644,root,root,755)
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%doc %{pginstdir}/doc/extension/README-%{sname}.md

%changelog
* Thu Aug 28 2025 Devrim Gündüz <devrim@gunduz.org> - 0.30-1PGDG
- Update to 0.30 per changes described at:
  https://github.com/lacanoid/pgddl/releases/tag/0.30

* Fri Dec 13 2024 Devrim Gündüz <devrim@gunduz.org> - 0.29-1PGDG
- Update to 0.29 per changes described at:
  https://github.com/lacanoid/pgddl/releases/tag/0.29

* Mon Oct 14 2024 Devrim Gündüz <devrim@gunduz.org> - 0.28-1PGDG
- Update to 0.28 per changes described at:
  https://github.com/lacanoid/pgddl/releases/tag/0.28

* Sun Oct 22 2023 Devrim Gündüz <devrim@gunduz.org> - 0.27-1PGDG
- Update to 0.27 per changes described at:
  https://github.com/lacanoid/pgddl/releases/tag/0.27

* Wed Oct 4 2023 Devrim Gündüz <devrim@gunduz.org> - 0.26-1PGDG
- Update to 0.26

* Thu Sep 21 2023 Devrim Gündüz <devrim@gunduz.org> - 0.24-1PGDG
- Update to 0.24

* Mon Aug 21 2023 Devrim Gündüz <devrim@gunduz.org> - 0.23-2PGDG
- Remove RHEL 6 bits
- Add PGDG branding
- Fix rpmlint warning

* Tue Jun 6 2023 Devrim Gündüz <devrim@gunduz.org> - 0.23-1
- Update to 0.23

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 0.22-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue Aug 3 2021 Devrim Gündüz <devrim@gunduz.org> - 0.22-1
- Update to 0.22

* Thu Jul 15 2021 Devrim Gündüz <devrim@gunduz.org> - 0.21-1
- Update to 0.21.0

* Fri Jun 18 2021 Devrim Gündüz <devrim@gunduz.org> - 0.19-1
- Update to 0.19.0

* Fri May 21 2021 Devrim Gündüz <devrim@gunduz.org> - 0.18-1
- Update to 0.18

* Thu Oct 8 2020 Devrim Gündüz <devrim@gunduz.org> - 0.17-1
- Update to 0.17

* Sun May 3 2020 Devrim Gündüz <devrim@gunduz.org> - 0.16-1
- Update to 0.16

* Mon Oct 28 2019 Devrim Gündüz <devrim@gunduz.org> - 0.15.0.1
- Update to 0.15.0

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 0.14-2.1
- Rebuild for PostgreSQL 12

* Sun Sep 1 2019 Devrim Gündüz <devrim@gunduz.org> - 0.14-1
- Fix OS versions in Makefile, the distro name in the packages changed.

* Wed Aug 14 2019 Devrim Gündüz <devrim@gunduz.org> 0.14-1
- Initial packaging for PostgreSQL RPM Repository
