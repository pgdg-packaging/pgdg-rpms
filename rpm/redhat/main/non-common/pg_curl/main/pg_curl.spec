%global sname pg_curl

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL tool for transferring data with URL syntax
Name:		%{sname}_%{pgmajorversion}
Version:	2.4.4
Release:	3PGDG%{?dist}
URL:		https://github.com/RekGRpth/%{sname}
Source0:	https://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
License:	MIT
BuildRequires:	postgresql%{pgmajorversion}-devel libcurl-devel libxml2-devel
Requires:	postgresql%{pgmajorversion}-server

%description
pg_curl is a PostgreSQL tool for transferring data with URL syntax, supporting
DICT, FILE, FTP, FTPS, GOPHER, GOPHERS, HTTP, HTTPS, IMAP, IMAPS, LDAP, LDAPS,
MQTT, POP3, POP3S, RTMP, RTMPS, RTSP, SCP, SFTP, SMB, SMBS, SMTP, SMTPS,
TELNET, TFTP, WS and WSS.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_curl
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
This package provides JIT support for pg_curl
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
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}.index*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif
%changelog
* Tue Oct 7 2025 Devrim Gündüz <devrim@gunduz.org> - 2.4.4-3PGDG
- Add SLES 16 support

* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 2.4.4-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Tue Jun 17 2025 Devrim Gunduz <devrim@gunduz.org> - 2.4.4-1PGDG
- Update to 2.4.4

* Tue Apr 1 2025 Devrim Gunduz <devrim@gunduz.org> - 2.4.3-2PGDG
- Fix llvmjit subpackage description and summary

* Wed Mar 26 2025 Devrim Gunduz <devrim@gunduz.org> - 2.4.3-1PGDG
- Initial packaging for the PostgreSQL RPM repository

