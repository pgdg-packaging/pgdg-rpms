%global sname	pg_readme

Summary:	PostgreSQL extension to generate a README.md document for a database extension or schema
Name:		%{sname}_%{pgmajorversion}
Version:	0.7.1
Release:	1PGDG%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		https://github.com/bigsmoke/%{sname}
Source0:	https://github.com/bigsmoke/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildArch:	noarch

%description
The pg_readme PostgreSQL extension provides functions to generate a README.md
document for a database extension or schema, based on COMMENT objects found
in the pg_description system catalog.

%prep
%setup -q -n %{sname}-%{version}

%build
%{__make} PG_CONFIG=%{pginstdir}/bin/pg_config USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} PG_CONFIG=%{pginstdir}/bin/pg_config USE_PGXS=1 %{?_smp_mflags} DESTDIR=%{buildroot} install
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__mv} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENCE.txt
%defattr(-,root,root,-)
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}*.control

%changelog
* Mon Aug 31 2026 - Devrim Gündüz <devrim@gunduz.org> - 0.7.1-1PGDG
- Update to 0.7.1 per changes described at:
  https://github.com/bigsmoke/pg_readme/releases/tag/v0.7.1

* Tue Sep 3 2024 - Devrim Gündüz <devrim@gunduz.org> - 0.7.0-1PGDG
- Initial RPM packaging for the PostgreSQL RPM repository.
