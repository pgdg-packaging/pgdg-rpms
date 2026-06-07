%global sname toastinfo

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL extension exposes the internal storage structure of variable-length datatypes
Name:		%{sname}_%{pgmajorversion}
Version:	1.7
Release:	1PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/df7cb/%{sname}
Source0:	https://github.com/df7cb/%{sname}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
This PostgreSQL extension exposes the internal storage structure of
variable-length datatypes, called varlena.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for toastinfo
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
This packages provides JIT support for toastinfo
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README
%{__install} -d %{buildroot}%{pginstdir}/doc/extension/
%{__install} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
 %{pginstdir}/lib/bitcode/%{sname}*.bc
 %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Sun Jun 7 2026 - Devrim Gündüz <devrim@gunduz.org> - 1.7-1PGDG
- Update to 1.7 per changes described at:
  https://github.com/df7cb/toastinfo/releases/tag/v1.7

* Sun Jun 7 2026 - Devrim Gündüz <devrim@gunduz.org> - 1.6-1PGDG
- Initial RPM packaging for PostgreSQL RPM Repository
