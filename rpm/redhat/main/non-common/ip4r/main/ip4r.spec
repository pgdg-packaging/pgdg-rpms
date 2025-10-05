%global sname ip4r

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Summary:	IPv4/v6 and IPv4/v6 range index type for PostgreSQL
Version:	2.4.2
Release:	5PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/RhodiumToad/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/RhodiumToad/ip4r
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

Provides:	postgresql-ip4r = %{version}-%{release}
Obsoletes:	%{sname}%{pgmajorversion} < 2.4.1-2

%description
ip4r is IPv4/v6 and IPv4/v6 range index type for PostgreSQL. ip4, ip4r, ip6,
ip6r, ipaddress and iprange are types that contain a single IPv4/IPv6 address
and a range of IPv4/IPv6 addresses respectively. They can be used as a more
flexible, indexable version of the cidr type.

~%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for ip4r
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
This package provides JIT support for ip4r
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%{__rm} -f %{buildroot}%{pginstdir}/include/server/extension/ip4r/ipr.h

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README.ip4r
%{pginstdir}/lib/ip4r.so
%{pginstdir}/share/extension/ip4r*

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Mon Oct 6 2025 Devrim Gunduz <devrim@gunduz.org> - 2.4.2-5PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 2.4.2-4PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Thu Jan 2 2025 Devrim Gündüz <devrim@gunduz.org> - 2.4.2-3PGDG
- Update LLVM dependencies and improve description.

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 2.4.2-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Tue Aug 1 2023 Devrim Gündüz <devrim@gunduz.org> - 2.4.2-1PGDG
- Update to 2.4.2
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 2.4.1-3.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.4.1-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 2.4.1-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org>
- Rebuild for PostgreSQL 12

* Wed May 22 2019 Devrim Gündüz <devrim@gunduz.org> - 2.4.1-1
- Update to 2.4.1

* Tue Apr 16 2019 Devrim Gündüz <devrim@gunduz.org> - 2.4-1
- Update to 2.4

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org>
- Rebuild against PostgreSQL 11.0

* Mon Jun 11 2018 Devrim Gündüz <devrim@gunduz.org> - 2.3-1
- Update to 2.3

* Wed Apr 26 2017 Devrim Gündüz <devrim@gunduz.org> - 2.2-1
- Update to 2.2

* Sun Sep 18 2016 Devrim Gündüz <devrim@gunduz.org> - 2.1-1
- Update to 2.1

* Sat Aug 13 2016 Devrim Gündüz <devrim@gunduz.org> - 2.0.3-1
- Update to 2.0.3

* Mon Nov 9 2015 Devrim Gündüz <devrim@gunduz.org> - 2.0.2-2
- Fixes for Fedora 23 and new doc layout in 9.5.

* Wed Jun 11 2014 Devrim Gündüz <devrim@gunduz.org> - 2.0.2-1
- Update to 2.0.2
- Update summary and description

* Sun Sep 15 2013 Devrim Gündüz <devrim@gunduz.org> - 2.0-1
- Update to 2.0, using the "extension" tarball.

* Thu Mar 08 2012 Devrim Gündüz <devrim@gunduz.org> - 1.05-3
- Provide postgresql-ip4r, to match the package name in EPEL.

* Tue Oct 12 2010 - Devrim Gündüz <devrim@gunduz.org> 1.05-2
- Apply 9.0 specific changes to spec file.

* Wed Apr 21 2010 - Devrim Gündüz <devrim@gunduz.org> 1.05-1
- Update to 1.05

* Mon Sep 7 2009 - Devrim Gündüz <devrim@gunduz.org> 1.04-1
- Update to 1.04

* Fri Feb 1 2008 - Devrim Gündüz <devrim@gunduz.org> 1.03-1
- Update to 1.03

* Sun Jan 20 2008 - Devrim Gündüz <devrim@gunduz.org> 1.02-1
- Update to 1.02

* Mon Jul 9 2007 - Devrim Gündüz <devrim@gunduz.org> 1.01-2
- Removed unneeded ldconfig calls, per bz review #246747

* Wed Jul 4 2007 - Devrim Gündüz <devrim@gunduz.org> 1.01-1
- Initial RPM packaging for Fedora
