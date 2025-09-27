Name:		pgdg-suse-repo
Version:	42.0
Release:	47PGDG
Summary:	PostgreSQL PGDG RPMs - Zypper Repository Configuration for SuSE Enterprise Linux
License:	PostgreSQL
URL:		https://zypp.postgresql.org
Source0:	pgdg-suse-all-sles15.repo
Source1:	PGDG-RPM-GPG-KEY-SLES15
BuildArch:	noarch
Requires:	sles-release

%description
This package contains zypper configuration for SuSE Enterprise Linux.

%prep
%setup -q -c -T

%build

%install
%{__rm} -rf %{buildroot}

%{__install} -dm 755 %{buildroot}%{_sysconfdir}/zypp/repos.d

%{__install} -pm 644 %{SOURCE0} \
	%{buildroot}%{_sysconfdir}/zypp/repos.d/pgdg-sles-all.repo

%{__mkdir} -p %{buildroot}%{_sysconfdir}/pki/

%{__install} -Dpm 644 %{SOURCE1} \
		%{buildroot}%{_sysconfdir}/pki/

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/zypp/repos.d/*
%{_sysconfdir}/pki/PGDG-RPM-GPG-KEY-SLES15

%changelog
* Sat Sep 27 2025 Devrim Gündüz <devrim@gunduz.org> - 42.0-47PGDG
- Add missing source and debuginfo repos

* Thu Sep 25 2025 Devrim Gündüz <devrim@gunduz.org> - 42.0-46PGDG
- Add v18 repos

* Thu Aug 28 2025 Devrim Gündüz <devrim@gunduz.org> - 42.0-45PGDG
- Add PostgreSQL 19 repos

* Sun Jun 22 2025 Devrim Gündüz <devrim@gunduz.org> - 42.0-44PGDG
- Remove v12 repos

* Mon Sep 23 2024 Devrim Gündüz <devrim@gunduz.org> - 42.0-43PGDG
- Add v17 repos

* Thu Aug 8 2024 Devrim Gündüz <devrim@gunduz.org> - 42.0-42PGDG
- Introduce PostgreSQL 18 testing repo

* Sun Jun 2 2024 Devrim Gündüz <devrim@gunduz.org> - 42.0-41PGDG
- Fix extras repo URL per https://redmine.postgresql.org/issues/7993

* Wed Mar 20 2024 Devrim Gündüz <devrim@gunduz.org> - 42.0-40PGDG
- Install GPG signing key along with the repo RPM. Fixes multiple
  reports in mailing lists, redmine, etc.

* Wed Feb 7 2024 Devrim Gündüz <devrim@gunduz.org> - 42.0-39PGDG
- The new repo package, that contains all supported distros.
