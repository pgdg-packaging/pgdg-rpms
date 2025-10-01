%global sname	plprofiler

%global plprofilermajver 4
%global plprofilermidver 2
%global plprofilerminver 5

%global git_tag	REL%{plprofilermajver}_%{plprofilermidver}_%{plprofilerminver}
%global ppmajorver %{plprofilermajver}.%{plprofilermidver}

%global __ospython %{_bindir}/python3
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 10
%{expand: %%global pyver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%else
%{expand: %%global pyver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%endif
%global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	%{ppmajorver}.5
Release:	2PGDG%{dist}
Summary:	PL/pgSQL profiler
License:	Artistic-1.0, CDDL-1.0
URL:		https://github.com/bigsql/%{sname}
Source0:	https://github.com/bigsql/%{sname}/archive/refs/tags/%{git_tag}.tar.gz

Requires:	%{name}-server = %{version}
Requires:	%{name}-client

%description
PL/pgSQL profiler is an extension and command line tool to generate performance
profiles of PL/pgSQL code.

%package server
Provides:		%{name}%{version}-server%{?_isa} = %{version}-%{release}
Summary:		PostgreSQL server side extension part of the PL/pgSQL profiler
Requires:		postgresql%{pgmajorversion}-server
BuildRequires:	postgresql%{pgmajorversion}-devel

%description server
PostgreSQL server side extension part of the PL/pgSQL profiler.

%package client
Provides:		%{name}%{version}-client%{?_isa} = %{version}-%{release}
Summary:		Command Line Tool for the PL/pgSQL profiler
Requires:		python3
Requires:		python3-psycopg2
BuildRequires:	python3-six >= 1.4
BuildRequires:	python3-psycopg2
BuildRequires:	python3-devel python3-setuptools

%description client
Command Line Tool for the PL/pgSQL profiler

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for plprofiler
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 17.0 clang-devel >= 17.0
Requires:	llvm >= 17.0
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
cd python-%{sname}
%{__ospython} ./setup.py build
cd ..

%install
export USE_PGXS=1
export PATH=%{pginstdir}/bin:${PATH}
%make_install
cd python-%{sname}
%{__ospython} ./setup.py install -O1 --skip-build --root %{buildroot}
cd ..

%files

%files server
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*

%files client
%{_bindir}/%{sname}
%{python3_sitelib}/%{sname}/*
%{python3_sitelib}/%{sname}_client-%{ppmajorver}-*/*

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
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
