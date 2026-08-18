Name:		pgdg-redhat-repo
Version:	42.0
Release:	67.al%{dist}PGDG
Summary:	PostgreSQL PGDG RPMs - DNF Repository Configuration for Amazon Linux 2023
License:	PostgreSQL
URL:		https://yum.postgresql.org

%ifarch aarch64
Source0:	https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-AMAZONLINUX
Source2:	pgdg-amazonlinux-all-rhel%{dist}-aarch64.repo
%endif
%ifarch x86_64
Source0:	https://yum.postgresql.org/keys/PGDG-RPM-GPG-KEY-AMAZONLINUX
Source2:	pgdg-amazonlinux-all-rhel%{dist}.repo
%endif

BuildArch:	noarch
Requires:	/etc/amazon-linux-release

%description
This package contains DNF configuration for Amazon Linux 2023 and also the GPG
key for PGDG RPMs.

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
	%{buildroot}%{_sysconfdir}/yum.repos.d/pgdg-amazonlinux-all.repo

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/*
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Tue Aug 18 2026 Devrim Gündüz <devrim@gunduz.org> - 42.0-67PGDG
- The new repo package for Amazon Linux 2023
