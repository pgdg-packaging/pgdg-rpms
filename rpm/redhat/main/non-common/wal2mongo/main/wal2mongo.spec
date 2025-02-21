%global sname wal2mongo

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL logical decoding output plugin for MongoDB
Name:		%{sname}_%{pgmajorversion}
Version:	1.0.7
Release:	3PGDG%{?dist}
License:	BSD
Source0:	https://github.com/HighgoSoftware/%{sname}/archive/v%{version}.tar.gz
URL:		https://github.com/HighgoSoftware/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 1.0.6-2

%description
wal2mongo is a PostgreSQL logical decoding output plugin designed to make the
logical replication easier from PostgreSQL to MongoDB by formating the output
to a JSON-like format accepted by mongo.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for wal2mongo
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
This package provides JIT support for wal2mongo
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %make_install DESTDIR=%{buildroot}
%{__install} -d %{buildroot}/%{pginstdir}/doc/extension/
%{__mv} README.md %{buildroot}/%{pginstdir}/doc/extension/README-%{sname}.md

%postun -p /sbin/ldconfig
%post -p /sbin/ldconfig

%files
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Fri Feb 21 2025 Devrim Gündüz <devrim@gunduz.org> - 1.0.7-3PGDG
- Update LLVM dependencies
- Remove reduntant BR

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.0.7-2PGDG
- Update LLVM dependencies

* Wed Jun 12 2024 Devrim Gunduz <devrim@gunduz.org> - 1.0.7-1PGDG
- Update to 1.0.7
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 1.0.6-4.1
- Rebuild against LLVM 15 on SLES 15

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.0.6-4
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> - 1.0.6-3
- Remove pgxs patch, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.0.6-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Tue Jun 2 2020 Devrim Gündüz <devrim@gunduz.org> 1.0.6-1
- Initial RPM packaging for yum.postgresql.org
