%global sname postgresbson
%global pname pgbson
%global pgxnname bson

%{!?llvm:%global llvm 1}

# Propagate %%llvm into the actual build: PGXS decides whether to invoke
# clang/llvm-config based on with_llvm from the installed postgresql*-devel's
# Makefile.global, not from this spec's %%llvm. Without passing with_llvm=no
# through to make, setting %%llvm 0 here only drops the llvm BuildRequires/
# subpackage/files, while the build still tries to run clang regardless.
%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	2.2.0
Release:	1PGDG%{?dist}
Summary:	BSON data type for PostgreSQL
License:	MIT
URL:		https://github.com/buzzm/%{sname}
Source0:	https://api.pgxn.org/dist/%{pgxnname}/%{version}/%{pgxnname}-%{version}.zip
# Support libbson 2.x (Fedora 45+, EPEL 10.3+), per
# https://github.com/buzzm/postgresbson/pull/8
Patch0:		%{sname}-libbson2.patch

BuildRequires:	postgresql%{pgmajorversion}-devel unzip pkgconfig
# Not built on SLES and Amazon Linux 2023: they do not ship libbson.
BuildRequires:	libbson-devel
Requires:	postgresql%{pgmajorversion}-server

%description
This PostgreSQL extension implements the BSON data type, together with
functions to create and inspect BSON objects, typesafe dotpath accessors
and arrow operators similar to the ones of the json and jsonb types.
BSON is castable to json and jsonb in EJSON format to preserve type
fidelity.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for postgresbson
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
This package provides JIT support for postgresbson
%endif

%prep
%setup -q -n %{pgxnname}-%{version}
%patch -P0 -p1

# libbson 1.x and 2.x both ship bson/bson.h under the include directory
# that pkg-config reports, but only 1.x has a top level bson.h:
sed -i 's:^#include "bson.h":#include <bson/bson.h>:' %{pname}.c

%build
# libbson 2.x renamed the pkg-config module and the library:
if pkg-config --exists bson2; then
	bsonpc=bson2
else
	bsonpc=libbson-1.0
fi

# Upstream passes BSON_INCLUDES through PG_CFLAGS, which PGXS does not hand
# to clang when building the bitcode, so use PG_CPPFLAGS instead:
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} %{with_llvm_arg} \
	BSON_INCLUDES= PG_CPPFLAGS="$(pkg-config --cflags $bsonpc)" \
	BSON_SHLIB="$(pkg-config --libs $bsonpc)"

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} DESTDIR=%{buildroot} install

%files
%defattr(644,root,root,755)
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}--*.sql
%{pginstdir}/share/extension/%{pname}.control

%if %llvm
%files llvmjit
	%{pginstdir}/lib/bitcode/%{pname}*.bc
	%{pginstdir}/lib/bitcode/%{pname}/*.bc
%endif

%changelog
* Wed Oct 21 2026 Devrim Gündüz <devrim@gunduz.org> - 2.2.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/418
