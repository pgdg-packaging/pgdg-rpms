Name:		pgdg-suse-repo
Version:	42.0
Release:	51PGDG
Summary:	PostgreSQL PGDG RPMs - Zypper Repository Configuration for OpenSuSE Leap
License:	PostgreSQL
URL:		https://zypp.postgresql.org
%if %{?suse_version} == 1600
Source0:	pgdg-opensuse-all-leap16.repo
Source1:	PGDG-RPM-GPG-KEY-LEAP16
%endif
BuildArch:	noarch
Requires:	Leap-release

%description
This package contains zypper configuration for OpenSuSE Leap

%prep
%setup -q -c -T

%build

%install
%{__rm} -rf %{buildroot}

%{__install} -dm 755 %{buildroot}%{_sysconfdir}/zypp/repos.d
%{__mkdir} -p %{buildroot}%{_sysconfdir}/pki/

%{__install} -pm 644 %{SOURCE0} \
	%{buildroot}%{_sysconfdir}/zypp/repos.d/pgdg-opensuse-all-leap.repo
%{__install} -Dpm 644 %{SOURCE1} \
		%{buildroot}%{_sysconfdir}/pki/

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/zypp/repos.d/*
%{_sysconfdir}/pki/PGDG-RPM-GPG-KEY-LEAP1*

%changelog
* Tue Mar 24 2026 Devrim Gündüz <devrim@gunduz.org> - 42.0-51PGDG
- Initial OpenSuSE Leap repo packaging for the PostgreSQL RPM repository.
