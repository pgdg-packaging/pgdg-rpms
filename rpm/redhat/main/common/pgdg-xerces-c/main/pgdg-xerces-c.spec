%global		sname xerces-c
# Versionless prefix from pgdg-srpm-macros, per
# https://github.com/pgdg-packaging/pgdg-rpms/issues/28
%global		xercescinstdir %{pgdg_xercescinstdir}

# The library is found through the rpath only (there is no ld.so.conf.d
# file), so it must not satisfy the dependencies of OS or EPEL packages,
# and our packages must not pick the OS or EPEL xerces-c. Consumers require
# pgdg-xerces-c by name instead:
%global		__provides_exclude_from ^%{xercescinstdir}/
%global		__requires_exclude ^libxerces-c.*\\.so

%if 0%{?rhel} == 8
%undefine __cmake_in_source_build
%endif

Name:		pgdg-%{sname}
Version:	3.3.0
Release:	1PGDG%{?dist}
Summary:	Validating XML Parser
License:	Apache-2.0
URL:		https://xerces.apache.org/xerces-c/
Source0:	https://downloads.apache.org/xerces/c/3/sources/%{sname}-%{version}.tar.xz

BuildRequires:	pgdg-srpm-macros >= 2.1.0
BuildRequires:	cmake gcc-c++ make
%if 0%{?suse_version} >= 1500
BuildRequires:	cmake-full
%else
BuildRequires:	cmake-rpm-macros
%endif

%description
Xerces-C is a validating XML parser written in a portable subset of C++.
Xerces-C makes it easy to give your application the ability to read and write
XML data. A shared library is provided for parsing, generating, manipulating,
and validating XML documents. Xerces-C is faithful to the XML 1.0
recommendation and associated standards: XML 1.0 (Third Edition), XML 1.1
(First Edition), DOM Level 1, 2, 3 Core, DOM Level 2.0 Traversal and Range, DOM
Level 3.0 Load and Save, SAX 1.0 and SAX 2.0, Namespaces in XML, Namespaces in
XML 1.1, XML Schema, XML Inclusions).

This package installs Xerces-C under %{xercescinstdir}, for the packages
in the PostgreSQL RPM repository.

%package devel
Summary:	Header files and libraries for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files and libraries for %{sname}.

%prep
%setup -q -n %{sname}-%{version}

%build
export CFLAGS="%{optflags} -fno-strict-aliasing"
export CXXFLAGS="$CFLAGS"
%cmake \
	-DCMAKE_INSTALL_PREFIX:PATH=%{xercescinstdir} \
	-DCMAKE_INSTALL_LIBDIR:PATH=lib64 \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=include \
	-DCMAKE_INSTALL_RPATH:PATH=%{xercescinstdir}/lib64 \
	-Dsse2=FALSE
%cmake_build

%install
%cmake_install
# The samples, as in the Fedora package:
%{__rm} -rf %{buildroot}%{xercescinstdir}/bin
%{__rm} -f %{buildroot}%{xercescinstdir}/lib64/*.la
%{__rm} -rf %{buildroot}%{xercescinstdir}/share/doc

%files
%license LICENSE
%doc README NOTICE
%dir %{xercescinstdir}
%dir %{xercescinstdir}/lib64
%{xercescinstdir}/lib64/libxerces-c-3.3.so

%files devel
%{xercescinstdir}/include/
%{xercescinstdir}/lib64/cmake/
%{xercescinstdir}/lib64/libxerces-c.so
%{xercescinstdir}/lib64/pkgconfig/

%changelog
* Wed Oct 21 2026 Devrim Gunduz <devrim@gunduz.org> - 3.3.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, installed under
  /usr/pgdg-xerces-c, so that the GIS stack does not need the EPEL
  xerces-c package on RHEL. Based on the Fedora spec file. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
