%global _privatelibs (libifasf15a|libifgen15a|libifgls|libifos15a|libifsql15a)\\.so
%global __requires_exclude (%{_privatelibs})
%global sname	informix_fdw
%global ifxfdwmajver 0
%global ifxfdwmidver 6
%global ifxfdwminver 3

%{!?llvm:%global llvm 1}

Summary:	A PostgreSQL Foreign Data Wrapper for Informix
Name:		%{sname}_%{pgmajorversion}
Version:	%{ifxfdwmajver}.%{ifxfdwmidver}.%{ifxfdwminver}
Release:	1PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/credativ/%{sname}
Source0:	https://github.com/credativ/%{sname}/archive/REL%{ifxfdwmajver}_%{ifxfdwmidver}_%{ifxfdwminver}.tar.gz
Source1:	%{sname}-libs.conf
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	postgresql%{pgmajorversion}-server
#BuildRequires:	some-informix-dependency maybe?
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 0.5.3-2

%description
The PostgreSQL Informix Foreign Datawrapper (FDW) module is a driver
for accessing remote Informix table from within PostgreSQL databases.
Foreign Tables are transparently accessed as normal PostgreSQL tables,
they can be used to join remote data against real PostgreSQL tables,
import remote data and more.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for informix_fdw
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for informix_fdw
%endif

%prep
%setup -q -n %{sname}-REL%{ifxfdwmajver}_%{ifxfdwmidver}_%{ifxfdwminver}
%patch -P 0 -p0

%build
PATH=/opt/IBM/Informix/bin:$PATH INFORMIXDIR=/opt/IBM/Informix USE_PGXS=1 %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install linker conf file:
%{__install} -d -m 755 %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%{__install} -m 700 %{SOURCE1} %{buildroot}%{_sysconfdir}/ld.so.conf.d/

%post
/usr/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.sql
%{pginstdir}/share/extension/*.control
%config %{_sysconfdir}/ld.so.conf.d/informix_fdw-libs.conf

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/ifx_fdw.*bc
    %{pginstdir}/lib/bitcode/ifx_fdw/*bc
%endif

%changelog
* Wed Oct 1 2025 2024 Devrim Gündüz <devrim@gunduz.org> - 0.6.3-1PGDG
- Update to 0.6.3 per changes described at:
  https://github.com/credativ/informix_fdw/releases/tag/REL0_6_3

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 0.6.2-3PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Sun Sep 28 2025 2024 Devrim Gündüz <devrim@gunduz.org> - 0.6.2-2PGDG
- Fix a few packaging issues:
  * Add patches for recent PostgreSQL versions
  * Ignore Informix related dependencies. They need be a parf of
    LD_LIBRARY_PATH or so.
  * Add LLVM subpackage
  * Add linker config file

* Wed Aug 28 2024 2024 Devrim Gündüz <devrim@gunduz.org> - 0.6.2-1PGDG
- Update to 0.6.2
- Add PGDG branding

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 0.5.3-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Wed Oct 21 2020 Devrim Gündüz <devrim@gunduz.org> - 0.5.3-1
- Update to 0.5.3

* Wed Aug 12 2020 Devrim Gündüz <devrim@gunduz.org> - 0.5.2-1
- Update to 0.5.2

* Tue Oct 23 2018 Devrim Gündüz <devrim@gunduz.org> - 0.5.0-1
- Update to 0.5.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.3.1-1.1
- Rebuild against PostgreSQL 11.0

* Thu Aug 25 2016 Devrim Gündüz <devrim@gunduz.org> 0.3.1-1
- Initial packaging for PostgreSQL RPM repository.
