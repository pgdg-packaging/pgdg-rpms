%global sname	login_hook

%{!?llvm:%global llvm 1}

Summary:	Postgres database extension to execute some code on user login, comparable to Oracle's after logon trigger.
Name:		%{sname}_%{pgmajorversion}
Version:	1.7
Release:	1PGDG%{?dist}
License:	GPLv3
URL:		https://github.com/splendiddata/%{sname}
Source0:	https://github.com/splendiddata/%{sname}/archive/refs/tags/Version_%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
Postgres database extension to execute some code on user login,
comparable to Oracle's after logon trigger.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for login_hook
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
This packages provides JIT support for login_hook
%endif

%prep
%setup -q -n %{sname}-Version_%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
# No need to ship these files:
%{__rm} %{buildroot}%{pginstdir}/doc/extension/%{sname}.css
%{__rm} %{buildroot}%{pginstdir}/doc/extension/%{sname}.html

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
* Mon May 5 2025 Devrim Gündüz <devrim@gunduz.org> - 1.7-1PGDG
- Update to 1.7 per changes described at:
  https://github.com/splendiddata/login_hook/releases/tag/Version_1.7

* Thu Jan 9 2025 Devrim Gündüz <devrim@gunduz.org> - 1.6-2PGDG
- Update LLVM dependencies

* Fri Aug 16 2024 Devrim Gündüz <devrim@gunduz.org> - 1.6-1PGDG
- Update to 1.6 per changes described at:
  https://github.com/splendiddata/login_hook/releases/tag/Version_1.6

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 1.5-2PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Mon Oct 30 2023 Devrim Gunduz <devrim@gunduz.org> - 1.5-1PGDG
- Initial packaging for PostgreSQL RPM Repository
