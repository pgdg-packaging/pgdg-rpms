%global sname pgpcre

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	0.20190509
Release:	4PGDG%{?dist}
Summary:	PostgreSQL extension that exposes PCRE functionality as functions and operators
License:	GPLv2
URL:		https://github.com/petere/%{sname}
Source0:	https://github.com/petere/%{sname}/archive/refs/tags/%{version}.tar.gz
Patch0:		%{sname}-pcre2.patch

BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}

%if 0%{?rhel} && 0%{?rhel} == 10
BuildRequires:	pcre2-devel
Requires:	pcre2
%endif
%if 0%{?fedora} && 0%{?fedora} >= 43
BuildRequires:	pcre2-devel
Requires:	pcre2
%endif
%if 0%{?fedora} && 0%{?fedora} <= 42
BuildRequires:	pcre-devel
Requires:	pcre
%endif
%if 0%{?rhel} && 0%{?rhel} <= 9
BuildRequires:	pcre-devel
Requires:	pcre
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	pcre2-devel
Requires:	libpcre2-32-0
%endif

%description
This is a module for PostgreSQL that exposes Perl-compatible regular
expressions (PCRE) functionality as functions and operators. It is
based on the popular PCRE library.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgpcre
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
This package provides JIT support for pgpcre
%endif

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p1

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} DESTDIR=%{buildroot} install
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__mv} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Thu Sep 25 2025 Devrim Gündüz <devrim@gunduz.org> 0.20190509-4PGDG
- Fix RHEL 10, Fedora 43 and SLES 15 dependencies

* Fri Sep 5 2025 Devrim Gündüz <devrim@gunduz.org> 0.20190509-3PGDG
- Update LLVM dependencies

* Sat Jul 5 2025 Devrim Gündüz <devrim@gunduz.org> 0.20190509-2PGDG
- Add a patch to support pcre2. Per https://github.com/petere/pgpcre/pull/9

* Mon Apr 14 2025 Devrim Gündüz <devrim@gunduz.org> 0.20190509-1PGDG
- Initial packaging for the PostgreSQL RPM repository
