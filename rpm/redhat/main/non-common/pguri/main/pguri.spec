%global sname pguri

%{!?llvm:%global llvm 1}

Summary:	uri type for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.20151224
Release:	7PGDG%{?dist}
License:	BSD
Source0:	https://github.com/petere/%{sname}/archive/%{version}.tar.gz
Patch0:		%{sname}-fix-pg_cppflags.patch
URL:		https://github.com/petere/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel uriparser-devel
Requires:	postgresql%{pgmajorversion}-server uriparser

Obsoletes:	%{sname}%{pgmajorversion} < 1.20151224-2

%description
This is an extension for PostgreSQL that provides a uri data type. Advantages
over using plain text for storing URIs include:

 * URI syntax checking
 * functions for extracting URI components
 * human-friendly sorting

The actual URI parsing is provided by the uriparser library, which supports
URI syntax as per RFC 3986.

Note that this might not be the right data type to use if you want to store
user-provided URI data, such as HTTP referrers, since they might contain
arbitrary junk.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pguri
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 17.0 clang-devel >= 17.0
Requires:	llvm => 17.0
%endif

%description llvmjit
This package provides JIT support for pguri
%endif

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p0

%build
#export PG_CPPFLAGS="$PG_CPPFLAGS -Wno-int-conversion"
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%license LICENSE.md
%{pginstdir}/lib/uri.so
%{pginstdir}/share/extension/uri-*.sql
%{pginstdir}/share/extension/uri.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/uri*.bc
   %{pginstdir}/lib/bitcode/uri/*.bc
%endif

%changelog
* Sun Jan 19 2025 Devrim Gündüz <devrim@gunduz.org> - 1.20151224-8PGDG
- Update LLVM dependencies
- Install licensef file

* Sun Sep 22 2024 Devrim Gündüz <devrim@gunduz.org> - 1.20151224-7PGDG
- Fix builds against PostgreSQL 16+. Per
  https://github.com/petere/pguri/issues/16#issuecomment-1827546607

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.20151224-6PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Sun Feb 25 2024 Devrim Gunduz <devrim@gunduz.org> - 1.20151224-5PGDG
- Add PGDG branding
- Fix PostgreSQL 16 builds

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.20151224-4.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.20151224-4
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> - 1.20151224-3
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.20151224-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.20151224-1.1
- Rebuild against PostgreSQL 11.0

* Tue Jan 26 2016 - Devrim Gündüz <devrim@gunduz.org> 1.20151224-1
- Update to 1.20151224

* Fri Apr 17 2015 - Devrim Gündüz <devrim@gunduz.org> 1.20150415-1
- Initial RPM packaging for PostgreSQL YUM Repository
