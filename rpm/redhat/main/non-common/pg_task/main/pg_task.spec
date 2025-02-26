%global sname	pg_task

%{!?llvm:%global llvm 1}

Summary:	PostgreSQL and Greenplum job scheduler
Name:		%{sname}_%{pgmajorversion}
Version:	2.1.7
Release:	3PGDG%{?dist}
License:	MIT
URL:		https://github.com/RekGRpth/%{sname}
Source0:	https://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
BuildRequires:	postgresql%{pgmajorversion}-devel wget
Requires:	postgresql%{pgmajorversion}-server

%description
pg_task allows to execute any sql command at any specific time at background
asynchronously.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for pg_task
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
This packages provides JIT support for pg_task
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
%{__make} PG_CONFIG=%{pginstdir}/bin/pg_config PATH=%{pginstdir}/bin/:$PATH USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} PG_CONFIG=%{pginstdir}/bin/pg_config PATH=%{pginstdir}/bin/:$PATH USE_PGXS=1 %{?_smp_mflags} DESTDIR=%{buildroot} install
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__mv} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%defattr(-,root,root,-)
%{pginstdir}/lib/%{sname}.so

%if %llvm
%files llvmjit
    %{pginstdir}/lib/bitcode/%{sname}/*.bc
    %{pginstdir}/lib/bitcode/%{sname}*.bc
%endif

%changelog
* Wed Feb 26 2025 - Devrim Gündüz <devrim@gunduz.org> - 2.1.7-3PGDG
- Add missing BR

* Sat Jan 11 2025 - Devrim Gündüz <devrim@gunduz.org> - 2.1.7-2PGDG
- Update LLVM dependencies

* Tue Sep 24 2024 - Devrim Gündüz <devrim@gunduz.org> - 2.1.7-1PGDG
- Update to 2.1.7

* Tue Sep 3 2024 - Devrim Gündüz <devrim@gunduz.org> - 2.1.5-1PGDG
- Initial RPM packaging for the PostgreSQL RPM repository.
