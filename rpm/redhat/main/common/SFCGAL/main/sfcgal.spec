%global _vpath_builddir .

Summary:	C++ wrapper library around CGAL for PostGIS
Name:		SFCGAL
%if 0%{?suse_version} && 0%{?suse_version} >= 1500
Version:	1.4.1
BuildRequires:	cgal-devel
%endif

%if 0%{?rhel} && 0%{?rhel} == 8
Version:	1.4.1
Requires:	CGAL => 4.7
BuildRequires:	CGAL-devel >= 5.4
%endif

%if 0%{?rhel} && 0%{?rhel} >= 9
Version:	2.1.0
BuildRequires:	CGAL-devel >= 5.6
%endif

%if 0%{?fedora} && 0%{?fedora} >= 41
Version:	2.1.0
BuildRequires:	CGAL-devel >= 5.6
%endif

Release:	1PGDG%{?dist}
License:	GLPLv2
Source:		https://gitlab.com/sfcgal/SFCGAL/-/archive/v%{version}/SFCGAL-v%{version}.tar.gz

URL:		https://sfcgal.gitlab.io/SFCGAL/

%if 0%{?suse_version} >= 1500
BuildRequires:  cmake-full
%else
BuildRequires:  cmake-rpm-macros
%endif
BuildRequires:	cmake pgdg-srpm-macros

%if 0%{?suse_version} >= 1500
BuildRequires:	libboost_date_time1_66_0 libboost_thread1_66_0
BuildRequires:	libboost_system1_66_0 libboost_serialization1_66_0
BuildRequires:	libboost_serialization1_66_0-devel libboost_atomic1_66_0-devel
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	boost-thread, boost-system, boost-date-time, boost-serialization
%endif

BuildRequires:	mpfr-devel, gmp-devel, gcc-c++
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description
SFCGAL is a C++ wrapper library around CGAL with the aim of supporting
ISO 19107:2013 and OGC Simple Features Access 1.2 for 3D operations.

SFCGAL provides standard compliant geometry types and operations, that
can be accessed from its C or C++ APIs. PostGIS uses the C API, to
expose some SFCGAL's functions in spatial databases (cf. PostGIS
manual).

Geometry coordinates have an exact rational number representation and
can be either 2D or 3D.

%package libs
Summary:	The shared libraries required for SFCGAL

%description libs
The sfcgal-libs package provides the essential shared libraries for SFCGAL.

%package devel
Summary:	The development files for SFCGAL
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description devel
Development headers and libraries for SFCGAL.

%prep
%setup -q -n SFCGAL-v%{version}

%build

%{__install} -d build

%cmake .. \
%if 0%{?suse_version} >= 1500
	-DCMAKE_INSTALL_PREFIX:PATH=/usr \
%endif
	-D LIB_INSTALL_DIR=%{_lib} -DBoost_NO_BOOST_CMAKE=BOOL:ON .

%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags}

%install
%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} install/fast \
	DESTDIR=%{buildroot}

%post
/sbin/ldconfig

%post libs
/sbin/ldconfig

%postun
/sbin/ldconfig

%postun libs
/sbin/ldconfig

%files
%doc AUTHORS README.md NEWS
%license LICENSE
%{_bindir}/sfcgal-config

%files devel
%{_includedir}/%{name}/
%if 0%{?fedora} || 0%{?rhel} >= 8 || 0%{?suse_version} >= 1500
%{_libdir}/pkgconfig/sfcgal.pc
%endif

%files libs
%{_libdir}/libSFCGAL.so*

%changelog
* Wed May 14 2025 Devrim Gunduz <devrim@gunduz.org> - 2.1.0-1PGDG
- Update to 2.1.0 on RHEL and Fedora per changes described at:
  https://gitlab.com/sfcgal/SFCGAL/-/releases/v2.1.0

* Mon Apr 7 2025 Devrim Gunduz <devrim@gunduz.org> - 2.0.0-3PGDG
- Add missing BRs.

* Sat Dec 28 2024 Devrim Gunduz <devrim@gunduz.org> - 1.4.1-2PGDG
- Update to 1.4.1 on SLES 15

* Mon Dec 16 2024 Devrim Gunduz <devrim@gunduz.org> - 2.0.0-2PGDG
- Add RHEL 10 support

* Thu Oct 10 2024 Devrim Gunduz <devrim@gunduz.org> - 2.0.0-1PGDG
- Update to 2.0.0 on RHEL and Fedora per changes described at:
  https://gitlab.com/sfcgal/SFCGAL/-/releases/v2.0.0

