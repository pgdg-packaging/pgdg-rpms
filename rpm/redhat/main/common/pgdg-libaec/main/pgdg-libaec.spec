%global		sname libaec
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		libaecinstdir %{pgdg_libaecinstdir}

# The libraries are found through the rpath only (there is no ld.so.conf.d
# file), so they must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL libaec. Consumers require
# pgdg-libaec by name instead:
%global		__provides_exclude_from ^%{libaecinstdir}/
%global		__requires_exclude ^lib(aec|sz)\\.so

%{!?runselftest:%global runselftest 0}

%if 0%{?rhel} == 8
%undefine __cmake_in_source_build
%endif

Name:		pgdg-%{sname}
Version:	1.1.7
Release:	1PGDG%{?dist}
Summary:	Adaptive Entropy Coding library
License:	BSD-2-Clause
URL:		https://gitlab.dkrz.de/k202009/libaec
Source0:	https://github.com/MathisRosenhauer/%{sname}/releases/download/v%{version}/%{sname}-%{version}.tar.gz

BuildRequires:	pgdg-srpm-macros >= 2.1.0
BuildRequires:	cmake >= 3.26 gcc
%if 0%{?suse_version} >= 1500
BuildRequires:	cmake-full
%else
BuildRequires:	cmake-rpm-macros
%endif

%description
Libaec provides fast loss-less compression of 1 up to 32 bit wide
signed or unsigned integers (samples). The library achieves best
results for low entropy data as often encountered in space imaging
instrument data or numerical model output from weather or climate
simulations. While floating point representations are not directly
supported, they can also be efficiently coded by grouping exponents
and mantissa.

Libaec implements Golomb Rice coding as defined in the Space Data
System Standard documents 121.0-B-2 and 120.0-G-2.

Libaec includes a free drop-in replacement for the SZIP library.

This package installs libaec under %{libaecinstdir}, for the packages in
the PostgreSQL RPM repository.

%package devel
Summary:	Development files for libaec (Adaptive Entropy Coding library)
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for libaec (Adaptive Entropy Coding library).

%prep
%setup -q -n %{sname}-%{version}

%build
%cmake \
	-DCMAKE_INSTALL_PREFIX:PATH=%{libaecinstdir} \
	-DCMAKE_INSTALL_LIBDIR:PATH=lib64 \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=include \
	-DCMAKE_INSTALL_RPATH:PATH=%{libaecinstdir}/lib64 \
	-DBUILD_STATIC_LIBS:BOOL=OFF \
%if %runselftest
	-DBUILD_TESTING:BOOL=ON
%else
	-DBUILD_TESTING:BOOL=OFF
%endif
%cmake_build

%install
%cmake_install

%check
%if %runselftest
%ctest
%endif

%files
%doc README.md CHANGELOG.md
%license LICENSE.txt
%dir %{libaecinstdir}
%dir %{libaecinstdir}/lib64
%{libaecinstdir}/lib64/lib*.so.*

%files devel
%{libaecinstdir}/include/
%{libaecinstdir}/lib64/lib*.so
%{libaecinstdir}/lib64/cmake/

%changelog
* Wed Oct 21 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1.7-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-libaec, so that the GIS stack does not need the EPEL libaec
  package on RHEL. Based on the Fedora spec file. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
