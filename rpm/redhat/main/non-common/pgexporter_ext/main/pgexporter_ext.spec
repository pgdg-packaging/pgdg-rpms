%global sname	pgexporter_ext
%global _vpath_builddir .

Name:           %{sname}_%{pgmajorversion}
Version:	0.2.5
Release:	2PGDG%{dist}
%if 0%{?pgminorversion:1}
# Built against this PostgreSQL minor release: require at least that one.
# The other postgresqlNN-* dependencies need no version here: the PostgreSQL
# subpackages require each other's exact version-release (all of them pin
# the client package, which pins -libs), so the server, contrib etc. follow
# -devel at build time and -libs at runtime.
BuildRequires:	postgresql%{pgmajorversion}-devel >= %{pgminorversion}
Requires:	postgresql%{pgmajorversion}-libs%{?_isa} >= %{pgminorversion}
%endif
Summary:	PostgreSQL extension to provide additional Prometheus metrics for pgexporter.
License:	BSD
URL:		https://github.com/pgexporter/%{sname}
Source0:	https://github.com/pgexporter/%{sname}/archive/refs/tags/%{version}.tar.gz

BuildRequires:	gcc cmake make
BuildRequires:	openssl openssl-devel postgresql%{pgmajorversion}-devel
Requires:	openssl postgresql%{pgmajorversion}-server

%description
pgexporter_ext is an extension for PostgreSQL to provide additional
Prometheus metrics for pgexporter.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__mkdir} build
pushd build
export PATH=%{pginstdir}/bin/:$PATH
cmake -DCMAKE_BUILD_TYPE=Release ..
%cmake_build
popd

%install
pushd build
export PATH=%{pginstdir}/bin/:$PATH
%cmake_install
popd

%files
%license LICENSE
%doc CODE_OF_CONDUCT.md README.md AUTHORS
%{pginstdir}/lib/%{sname}.so*
%{pginstdir}/share/extension/%{sname}*

%changelog
* Mon Nov 9 2026 Devrim Gündüz <devrim@gunduz.org> - 0.2.5-2PGDG
- Rebuild against latest PostgreSQL minor releases
- Require at least the PostgreSQL minor release that the package is
  built against (pgminorversion, set by the build server Makefiles).

* Sat Jun 20 2026 - Devrim Gündüz <devrim@gunduz.org> 0.2.5-1PGDG
- Update to 0.2.5 per changes described at:
  https://github.com/pgexporter/pgexporter_ext/releases/tag/0.2.5

* Mon Apr 20 2026 - Devrim Gündüz <devrim@gunduz.org> 0.2.4-2PGDG
- Fix builds against CMake 4.

* Mon Sep 23 2024 - Devrim Gündüz <devrim@gunduz.org> 0.2.4-1PGDG
- Update to 0.2.4 per changes described at:
  https://github.com/pgexporter/pgexporter_ext/releases/tag/0.2.4

* Mon Sep 11 2023 - Devrim Gündüz <devrim@gunduz.org> 0.2.3-1PGDG
- Update to 0.2.3
- Add PGDG branding

* Mon Apr 24 2023 - Devrim Gündüz <devrim@gunduz.org> 0.2.2-1
- Update to 0.2.2

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 0.2.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu Nov 3 2022 - Devrim Gündüz <devrim@gunduz.org> 0.2.0-1
- Update to 0.2.0

* Fri May 27 2022 - Devrim Gündüz <devrim@gunduz.org> 0.1.2-1
- Update to 0.1.2

* Wed Apr 27 2022 - Devrim Gündüz <devrim@gunduz.org> 0.1.1-1
- Update to 0.1.1

* Fri Oct 22 2021 - Devrim Gündüz <devrim@gunduz.org> 0.1.0-1
- Initial packaging for PostgreSQL RPM repository. Used upstream's
  spec file.

