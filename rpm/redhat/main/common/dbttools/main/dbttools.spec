Summary:	Shared tools for dbt2 tests
Name:		dbttools
Version:	0.5.1
Release:	1PGDG%{dist}
License:	GPLv2+
Source0:	https://github.com/osdldbt/%{name}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/osdldbt/%{name}

BuildArch:	noarch
Requires:	R-core >= 2.9.2 pandoc

%description
The purpose of this package is to provide tools that are shared between
all kits in the database test projects.

These scripts currently depend on R or Julia to generate charts.

%prep
%setup -q -n %{name}-%{version}

%build

%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p %{buildroot}/%{_bindir}

%{__cp} bin/dbt-p* %{buildroot}/%{_bindir}
%{__cp} bin/pgsql/* %{buildroot}/%{_bindir}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
%license LICENSE
%attr (755,root,root) %{_bindir}/dbt-pgsql*
%attr (755,root,root) %{_bindir}/dbt-plot*


%changelog
* Tue Apr 8 2025 Devrim Gündüz <devrim@gunduz.org> - 0.5.1-1PGDG
- Update to 0.5.1

* Sun Jul 23 2023 Devrim Gündüz <devrim@gunduz.org> - 0.5.0-1PGDG
- Update to 0.5.0
- Add PGDG branding

* Tue Mar 7 2023 Devrim Gündüz <devrim@gunduz.org> - 0.4.1-1
- Update to 0.4.1

* Mon Feb 27 2023 Devrim Gündüz <devrim@gunduz.org> - 0.3.2-1
- Update to 0.3.2

* Mon Oct 3 2022 Devrim Gündüz <devrim@gunduz.org> - 0.3.1-1
- Initial packaging
