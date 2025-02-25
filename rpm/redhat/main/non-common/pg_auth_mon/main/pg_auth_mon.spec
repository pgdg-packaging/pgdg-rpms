%global sname	pg_auth_mon

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL extension to store authentication attempts
Name:		%{sname}_%{pgmajorversion}
Version:	3.0
Release:	3PGDG%{?dist}
License:	MIT
Source0:	https://github.com/RafiaSabih/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/RafiaSabih/%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel krb5-devel openssl-devel
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-libs

%description
This extension eases monitoring of login attempts to your database. Postgres
writes each login attempt to a log file, but it is hard to identify through
that information alone if your database is under malicious activity.
Maintaining separately information like the total number of successful login
attempts, or a timestamp of the last failed login helps to answer questions
like:
 - when has a user successfully logged in for the last time ?
 - has a user genuinely mistyped their password or has their username been compromised?
 - is there any particular time when a malicious role is active?

Once we have spot a suspicious activity, we may dig deeper by using this
information along with the log file to identify the particular IP address etc.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_auth_mon
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
This packages provides JIT support for pg_auth_mon
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Tue Feb 25 2025 Devrim Gunduz <devrim@gunduz.org> - 3.0-3PGDG
- Add missing BRs

* Thu Sep 19 2024 Devrim Gunduz <devrim@gunduz.org> - 3.0-2PGDG
- Update description and LLVM dependencies.

* Tue Aug 6 2024 Devrim Gunduz <devrim@gunduz.org> - 3.0-1PGDG
- Update to 3.0 per changes described at:
  https://github.com/RafiaSabih/pg_auth_mon/releases/tag/v3.0

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 2.0-3PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Fri Feb 23 2024 Devrim Gunduz <devrim@gunduz.org> - 2.0-2PGDG
- Add PGDG branding

* Sun Jun 4 2023 Devrim Gunduz <devrim@gunduz.org> - 2.0-1
- Update to 2.0

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.0-2.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu Feb 25 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Initial packaging for PostgreSQL RPM Repository
