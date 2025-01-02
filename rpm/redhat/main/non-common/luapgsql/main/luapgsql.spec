%global sname luapgsql

%{!?luaver: %global luaver %(lua -e "print(string.sub(_VERSION, 5))")}
# for compiled modules
%global lualibdir %{_libdir}/lua/%{luaver}
# for arch-independent modules
%global luapkgdir %{_datadir}/lua/%{luaver}

Summary:	Lua binding for PostgreSQL
Name:		%{sname}
Version:	1.6.7
Release:	7PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/arcapos/%{name}/archive/pgsql-%{version}.tar.gz
Patch0:		%{sname}-pg%{pgmajorversion}-makefile-pgxs.patch
URL:		https://github.com/arcapos/%{name}/
BuildRequires:	lua-devel
BuildRequires:	postgresql%{pgmajorversion}-devel lua-devel
Requires:	postgresql%{pgmajorversion}-server
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	lua(abi) = %{luaver}
%else
%global luanext 5.2
Requires:	lua >= %{luaver}
Requires:	lua < %{luanext}
%endif

%description
A Lua Binding for PostgreSQL.

%prep
%setup -q -n %{sname}-pgsql-%{version}
%patch -P 0 -p0

%build
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{lualibdir}/pgsql.so

%changelog
* Thu Jan 2 2025 Devrim Gunduz <devrim@gunduz.org> - 1.6.7-7PGDG
- Update license and remove RHEL 7 dependency

* Thu Feb 22 2024 Devrim Gunduz <devrim@gunduz.org> - 1.6.7-6PGDG
- Enable debug package

* Wed Sep 13 2023 Devrim Gunduz <devrim@gunduz.org> - 1.6.7-5PGDG
- Add PGDG branding
- Fix rpmlint warnings

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 1.6.7-4.1
- Modernise %%patch usage, which has been deprecated in Fedora 38

* Sat Apr 22 2023 Devrim Gündüz <devrim@gunduz.org> - 1.6.7-4
- Update patch and also add patches for PostgreSQL 13+.

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.6.7-3
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 1.6.7-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 1.6.7-1.1
- Rebuild for PostgreSQL 12

* Tue Apr 16 2019 Devrim Gündüz <devrim@gunduz.org> - 1.6.7-1
- Update to 1.6.7

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 1.6.1-1.1
- Rebuild against PostgreSQL 11.0

* Wed Nov 9 2016 - Devrim Gündüz <devrim@gunduz.org> 1.6.1-1
- Update to 1.6.1

* Sat Aug 27 2016 - Devrim Gündüz <devrim@gunduz.org> 1.6.0-1
- Initial RPM packaging for PostgreSQL RPM Repository
