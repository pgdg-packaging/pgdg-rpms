%global		_sourcename json

Name:		nlohmann_json
Version:	3.12.0
Release:	1PGDG%{?dist}
Summary:	JSON for Modern C++
License:	MIT
URL:		https://github.com/nlohmann/json
Source0:	https://github.com/nlohmann/%{_sourcename}/archive/v%{version}/%{_sourcename}-%{version}.tar.gz
BuildRequires:	cmake >= 3.5 gcc-c++
BuildArch:	noarch

%description
nlohmann_json is a header-only JSON library for Modern C++, with an
intuitive syntax, and full STL-like access and support for arbitrary
data types.

%package devel
Summary:	Header files for nlohmann_json, the JSON library for Modern C++
Provides:	%{name}-static = %{version}-%{release}

%description devel
This package provides the header files and the CMake and pkg-config
files of nlohmann_json, a header-only JSON library for Modern C++.

It is needed to build SFCGAL on distributions that do not ship it.

%prep
%setup -q -n %{_sourcename}-%{version}

%build
%cmake -DJSON_BuildTests=OFF -DJSON_Install=ON \
	-DJSON_MultipleHeaders=ON
%cmake_build

%install
%cmake_install

%files devel
%license LICENSE.MIT
%doc README.md ChangeLog.md
%{_includedir}/nlohmann/
%{_datadir}/cmake/%{name}/
%{_datadir}/pkgconfig/%{name}.pc

%changelog
* Wed Oct 21 2026 Devrim Gündüz <devrim@gunduz.org> - 3.12.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to support
  SFCGAL on Amazon Linux 2023, which does not ship nlohmann_json.
