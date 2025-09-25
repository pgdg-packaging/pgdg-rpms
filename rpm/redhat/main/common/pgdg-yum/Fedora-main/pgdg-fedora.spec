Name:		pgdg-fedora-repo
Version:	42.0
Release:	42PGDG
Summary:	PostgreSQL PGDG RPMs - Yum Repository Configuration for Fedora
License:	PostgreSQL
URL:		https://yum.postgresql.org
Source0:	https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-Fedora
Source2:	pgdg-fedora-all.repo
BuildArch:	noarch
Requires:	/etc/fedora-release

%description
This package contains yum configuration for Fedora, and also the GPG
key for PGDG RPMs.

%prep
%setup -q -c -T

%build

%install
%{__rm} -rf %{buildroot}

%{__install} -Dpm 644 %{SOURCE0} \
	%{buildroot}%{_sysconfdir}/pki/rpm-gpg/PGDG-RPM-GPG-KEY-Fedora

%{__install} -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
%{__install} -pm 644 %{SOURCE2} \
	%{buildroot}%{_sysconfdir}/yum.repos.d/

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/*
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Thu Sep 25 2025 Devrim Gündüz <devrim@gunduz.org> - 42.0-42PGDG
- Add v18 repos

* Thu Aug 28 2025 Devrim Gündüz <devrim@gunduz.org> - 42.0-41PGDG
- Enable gpgcheck for v18 repositories.

* Mon Jun 30 2025 Devrim Gündüz <devrim@gunduz.org> - 42.0-40PGDG
- Introduce PostgreSQL 19 testing repo

* Thu Apr 17 2025 Devrim Gündüz <devrim@gunduz.org> - 42.0-39PGDG
- Set the priority of our repo to highest. Upstream started obsoleting
  our packages, so this is the simplest way to overcome that problem
  for now.

* Wed Apr 2 2025 Devrim Gündüz <devrim@gunduz.org> - 42.0-38PGDG
- Add missing pgdg18-updates-testing-debuginfo repo.

* Tue Mar 25 2025 Devrim Gündüz <devrim@gunduz.org> - 42.0-37PGDG
- All SRPM repos must end with -source so that dnf picks that up.

* Thu Mar 13 2025 Devrim Gündüz <devrim@gunduz.org> - 42.0-36PGDG
- Use new URL for SRPMs

* Mon Feb 24 2025 Devrim Gündüz <devrim@gunduz.org> - 42.0-35PGDG
- Remove v12 repos

* Mon Sep 23 2024 Devrim Gündüz <devrim@gunduz.org> - 42.0-34PGDG
- Add v17 repos

* Tue Aug 6 2024 Devrim Gündüz <devrim@gunduz.org> - 42.0-33PGDG
- Introduce PostgreSQL 18 testing repo

* Wed Apr 10 2024 Devrim Gündüz <devrim@gunduz.org> - 42.0-32PGDG
- Introduce debuginfo repo for the common RPMs

* Mon Jan 8 2024 Devrim Gündüz <devrim@gunduz.org> - 42.0-31PGDG
- Use new URL for debuginfo RPMs

* Mon Dec 25 2023 Devrim Gündüz <devrim@gunduz.org> - 42.0-30PGDG
- Update GPG keys

* Mon Nov 20 2023 Devrim Gündüz <devrim@gunduz.org> - 42.0-29PGDG
- Remove v11 repos

* Tue Sep 12 2023 Devrim Gündüz <devrim@gunduz.org> - 42.0-28PGDG
- Add v16 repos

* Mon Aug 14 2023 Devrim Gündüz <devrim@gunduz.org> - 42.0-27PGDG
- Introduce PostgreSQL 17 testing repo
- Add PGDG branding
- Add missing v16 repos

* Wed Nov 23 2022 Devrim Gündüz <devrim@gunduz.org> - 42.0-26
* Remove v10 repos.

* Sat Oct 15 2022 Devrim Gündüz <devrim@gunduz.org> - 42.0-25
- Add missing srpm and debuginfo repositories, per report from
  Justin Pryzby.

* Thu Sep 29 2022 Devrim Gündüz <devrim@gunduz.org> - 42.0-24
- Add v15 stable repo.

* Fri Aug 19 2022 Devrim Gündüz <devrim@gunduz.org> - 42.0-23
- Add pgdg15-source-updates-testing and pgdg15-updates-testing-debuginfo
  repos. Per report from Justin Pryzby .

* Wed Aug 10 2022 Devrim Gündüz <devrim@gunduz.org> - 42.0-22
- Introduce PostgreSQL 16 testing repo

* Fri Feb 18 2022 Devrim Gündüz <devrim@gunduz.org> - 42.0-21
- Remove 9.6 repo.

* Fri Oct 1 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-20
- Add v14 debuginfo repo, per report from Laurenz Albe.

* Mon Sep 20 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-18
- Add v14 stable repo.

* Tue Jun 29 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-17
- Add v15 testing repo

* Mon May 17 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-16
- Remove deprecated "failovermethod" parameter.

* Fri Apr 30 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-15
- Sign repository metadata to fix CVE-2021-20271, per
  https://access.redhat.com/security/cve/cve-2021-20271

* Thu Feb 25 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-14
- Remove 9.5 repo

* Thu Sep 24 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-13
- Add v14 testing repo
- Remove 9.4 repo

* Sun Sep 13 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-12
- Add v13 stable repo.

* Tue Apr 28 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-11
- Disable 9.4 repo

* Sat Apr 11 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-10
- Add missing pgdg-source-common repo

* Mon Apr 6 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-9
- Disable testing-common repo by default.

* Fri Apr 3 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-8
- Introduce "common" repository.

* Wed Mar 11 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-7
- Fix some debuginfo repos.

* Sat Dec 28 2019 Devrim Gündüz <devrim@gunduz.org> - 42.0-6
- Do not replace repo config file after each update. Per #4905

* Wed Sep 25 2019 Devrim Gündüz <devrim@gunduz.org> - 42.0-5
- Enable v12 stable repo, and improve description of repo names.
- Add v13 testing repo, and make repo files more consistent with RHEL ones.

* Wed Apr 17 2019 Devrim Gündüz <devrim@gunduz.org> - 42.0-4
- Remove major version from GPG file name in the repo file as well.

* Tue Apr 16 2019 Devrim Gündüz <devrim@gunduz.org> - 42.0-3
- Remove major version from GPG file name, per various reports.

* Thu Apr 11 2019 Devrim Gündüz <devrim@gunduz.org> - 42.0-2
- Disable v12 testing repo, it is still in development phase. Per Dave Page.

* Wed Apr 10 2019 Devrim Gündüz <devrim@gunduz.org> - 42.0-1
- The new repo package, that contains all supported distros.

