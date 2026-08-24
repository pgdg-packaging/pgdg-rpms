%global _vpath_builddir .
%global sname	dbt2

Summary:	Database Test 2 Differences from the TPC-C - Common package
Name:		%{sname}-common
Version:	0.62.0
Release:	2PGDG%{dist}
License:	GPLv2+
Source0:	https://github.com/osdldbt/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/osdldbt/%{sname}/
Patch1:		%{sname}-profile.patch

BuildRequires:	cmake curl-devel libev-devel
BuildRequires:	libpq5-devel gcc-c++

%if 0%{?suse_version} >= 1500
Requires:	libopenssl3
BuildRequires:	libopenssl-3-devel
%endif
%if 0%{?fedora} >= 41 || 0%{?rhel} >= 8 || 0%{?amzn}
Requires:	openssl-libs >= 1.1.1k
BuildRequires:	openssl-devel
%endif
%if 0%{?fedora} && 0%{?fedora} <= 44 && !0%{?amzn}
BuildRequires:	openssl-devel-engine
%endif

%if 0%{?suse_version} >= 1500
BuildRequires:	cmake-full
%else
BuildRequires:	cmake-rpm-macros

%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	libexpat-devel
Requires:	libev4
%else
BuildRequires:	expat-devel libev-devel
Requires:	libev
%endif

Requires:	R

%description
The Open Source Development Lab's Database Test 2 (DBT-2) test kit.

The database management systems that are currently supported are:

* PostgreSQL
* SQLite

This package includes binaries to run the test.

%prep
%setup -q -n %{sname}-%{version}
%patch -P 1 -p0

%build

CFLAGS="$CFLAGS -I%{pginstdir}/include/server -g -fPIE"; export CFLAGS

%{__install} -d build
pushd build
%cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr ..
%cmake_build
popd

%install
%{__rm} -rf %{buildroot}
pushd build
%cmake_install
popd

# Remove some files, we'll ship them with -extensions subpackages.
%{__rm} -f %{buildroot}/%{_datadir}/pgsql/*.sql
%{__rm} -rf %{buildroot}/usr/src/%{sname}/storedproc/

%{__mkdir} -p %{buildroot}/%{_sysconfdir}/
%{__cp} examples/dbt2_profile %{buildroot}/%{_sysconfdir}/dbt2_profile.conf

%files
%defattr(644,root,root,755)
%license LICENSE
%config %{_sysconfdir}/dbt2_profile.conf
%doc README
%attr (755,root,root) %{_bindir}/%{sname}*
%{_mandir}/man1/dbt2*

%changelog
* Mon Aug 24 2026 Devrim Gündüz <devrim@gunduz.org> - 0.62.0-2PGDG
- Fix macros for Amazon Linux 2023

* Fri Aug 14 2026 Devrim Gündüz <devrim@gunduz.org> - 0.62.0-1PGDG
- Update to 0.62.0

* Tue Apr 28 2026 Devrim Gündüz <devrim@gunduz.org> - 0.61.7-3PGDG
- (Once again) fix builds against CMake 4

* Thu Mar 19 2026 Devrim Gündüz <devrim@gunduz.org> - 0.61.7-2PGDG
- Fix builds against CMake 4

* Thu Jul 10 2025 Devrim Gündüz <devrim@gunduz.org> - 0.61.7-1PGDG
- Update to 0.61.7

* Mon Apr 7 2025 Devrim Gündüz <devrim@gunduz.org> - 0.61.6-1PGDG
- Update to 0.61.6
- Add missing BRs
- Remove RHEL 7 and SLES 12 support

* Fri Feb 16 2024 Devrim Gündüz <devrim@gunduz.org> - 0.53.9-1PGDG
- Update to 0.53.9
- Fix rpmlint warnings

* Tue Oct 24 2023 Devrim Gündüz <devrim@gunduz.org> - 0.53.7-1PGDG
- Update to 0.53.7
- Add SLES 15 support

* Thu Sep 7 2023 Devrim Gündüz <devrim@gunduz.org> - 0.53.6-1PGDG
- Update to 0.53.6

* Sun Jul 23 2023 Devrim Gündüz <devrim@gunduz.org> - 0.53.4-1PGDG
- Update to 0.53.4
- Add PGDG branding

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 0.50.1-1.1
- Modernise %%patch usage, which has been deprecated in Fedora 38

* Tue Mar 7 2023 Devrim Gündüz <devrim@gunduz.org> - 0.50.1-1
- Update to 0.50.1

* Mon Feb 27 2023 Devrim Gündüz <devrim@gunduz.org> - 0.49.1-1
- Update to 0.49.1

* Wed Jan 18 2023 Devrim Gündüz <devrim@gunduz.org> - 0.48.7-1
- Update to 0.48.7
- Remove Patch2, already in upstream.

* Sun Aug 28 2022 Devrim Gündüz <devrim@gunduz.org> - 0.48.3-2
- Add config file, and docs.

* Thu Aug 11 2022 Devrim Gündüz <devrim@gunduz.org> - 0.48.3-1
- Initial packaging
