%global sname pgextwlist

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	1.20
Release:	2PGDG%{?dist}
Summary:	PostgreSQL Extension Whitelist
License:	PostgreSQL
URL:		https://github.com/dimitri/%{sname}
Source0:	https://github.com/dimitri/%{sname}/archive/refs/tags/v%{version}.tar.gz
Source1:	LICENSE.txt

BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
This extension implements extension whitelisting, and will actively prevent
users from installing extensions not in the provided list. Also, this extension
implements a form of sudo facility in that the whitelisted extensions will get
installed as if superuser. Privileges are dropped before handing the control
back to the user.

The operations CREATE EXTENSION, DROP EXTENSION, ALTER EXTENSION ... UPDATE,
and COMMENT ON EXTENSION are run by superuser. The ALTER EXTENSION ...
ADD|DROP command is intentionally not supported so as not to allow users to
modify an already installed extension. That means that it's not currently
possible to CREATE EXTENSION ... FROM 'unpackaged';.

Note that the extension script is running as if run by a stored procedure owned
by your bootstrap superuser and with SECURITY DEFINER, meaning that the
extension and all its objects are owned by this superuser.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pgextwlist
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} == 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?suse_version} == 1600
BuildRequires:	llvm19-devel clang19-devel
Requires:	llvm19
%endif
%if 0%{?amzn}
BuildRequires:	llvm-devel >= 15.0 clang-devel >= 15.0
Requires:	llvm >= 15.0
%endif
%if ( 0%{?fedora} || 0%{?rhel} >= 8 ) && !0%{?amzn}
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for pgextwlist
%endif

%prep
%setup -q -n %{sname}-%{version}
%{__cp} %{SOURCE1} .
%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__mv} -f %{buildroot}%{pginstdir}/doc/contrib/README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE.txt
%{pginstdir}/lib/%{sname}.so
%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}*.bc
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Fri Aug 7 2026 Devrim Gunduz <devrim@gunduz.org> - 1.20-2PGDG
- Add Amazon Linux 2023 support.

* Thu Jul 9 2026 Devrim Gündüz <devrim@gunduz.org> - 1.20-1PGDG
- Update to 1.20 per changes described at:
  https://github.com/dimitri/pgextwlist/releases/tag/v1.20

* Mon Apr 6 2026 Devrim Gündüz <devrim@gunduz.org> - 1.19-1PGDG
- Initial packaging for PostgreSQL YUM repository.

