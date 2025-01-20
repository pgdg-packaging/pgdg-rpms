%global sname	pg_extra_time

Summary:	Extra date time functions and operators for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	2.0.0
Release:	1PGDG%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		https://github.com/bigsmoke/%{sname}
Source0:	https://github.com/bigsmoke/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildArch:	noarch

%description
The pg_extra_time PostgreSQL extension contains some date time
functions and operators.

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
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENCE.txt
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}*.control

%changelog
* Wed Jun 26 2024 - Devrim Gündüz <devrim@gunduz.org> - 2.0.0-1PGDG
- Update to 2.0.0 per changes described at:
  https://github.com/bigsmoke/pg_extra_time/releases/tag/v2.0.0
  https://github.com/bigsmoke/pg_extra_time/blob/v2.0.0/CHANGELOG.md

* Wed Jun 26 2024 - Devrim Gündüz <devrim@gunduz.org> - 1.1.3-1PGDG
- Update to 1.1.3 per changes described at:
  https://github.com/bigsmoke/pg_extra_time/releases/tag/v1.1.3

* Thu Dec 21 2023 - Devrim Gündüz <devrim@gunduz.org> - 1.1.2-1PGDG
- Initial RPM packaging for the PostgreSQL RPM repository.
