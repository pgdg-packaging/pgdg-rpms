Name:		pgdg-redhat-repo
Version:	42.0
Release:	57PGDG
Summary:	PostgreSQL PGDG RPMs - Yum Repository Configuration for Red Hat / Rocky / AlmaLinux
License:	PostgreSQL
URL:		https://yum.postgresql.org

# RHEL 8
%if 0%{?rhel} && 0%{?rhel} == 8
%ifarch aarch64
Source0:	https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-AARCH64-RHEL
Source2:	pgdg-redhat-all-rhel8-aarch64.repo
%endif
%ifarch ppc64le
Source0:	https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-RHEL
Source2:	pgdg-redhat-all-rhel8-ppc64le.repo
%endif
%ifarch x86_64
Source0:	https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-RHEL
Source2:	pgdg-redhat-all-rhel8.repo
%endif
%endif

# RHEL 9
%if 0%{?rhel} && 0%{?rhel} == 9
%ifarch aarch64
Source0:	https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-AARCH64-RHEL
Source2:	pgdg-redhat-all-rhel9-aarch64.repo
%endif
%ifarch ppc64le
Source0:	https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-RHEL
Source2:	pgdg-redhat-all-rhel9-ppc64le.repo
%endif
%ifarch x86_64
Source0:	https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-RHEL
Source2:	pgdg-redhat-all-rhel9.repo
%endif
%endif

# RHEL 10
%if 0%{?rhel} && 0%{?rhel} == 10
%ifarch aarch64
Source0:	https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-AARCH64-RHEL
Source2:	pgdg-redhat-all-rhel10-aarch64.repo
%endif
%ifarch ppc64le
Source0:	https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-RHEL
Source2:	pgdg-redhat-all-rhel10-ppc64le.repo
%endif
%ifarch x86_64
Source0:	https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-RHEL
Source2:	pgdg-redhat-all-rhel10.repo
%endif
%endif

BuildArch:	noarch
Requires:	/etc/redhat-release

%description
This package contains yum configuration for Red Hat Enterprise Linux,
Rocky Linux, AlmaLinux and also the GPG key for PGDG RPMs.

%prep
%setup -q -c -T

%build

%install
%{__rm} -rf %{buildroot}

%{__mkdir} -p %{buildroot}%{_sysconfdir}/pki/rpm-gpg

%{__install} -Dpm 644 %{SOURCE0} \
	%{buildroot}%{_sysconfdir}/pki/rpm-gpg/

%{__install} -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d

