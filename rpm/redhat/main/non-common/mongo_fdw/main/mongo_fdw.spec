%global sname mongo_fdw

%global mongofdwmajver 5
%global mongofdwmidver 5
%global mongofdwminver 3

%global relver %{mongofdwmajver}_%{mongofdwmidver}_%{mongofdwminver}

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL foreign data wrapper for MongoDB
Name:		%{sname}_%{pgmajorversion}
Version:	%{mongofdwmajver}.%{mongofdwmidver}.%{mongofdwminver}
Release:	3PGDG%{?dist}
License:	LGPLv3
URL:		https://github.com/EnterpriseDB/%{sname}
Source0:	https://github.com/EnterpriseDB/%{sname}/archive/REL-%{relver}.tar.gz
Source1:	%{sname}-config.h
Patch0:		%{sname}-makefile-rpm.patch

BuildRequires:	postgresql%{pgmajorversion}-devel

%if 0%{?suse_version} >= 1499
Requires:		libsnappy1 libbson-1_0-0 libmongoc-1_0-0 libjson-c5
BuildRequires:		snappy-devel libbson-1_0-0-devel libmongoc-1_0-0-devel
%else
Requires:	snappy
Requires:	mongo-c-driver-libs libbson
BuildRequires:	mongo-c-driver-devel snappy-devel json-c-devel
BuildRequires:	cyrus-sasl-devel krb5-devel
BuildRequires:	libbson-devel
%endif
%if 0%{?suse_version} >= 1500
Requires:	libopenssl3
BuildRequires:	libopenssl-3-devel
%endif
%if 0%{?fedora} >= 41 || 0%{?rhel} >= 8
Requires:	openssl-libs >= 1.1.1k
BuildRequires:	openssl-devel
%endif

Requires:	postgresql%{pgmajorversion}-server cyrus-sasl-lib

%description
This PostgreSQL extension implements a Foreign Data Wrapper (FDW) for
MongoDB.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for mongo_fdw
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
This package provides JIT support for mongo_fdw
%endif

%prep
%setup -q -n %{sname}-REL-%{relver}
%patch -P0 -p0

%build

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1499
sed -i "s:^\(PG_CPPFLAGS.*\):\1 -I/usr/include/libmongoc-1.0 -I/usr/include/libbson-1.0 -I/usr/include/json-c -fPIC:g" Makefile
sed -i "s:\(^#include \"bson.h\"\):#include <bson.h>:g" mongo_fdw.c
sed -i "s:\(^#include \"bson.h\"\):#include <bson.h>:g" mongo_fdw.h
sed -i "s:\(^#include \"bson.h\"\)://\1:g" mongo_wrapper.h
%endif
%endif

%if 0%{?fedora} || 0%{?rhel} >= 8
sed -i "s:^\(PG_CPPFLAGS.*\):\1 -I/usr/include/json-c -fPIC:g" Makefile
sed -i "s:\(^#include \"bson.h\"\):#include <bson.h>:g" mongo_fdw.c
sed -i "s:\(^#include \"bson.h\"\):#include <bson.h>:g" mongo_fdw.h
sed -i "s:\(^#include \"bson.h\"\)://\1:g" mongo_wrapper.h
%endif

export LIBJSON=%{_includedir}/json-c

PATH=%{pginstdir}/bin:$PATH %{__make} -f Makefile USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

PATH=%{pginstdir}/bin:$PATH %{__make} -f Makefile USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/share/extension
%{__install} -m 755 README.md %{buildroot}%{pginstdir}/share/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{_docdir}/pgsql/extension/README.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/README-%{sname}.md
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Wed Nov 5 2025 Devrim Gunduz <devrim@gunduz.org> - 5.5.3-3PGDG
- Rebuild against OpenSSL 3 on SLES 15

* Tue Oct 28 2025 Devrim Gunduz <devrim@gunduz.org> - 5.5.3-2PGDG
- Do not run autogen.sh, so that we depend on the libraries in the
  operating system.

* Mon Oct 6 2025 Devrim Gunduz <devrim@gunduz.org> - 5.5.3-1PGDG
- Update to 5.5.3 per changes described at:
  https://github.com/EnterpriseDB/mongo_fdw/releases/tag/REL-5_5_3
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 5.5.2-4PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Fri Jan 3 2025 Devrim Gündüz <devrim@gunduz.org> - 5.5.2-3PGDG
- Use macros for version numbers to avoid build errors.

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 5.5.2-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support
- Re-add autogen.sh per:
  https://github.com/EnterpriseDB/mongo_fdw/issues/185#issuecomment-2371352239

* Fri Jul 12 2024 Devrim Gündüz <devrim@gunduz.org> - 5.5.2-1PGDG
- Update to 5.5.2 per changes described at:
  https://github.com/EnterpriseDB/mongo_fdw/releases/tag/REL-5_5_2

* Thu Jul 20 2023 Devrim Gündüz <devrim@gunduz.org> - 5.5.1-1PGDG
- Update to 5.5.1
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 5.5.0-1.1
- Rebuild against LLVM 15 on SLES 15

* Thu Dec 22 2022 Devrim Gündüz <devrim@gunduz.org> - 5.5.0-1
- Update to 5.5.0

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 5.4.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon May 30 2022 Devrim Gündüz <devrim@gunduz.org> - 5.4.0-1
- Update to 5.4.0

* Mon Feb 28 2022 Devrim Gündüz <devrim@gunduz.org> - 5.3.0-2
- Fix mongo_fdw installation on RHEL 7, per report and patch
  from Varsha Mehtre.

* Tue Jan 18 2022 Devrim Gündüz <devrim@gunduz.org> - 5.3.0-1
- Update to 5.3.0

* Tue Sep 21 2021 Devrim Gündüz <devrim@gunduz.org> - 5.2.10-2
- Remove patch0, no more needed.

* Thu Sep 16 2021 Devrim Gündüz <devrim@gunduz.org> - 5.2.10-1
- Update to 5.2.10

* Tue Sep 14 2021 Devrim Gündüz <devrim@gunduz.org> - 5.2.9-1
- Update to 5.2.9
- Add llvmjit subpackage
- Use OS supplied mongo-c-driver on RHEL8+ and Fedora.

* Mon May 3 2021 Devrim Gündüz <devrim@gunduz.org> - 5.2.8-1
- Update to 5.2.8
- Add missing BR and Requires, per Martin Marques.
- Use custom mongo-c-driver package on RHEL 7, per:
  https://redmine.postgresql.org/issues/6424
- Get rid of pg_config patches, export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 5.2.7-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Mon Aug 3 2020 Devrim Gündüz <devrim@gunduz.org> - 5.2.7-1
- Update to 5.2.7

* Fri Sep 27 2019 Devrim Gündüz <devrim@gunduz.org> - 5.2.6-1
- Update to 5.2.6

* Wed May 1 2019 Devrim Gündüz <devrim@gunduz.org> - 5.2.3-1
- Update to 5.2.3

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 5.2.1-1.1
- Rebuild against PostgreSQL 11.0

* Wed Mar 21 2018 - Devrim Gündüz <devrim@gunduz.org> 5.2.1-1
- Update to 5.2.1

* Wed Mar 14 2018 - Devrim Gündüz <devrim@gunduz.org> 5.2.0-1
- Update to 5.2.0

* Tue Jun 6 2017 - Devrim Gündüz <devrim@gunduz.org> 5.0.0-1
- Update to 5.2.0

* Sun Sep 7 2014 - Devrim Gündüz <devrim@gunduz.org> 1.0.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
