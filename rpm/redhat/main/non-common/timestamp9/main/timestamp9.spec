%global sname timestamp9

Summary:	An efficient nanosecond precision timestamp type for Postgres
Name:		%{sname}_%{pgmajorversion}
Version:	1.4.0
Release:	3PGDG%{?dist}
License:	MIT
Source0:	https://github.com/optiver/%{sname}/archive/refs/tags/%{sname}-%{version}.tar.gz
URL:		https://github.com/optiver/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	cmake >= 3.17
Requires:	postgresql%{pgmajorversion}-server

%description
timestamp9 is an efficient nanosecond precision timestamp type for PostgreSQL.

%prep
%setup -q -n %{sname}-%{sname}-%{version}

%build
%{__mkdir} build
pushd build
export PATH=%{pginstdir}/bin/:$PATH
%if 0%{?suse_version} >= 1500
cmake ..
%else
cmake3 ..
%endif

popd

%install
%{__rm} -rf %{buildroot}
pushd build
PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
popd

%files
%defattr(644,root,root,755)
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Tue Jan 28 2025 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-3PGDG
- Update project URL and remove reduntant BRs
- Remove RHEL 7 and SLES 12 support

* Wed Sep 13 2023 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-2PGDG
- Add PGDG branding

* Tue Jun 6 2023 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-1
- Update to 1.4.0

* Mon Feb 27 2023 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-1
- Update to 1.3.0

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Sun Aug 28 2022 - Devrim Gündüz <devrim@gunduz.org> 1.1.0-1
- Initial RPM packaging for PostgreSQL YUM Repository
