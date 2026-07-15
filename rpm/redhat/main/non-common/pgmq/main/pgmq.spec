%global sname pgmq

Summary:	A lightweight message queue on PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.12.0
Release:	1PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/%{sname}/%{sname}/
Source0:	https://github.com/%{sname}/%{sname}/archive/refs/tags/v%{version}.tar.gz
Requires:	postgresql%{pgmajorversion}-server
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildArch:	noarch

%description
A lightweight message queue. Like AWS SQS and RSMQ but on Postgres.

%prep
%setup -q -n %{sname}-%{version}

%build
pushd pgmq-extension
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot}
popd

%install
pushd pgmq-extension
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
popd

%files
%doc docs/ README.md
%license LICENSE
%{pginstdir}/share/extension/pgmq.control
%{pginstdir}/share/extension/pgmq--*.sql

%changelog
* Wed Jul 15 2026 Devrim Gündüz <devrim@gunduz.org> - 1.12.0-1PGDG
- Update to 1.12.0 per changes described at:
  https://github.com/pgmq/pgmq/releases/tag/v1.12.0

* Mon Apr 20 2026 Devrim Gündüz <devrim@gunduz.org> - 1.11.1-1PGDG
- Update to 1.11.1 per changes described at:
  https://github.com/pgmq/pgmq/releases/tag/v1.11.1

* Thu Feb 19 2026 Devrim Gündüz <devrim@gunduz.org> - 1.11.0-1PGDG
- Update to 1.11.0 per changes described at:
  https://github.com/pgmq/pgmq/releases/tag/v1.11.0

* Tue Feb 17 2026 Devrim Gündüz <devrim@gunduz.org> - 1.10.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository.
