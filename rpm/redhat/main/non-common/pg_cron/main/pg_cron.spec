%global sname pg_cron

%{!?llvm:%global llvm 1}

Summary:	Run periodic jobs in PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.6.7
Release:	4PGDG%{dist}
License:	AGPLv3
Source0:	https://github.com/citusdata/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/citusdata/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel libxml2-devel
Requires:	postgresql%{pgmajorversion}-server
Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

%if 0%{?suse_version} >= 1500
Requires:	libopenssl3
BuildRequires:	libopenssl-3-devel openldap2-devel
%endif
%if 0%{?fedora} >= 41 || 0%{?rhel} >= 8
Requires:	openssl-libs >= 1.1.1k
BuildRequires:	openssl-devel openldap-devel
%endif

%description
pg_cron is a simple cron-based job scheduler for PostgreSQL
that runs inside the database as an extension. It uses the
same syntax as regular cron, but it allows you to schedule
PostgreSQL commands directly from the database.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_cron
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} == 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?suse_version} == 1600
BuildRequires:	llvm19-devel clang19-devel
Requires:	llvm19
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for pg_cron
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
PATH=%{pginstdir}/bin/:$PATH %make_install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md
%license LICENSE
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}-*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Wed Nov 5 2025 Devrim Gündüz <devrim@gunduz.org> - 1.6.7-4PGDG
- Rebuild against OpenSSL 3 on SLES 15

* Tue Oct 7 2025 Devrim Gündüz <devrim@gunduz.org> - 1.6.7-3PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.6.7-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Thu Sep 4 2025 Devrim Gündüz <devrim@gunduz.org> - 1.6.7-1PGDG
- Update to 1.6.7, per changes described at:
  https://github.com/citusdata/pg_cron/releases/tag/v1.6.7
  https://github.com/citusdata/pg_cron/releases/tag/v1.6.6

* Thu Dec 12 2024 Devrim Gündüz <devrim@gunduz.org> - 1.6.5-1PGDG
- Update to 1.6.5, per changes described at:
  https://github.com/citusdata/pg_cron/releases/tag/v1.6.5
- Remove SLES 12 bits and also update LLVM dependencies.

* Fri Aug 16 2024 Devrim Gündüz <devrim@gunduz.org> - 1.6.4-1PGDG
- Update to 1.6.4, per changes described at:
  https://github.com/citusdata/pg_cron/releases/tag/v1.6.4

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.6.3-1PGDG
- Update to 1.6.3, per changes described at:
  https://github.com/citusdata/pg_cron/releases/tag/v1.6.3
- Update LLVM dependencies
- Remove RHEL 7 support

* Tue Oct 24 2023 Devrim Gündüz <devrim@gunduz.org> - 1.6.2-1PGDG
- Update to 1.6.2, per changes described at:
  https://github.com/citusdata/pg_cron/releases/tag/v1.6.2

* Wed Oct 18 2023 Devrim Gündüz <devrim@gunduz.org> - 1.6.1-1PGDG
- Update to 1.6.1, per changes described at:
  https://github.com/citusdata/pg_cron/releases/tag/v1.6.1

* Fri Sep 8 2023 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-1PGDG
- Update to 1.6.0, per changes described at:
  https://github.com/citusdata/pg_cron/releases/tag/v1.6.0
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.5.2-1.1
- Rebuild against LLVM 15 on SLES 15

* Mon Apr 10 2023 Devrim Gündüz <devrim@gunduz.org> - 1.5.2-1
- Update to 1.5.2, per changes described at:
  https://github.com/citusdata/pg_cron/releases/tag/v1.5.2

* Mon Feb 27 2023 Devrim Gündüz <devrim@gunduz.org> - 1.5.1-1
- Update to 1.5.1, per changes described at:
  https://github.com/citusdata/pg_cron/releases/tag/v1.5.0
  and
  https://github.com/citusdata/pg_cron/releases/tag/v1.5.1

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.4.2-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue Aug 23 2022 Devrim Gündüz <devrim@gunduz.org> - 1.4.2-1
- Update to 1.4.2
- Add a (temp) patch to fix builds on Fedora 36, per
  https://github.com/citusdata/pg_cron/issues/187

* Sat Oct 16 2021 Devrim Gündüz <devrim@gunduz.org> - 1.4.1-2
- Fix SLES dependencies, per report from Tiago ANASTACIO.

* Mon Sep 27 2021 Devrim Gündüz <devrim@gunduz.org> - 1.4.1-1
- Update to 1.4.1

* Wed May 26 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-2
- Remove pgxs patches, and export PATH instead.

* Thu Apr 22 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-1
- Update to 1.3.1

* Thu Oct 8 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-1
- Update to 1.3.0

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1.1
- Rebuild for PostgreSQL 12

* Fri Sep 6 2019 Devrim Gündüz <devrim@gunduz.org> 1.2.0-1
- Update to 1.2.0

* Tue Apr 16 2019 Devrim Gündüz <devrim@gunduz.org> 1.1.4-1
- Update to 1.1.4

* Wed Feb 13 2019 Devrim Gündüz <devrim@gunduz.org> 1.1.3-2
- Rebuild against PostgreSQL 11.2

* Tue Feb 5 2019 Devrim Gündüz <devrim@gunduz.org> 1.1.3-1
- Initial RPM packaging for PostgreSQL RPM Repository,
