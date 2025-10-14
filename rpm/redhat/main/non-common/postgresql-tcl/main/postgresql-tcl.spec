%if 0%{?fedora} || 0%{?rhel}
%global debug_package %{nil}
%endif

%global _build_id_links none

%global pgtclmajorversion 3.1
%global pgtclprefix /usr/pgtcl%{pgtclmajorversion}

Name:		postgresql%{pgmajorversion}-tcl
Version:	%{pgtclmajorversion}.1
Release:	3PGDG%{?dist}
Summary:	A Tcl client library for PostgreSQL

URL:		https://github.com/flightaware/Pgtcl
License:	BSD

Source0:	https://github.com/flightaware/Pgtcl/archive/v%{version}.tar.gz

Requires:	tcl(abi) >= 8.5

BuildRequires:	postgresql%{pgmajorversion}-devel tcl-devel
BuildRequires:	autoconf

%{!?tcl_version: %global tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitearch: %global tcl_sitearch %{_libdir}/tcl%{tcl_version}}

%description
PostgreSQL is an advanced Object-Relational database management system.
The tcl-pgtcl package contains Pgtcl, a Tcl client library for connecting
to a PostgreSQL server.

%prep
%setup -q -n Pgtcl-%{version}

autoconf

%build
./configure --prefix=%{pgtclprefix}-%{pgmajorversion} \
	--libdir=%{pgtclprefix}-%{pgmajorversion}/lib \
	--with-tcl=%{_libdir} --with-postgres-include=%{pginstdir}/include \
	--with-postgres-lib=%{pginstdir}/lib --disable-rpath

%{__make} %{?_smp_mflags} all

%install
%{__rm} -rf %{buildroot}

%{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
# we don't really need to ship the .h file
%{__rm} -f %{buildroot}%{pgtclprefix}-%{pgmajorversion}/include/pgtclId.h

%files
%defattr(-,root,root,-)
%doc doc
%license LICENSE
%dir %{pgtclprefix}-%{pgmajorversion}/
%dir %{pgtclprefix}-%{pgmajorversion}/share/man/mann/
%{pgtclprefix}-%{pgmajorversion}/lib/libpgtcl.so
%{pgtclprefix}-%{pgmajorversion}/lib/pgtcl%{pgtclmajorversion}/libpgtcl%{version}.so
%{pgtclprefix}-%{pgmajorversion}/lib/pgtcl%{pgtclmajorversion}/pkgIndex.tcl
%{pgtclprefix}-%{pgmajorversion}/lib/pgtcl%{pgtclmajorversion}/postgres-helpers.tcl
%{pgtclprefix}-%{pgmajorversion}/share/man/mann/*

%changelog
* Wed Oct 15 2025 Devrim Gunduz <devrim@gunduz.org> - 3.1.1-3PGDG
- Oops, really update to 3.1.1

* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 3.1.1-2PGDG
- Remove redundant BR

* Sat Sep 27 2025 Devrim Gunduz <devrim@gunduz.org> - 3.1.1-1PGDG
- Update to 3.1.1 per changes described at:
  https://github.com/flightaware/Pgtcl/releases/tag/v3.1.1

* Fri Jun 14 2024 Devrim Gunduz <devrim@gunduz.org> - 3.1.0-1PGDG
- Update to 3.1.0 per changes described at:
  https://github.com/flightaware/Pgtcl/releases/tag/v3.1.0

* Mon Feb 26 2024 Devrim Gunduz <devrim@gunduz.org> - 3.0.1-1PGDG
- Update to 3.0.1
- Remove patch, not needed anymore.
- Enable -debug* subpackages

* Thu Oct 26 2023 Devrim Gunduz <devrim@gunduz.org> - 3.0.0-3PGDG
- Add PGDG branding
- Clean up rpmlint warnings
- Remove RHEL 6 bits

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 3.0.0-2.1
- Modernise %%patch usage, which has been deprecated in Fedora 38

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue May 31 2022 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-1
- Update to 3.0.0

* Thu Mar 31 2022 Devrim Gündüz <devrim@gunduz.org> - 2.8.0-1
- Update to 2.8.0
- Add a temp patch to fix version number in configure.in

* Tue Sep 21 2021 Devrim Gündüz <devrim@gunduz.org> - 2.7.7-1
- Update to 2.7.7

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.7.5-1
- Update to 2.7.5
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Fri Aug 28 2020 Devrim Gündüz <devrim@gunduz.org> - 2.7.4-1
- Update to 2.7.4

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-2.2
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.4.0-2.1
- Rebuild against PostgreSQL 11.0

* Sun Apr 1 2018 Devrim Gündüz <devrim@gunduz.org> 2.4.0-2
- Apply a workaround for conflicting build-ids.

* Thu Mar 1 2018 Devrim Gündüz <devrim@gunduz.org> 2.4.0-1
- Update to 2.4.0
- Move files under a new directory. This fixes the parallel
  installation issue (the previous version used to conflict)

* Sun Aug 6 2017 Devrim Gündüz <devrim@gunduz.org> 2.3.1-1
- Update to 2.3.1, by switching to pgtcl maintained by FlightAware.

* Wed Jan 27 2016 Devrim Gündüz <devrim@gunduz.org> 2.1.1-1
- Update to 2.1.1
- Unified spec file for all distros.

* Thu Nov 10 2011 Devrim Gunduz <devrim@gunduz.org> 2.0.0-1
- Update to 2.0.0
- Use better download URLs.

* Tue Aug 09 2011 Devrim Gunduz <devrim@gunduz.org> 1.9.0-1
- Update to 1.9.0, per #65.

* Fri Mar 12 2010 Devrim Gunduz <devrim@gunduz.org> 1.8.0-1
- Update to 1.8.0, per:
  http://pgfoundry.org/forum/forum.php?forum_id=1766

* Fri Mar 12 2010 Devrim Gunduz <devrim@gunduz.org> 1.7.1-1
- Use Fedora's spec for consistency, and update to 1.7.1
- Update spec for 9.0 multiple postmaster support.
