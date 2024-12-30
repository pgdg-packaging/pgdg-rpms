%global _build_id_links none
%global sname ogr_fdw

%{!?llvm:%global llvm 1}

%pgdg_set_gis_variables

# Use GDAL 3.10 on all of the platforms except RHEL 8:
%if 0%{?rhel} == 8
%global gdalfullversion %gdal38fullversion
%global gdalmajorversion %gdal38majorversion
%global gdalinstdir %gdal38instdir
%else
%global gdalfullversion %gdal310fullversion
%global gdalmajorversion %gdal310majorversion
%global gdalinstdir %gdal310instdir
%endif

Summary:	PostgreSQL foreign data wrapper for OGR
Name:		%{sname}_%{pgmajorversion}
Version:	1.1.5
Release:	4PGDG%{?dist}
License:	MIT
Source0:	https://github.com/pramsey/pgsql-ogr-fdw/archive/v%{version}.tar.gz
URL:		https://github.com/pramsey/pgsql-ogr-fdw
BuildRequires:	postgresql%{pgmajorversion}-devel gdal%{gdalmajorversion}-devel
BuildRequires:	pgdg-srpm-macros >= 1.0.34
Requires:	postgresql%{pgmajorversion}-server gdal%{gdalmajorversion}-libs

Obsoletes:	%{sname}%{pgmajorversion} < 1.0.12-3

%description
This library contains a PostgreSQL extension, a Foreign Data Wrapper (FDW)
handler of PostgreSQL which provides easy way for interacting with OGR.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for ogr_fdw
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 17.0 clang-devel >= 17.0
Requires:	llvm => 17.0
%endif

%description llvmjit
This packages provides JIT support for ogr_fdw
%endif

%prep
%setup -q -n pgsql-ogr-fdw-%{version}

%build
PATH=%{pginstdir}/bin:%{gdalinstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{pginstdir}/
%{__install} -d %{buildroot}%{pginstdir}/bin/
%{__install} -d %{buildroot}%{pginstdir}/share/extension
PATH=%{pginstdir}/bin:%{gdalinstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
%{__install} -m 755 README.md %{buildroot}%{pginstdir}/share/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{_docdir}/pgsql/extension/README.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/share/extension/README-%{sname}.md
%attr (755,root,root) %{pginstdir}/bin/ogr_fdw_info
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Mon Dec 30 2024 Devrim Gündüz <devrim@gunduz.org> - 1.1.5-4PGDG
- Rebuild against GDAL 3.10

* Fri Nov 22 2024 Devrim Gündüz <devrim@gunduz.org> - 1.1.5-4PGDG
- Use GDAL 3.8 on RHEL 8

* Sat Sep 21 2024 Devrim Gündüz <devrim@gunduz.org> - 1.1.5-3PGDG
- Rebuild against GDAL 3.9

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.1.5-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Mon Jul 1 2024 Devrim Gündüz <devrim@gunduz.org> 1.1.5-1PGDG
- Update to 1.1.5 per changes described at:
  https://github.com/pramsey/pgsql-ogr-fdw/releases/tag/v1.1.5

* Thu Feb 22 2024 Devrim Gündüz <devrim@gunduz.org> 1.1.4-3PGDG
- Rebuild against GDAL 3.8

* Thu Sep 14 2023 Devrim Gündüz <devrim@gunduz.org> 1.1.4-2PGDG
- Rebuild against GDAL 3.6
- Cleanup rpmlint warnings

* Wed Jul 19 2023 Devrim Gündüz <devrim@gunduz.org> 1.1.4-1
- Update to 1.1.4
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.1.3-5.1
- Rebuild against LLVM 15 on SLES 15

* Sat Apr 22 2023 Devrim Gündüz <devrim@gunduz.org> - 1.1.3-5
- Explicity specify GDAL versions, and use GDAL 3.6 on Fedora 38+

* Thu Mar 16 2023 John Harvey <john.harvey@crunchydata.com> - 1.1.3-4
- Add _build_id_links macro to stop mult. install conflicts

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.1.3-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Sat Oct 22 2022 Devrim Gündüz <devrim@gunduz.org> 1.1.3-2
- Oops, really build against GDAL 3.5.

* Wed Oct 19 2022 Devrim Gündüz <devrim@gunduz.org> 1.1.3-1
- Update to 1.1.3
- Simplify llvm part.

* Fri Sep 9 2022 Devrim Gündüz <devrim@gunduz.org> 1.1.2-2
- Rebuild against GDAL 3.5.X
- Update LLVM requirements for SLES 15

* Mon Aug 8 2022 Devrim Gündüz <devrim@gunduz.org> 1.1.2-1
- Update to 1.1.2

* Mon Sep 20 2021 Devrim Gündüz <devrim@gunduz.org> 1.1.1-1
- Update to 1.1.1

* Fri Feb 26 2021 Devrim Gündüz <devrim@gunduz.org> 1.1.0-2
- Rebuilt to fix some repo related issues

* Fri Feb 5 2021 Devrim Gündüz <devrim@gunduz.org> 1.1.0-1
- Update to 1.1.0
- Remove patches, and export PATH instead of them.
- Split llvmjit into its own subpackage.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 1.0.12-3
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Aug 20 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.12-2
- Rebuild against GDAL 3.1.2

* Wed Aug 12 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.12-1
- Update to 1.0.12

* Mon Nov 4 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0.9-1
- Update to 1.0.9

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0.8-2.1
- Rebuild for PostgreSQL 12

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0.8-2
- Use our gdal30 package

* Wed Aug 7 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0.8-1
- Update to 1.0.8
- Use our gdal23 packages

* Tue Oct 16 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0.7-1
- Update to 1.0.7
- Install bitcode files.

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0.5-1.1
- Rebuild against PostgreSQL 11.0

* Sun Jul 1 2018 Devrim Gündüz <devrim@gunduz.org> 1.0.5-1
- Update to 1.0.5

* Sat Oct 14 2017 Devrim Gündüz <devrim@gunduz.org> 1.0.4-1
- Update to 1.0.4

* Sat Aug 13 2016 Devrim Gündüz <devrim@gunduz.org> 1.0.2-1
- Update to 1.0.2

* Wed Jan 06 2016 Devrim Gündüz <devrim@gunduz.org> 1.0.1-1
- Update to 1.0.1

* Mon Sep 21 2015 - Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
