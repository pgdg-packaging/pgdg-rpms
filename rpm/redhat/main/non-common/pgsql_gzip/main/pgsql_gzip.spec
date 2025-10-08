%global pname pgsql_gzip
%global sname pgsql-gzip

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL gzip/gunzip functions
Name:		%{pname}_%{pgmajorversion}
Version:	1.0.0
Release:	8PGDG%{?dist}
URL:		https://github.com/pramsey/%{sname}
Source0:	https://github.com/pramsey/%{sname}/archive/refs/tags/v%{version}.tar.gz
License:	MIT
BuildRequires:	postgresql%{pgmajorversion}-devel

%if 0%{?fedora} == 40
BuildRequires:	zlib-ng-compat-devel
Requires:	zlib-ng-compat
%endif
%if 0%{?rhel} >= 8
BuildRequires:	zlib-devel
Requires:	zlib
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	zlib-devel
Requires:	libz1
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
Sometimes you just need to compress your bytea object before you return it to
the client.

Sometimes you receive a compressed bytea from the client, and you have to
uncompress it before you can work with it.

This extension is for that.

This extension is not for storage compression. PostgreSQL already does tuple
compression on the fly if your tuple gets large enough, manually
pre-compressing your data using this function won't make things smaller.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgsql_gzip
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
This package provides JIT support for pgsql_gzip
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
%{pginstdir}/lib/gzip.so
%{pginstdir}/share/extension/gzip*.sql
%{pginstdir}/share/extension/gzip*.control

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/gzip.index*.bc
    %{pginstdir}/lib/bitcode/gzip/*.bc
%endif

%changelog
* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.0.0-7PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Wed Mar 12 2025 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-6PGDG
- Remove duplicate BR

* Tue Feb 25 2025 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-5PGDG
- Add missing BR

* Mon Jan 13 2025 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-4PGDG
- Update LLVM dependencies

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-3PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Sun May 12 2024 Devrim Gunduz <devrim@gunduz.org> - 1.0.0-2PGDG
- Fix dependency on RHEL 8

* Fri May 10 2024 Devrim Gunduz <devrim@gunduz.org> - 1.0.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository

