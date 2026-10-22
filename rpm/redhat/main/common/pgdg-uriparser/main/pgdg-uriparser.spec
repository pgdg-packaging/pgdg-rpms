%global		sname uriparser
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		uriparserinstdir %{pgdg_uriparserinstdir}

# The library is found through the rpath only (there is no ld.so.conf.d
# file), so it must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL uriparser. Consumers require
# pgdg-uriparser by name instead:
%global		__provides_exclude_from ^%{uriparserinstdir}/
%global		__requires_exclude ^liburiparser\\.so

%if 0%{?rhel} == 8
%undefine __cmake_in_source_build
%endif

Name:		pgdg-%{sname}
Version:	1.0.2
Release:	1PGDG%{?dist}
Summary:	URI parsing library - RFC 3986
License:	BSD-3-Clause
URL:		https://uriparser.github.io/
Source0:	https://github.com/%{sname}/%{sname}/releases/download/%{sname}-%{version}/%{sname}-%{version}.tar.bz2

BuildRequires:	pgdg-srpm-macros >= 2.1.0
BuildRequires:	cmake gcc-c++ make
%if 0%{?suse_version} >= 1500
BuildRequires:	cmake-full
%else
BuildRequires:	cmake-rpm-macros
%endif

%description
Uriparser is a strictly RFC 3986 compliant URI parsing library written
in C. uriparser is cross-platform, fast, supports Unicode and is
licensed under the New BSD license.

This package installs uriparser under %{uriparserinstdir}, for the
packages in the PostgreSQL RPM repository.

%package devel
Summary:	Development files for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{sname}.

%prep
%setup -q -n %{sname}-%{version}

%build
# The test suite needs GTest, which is not available on RHEL without EPEL:
%cmake \
	-DCMAKE_INSTALL_PREFIX:PATH=%{uriparserinstdir} \
	-DCMAKE_INSTALL_LIBDIR:PATH=lib64 \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=include \
	-DCMAKE_INSTALL_RPATH:PATH=%{uriparserinstdir}/lib64 \
	-DURIPARSER_BUILD_DOCS:BOOL=OFF \
	-DURIPARSER_BUILD_TESTS:BOOL=OFF \
	-DURIPARSER_BUILD_TOOLS:BOOL=ON
%cmake_build

%install
%cmake_install

%files
%doc THANKS AUTHORS ChangeLog
%license COPYING.BSD-3-Clause
%dir %{uriparserinstdir}
%dir %{uriparserinstdir}/bin
%dir %{uriparserinstdir}/lib64
%{uriparserinstdir}/bin/uriparse
%{uriparserinstdir}/lib64/lib%{sname}.so.1*

%files devel
%{uriparserinstdir}/include/
%{uriparserinstdir}/lib64/lib%{sname}.so
%{uriparserinstdir}/lib64/cmake/
%{uriparserinstdir}/lib64/pkgconfig/

%changelog
* Wed Oct 21 2026 Devrim Gunduz <devrim@gunduz.org> - 1.0.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-uriparser, so that the GIS stack does not need the EPEL
  uriparser package on RHEL. Based on the Fedora spec file. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
