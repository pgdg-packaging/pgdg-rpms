%global sname pg_failover_slots

%{!?llvm:%global llvm 1}

Summary:	Makes PostgreSQL logical replication slots practically usable across physical failover.
Name:		%{sname}_%{pgmajorversion}
Version:	1.1.0
Release:	2PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/EnterpriseDB/%{sname}
Source0:	https://github.com/EnterpriseDB/%{sname}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel wget pgdg-srpm-macros


Requires:	postgresql%{pgmajorversion}-server

%description
An extension that makes logical replication slots practically usable across
physical failover.

This extension does the following:

* Copy any missing slots from primary to standby
* Remove any slots from standby that are not found on primary
* Periodically synchronize position of slots on standby based on primary
* Ensure that selected standbys receive data before any of the logical slot
  walsenders can send data to consumers.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_failover_slots
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
This packages provides JIT support for pg_failover_slots
%endif

%prep
%setup -q -n %{sname}-%{version}
%build

PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 755 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Thu Jan 9 2025 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-2PGDG
- Update LLVM dependencies
- Fix location of the README file

* Tue Aug 27 2024 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1PGDG
- Update to 1.1.0 per changes described at:
  https://github.com/EnterpriseDB/pg_failover_slots/releases/tag/v1.1.0

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.0.1-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Fri Sep 8 2023 Devrim Gunduz <devrim@gunduz.org> - 1.0.1-1PGDG
- Update to 1.0.1
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.0.0-1.1
- Rebuild against LLVM 15 on SLES 15

* Mon Apr 17 2023 - Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1
- Initial packaging for the PostgreSQL RPM repository.
