%global sname timestamp9

Summary:	An efficient nanosecond precision timestamp type for Postgres
Name:		%{sname}_%{pgmajorversion}
Version:	1.4.0
Release:	7PGDG%{?dist}
%if 0%{?pgminorversion:1}
# pgminorversion is the PostgreSQL minor release that the build servers
# build against (global/Makefile.global): require at least that one, at
# build time and at runtime.
# The other postgresqlNN-* dependencies need no version here: the PostgreSQL
# subpackages require each other's exact version-release (all of them pin
# the client package, which pins -libs), so the server, contrib etc. follow
# -devel at build time and -libs at runtime.
BuildRequires:	postgresql%{pgmajorversion}-devel >= %{pgminorversion}
Requires:	postgresql%{pgmajorversion}-libs%{?_isa} >= %{pgminorversion}
%endif
License:	MIT
Source0:	https://github.com/optiver/%{sname}/archive/refs/tags/%{sname}-%{version}.tar.gz
URL:		https://github.com/optiver/%{sname}
BuildRequires:	gcc gcc-c++
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	cmake >= 3.17
Requires:	postgresql%{pgmajorversion}-server

%description
timestamp9 is an efficient nanosecond precision timestamp type for PostgreSQL.

%prep
%setup -q -n %{sname}-%{sname}-%{version}

%build
export PATH=%{pginstdir}/bin/:$PATH
%if 0%{?suse_version} >= 1500
# SUSE's %%cmake creates and enters the build directory itself, and its
# %%cmake_install runs make with -C build, so do not cd into it here.
%cmake -DCMAKE_POLICY_VERSION_MINIMUM=3.5
%cmake_build
%else
%{__mkdir} build
pushd build
%cmake -DCMAKE_POLICY_VERSION_MINIMUM=3.5 ..
%cmake_build
popd
%endif

%install
%{__rm} -rf %{buildroot}
export PATH=%{pginstdir}/bin/:$PATH
%if 0%{?suse_version} >= 1500
%cmake_install
%else
pushd build
%cmake_install
popd
%endif

%files
%defattr(644,root,root,755)
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Tue Nov 10 2026 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-7PGDG
- Fix the build on SLES: SUSE's %%cmake and %%cmake_install handle the
  build directory themselves, so do not cd into it first. Rebuilt on SLES
  only.

* Mon Nov 9 2026 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-6PGDG
- Rebuild against latest PostgreSQL minor releases
- Require at least the PostgreSQL minor release that the package is
  built against (pgminorversion, set by the build server Makefiles).

* Thu Sep 10 2026 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-5PGDG
- Add missing BR

* Mon Apr 13 2026 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-4PGDG
- Fix builds against CMake 4

* Tue Jan 28 2025 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-3PGDG
- Update project URL and remove reduntant BRs
- Remove RHEL 7 and SLES 12 support

* Wed Sep 13 2023 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-2PGDG
- Add PGDG branding

* Tue Jun 6 2023 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-1
- Update to 1.4.0

* Mon Feb 27 2023 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-1
- Update to 1.3.0

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Sun Aug 28 2022 - Devrim Gündüz <devrim@gunduz.org> 1.1.0-1
- Initial RPM packaging for PostgreSQL YUM Repository
