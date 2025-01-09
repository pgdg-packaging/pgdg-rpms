%global sname pgmemcache

%{!?llvm:%global llvm 1}

Summary:	A PostgreSQL API to interface with memcached
Name:		%{sname}_%{pgmajorversion}
Version:	2.3.0
Release:	9PGDG%{?dist}
License:	BSD
Source0:	https://github.com/ohmu/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/Ohmu/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel libmemcached-devel
BuildRequires:	pgdg-srpm-macros cyrus-sasl-devel
Requires:	postgresql%{pgmajorversion}-server libmemcached

Obsoletes:	%{sname}-%{pgmajorversion} < 2.3.0-4

%description
pgmemcache is a set of PostgreSQL user-defined functions that provide
an interface to memcached.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgmemcache
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
This packages provides JIT support for pgmemcache
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.rst
%license LICENSE
%{pginstdir}/lib/pgmemcache.so
%{pginstdir}/share/extension/pgmemcache--*.sql
%{pginstdir}/share/extension/pgmemcache.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Thu Jan 9 2025 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-9PGDG
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-8PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Tue Oct 24 2023 Devrim Gunduz <devrim@gunduz.org> - 2.3.0-7PGDG
- Add PGDG branding
- Cleanup rpmlint warnings

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 2.3.0-6.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-6
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-4
- Remove pgxs patches, and export PATH instead.
- Remove RHEL 6 stuff.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-4
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-3.2
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-3.1
- Rebuild against PostgreSQL 11.0

* Wed Aug 22 2018 - Devrim Gündüz <devrim@gunduz.org> 2.3.0-3
- Add v11+ support

* Mon Jul 17 2017 - Devrim Gündüz <devrim@gunduz.org> 2.3.0-2
- Add libmemcached dependency, per Fahar Abbas (EDB QA)

* Tue Jan 26 2016 - Devrim Gündüz <devrim@gunduz.org> 2.3.0-1
- Update to 2.3.0
- Use more macros in spec file

* Wed Nov 20 2013 - Devrim GÜNDÜZ <devrim@gunduz.org> 2.1.2-1
- Update to 2.1.2
- Fix various issues in init script

* Sat Jul 3 2010 - Devrim GÜNDÜZ <devrim@gunduz.org> 2.0.4-1
- Initial packaging for PostgreSQL RPM Repository
