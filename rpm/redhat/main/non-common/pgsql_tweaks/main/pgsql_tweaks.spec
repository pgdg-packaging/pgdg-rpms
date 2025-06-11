%global sname pgsql_tweaks
%global pname pgsql-tweaks

Summary:	PostgreSQL functions which a DBA regularly needs
Name:		%{sname}_%{pgmajorversion}
Version:	0.11.3
Release:	1PGDG%{?dist}
License:	PostgreSQL
URL:		https://gitlab.com/sjstoelting/%{pname}
Source0:	https://gitlab.com/sjstoelting/%{pname}/-/archive/v%{version}/%{pname}-v%{version}.tar.bz2
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server
BuildArch:	noarch

%description
The package includes several functions and views to help daily PostgreSQL work.

%prep
%setup -q -n %{pname}-v%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install

# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/share/extension/%{sname}--%{version}.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Wed Jun 11 2025 Devrim Gündüz <devrim@gunduz.org> 0.11.3-1PGDG
- Update to 0.11.3

* Wed Feb 19 2025 Devrim Gündüz <devrim@gunduz.org> 0.11.0-1PGDG
- Update to 0.11.0

* Mon Oct 21 2024 Devrim Gündüz <devrim@gunduz.org> 0.10.7-1PGDG
- Update to 0.10.7

* Sun Sep 29 2024 Devrim Gündüz <devrim@gunduz.org> 0.10.6-1PGDG
- Update to 0.10.6

* Tue Jun 4 2024 Devrim Gündüz <devrim@gunduz.org> 0.10.3-1PGDG
- Update to 0.10.3

* Mon Nov 20 2023 Devrim Gündüz <devrim@gunduz.org> 0:0.10.2-1PGDG
- Update to 0.10.2
- Add PGDG branding

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 0.10.1-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Tue Oct 18 2022 Devrim Gündüz <devrim@gunduz.org> 0:0.10.1-1
- Update to 0.10.1

* Mon Aug 15 2022 Devrim Gündüz <devrim@gunduz.org> 0:0.10.0-1
- Update to 0.10.0

* Sun Jul 10 2022 Devrim Gündüz <devrim@gunduz.org> 0:0.9.1-1
- Update to 0.9.1

* Mon Sep 20 2021 Devrim Gündüz <devrim@gunduz.org> 0:0.8.0-1
- Update to 0.8.0

* Fri Sep 10 2021 Devrim Gündüz <devrim@gunduz.org> 0:0.7.1-1
- Initial packaging for PostgreSQL RPM Repository
