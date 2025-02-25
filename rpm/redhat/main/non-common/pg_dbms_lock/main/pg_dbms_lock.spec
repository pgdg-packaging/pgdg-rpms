%global sname	pg_dbms_lock

Summary:	PostgreSQL extension to manage advisory locks in a way compatible to Oracle DBMS_LOCK package.
Name:		%{sname}_%{pgmajorversion}
Version:	1.0
Release:	2PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/hexacluster/%{sname}/
Source0:	https://github.com/HexaCluster/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel make
Requires:	postgresql%{pgmajorversion}-server

BuildArch:	noarch

%description
This extension uses PostgreSQL advisory locks to emulate the same behavior
following the lock mode (exclusive or shared), the timeout and the on commit
release settings.

%prep
%setup -q -n %{sname}-%{version}

%build

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} INSTALL_PREFIX=%{buildroot} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Tue Feb 25 2025 Devrim Gündüz <devrim@gunduz.org> - 1.0-2PGDG
- Add missing BRs and dependency.

* Mon Dec 4 2023 Devrim Gündüz <devrim@gunduz.org> - 1.0-1PGDG
- Initial RPM packaging for the PostgreSQL RPM Repository.
