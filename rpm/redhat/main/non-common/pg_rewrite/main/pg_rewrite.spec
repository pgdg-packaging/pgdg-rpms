%global sname pg_rewrite

%global pgrwmajver 2
%global pgrwmidver 0
%global pgrwminver 0

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL tool to rewrite a table
Name:		%{sname}_%{pgmajorversion}
Version:	%{pgrwmajver}.%{pgrwmidver}.%{pgrwminver}
Release:	2PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/%{sname}/%{sname}
Source0:	https://github.com/cybertec-postgresql/pg_rewrite/archive/refs/tags/REL%{pgrwmajver}_%{pgrwmidver}_%{pgrwminver}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
pg_rewrite is a tool to rewrite table (i.e. to copy its data to a new file).
It allows both read and write access to the table during the rewriting.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_rewrite
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for pg_rewrite
%endif

%prep
%setup -q -n %{sname}-REL%{pgrwmajver}_%{pgrwmidver}_%{pgrwminver}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/%{sname}.md
%{pginstdir}/lib/%{sname}*.*
%{pginstdir}/share/extension/%{sname}*.*

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}.index.bc
    %{pginstdir}/lib/bitcode/%{sname}/*bc
%endif

%changelog
* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 2.0.0-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Tue Sep 2 2025 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-1PGDG
- Update to 2.0.0 per changes described at:
  https://github.com/cybertec-postgresql/pg_rewrite/releases/tag/REL2_0_0

* Wed Jul 30 2025 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1PGDG
- Initial packaging for the PostgreSQL RPM Repository
