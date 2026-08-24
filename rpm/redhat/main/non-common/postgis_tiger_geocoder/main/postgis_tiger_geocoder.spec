%global	sname	postgis_tiger_geocoder

Summary:	Functions for geocoding, reverse geocoding, and standardizing address data using US Census TIGER/Line data.

Name:		%{sname}_%{pgmajorversion}
Version:	2025.2
Release:	1PGDG%{?dist}
License:	MIT
URL:		https://gitea.osgeo.org/postgis/%{sname}
Source0:	https://gitea.osgeo.org/postgis/%{sname}/releases/download/%{version}/%{sname}-%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion} postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion} postgis3_%{version} >= 3.7.0
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

%files
%defattr(-,root,root,-)
%doc SECURITY.md
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/share/extension/%{sname}*

%changelog
* Mon Aug 24 2026 Devrim Gündüz <devrim@gunduz.org> - 2025.2-1PGDG
- Initial RPM packaging for PostgreSQL RPM Repository
