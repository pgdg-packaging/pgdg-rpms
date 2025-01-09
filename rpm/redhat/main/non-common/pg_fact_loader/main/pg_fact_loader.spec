%global sname pg_fact_loader

Summary:	Build fact tables with Postgres using replicated tables and a queue
Name:		%{sname}_%{pgmajorversion}
Version:	2.0.1
Release:	3PGDG%{?dist}
License:	MIT
Source0:	https://github.com/enova/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/enova/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-contrib

BuildArch:	noarch

%description
pg_fact_loader is a PostgreSQL extension to build fact tables with
Postgres using replicated tables and a queue.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%defattr(644,root,root,755)
%{pginstdir}/share/extension/%{sname}*sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Thu Jan 9 2025 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-3PGDG
- Add -contrib dependency for the required dblink extension.

* Tue Oct 24 2023 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-2PGDG
- Rebuilt

* Wed Oct 18 2023 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-1PGDG
- Initial RPM packaging for the PostgreSQL RPM Repository
