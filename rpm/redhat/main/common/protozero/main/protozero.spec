%global debug_package %{nil}

Name:		protozero
Version:	1.8.2
Release:	1PGDG%{?dist}
Summary:	Minimalistic protocol buffer decoder and encoder in C++

License:	BSD-2-Clause
URL:		https://github.com/mapbox/protozero
Source0:	https://github.com/mapbox/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:	cmake make gcc-c++
BuildRequires:	doxygen graphviz
BuildRequires:	protobuf-devel protobuf-lite-devel protobuf-compiler

%description
Minimalistic protocol buffer decoder and encoder in C++.

Designed for high performance. Suitable for writing zero copy parsers
and encoders with minimal need for run-time allocation of memory.

Low-level: this is designed to be a building block for writing a
very customized decoder for a stable protobuf schema. If your protobuf
schema is changing frequently or lazy decoding is not critical for your
application then this approach offers no value: just use the decoding
API available via the C++ API that can be generated via the Google
Protobufs protoc program.


%package	devel
Summary:	Development files for %{name}
Provides:	%{name}-static = %{version}-%{release}

%description	devel
Minimalistic protocol buffer decoder and encoder in C++.

Designed for high performance. Suitable for writing zero copy parsers
and encoders with minimal need for run-time allocation of memory.

Low-level: this is designed to be a building block for writing a
very customized decoder for a stable protobuf schema. If your protobuf
schema is changing frequently or lazy decoding is not critical for your
application then this approach offers no value: just use the decoding
API available via the C++ API that can be generated via the Google
Protobufs protoc program.

%prep
%autosetup -p 1 -n %{name}-%{version}
%{__mkdir} build

%build
%cmake -DWERROR=OFF
%cmake_build

%install
%cmake_install

%files devel
%doc README.md doc/*.md %{__cmake_builddir}/doc/html
%license LICENSE.md LICENSE.from_folly
%{_includedir}/protozero

%changelog
* Mon Aug 31 2026 Devrim Gündüz <devrim@gunduz.org> - 1.8.2-1PGDG
- Update to 1.8.2 per changes described at:
  https://github.com/mapbox/protozero/releases/tag/v1.8.2

* Tue Dec 5 2023 Devrim Gündüz <devrim@gunduz.org> - 1.7.1-42PGDG
- Initial packaging to support libosmium builds on EL-*
