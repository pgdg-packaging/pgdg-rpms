%global sname	pg_tle

%{!?llvm:%global llvm 1}

Summary:	Trusted Language Extensions for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.5.2
Release:	2PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/aws/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/aws/%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel flex krb5-devel
Requires:	postgresql%{pgmajorversion}-server

%if 0%{?suse_version} == 1500
Requires:	libopenssl1_1
BuildRequires:	libopenssl-1_1-devel
%endif
%if 0%{?suse_version} == 1600
Requires:	libopenssl3
BuildRequires:	libopenssl3-devel
%endif
%if 0%{?fedora} >= 41 || 0%{?rhel} >= 8
Requires:	openssl-libs >= 1.1.1k
BuildRequires:	openssl-devel
%endif

%description
Trusted Language Extensions (TLE) for PostgreSQL (pg_tle) is an open source
project that lets developers extend and deploy new PostgreSQL functionality
with lower administrative and technical overhead. Developers can use Trusted
Language Extensions for PostgreSQL to create and install extensions on
restricted filesystems and work with PostgreSQL internals through a SQL API.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for xxx
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
This package provides JIT support for xxx
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
%license LICENSE
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/src/*.bc
%endif

%changelog
* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 1.5.2-2PGDG
- Add SLES 16 support

* Wed Oct 1 2025 Devrim Gündüz <devrim@gunduz.org> - 1.5.2-1PGDG
- Update to 1.5.2 per changes described at:
  https://github.com/aws/pg_tle/releases/tag/v1.5.2

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.5.1-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Thu May 8 2025 Devrim Gündüz <devrim@gunduz.org> - 1.5.1-1PGDG
- Update to 1.5.1 per changes described at:
  https://github.com/aws/pg_tle/releases/tag/v1.5.1

* Sat Mar 22 2025 Devrim Gündüz <devrim@gunduz.org> - 1.5.0-1PGDG
- Update to 1.5.0 per changes described at:
  https://github.com/aws/pg_tle/releases/tag/v1.5.0
  https://github.com/aws/pg_tle/releases/tag/v1.4.0
  https://github.com/aws/pg_tle/releases/tag/v1.3.4
  https://github.com/aws/pg_tle/releases/tag/v1.3.3
  https://github.com/aws/pg_tle/releases/tag/v1.3.2
  https://github.com/aws/pg_tle/releases/tag/v1.3.1
  https://github.com/aws/pg_tle/releases/tag/v1.3.0

* Wed Feb 26 2025 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-4PGDG
- Add missing BRs

* Fri Jan 17 2025 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-3PGDG
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Thu Apr 4 2024 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1PGDG
- Initial packaging for the PostgreSQL RPM Repository
