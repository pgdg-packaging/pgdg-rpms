%global	commit	7e23085e7da80c8805fff54cc18e2705ac332074
%global	shortcommit %(c=%{commit}; echo ${c:0:7})

%pgdg_set_gis_variables
%global gdalinstdir %gdal38instdir

Name:		gdalcpp
Version:	1.3.0
Release:	6PGDG.20210925git%{shortcommit}%{?dist}
Summary:	C++11 wrapper classes for GDAL/OGR

License:	BSL-1.0
URL:		https://github.com/joto/gdalcpp
Source0:	https://github.com/joto/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildRequires:	pgdg-srpm-macros >= 1.0.37
BuildArch:	noarch

%description
These are some small wrapper classes for GDAL offering:

* classes with RAII instead of the arcane cleanup functions in stock GDAL
* works with GDAL 1 and 2
* allows you to write less boilerplate code

The classes are not very complete, they just have the code I needed for
various programs.

%package	devel
Summary:	Development files for %{name}
Provides:	%{name}-static = %{version}-%{release}

%description	devel
These are some small wrapper classes for GDAL offering:

* classes with RAII instead of the arcane cleanup functions in stock GDAL
* works with GDAL 1 and 2
* allows you to write less boilerplate code

The classes are not very complete, they just have the code I needed for
various programs.

%prep
%setup -q -n %{name}-%{commit}

%build

%install
%{__mkdir} -p %{buildroot}%{gdalinstdir}/include
%{__cp} -p *.hpp %{buildroot}%{gdalinstdir}/include

%files devel
%doc README.md
%license LICENSE.txt
%{gdalinstdir}/include/*.hpp

%changelog
* Sun Feb 18 2024 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-6PGDG.20210925git7e23085
- Rebuild against GDAL 3.8

* Tue Dec 5 2023 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-5PGDG.20210925git7e23085
- Initial packaging for the PostgreSQL RPM repository to support
  libosmium builds on EL*.
