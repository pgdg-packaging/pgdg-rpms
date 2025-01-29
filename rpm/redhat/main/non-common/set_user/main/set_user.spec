%global sname	set_user

%global setusermajver 4
%global setusermidver 1
%global setuserminver 0

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL extension allowing privilege escalation with enhanced logging and control
Name:		%{sname}_%{pgmajorversion}
Version:	%{setusermajver}.%{setusermidver}.%{setuserminver}
Release:	2PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/pgaudit/%{sname}
Source0:	https://github.com/pgaudit/%{sname}/archive/refs/tags/REL%{setusermajver}_%{setusermidver}_%{setuserminver}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel postgresql%{pgmajorversion}
Requires:	postgresql%{pgmajorversion}-server

%description
This PostgreSQL extension allows switching users and optional privilege
escalation with enhanced logging and control. It provides an additional layer
of logging and control when unprivileged users must escalate themselves to
superuser or object owner roles in order to perform needed maintenance tasks.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for set_user
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
This package provides JIT support for set_user
%endif

%prep
%setup -q -n %{sname}-REL%{setusermajver}_%{setusermidver}_%{setuserminver}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

# Remove header file, we don't need to ship it:
%{__rm} -f %{buildroot}%{pginstdir}/include/%{sname}.h

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/src/%{sname}*.bc
    %{pginstdir}/lib/bitcode/src/%{sname}/src/%{sname}.bc
%endif

%changelog
* Wed Jan 29 2025 Devrim Gündüz <devrim@gunduz.org> - 4.1.0-2PGDG
- Update LLVM dependencies

* Sun Sep 8 2024 Devrim Gündüz <devrim@gunduz.org> - 4.1.0-1PGDG
  Update to 4.1.0 per changes described at
  https://github.com/pgaudit/set_user/releases/tag/REL4_1_0

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 4.0.1-4PGDG
- Update LLVM dependencies
- Remove RHEL 7 support

* Mon Feb 26 2024 Devrim Gunduz <devrim@gunduz.org> - 4.0.1-3PGDG
- Add PGDG branding

* Sat Jun 03 2023 Devrim Gunduz <devrim@gunduz.org> - 4.0.1-2
- Rebuild against LLVM 15 on SLES 15

* Wed Feb 22 2023 Devrim Gündüz <devrim@gunduz.org> - 4.0.1-1
- Update to 4.0.1

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 4.0.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Sun Nov 13 2022 Devrim Gündüz <devrim@gunduz.org> - 4.0.0-1
- Update to 4.0.0

* Tue Oct 19 2021 Devrim Gündüz <devrim@gunduz.org> - 3.0.0-1
- Update to 3.0.0

* Tue Aug 31 2021 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