%{__install} -pm 644 %{SOURCE2} \
	%{buildroot}%{_sysconfdir}/yum.repos.d/pgdg-redhat-all.repo

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/*
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Thu Sep 25 2025 Devrim Gündüz <devrim@gunduz.org> - 42.0-57PGDG
- Add v18 repos

* Thu Aug 28 2025 Devrim Gündüz <devrim@gunduz.org> - 42.0-56PGDG
- Enable gpgcheck for v18 repositories.

* Tue Aug 5 2025 Devrim Gündüz <devrim@gunduz.org> - 42.0-55PGDG
- Fix/update debuginfo URLs in ppc64le repo files.

* Mon Jun 30 2025 Devrim Gündüz <devrim@gunduz.org> - 42.0-54PGDG
- Introduce PostgreSQL 19 testing repo

* Thu May 22 2025 Devrim Gündüz <devrim@gunduz.org> - 42.0-53PGDG
- RHEL 10 is now GA.

* Tue May 6 2025 Devrim Gündüz <devrim@gunduz.org> - 42.0-52PGDG
- Rebuilt.

* Mon May 5 2025 Devrim Gündüz <devrim@gunduz.org> - 42.0-51PGDG
- Add extras SRPM repos

* Tue Mar 25 2025 Devrim Gündüz <devrim@gunduz.org> - 42.0-50PGDG
- All SRPM repos must end with -source so that dnf picks that up.

* Thu Mar 13 2025 Devrim Gündüz <devrim@gunduz.org> - 42.0-49PGDG
- Use new URL for SRPMs

* Mon Feb 24 2025 Devrim Gündüz <devrim@gunduz.org> - 42.0-48PGDG
- Remove v12 repos

* Wed Dec 18 2024 Devrim Gündüz <devrim@gunduz.org> - 42.0-47PGDG
- Add RHEL 10 repo files
- Remove RHEL 7 repos

* Tue Oct 1 2024 Devrim Gündüz <devrim@gunduz.org> - 42.0-46PGDG
- Rebuild on RHEL 9 to properly propagate commit e47a6146 .

* Mon Sep 23 2024 Devrim Gündüz <devrim@gunduz.org> - 42.0-45PGDG
- Add v17 repos

* Tue Aug 6 2024 Devrim Gündüz <devrim@gunduz.org> - 42.0-44PGDG
- Introduce PostgreSQL 18 testing repo

* Wed Apr 10 2024 Devrim Gündüz <devrim@gunduz.org> - 42.0-43PGDG
- Disable pgdg-common-debuginfo by default.

* Tue Apr 9 2024 Devrim Gündüz <devrim@gunduz.org> - 42.0-42PGDG
- Fix GPG key names of the pgdg-common-debuginfo in RHEL 8 and RHEL 9 ,
  per report from Klaus Kindlinger: https://redmine.postgresql.org/issues/7976

* Mon Apr 8 2024 Devrim Gündüz <devrim@gunduz.org> - 42.0-41PGDG
- Enable debuginfo for the common repo on RHEL 8+.

* Tue Mar 5 2024 Devrim Gündüz <devrim@gunduz.org> - 42.0-40PGDG
- Unify repo spec files for RHEL

* Thu Jan 11 2024 Devrim Gündüz <devrim@gunduz.org> - 42.0-39PGDG
- Use new URL for debuginfo RPMs on RHEL 8 and RHEL 9.

* Mon Dec 25 2023 Devrim Gündüz <devrim@gunduz.org> - 42.0-38PGDG
- Update GPG keys

* Mon Nov 20 2023 Devrim Gündüz <devrim@gunduz.org> - 42.0-37PGDG
- Remove v11 repos

* Tue Oct 17 2023 Devrim Gündüz <devrim@gunduz.org> - 42.0-36PGDG
- Add missing pgdg16-debuginfo repository to RHEL 9 repo, per report
  from Justin Pryzby.

* Tue Sep 12 2023 Devrim Gündüz <devrim@gunduz.org> - 42.0-35PGDG
- Add v16 repos
- Remove v16 repos from RHEL 7

* Mon Aug 14 2023 Devrim Gündüz <devrim@gunduz.org> - 42.0-34PGDG
- Introduce PostgreSQL 17 testing repo
- Add PGDG branding

* Thu Mar 16 2023 Devrim Gündüz <devrim@gunduz.org> - 42.0-33
- Introduce new repo: pgdg-rhel7-extras.

* Wed Nov 23 2022 Devrim Gündüz <devrim@gunduz.org> - 42.0-32
- Remove v10 repos, add pgdg16-updates-testing-debuginfo repo.

* Fri Oct 28 2022 Devrim Gündüz <devrim@gunduz.org> - 42.0-31
- Bump up release number to fix ppc64le repo file issue :(

* Sat Oct 15 2022 Devrim Gündüz <devrim@gunduz.org> - 42.0-28
- Add missing srpm and debuginfo repositories, per report from
  Justin Pryzby.

* Thu Sep 29 2022 Devrim Gündüz <devrim@gunduz.org> - 42.0-27
- Add v15 stable repo.

* Fri Aug 19 2022 Devrim Gündüz <devrim@gunduz.org> - 42.0-26
- Add pgdg15-source-updates-testing and pgdg15-updates-testing-debuginfo
  repos. Per report from Justin Pryzby .

* Wed Aug 10 2022 Devrim Gündüz <devrim@gunduz.org> - 42.0-25
- Introduce PostgreSQL 16 testing repo

* Wed Mar 16 2022 Devrim Gündüz <devrim@gunduz.org> - 42.0-24
- Introduce new repos: pgdg-rhel8-extras and pgdg-rhel9-extras
- Remove 9.6 repos.

* Tue Nov 30 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-23
- Change -debuginfo repo names, so that yum/dnf will be able
  to pick up these repos automagically with debuginfo-install
  (RHEL 7), and dnf debuginfo-install (on RHEL 8 and 9).
- Rename Source3

* Wed Nov 3 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-22
- Add RHEL 9 repo.

* Sat Oct 16 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-21
- Add missing v14 debuginfo repos, per Demur Rumed.

* Mon Sep 20 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-20
- Add v14 stable repo.

* Thu Jul 15 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-19
- Remove deprecated "failovermethod" parameter from RHEL 8 repo
  config file.

* Tue Jun 29 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-18
- Add v15 testing repo

* Tue Jun 22 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-17.2
- Remove obsoletes for 9.5 and 9.4.

* Thu May 6 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-17.1
- Sign repository metadata also on RHEL 7.

* Fri Apr 30 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-17
- Sign repository metadata on RHEL 8+ to fix CVE-2021-20271, per
  https://access.redhat.com/security/cve/cve-2021-20271

* Thu Feb 25 2021 Devrim Gündüz <devrim@gunduz.org> - 42.0-16
- Remove 9.5 repo

* Fri Nov 13 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-15
- Add a (hopefully temporary) repo to RHEL 8, which supplies
  latest-ish LLVM and CLANG, so that we can respond breakages
  between RHEL 8.n and CentOS 8.n-1, which breaks our llvmjit
  package.

* Thu Sep 24 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-14
- Add v14 testing repo.
- Remove 9.4 repo

* Sun Sep 13 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-13
- Add v13 stable repo.

* Fri Aug 28 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-12
- Fix v13 debug repo URL, per report from Justin Pryzby.

* Tue Apr 28 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-11
- Disable 9.4 repo

* Sat Apr 11 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-10
- Remove duplicate srpm repo, and sync with Fedora repo file (a bit)

* Fri Apr 3 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-9
- Introduce "common" repository.

* Wed Mar 11 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-8
- Fix typo in repo file

* Wed Mar 11 2020 Devrim Gündüz <devrim@gunduz.org> - 42.0-7
- Add debuginfo repos.

* Sat Dec 28 2019 Devrim Gündüz <devrim@gunduz.org> - 42.0-6
- Do not replace repo config file after each update. Per #4905

* Wed Sep 25 2019 Devrim Gündüz <devrim@gunduz.org> - 42.0-5
- Enable v12 stable repo, and improve description of repo names.
- Drop support for Scientific Linux (project discontinued)
- Add v13 testing repo, and make repo files more consistent with RHEL ones.

* Wed Apr 17 2019 Devrim Gündüz <devrim@gunduz.org> - 42.0-4
- Remove major version from GPG file name in the repo file as well.

* Tue Apr 16 2019 Devrim Gündüz <devrim@gunduz.org> - 42.0-3
- Remove major version from GPG file name, per various reports.

* Thu Apr 11 2019 Devrim Gündüz <devrim@gunduz.org> - 42.0-2
- Disable v12 testing repo, it is still in development phase. Per Dave Page.

* Wed Apr 10 2019 Devrim Gündüz <devrim@gunduz.org> - 42.0
- The new repo package, that contains all supported distros.
