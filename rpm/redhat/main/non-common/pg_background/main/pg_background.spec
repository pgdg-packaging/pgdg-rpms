%global sname	pg_background

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL Background Worker
Name:		%{sname}_%{pgmajorversion}
Version:	1.5
Release:	3PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/vibhorkum/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/vibhorkum/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	krb5-devel openssl-devel
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-libs

%description
This extension allows you to execute arbitrary SQL commands in background
worker processes within PostgreSQL. It provides a convenient way to offload
long-running tasks, perform operations asynchronously, and implement
autonomous transactions.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_background
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
This package provides JIT support for pg_background
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
* Tue Oct 7 2025 Devrim Gündüz <devrim@gunduz.org> - 1.5-3PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.5-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Thu Sep 4 2025 Devrim Gündüz <devrim@gunduz.org> - 1.5-1PGDG
- Update to 1.5 per changes described at:
  https://github.com/vibhorkum/pg_background/releases/tag/v1.4
  https://github.com/vibhorkum/pg_background/releases/tag/v1.5

* Tue Feb 25 2025 Devrim Gündüz <devrim@gunduz.org> - 1.3-3PGDG
- Add missing BRs

* Mon Jan 6 2025 Devrim Gündüz <devrim@gunduz.org> - 1.3-2PGDG
- Update description

* Tue Oct 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.3-1PGDG
- Update to 1.3 per changes described at:
  https://github.com/vibhorkum/pg_background/releases/tag/v1.3

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.2-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Thu Sep 7 2023 Devrim Gündüz <devrim@gunduz.org> - 1.2-1PGDG
- Update to 1.2
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.1-1.1
- Rebuild against LLVM 15 on SLES 15

* Sun Apr 23 2023 Devrim Gündüz <devrim@gunduz.org> - 1.1-1
- Update to 1.1

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu May 20 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0-1
- Initial packaging for PostgreSQL RPM Repository
