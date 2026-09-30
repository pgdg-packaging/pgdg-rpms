%global sname pg_permissions

%{!?runselftest:%global runselftest 0}

%global permissionsmajver 1
%global permissionsminver 3

Summary:	PostgreSQL permission reports and checks
Name:		%{sname}_%{pgmajorversion}
Version:	1.4.1
Release:	3PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/cybertec-postgresql/%{sname}/archive/refs/tags/REL_%{permissionsmajver}_%{permissionsminver}.tar.gz
URL:		https://github.com/cybertec-postgresql/%{sname}
BuildRequires:	make
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
%if %runselftest
BuildRequires:	postgresql%{pgmajorversion}-server pgdg-srpm-macros >= 2.0.0
%endif
BuildArch:	noarch

%description
This extension allows you to review object permissions on a PostgreSQL
database.

%prep
%setup -q -n %{sname}-REL_%{permissionsmajver}_%{permissionsminver}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension

%check
%if %runselftest
%pgdg_check_installcheck
%endif

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README.%{sname}
%{pginstdir}/share/extension/%{sname}*.*

%changelog
* Tue Sep 29 2026 Devrim Gündüz <devrim@gunduz.org> - 1.4.1-3PGDG
- Add %%check, running the regression tests with the %%check helpers
  from pgdg-srpm-macros 2.0.0. It is disabled by default; enable it
  with --define 'runselftest 1'.

* Thu Sep 10 2026 Devrim Gündüz <devrim@gunduz.org> - 1.4.1-2PGDG
- Add missing BR

* Mon Jun 29 2026 Devrim Gündüz <devrim@gunduz.org> - 1.4.1-1PGDG
- Update to 1.4.1 per changes described at:
  https://github.com/cybertec-postgresql/pg_permissions/releases/tag/REL_1_4_1

* Fri Sep 5 2025 Devrim Gündüz <devrim@gunduz.org> - 1.4-2PGDG
- Rebuild

* Mon Aug 4 2025 Devrim Gündüz <devrim@gunduz.org> - 1.4-1PGDG
- Update to 1.4 per changes described at:
  https://github.com/cybertec-postgresql/pg_permissions/releases/tag/REL_1_4

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.3-2PGDG
- Fix tarball version

* Tue Jun 25 2024 Devrim Gündüz <devrim@gunduz.org> - 1.3-1PGDG
- Update to 1.3 per changes described at:
  https://github.com/cybertec-postgresql/pg_permissions/releases/tag/REL_1_3

* Fri Feb 23 2024 Devrim Gündüz <devrim@gunduz.org> - 1.2-1PGDG
- Update to 1.2
- Add PGDG branding

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.1-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Fri Sep 10 2021 Devrim Gündüz <devrim@gunduz.org> - 1.1-2
- Bump of for rpm Makefile issues on RHEL 7 and RHEL 8.

* Wed Sep 8 2021 Devrim Gündüz <devrim@gunduz.org> - 1.1-1
- Initial packaging for PostgreSQL RPM Repository