* Fri Sep 6 2024 Devrim Gunduz <devrim@gunduz.org> - 1.5.1-1PGDG
- Update to 1.5.1 on RHEL 9

* Tue Jul 30 2024 Devrim Gunduz <devrim@gunduz.org> - 1.5.2-1PGDG
- Update to 1.5.2 on Fedora

* Wed Feb 21 2024 Devrim Gunduz <devrim@gunduz.org> - 1.3.10-2PGDG
- Add PGDG branding
- Switch back to boot 1.66 on SLES 15, which is the version in the
  SuSE repos.

* Tue Feb 6 2024 Devrim Gunduz <devrim@gunduz.org> - 1.3.10-1PGDG
- Update to 1.3.10 on SLES 15
- Rebuild against boost 1.80 on SLES 15

* Wed Jan 3 2024 Devrim Gunduz <devrim@gunduz.org> - 1.5.1-1PGDG
- Update to 1.5.1 on Fedora 39

* Tue Nov 7 2023 Devrim Gunduz <devrim@gunduz.org> - 1.5.0-1PGDG
- Update to 1.5.0 on Fedora 39 (1.5.0 requires CGAL 5.6).

* Tue Nov 7 2023 Devrim Gunduz <devrim@gunduz.org> - 1.4.1-15-1
- Fix setup line
- Remove support for older distros

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 1.4.1-14.1
- Modernise %%patch usage, which has been deprecated in Fedora 38

* Mon Mar 27 2023 Devrim Gündüz <devrim@gunduz.org> - 1.4.1-14
- Update download URL

* Tue Dec 6 2022 Devrim Gündüz <devrim@gunduz.org> - 1.4.1-13
- Remove AT support from RHEL 7 - ppc64le.

* Mon Aug 22 2022 Devrim Gündüz <devrim@gunduz.org> - 1.4.1-12
- Update RHEL 8 version to 1.4.1

* Wed Jul 13 2022 Devrim Gündüz <devrim@gunduz.org> - 1.4.1-11
- Add RHEL 9 support, and remove Fedora <= 34 support.

* Tue Feb 8 2022 Devrim Gündüz <devrim@gunduz.org> - 1.4.1-10
- Update to 1.4.1 for Fedora 35

* Tue Oct 19 2021 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-1
- Update to 1.4.0 for Fedora 35

* Mon Jun 14 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3.10-10
- Bump up release version to prevent conflict with OS packages.

* Wed Apr 14 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3.10-1
- Update to 1.3.10 for Fedora 33+

* Wed Apr 14 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3.9-5
- Add BR for Fedora 33+

* Wed Jan 27 2021 Devrim Gündüz <devrim@gunduz.org> - 1.3.9-4
- Add proper SLES 15 support

* Fri Oct 30 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.9-3
- Use cmake3 macro to build packages, and define vpath_builddir macro
  manually. This will solve the FTBFS issue on Fedora 33, per:
  https://fedoraproject.org/wiki/Changes/CMake_to_do_out-of-source_builds
  Also works on the other distros.

* Fri Oct 2 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.9-2
- We don't need CGAL dependency for CGAL >= 5.0 (Fedora 32 and above)

* Thu Oct 1 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.9-1
- Update to 1.3.9 for Fedora 33 (CGAL 5.1)

* Wed Aug 19 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.8-1
- Update to 1.3.8

* Thu Apr 23 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.7-4
- Add two patches for CGAL 5 builds

* Tue Mar 31 2020 Devrim Gündüz <devrim@gunduz.org> - 1.3.7-3
- Clarify dependencies on RHEL 8, per Talha Bin Rizwan.
- Depend on pgdg-srpm-macros

* Fri Jul 19 2019 John K. Harvey <john.harvey@crunchydata.com> - 1.3.7-2
- Fix broken macro

* Mon Jun 3 2019 Devrim Gündüz <devrim@gunduz.org> - 1.3.7-1
- Update to 1.3.7

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.3.2-1.1
- Rebuild against PostgreSQL 11.0

* Wed Sep 13 2017 Devrim Gündüz <devrim@gunduz.org> 1.3.2-1
- Update to 1.3.2 to support CGAL >= 4.10.1 on Fedora 26+

* Wed Jul 19 2017 Devrim Gündüz <devrim@gunduz.org> 1.2.2-2
- Also Requires CGAL, per Fahar Abbas (EDB QA)

* Thu Nov 19 2015 Oskari Saarenmaa <os@ohmu.fi> 1.2.2-1
- Update to 1.2.2 to support newer CGAL versions

* Fri Oct 30 2015 Devrim Gündüz <devrim@gunduz.org> 1.2.0-1
- Initial build for PostgreSQL YUM Repository.
