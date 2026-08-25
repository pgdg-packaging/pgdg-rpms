%global sname pg_statviz

%if 0%{?fedora} && 0%{?fedora} == 45
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?fedora} && 0%{?fedora} <= 44
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?suse_version} == 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

Summary:	CLI tool for time series analysis and visualization of PostgreSQL internal statistics.
Name:		%{sname}
Version:	1.2
Release:	2PGDG%{dist}
License:	GPLv2+
Source0:	https://github.com/vyruss/%{sname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/vyruss/%{sname}

BuildRequires:	python%{python3_pkgversion}-devel python%{python3_pkgversion}-wheel python%{python3_pkgversion}-pip

Requires:	python%{python3_pkgversion}-argh python%{python3_pkgversion}-kiwisolver
Requires:	python%{python3_pkgversion}-matplotlib python%{python3_pkgversion}-numpy
Requires:	python%{python3_pkgversion}-packaging python%{python3_pkgversion}-pandas
Requires:	python%{python3_pkgversion}-plac python3-psycopg3 >= 3.2.1
Requires:	python%{python3_pkgversion}-pyparsing python%{python3_pkgversion}-six

%if 0%{?fedora} >= 43 || 0%{?rhel} >= 8
Requires:	python3-cycler python3-dateutil python3-pillow
Requires:	python3-fonttools
%endif

%if 0%{?suse_version} >= 1500
Requires:	python%{python3_pkgversion}-Cycler python%{python3_pkgversion}-python-dateutil
Requires:	python%{python3_pkgversion}-Pillow python%{python3_pkgversion}-FontTools
%endif

BuildArch:	noarch

# AI deps. Currently only for Fedora:
%if 0%{?fedora} >= 43
# Claude:
Requires:	python3-anthropic
# Local:
Requires:	python3-ollama
# OpenAI:
Requires:	python3-openai
# Gemini:
Requires:	python3-google-genai
%endif

%description
pg_statviz is a minimalist extension and utility pair for time series analysis
and visualization of PostgreSQL internal statistics.

Created for snapshotting PostgreSQL's cumulative and dynamic statistics and
performing time series analysis on them. The accompanying utility can produce
visualizations for selected time ranges on the stored stats snapshots,
enabling the user to track PostgreSQL performance over time and potentially
perform tuning or troubleshooting.

Best served with pg_statviz extensions package, which includes the extension files.

%prep
%setup -q -n %{sname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%defattr(644,root,root,755)
%license LICENSE
%attr(0755,root,root) %{_bindir}/%{sname}
%{python3_sitelib}/%{sname}-%{version}.dist-info/*
%{python3_sitelib}/%{sname}

%changelog
* Tue Aug 25 2026 Devrim Gündüz <devrim@gunduz.org> - 1.2-2PGDG
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Fri Aug 21 2026 Devrim Gündüz <devrim@gunduz.org> - 1.2-1PGDG
- Update to 1.2 per changes described at:
  https://github.com/vyruss/pg_statviz/releases/tag/v1.2

* Wed May 27 2026 Devrim Gündüz <devrim@gunduz.org> - 1.1-1PGDG
- Update to 1.1 per changes described at:
  https://github.com/vyruss/pg_statviz/releases/tag/v1.0
  https://github.com/vyruss/pg_statviz/releases/tag/v1.1

* Thu Jan 15 2026 Devrim Gündüz <devrim@gunduz.org> - 0.9-1PGDG
- Update to 0.9 per changes described at:
  https://github.com/vyruss/pg_statviz/releases/tag/v0.9
  https://github.com/vyruss/pg_statviz/releases/tag/v0.8
- Add a temp patch to fix builds with "older" setuptools.

* Mon Jul 22 2024 Devrim Gündüz <devrim@gunduz.org> - 0.7-1PGDG
- Update to 0.7 per changes described at:
  https://github.com/vyruss/pg_statviz/releases/tag/v0.7

* Tue Feb 20 2024 Devrim Gündüz <devrim@gunduz.org> - 0.6-2PGDG
- Organise dependencies to support SLES 15.

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
