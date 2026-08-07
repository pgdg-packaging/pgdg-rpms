%global sname	plprofiler

%global plprofilermajver 4
%global plprofilermidver 2
%global plprofilerminver 5

%global git_tag	REL%{plprofilermajver}_%{plprofilermidver}_%{plprofilerminver}
%global ppmajorver %{plprofilermajver}.%{plprofilermidver}

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	%{ppmajorver}.5
Release:	6PGDG%{dist}
Summary:	PL/pgSQL profiler
License:	Artistic-1.0, CDDL-1.0
URL:		https://github.com/bigsql/%{sname}
Source0:	https://github.com/bigsql/%{sname}/archive/refs/tags/%{git_tag}.tar.gz

Requires:	%{name}-server = %{version}

%description
PL/pgSQL profiler is an extension and command line tool to generate performance
profiles of PL/pgSQL code.

%package server
Provides:	%{name}%{version}-server%{?_isa} = %{version}-%{release}
Summary:	PostgreSQL server side extension part of the PL/pgSQL profiler
Requires:	postgresql%{pgmajorversion}-server
BuildRequires:	postgresql%{pgmajorversion}-devel

%description server
PostgreSQL server side extension part of the PL/pgSQL profiler.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for plprofiler
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} == 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?suse_version} == 1600
BuildRequires:	llvm19-devel clang19-devel
Requires:	llvm19
%endif
%if 0%{?amzn}
BuildRequires:	llvm-devel >= 15.0 clang-devel >= 15.0
Requires:	llvm >= 15.0
%endif
%if ( 0%{?fedora} || 0%{?rhel} >= 8 ) && !0%{?amzn}
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for plprofiler
%endif

%prep
%setup -q -n %{sname}-%{git_tag}

%build
export USE_PGXS=1
export PATH=%{pginstdir}/bin:${PATH}
%make_build

%install
export USE_PGXS=1
export PATH=%{pginstdir}/bin:${PATH}
%make_install

%files

%files server
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 4.2.5-6PGDG
- Add Amazon Linux 2023 support.

* Wed Feb 4 2026 Devrim Gündüz <devrim@gunduz.org> - 4.2.5-5PGDG
- Split -client subpackage into its own package. Fixes
  https://github.com/pgdg-packaging/pgdg-rpms/issues/152

* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 4.2.5-4PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 4.2.5-3PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Mon Jan 27 2025 Devrim Gündüz <devrim@gunduz.org> - 4.2.5-2PGDG
- Update LLVM dependencies

* Fri Aug 16 2024 Devrim Gündüz <devrim@gunduz.org> - 4.2.5-1PGDG
- Update to 4.2.5

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 4.2.4-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Wed Sep 13 2023 Devrim Gündüz <devrim@gunduz.org> - 4.2.4-1PGDG
- Update to 4.2.4
.
* Tue Aug 1 2023 Devrim Gündüz <devrim@gunduz.org> - 4.2.2-1PGDG
- Update to 4.2.2
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 4.2.1-1.1
- Rebuild against LLVM 15 on SLES 15

* Wed Jan 4 2023 Devrim Gündüz <devrim@gunduz.org> - 4.2.1-1
- Update to 4.2.1

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 4.2-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Fri Oct 7 2022 Devrim Gündüz <devrim@gunduz.org> 4.2-1
- Initial packaging for the PostgreSQL RPM repository.
  First version of spec file is contributed by Jan Wieck,
  and I applied some changes to suit our style.
  Fixes https://redmine.postgresql.org/issues/7725
