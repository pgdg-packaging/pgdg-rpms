%global	sname	postgis_tiger_geocoder

%{!?runselftest:%global runselftest 0}

Summary:	Functions for geocoding, reverse geocoding, and standardizing address data using US Census TIGER/Line data.

Name:		%{sname}_%{pgmajorversion}
Version:	2025.2
Release:	3PGDG%{?dist}
License:	MIT
URL:		https://gitea.osgeo.org/postgis/%{sname}
Source0:	https://gitea.osgeo.org/postgis/%{sname}/releases/download/%{version}/%{sname}-%{version}.tar.gz
BuildRequires:	make
BuildRequires:	postgresql%{pgmajorversion} postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion} postgis3_%{pgmajorversion} >= 3.7.0
%if %runselftest
BuildRequires:	postgresql%{pgmajorversion}-server pgdg-srpm-macros >= 2.0.0
# The tests load postgis, fuzzystrmatch and address_standardizer
BuildRequires:	postgis3_%{pgmajorversion} postgresql%{pgmajorversion}-contrib
BuildRequires:	address_standardizer_%{pgmajorversion}
%endif
BuildArch:	noarch

%description
The postgis_tiger_geocoder is a PL/pgSQL extension that contains functions for
geocoding, reverse geocoding, and standardizing address data using US Census
TIGER/Line data.

To achieve this, it also includes helper functions that generate commandline
load scripts for downloading and loading into PostgreSQL the US Census TIGER
data.

%prep
%setup -q -n %{sname}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

# Install README file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%check
%if %runselftest
%pgdg_check_installcheck
%endif

%files
%defattr(-,root,root,-)
%doc SECURITY.md
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/share/extension/%{sname}*

%changelog
* Tue Sep 29 2026 Devrim Gündüz <devrim@gunduz.org> - 2025.2-3PGDG
- Add %%check, running the regression tests with the %%check helpers
  from pgdg-srpm-macros 2.0.0. It is disabled by default; enable it
  with --define 'runselftest 1'.

* Thu Sep 10 2026 Devrim Gündüz <devrim@gunduz.org> - 2025.2-2PGDG
- Add missing BR

* Mon Aug 24 2026 Devrim Gündüz <devrim@gunduz.org> - 2025.2-1PGDG
- Initial RPM packaging for PostgreSQL RPM Repository
