%global sname	pgtap
%global tapparserversion	3.37

Summary:	Unit testing for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.3.4
Release:	1PGDG%{?dist}
License:	PostgreSQL
URL:		https://github.com/theory/%{sname}
Source0:	https://github.com/theory/%{sname}/archive/refs/tags/v%{version}.tar.gz
# Use this source for pg_prove and pg_tapgen
Source1:	https://search.cpan.org/CPAN/authors/id/D/DW/DWHEELER/TAP-Parser-SourceHandler-pgTAP-%{tapparserversion}.tar.gz
BuildRequires:	postgresql%{pgmajorversion} postgresql%{pgmajorversion}-devel
BuildRequires:	perl-Test-Pod perl-Test-Pod-Coverage perl-Module-Build
BuildArch:	noarch

Requires:	postgresql%{pgmajorversion}-server, perl-Test-Harness >= 3.0

%description
pgTAP is a unit testing framework for PostgreSQL written in PL/pgSQL and
PL/SQL. It includes a comprehensive collection of TAP-emitting assertion
functions, as well as the ability to integrate with other TAP-emitting
test frameworks. It can also be used in the xUnit testing style.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} TAPSCHEMA=pgtap %{?_smp_mflags}

# Build pg_prove and pg_tapgen
tar zxf %{SOURCE1}
pushd TAP-Parser-SourceHandler-pgTAP-%{tapparserversion}
perl Build.PL
./Build
popd

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} install DESTDIR=%{buildroot} %{?_smp_mflags}

# Install pg_prove and pg_tapgen
pushd TAP-Parser-SourceHandler-pgTAP-%{tapparserversion}
%{__mkdir} -p %{buildroot}%{_bindir}
%{__install} -m 755 bin/* %{buildroot}%{_bindir}
%{__mkdir} -p %{buildroot}%{perl_privlib}/TAP/Parser/SourceHandler/
%{__install} lib/TAP/Parser/SourceHandler/pgTAP.pm %{buildroot}%{perl_privlib}/TAP/Parser/SourceHandler/
popd

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/pgtap.mmd
%{_bindir}/pg_prove
%{_bindir}/pg_tapgen
#{pginstdir}/lib/{sname}.so
%{pginstdir}/share/extension/*pgtap*.sql
%{pginstdir}/share/extension/pgtap.control
%{perl_privlib}/TAP/Parser/SourceHandler/pgTAP.pm

%changelog
* Sun Oct 5 2025 Devrim Gündüz <devrim@gunduz.org> - 1.3.4-1PGDG
- Update to 1.3.4
- Update TAP parser version to 3.37

* Tue Apr 9 2024 Devrim Gündüz <devrim@gunduz.org> - 1.3.3-1PGDG
- Update to 1.3.3

* Mon Feb 5 2024 Devrim Gündüz <devrim@gunduz.org> - 1.3.2-1PGDG
- Update to 1.3.2
- Remove llvmjit subpackage, not built as of this version.

* Fri Nov 10 2023 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-2PGDG
- Use pgtap Github URLs

* Mon Sep 25 2023 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-1PGDG
- Update to 1.3.1

* Mon Aug 21 2023 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-1PGDG
- Update to 1.3.0
- Add PGDG branding

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon Dec 6 2021 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1
- Update to 1.2.0

* Wed Jun 2 2021 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-3
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Sat Nov 30 2019 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1
- Update to 1.1.0

* Fri Feb 22 2019 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1
- Update to 1.0.0

* Sun Oct 28 2018 Devrim Gündüz <devrim@gunduz.org> - 0.99.0-2
- Attempt to fix #3720

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.99.0-1.1
- Rebuild against PostgreSQL 11.0

* Mon Sep 24 2018 Devrim Gündüz <devrim@gunduz.org> 0.99.0-1
- Update to 0.99.0

* Sat Mar 17 2018 Devrim Gündüz <devrim@gunduz.org> 0.98.0-2
- Add pg_prove and pg_tapgen, per #3167

* Wed Nov 8 2017 Devrim Gündüz <devrim@gunduz.org> 0.98.0-1
- Update to 0.98.0

* Sat Dec 3 2016 Devrim Gündüz <devrim@gunduz.org> 0.97.0-1
- Update to 0.97.0

- Fri Mar 27 2015 Devrim Gündüz <devrim@gunduz.org> 0.95.0-1
- Update to 0.95.0

* Wed Jul 2 2014 Devrim Gündüz <devrim@gunduz.org> 0.94.0-1
- Update to 0.94.0

* Fri Apr 1 2011 Devrim Gündüz <devrim@gunduz.org> 0.25.0-1
- Update to 0.25.0

* Fri Oct 8 2010 Devrim Gündüz <devrim@gunduz.org> 0.24-3
- Use alternatives method for binaries.
- Use %%{?_smp_mflags} macro for make.

* Thu Oct 7 2010 Devrim Gündüz <devrim@gunduz.org> 0.24-2
- Update spec for 9.0 layout.
- TODO: Use alternatives.

* Tue Jun 15 2010 Devrim Gündüz <devrim@gunduz.org> 0.24-1
- Update to 0.24

* Mon Dec 28 2009 Devrim Gündüz <devrim@gunduz.org> 0.23-1
- Update to 0.23

* Wed Aug 19 2009 Darrell Fuhriman <darrell@projectdx.com> 0.22-1
- initial RPM

