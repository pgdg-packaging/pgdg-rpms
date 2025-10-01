%global sname pg_snakeoil

%{!?llvm:%global llvm 1}

Summary:	The PostgreSQL Antivirus
Name:		%{sname}_%{pgmajorversion}
Version:	1.4
Release:	2PGDG%{?dist}
License:	BSD
Source0:	https://github.com/df7cb/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/df7cb//%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel clamav-devel
Requires:	postgresql%{pgmajorversion}-server clamav-lib clamav-freshclam

%description
pg_snakeoil provides ClamAV scanning of all data in PostgreSQL in a way
that does not interfere with the proper functioning of PostgreSQL and
does not cause collateral damage or unnecessary downtimes.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_snakeoil
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
This packages provides JIT support for pg_snakeoil
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
	%{pginstdir}/lib/bitcode/%{sname}*bc
	%{pginstdir}/lib/bitcode/%{sname}/%{sname}.bc
%endif

%changelog
* Wed Oct 01 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com> - 1.4-2PGDG
- Bump release number (missed in previous commit)

* Tue Sep 30 2025 Yogesh Sharma <yogesh.sharma@catprosystems.com>
- Change => to >= in Requires and BuildRequires

* Mon Oct 7 2024 - Devrim Gündüz <devrim@gunduz.org> 1.4-1PGDG
- Initial RPM packaging for PostgreSQL RPM Repository
