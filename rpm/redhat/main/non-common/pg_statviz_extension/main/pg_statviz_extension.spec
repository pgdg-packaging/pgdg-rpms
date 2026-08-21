%global sname pg_statviz

Summary:	CLI tool for time series analysis and visualization of PostgreSQL internal statistics.
Name:		%{sname}_extension_%{pgmajorversion}
Version:	1.2
Release:	1PGDG%{dist}
License:	GPLv2+
Source0:	https://github.com/vyruss/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/vyruss/%{sname}

BuildArch:	noarch

%description
pg_statviz is a minimalist extension and utility pair for time series analysis
and visualization of PostgreSQL internal statistics.

Created for snapshotting PostgreSQL's cumulative and dynamic statistics and
performing time series analysis on them. The accompanying utility can produce
visualizations for selected time ranges on the stored stats snapshots,
enabling the user to track PostgreSQL performance over time and potentially
perform tuning or troubleshooting.

Best served with pg_statviz extension package, which includes the extension
files.

%prep
%setup -q -n %{sname}-%{version}

%build

%install
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

# README is already installed with the main package:
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(644,root,root,755)
%license LICENSE
%{pginstdir}/share/extension/*.control
%{pginstdir}/share/extension/*.sql

%changelog
* Fri Aug 21 2026 Devrim Gündüz <devrim@gunduz.org> - 1.2-1PGDG
- Update to 1.2 per changes described at:
  https://github.com/vyruss/pg_statviz/releases/tag/v1.2
  https://github.com/vyruss/pg_statviz/releases/tag/v1.1
  https://github.com/vyruss/pg_statviz/releases/tag/v1.0

* Thu Jan 15 2026 Devrim Gündüz <devrim@gunduz.org> - 0.9-1PGDG
- Update to 0.9

* Thu Sep 7 2023 Devrim Gündüz <devrim@gunduz.org> - 0.6-1PGDG
- Update to 0.6

* Thu Aug 24 2023 Devrim Gündüz <devrim@gunduz.org> - 0.5-1PGDG
- Update to 0.5

* Mon Aug 21 2023 Devrim Gündüz <devrim@gunduz.org> - 0.4-1PGDG
- Update to 0.4

* Thu Aug 17 2023 Devrim Gündüz <devrim@gunduz.org> - 0.3-1PGDG
- Update to 0.3

* Thu Apr 20 2023 Devrim Gündüz <devrim@gunduz.org> - 0.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository
