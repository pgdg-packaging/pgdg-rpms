%global sname	pgpdf

%{!?llvm:%global llvm 1}

Summary:	pdf type for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	0.1.0
Release:	2PGDG%{?dist}
License:	GPLv2
URL:		https://github.com/Florents-Tselai/%{sname}/
Source0:	https://github.com/Florents-Tselai/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel
%if 0%{?suse_version} >= 1500
BuildRequires:	libpoppler-glib-devel
Requires:	libpoppler135 libpoppler-glib8
%else
BuildRequires:	poppler-glib-devel
Requires:	poppler
%endif
Requires:	postgresql%{pgmajorversion}-server

%description
This extension for PostgreSQL provides a pdf data type and assorted functions.

You can create a pdf type, by casting either a text filepath or bytea column.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgpdf
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 17.0 clang-devel >= 17.0
Requires:	llvm >= 17.0
%endif

%description llvmjit
This packages provides JIT support for pgpdf
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} INSTALL_PREFIX=%{buildroot} DESTDIR=%{buildroot} install

%files
%defattr(-,root,root,-)
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 0.1.0-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Thu Feb 20 2025 Devrim Gündüz <devrim@gunduz.org> - 0.1.0-1PGDG
- Initial RPM packaging for the PostgreSQL RPM Repository.
