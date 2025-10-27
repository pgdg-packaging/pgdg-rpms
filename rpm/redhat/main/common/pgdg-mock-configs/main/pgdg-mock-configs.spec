Name:		pgdg-mock-configs
Version:	2.0
Release:	1PGDG%{?dist}
Summary:	PGDG RPM mock core config files basic chroots
License:	PostgreSQL
URL:		https://yum.postgresql.org
Source0:	https://github.com/pgdg-packaging/%{name}/archive/refs/tags/%{name}-v1.0.tar.gz
BuildArch:	noarch

# distribution-gpg-keys contains GPG keys used by mock configs
Requires:	distribution-gpg-keys >= 1.105 mock-core-configs
# specify minimal compatible version of mock
Requires:	mock >= 5.4.post1
Requires:	mock-filesystem

Requires(post):	coreutils
# to detect correct default.cfg
Requires(post):	python3-dnf
Requires(post):	python3-hawkey
Requires(post):	system-release
Requires(post):	python3
Requires(post):	sed

%description
PGDG mock configuration files which allow you to create chroots for Fedora and RHEL

%prep
%setup -q -n %{name}-%{name}-v%{version}

%build

%install
%{__mkdir} -p %{buildroot}%{_sysconfdir}/mock/templates
%{__install} cfg/* %{buildroot}%{_sysconfdir}/mock
%{__install} templates/* %{buildroot}%{_sysconfdir}/mock/templates

%{__mkdir} -p %{buildroot}%{_docdir}/%{name}
%{__mkdir} -p %{buildroot}%{_licensedir}/%{name}
%{__cp} LICENSE.txt %{buildroot}%{_licensedir}/%{name}
%{__cp} README.txt %{buildroot}%{_docdir}/%{name}/

%files
%defattr(644,root,root)
%license LICENSE.txt
%doc README.txt
%{_sysconfdir}/mock/pgdg-fedora-*.cfg
%{_sysconfdir}/mock/pgdg-rocky-*.cfg
%{_sysconfdir}/mock/templates/pgdg-*.tpl

%changelog
* Mon Oct 27 2025 Devrim Gündüz <devrim@gunduz.org> 2.0-1PGDG
- Update to 2.0 per changes described at:
  https://github.com/pgdg-packaging/pgdg-mock-configs/releases/tag/pgdg-mock-config-v2.0

* Wed Feb 26 2025 Devrim Gündüz <devrim@gunduz.org> 1.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository
