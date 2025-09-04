%global sname pg_checksums

Summary:	Activate/deactivate/verify checksums in offline Postgres clusters
Name:		%{sname}_%{pgmajorversion}
Version:	1.3
Release:	1PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/credativ/%{sname}
Source0:	https://github.com/credativ/%{sname}/archive/%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 1.0-2

%description
pg_checksums is based on the pg_verify_checksums and pg_checksums programs
available in PostgreSQL version 11 and from 12, respectively. It cat verify,
activate or deactivate checksums. Activating requires all database blocks to
be read and all page headers to be updated, so can take a long time on a
large database.

The database cluster needs to be shutdown cleanly in the case of checksum
activation or deactivation, while checksum verification can be performed
online, contrary to PostgreSQL's pg_checksums.

Other changes include the possibility to toggle progress reporting via the
SIGUSR1 signal, more fine-grained progress reporting and I/O rate limiting.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install
# Install documentation with a better name:
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license COPYRIGHT
%attr (755,root,root) %{pginstdir}/bin/%{sname}_ext

%changelog
* Thu Sep 4 2025 Devrim Gündüz <devrim@gunduz.org> 1.3-1PGDGG
- Update to 1.3 per changes described at:
  https://github.com/credativ/pg_checksums/releases/tag/1.3

* Fri Sep 20 2024 Devrim Gündüz <devrim@gunduz.org> 1.2-1PGDGG
- Update to 1.2 per changes described at:
  https://github.com/credativ/pg_checksums/releases/tag/1.2

* Fri Sep 8 2023 Devrim Gündüz <devrim@gunduz.org> 1.1-3PGDGG
- Mark binary file as executable
- Add PGDG branding

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.1-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Fri Mar 4 2022 Devrim Gündüz <devrim@gunduz.org> 1.1-1
- Update to 1.1

* Mon Jun 28 2021 Devrim Gündüz <devrim@gunduz.org> 1.0-3
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 1.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Tue Oct 29 2019 - Devrim Gündüz <devrim@gunduz.org> 1.0-1
- Initial packaging for PostgreSQL RPM Repository
