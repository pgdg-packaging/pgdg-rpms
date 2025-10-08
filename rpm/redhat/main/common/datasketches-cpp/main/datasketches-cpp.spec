%global _vpath_builddir .
%global _libdir /usr/lib64

Summary:	Routing functionality for PostGIS
Name:		datasketches-cpp
Version:	5.2.0
Release:	2PGDG%{dist}
License:	GPLv2+
Source0:	https://github.com/apache/%{name}/archive/refs/tags/%{version}.tar.gz
Patch0:		%{name}-cmakelist-lib64.patch
URL:		https://github.com/apache/%{name}/
BuildRequires:	gcc-c++ cmake
%if 0%{?suse_version} >= 1500
BuildRequires:	cmake-full
%else
BuildRequires:	cmake-rpm-macros
%endif

BuildArch:	noarch

%description
This is the core C++ component of the Apache DataSketches library. It contains
all of the key sketching algorithms that are in the Java component and can be
accessed directly from user applications.

This component is also a dependency of other components of the library that
create adaptors for target systems, such as PostgreSQL.

%prep
%setup -q -n %{name}-%{version}
%patch -P 0 -p0

%build
%{__install} -d build
pushd build
%if 0%{?suse_version} >= 1500
cmake .. \
%else
%cmake3 .. \
%endif
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_BUILD_TYPE=Release \
	-DBUILD_TESTS=OFF \
	-DLIB_INSTALL_DIR=%{_libdir}

popd

%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} build

%install
%{__rm} -rf %{buildroot}
pushd build
%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} install \
	DESTDIR=%{buildroot}
popd

%files
%defattr(644,root,root,755)
%license LICENSE
%doc README.md
%dir %{_includedir}/DataSketches/
%dir %{_libdir}/DataSketches/
%{_includedir}/DataSketches/*
%{_libdir}/DataSketches/*

%changelog
* Wed Oct 8 2025 Devrim Gündüz <devrim@gunduz.org> - 5.2.0-2PGDG
- Fix SLES builds

* Mon Apr 7 2025 Devrim Gündüz <devrim@gunduz.org> - 5.2.0-1PGDG
- Update to 5.2.0
- Add missing BRs

* Thu Dec 19 2024 Devrim Gündüz <devrim@gunduz.org> - 5.1.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support
  datasketches-postgresql.
