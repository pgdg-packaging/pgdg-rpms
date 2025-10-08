%global sname pg_net

%{!?llvm:%global llvm 1}

Summary:	A PostgreSQL extension that enables asynchronous (non-blocking) HTTP/HTTPS requests with SQL
Name:		%{sname}_%{pgmajorversion}
Version:	0.19.7
Release:	3PGDG%{?dist}
URL:		https://github.com/supabase/%{sname}
Source0:	https://github.com/supabase/%{sname}/archive/refs/tags/v%{version}.tar.gz
License:	Apache-2.0
BuildRequires:	postgresql%{pgmajorversion}-devel libcurl-devel >= 7.83
Requires:	postgresql%{pgmajorversion}-server
%if 0%{?suse_version} >= 1500
Requires:	libcurl4 >= 7.83
%else
Requires:	libcurl >= 7.83
%endif

%description
The pg_net extension enables PostgreSQL to make asynchronous HTTP/HTTPS
requests in SQL. It eliminates the need for servers to continuously poll for
database changes and instead allows the database to proactively notify
external resources about significant events. It seamlessly integrates with
triggers, cron jobs (e.g., pg_cron), and procedures, unlocking numerous
possibilities.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_net
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
This package provides JIT support for pg_net
%endif


%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} DESTDIR=%{buildroot} install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{pginstdir}/lib/pg_net.so
%{pginstdir}/share/extension/pg_net*.sql
%{pginstdir}/share/extension/pg_net.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 0.19.7-3PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 0.19.7-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Thu Aug 28 2025 Devrim Gunduz <devrim@gunduz.org> - 0.19.7-1PGDG
- Update to 0.19.7 per changes described at
  https://github.com/supabase/pg_net/releases/tag/v0.19.7

* Sat Aug 23 2025 Devrim Gunduz <devrim@gunduz.org> - 0.19.6-1PGDG
- Update to 0.19.6 per changes described at
  https://github.com/supabase/pg_net/releases/tag/v0.19.6

* Tue Aug 5 2025 Devrim Gunduz <devrim@gunduz.org> - 0.19.5-1PGDG
- Update to 0.19.5 per changes described at
  https://github.com/supabase/pg_net/releases/tag/v0.19.5

* Thu Jul 31 2025 Devrim Gunduz <devrim@gunduz.org> - 0.19.4-1PGDG
- Update to 0.19.4 per changes described at
  https://github.com/supabase/pg_net/releases/tag/v0.19.4

* Wed Jul 16 2025 Devrim Gunduz <devrim@gunduz.org> - 0.19.3-1PGDG
- Update to 0.19.3 per changes described at
  https://github.com/supabase/pg_net/releases/tag/v0.19.3
  https://github.com/supabase/pg_net/releases/tag/v0.19.2

* Tue Jul 15 2025 Devrim Gunduz <devrim@gunduz.org> - 0.19.1-1PGDG
- Update to 0.19.1 per changes described at
  https://github.com/supabase/pg_net/releases/tag/v0.19.1

* Thu Jul 10 2025 Devrim Gunduz <devrim@gunduz.org> - 0.19.0-1PGDG
- Update to 0.19.0 per changes described at
  https://github.com/supabase/pg_net/releases/tag/v0.19.0

* Tue Jul 1 2025 Devrim Gunduz <devrim@gunduz.org> - 0.17.0-1PGDG
- Update to 0.17.0 per changes described at
  https://github.com/supabase/pg_net/releases/tag/v0.17.0

* Sun Jun 22 2025 Devrim Gunduz <devrim@gunduz.org> - 0.16.0-1PGDG
- Update to 0.16.0 per changes described at
  https://github.com/supabase/pg_net/releases/tag/v0.16.0

* Fri May 30 2025 Devrim Gunduz <devrim@gunduz.org> - 0.15.1-1PGDG
- Update to 0.15.1 per changes described at
  https://github.com/supabase/pg_net/releases/tag/v0.15.1

* Fri May 23 2025 Devrim Gunduz <devrim@gunduz.org> - 0.15.0-1PGDG
- Update to 0.15.0 per changes described at
  https://github.com/supabase/pg_net/releases/tag/v0.15.0

* Thu Jan 9 2025 Devrim Gunduz <devrim@gunduz.org> - 0.14.0-2PGDG
- Add SLES 15 support

* Wed Dec 11 2024 Devrim Gunduz <devrim@gunduz.org> - 0.14.0-1PGDG
- Update to 0.14.0 per changes described at
  https://github.com/supabase/pg_net/releases/tag/v0.14.0

* Tue Nov 5 2024 Devrim Gunduz <devrim@gunduz.org> - 0.13.0-1PGDG
- Update to 0.13.0 per changes described at
  https://github.com/supabase/pg_net/releases/tag/v0.13.0
  https://github.com/supabase/pg_net/releases/tag/v0.12.0

* Fri Oct 11 2024 Devrim Gunduz <devrim@gunduz.org> - 0.11.0-1PGDG
- Update to 0.11.0 per changes described at
  https://github.com/supabase/pg_net/releases/tag/v0.11.0

* Wed Sep 4 2024 Devrim Gunduz <devrim@gunduz.org> - 0.10.0-1PGDG
- Specify libcurl dependency per https://github.com/supabase/pg_net/issues/143 .
  This currently disables builds on RHEL 9 and 8.

* Tue Aug 27 2024 Devrim Gunduz <devrim@gunduz.org> - 0.10.0-1PGDG
- Update to 0.10.0 per changes described at
  https://github.com/supabase/pg_net/releases/tag/v0.10.0

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 0.9.2-2PGDG
- Update LLVM dependencies

* Thu Jul 18 2024 Devrim Gunduz <devrim@gunduz.org> - 0.9.2-1PGDG
- Update to 0.9.2 per changes described at
  https://github.com/supabase/pg_net/releases/tag/v0.9.2
- Update LLVM dependencies

* Fri May 10 2024 Devrim Gunduz <devrim@gunduz.org> - 0.9.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository

