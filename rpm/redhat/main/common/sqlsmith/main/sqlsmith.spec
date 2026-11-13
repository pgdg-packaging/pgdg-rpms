Name:		sqlsmith
Version:	1.5
Release:	3PGDG%{dist}
Summary:	Random SQL generator
License:	GPLv3
URL:		https://github.com/anse1/%{name}
Source0:	https://github.com/anse1/%{name}/archive/refs/tags/v%{version}.tar.gz
# ax_cxx_compile_stdcxx.m4 (serial 23) from autoconf-archive 2024.10.16.
# configure.ac needs AX_CXX_COMPILE_STDCXX(20), which the autoconf-archive
# on RHEL 9 and AL2023 does not know:
Source1:	%{name}-ax_cxx_compile_stdcxx.m4

BuildRequires:	autoconf autoconf-archive automake gcc-c++ libpq5-devel
BuildRequires:	libpqxx-devel sqlite-devel
Requires:	libpqxx boost-regex sqlite-libs

# libpqxx 8 needs C++20 <format>, which GCC 11 lacks:
%if 0%{?rhel} == 9
BuildRequires:	gcc-toolset-15 gcc-toolset-15-gcc gcc-toolset-15-gcc-c++ gcc-toolset-15-gcc-plugin-annobin
%endif
%if 0%{?amzn} == 2023
BuildRequires:	gcc14-c++
%endif

%description
SQLsmith is a random SQL query generator. Its paragon is Csmith, which proved
valuable for quality assurance in C compilers.

It currently supports generating queries for PostgreSQL, SQLite 3 and MonetDB.
To add support for another RDBMS, you need to implement two classes providing
schema information about and connectivity to the device under test.

Besides developers of the RDBMS products, users developing extensions might
also be interested in exposing their code to SQLsmith’s random workload.

%prep
%setup -q
%{__cp} -p %{SOURCE1} acinclude.m4
autoreconf -i

%build
%if 0%{?rhel} == 9
export PATH=/opt/rh/gcc-toolset-15/root/usr/bin/:$PATH
%endif
%if 0%{?amzn} == 2023
%undefine _annotated_build
%endif
%{?set_build_flags}
%if 0%{?amzn} == 2023
PKG_CONFIG_PATH=%{pginstdir}/lib/pkgconfig ./configure CXX='/usr/bin/gcc14-g++ -std=gnu++17' --with-postgresql=%{_bindir}/pg_config --prefix=/usr
%else
PKG_CONFIG=/usr/bin/pkg-config PKG_CONFIG_PATH=%{pginstdir}/lib/pkgconfig ./configure CXX='g++ -std=gnu++17' --with-postgresql=%{_bindir}/pg_config --prefix=/usr
%endif
%{__make} -j %{?_smp_mflags}

%install
%{__make} -j %{?_smp_mflags} DESTDIR=%{buildroot} install

%files
%doc README.org
%{_bindir}/%{name}
%license COPYING

%changelog
* Fri Nov 13 2026 Devrim Gunduz <devrim@gunduz.org> - 1.5-3PGDG
- Build with gcc-toolset-15 on RHEL 9, as libpqxx 8 needs C++20
  <format>, which GCC 11 lacks.
- Ship a newer ax_cxx_compile_stdcxx.m4, as configure.ac uses
  AX_CXX_COMPILE_STDCXX(20), which fails with the older autoconf-archive
  on RHEL 9 and AL2023.
- Call %%set_build_flags before configure, so that RHEL 9 builds get
  the distro compiler flags and debug info as well.

* Thu Sep 10 2026 Devrim Gündüz <devrim@gunduz.org> - 1.5-2PGDG
- Add missing BR

* Mon Aug 31 2026 Devrim Gündüz <devrim@gunduz.org> - 1.5-1PGDG
- Update to 1.5 per changes described at:
  https://github.com/anse1/sqlsmith/releases/tag/v1.5

* Thu Aug 27 2026 Devrim Gündüz <devrim@gunduz.org> - 1.4-3PGDG
- Fix Amazon Linux 2023 build: libpqxx headers need C++20's <format>,
  which requires gcc14-c++ since AL2023's default GCC (11) lacks it.

* Sat Jul 29 2023 Devrim Gündüz <devrim@gunduz.org> - 1.4-2PGDG
- Rebuild against new libpqxx
- Add PGDG branding

* Sat Oct 22 2022 Devrim Gündüz <devrim@gunduz.org> - 1.4-1
- Update to 1.4

* Wed Feb 23 2022 Devrim Gündüz <devrim@gunduz.org> - 1.3-1
- Initial packaging for PostgreSQL RPM repository, per upstream spec.
