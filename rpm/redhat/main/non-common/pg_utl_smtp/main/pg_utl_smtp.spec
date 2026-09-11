%global sname	pg_utl_smtp

Summary:	PostgreSQL extension to add compatibility to Oracle UTL_SMTP package.
Name:		%{sname}_%{pgmajorversion}
Version:	1.0
Release:	3PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/hexacluster/%{sname}/
Source0:	https://github.com/hexacluster/%{sname}/archive/refs/tags/v%{version}.tar.gz
BuildRequires:	make
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-plperl postgresql%{pgmajorversion}-server perl-Net-SNMP

BuildArch:	noarch

%description
PostgreSQL extension to add compatibility to Oracle UTL_SMTP package.

This extension uses plperlu stored procedures based on the Net::SMTP
Perl module to provide the procedures of the UTL_SMTP package

%prep
%setup -q -n %{sname}-%{version}

%build

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} INSTALL_PREFIX=%{buildroot} DESTDIR=%{buildroot} install
# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Thu Sep 10 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0-3PGDG
- Add missing BR

* Thu Jan 22 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0-2PGDG
- Fix plperl dependency

* Thu Jan 22 2026 Devrim Gündüz <devrim@gunduz.org> - 1.0-1PGDG
- Initial RPM packaging for the PostgreSQL RPM Repository:
  https://github.com/HexaCluster/pg_utl_smtp/releases/tag/v1.0
