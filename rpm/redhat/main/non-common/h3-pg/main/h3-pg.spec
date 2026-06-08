%global _vpath_builddir .
%global sname	h3-pg

%{!?llvm:%global llvm 1}

Summary:	Uber's H3 Hexagonal Hierarchical Geospatial Indexing System in PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	4.5.0
Release:	1PGDG%{dist}
License:	Apache
URL:		https://github.com/postgis/%{sname}
Source0:	https://github.com/postgis/%{sname}/archive/refs/tags/v%{version}.tar.gz
Patch0:		%{sname}-useosh3.patch
BuildRequires:	cmake >= 3.20 h3-devel >= 4.5.0-2
BuildRequires:	postgresql%{pgmajorversion}-devel

Requires:	postgresql%{pgmajorversion} h3 >= 4.5.0-2

%description
This library provides PostgreSQL bindings for the H3 Core Library.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for h3-pg
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
This package provides JIT support for h3-pg
%endif

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p0

%build
%{__install} -d build
pushd build
# h3-pg cannot find the header file on Fedora, so export CFLAGS:
%if 0%{?fedora}
CFLAGS="$CFLAGS -I%{_includedir}/h3"; export CFLAGS
%endif
%if 0%{?suse_version} >= 1500
cmake -DCMAKE_BUILD_TYPE=Release .. \
%else
%cmake .. -DCMAKE_BUILD_TYPE=Release .. \
%endif
	-DPostgreSQL_CONFIG=%{pginstdir}/bin/pg_config
%cmake_build
popd

%install
%{__rm} -rf %{buildroot}
pushd build
%cmake_install
popd

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%license LICENSE
%doc README.md
%{pginstdir}/lib/h3.so
%{pginstdir}/lib/h3_postgis.so
%{pginstdir}/share/extension/h3*.sql
%{pginstdir}/share/extension/h3.control
%{pginstdir}/share/extension/h3_postgis.control

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/h3*.bc
    %{pginstdir}/lib/bitcode/h3/src/*.bc
    %{pginstdir}/lib/bitcode/h3/src/binding/*.bc
    %{pginstdir}/lib/bitcode/h3_postgis/src/*.bc
%endif

%changelog
* Sun Jun 7 2026 Devrim Gündüz <devrim@gunduz.org> - 4.5.0-1PGDG
- Update to 4.5.0 per changes described at:
  https://github.com/postgis/h3-pg/releases/tag/v4.5.0
- Add llvmjit subpackage

* Thu Mar 19 2026 Devrim Gündüz <devrim@gunduz.org> - 4.2.3-4PGDG
- Fix builds against CMake 4

* Wed Feb 25 2026 Devrim Gündüz <devrim@gunduz.org> - 4.2.3-3PGDG
- Switch to using %%cmake macro instead of %%cmake3. This fixes
  Fedora 44 build and also works on other RHEL/Fedora distros.

* Mon Jan 19 2026 Devrim Gündüz <devrim@gunduz.org> - 4.2.3-2PGDG
- Use new URL

* Tue Jun 24 2025 Devrim Gündüz <devrim@gunduz.org> - 4.2.3-1PGDG
- Update to 4.2.3 per changes described at:
  https://github.com/zachasme/h3-pg/releases/tag/v4.2.3

* Tue Feb 11 2025 Devrim Gündüz <devrim@gunduz.org> - 4.2.2-1PGDG
- Update to 4.2.2 per changes described at:
  https://github.com/zachasme/h3-pg/releases/tag/v4.2.2

* Wed Feb 5 2025 Devrim Gündüz <devrim@gunduz.org> - 4.2.1-1PGDG
- Update to 4.2.1 per changes described at:
  https://github.com/zachasme/h3-pg/releases/tag/v4.2.1

* Mon Jan 20 2025 Devrim Gündüz <devrim@gunduz.org> - 4.2.0-1PGDG
- Update to 4.2.0 per changes described at:
  https://github.com/zachasme/h3-pg/releases/tag/v4.2.0

* Wed Nov 6 2024 Devrim Gündüz <devrim@gunduz.org> - 4.1.4-1PGDG
- Update to 4.1.4 per changes described at:
  https://github.com/zachasme/h3-pg/releases/tag/v4.1.4

* Thu Sep 19 2024 Devrim Gündüz <devrim@gunduz.org> - 4.1.3-3PGDG
- Fix builds on Fedora

* Thu May 23 2024 Devrim Gündüz <devrim@gunduz.org> - 4.1.3-2PGDG
- Fix changelog date.

* Sun Nov 5 2023 Devrim Gündüz <devrim@gunduz.org> - 4.1.3-1PGDG
- Initial packaging of h3-pg.
