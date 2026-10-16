# Only the C++ runtime of ANTLR 4 is packaged here: Babelfish needs it to
# link its generated parsers. The ANTLR tool itself is a Java application and
# is bundled in the Babelfish sources. Fedora ships this package, so this spec
# is meant for RHEL and Amazon Linux 2023, which do not.
%global giturl	https://github.com/antlr/antlr4

Name:		antlr4-cpp-runtime
Version:	4.13.2
Release:	2PGDG%{?dist}
Summary:	ANTLR runtime for C++
License:	BSD-3-Clause
URL:		https://www.antlr.org/
Source0:	%{giturl}/archive/%{version}/antlr4-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:	gcc-c++
BuildRequires:	make

%description
ANTLR (ANother Tool for Language Recognition) is a powerful parser generator
for reading, processing, executing, or translating structured text or binary
files.

This package provides the runtime library used by C++ ANTLR parsers.

%package devel
Summary:	Header files for programs that use C++ ANTLR parsers
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
ANTLR (ANother Tool for Language Recognition) is a powerful parser generator
for reading, processing, executing, or translating structured text or binary
files.

This package provides header files for programs that use C++ ANTLR parsers.

%prep
%setup -q -n antlr4-%{version}

%build
cd runtime/Cpp
# Tests are disabled because they try to download googletest from github.
%cmake \
  -DANTLR_BUILD_CPP_TESTS:BOOL=OFF \
  -DANTLR_BUILD_SHARED:BOOL=ON \
  -DANTLR_BUILD_STATIC:BOOL=OFF \
  -DANTLR4_INSTALL:BOOL=ON \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_INSTALL_LIBDIR=%{_libdir}
%cmake_build

%install
cd runtime/Cpp
%cmake_install
# README, LICENSE and VERSION are packaged with %%doc and %%license.
rm -rf %{buildroot}%{_docdir}/libantlr4

%files
%doc runtime/Cpp/README.md
%license LICENSE.txt
%{_libdir}/libantlr4-runtime.so.%{version}
%if 0%{?suse_version} >= 1500
%{_datadir}/doc/libantlr4/README.md
%{_datadir}/doc/libantlr4/VERSION
%endif

%files devel
%doc runtime/Cpp/cmake/Antlr4Package.md runtime/Cpp/cmake/README.md
%{_includedir}/antlr4-runtime/
%{_libdir}/libantlr4-runtime.so
%{_libdir}/cmake/antlr4-generator/
%{_libdir}/cmake/antlr4-runtime/

%changelog
* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 4.13.2-2PGDG
- Add/fix SLES support.

* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 4.13.2-1PGDG
- Initial packaging of the ANTLR 4 C++ runtime for RHEL and Amazon Linux
  2023, which do not ship it. Needed by babelfish_extensions.
