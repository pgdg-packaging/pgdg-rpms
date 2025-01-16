%global sname	pgstats
%global pgstatsmajver 1
%global pgstatsmidver 4
%global pgstatsminver 0

Summary:	vmstat-like tool for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	%{pgstatsmajver}.%{pgstatsmidver}.%{pgstatsminver}
Release:	1PGDG%{?dist}
License:	PostgreSQL
Source0:	https://github.com/gleu/pgstats/archive/refs/tags/REL%{pgstatsmajver}_%{pgstatsmidver}_%{pgstatsminver}.tar.gz
URL:		https://github.com/gleu/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-libs

%description
pgstat is a vmstat-like tool for PostgreSQL.

pgreport is a reporting tool for PostgreSQL. It tries to get a lot of
informations from the metadata and statistics of PostgreSQL.

pgwaitevent gathers every wait event for a specific PID, grouping them
by queries.

pgcsvstat outputs PostgreSQL statistics views into CSV files. The idea
is that you can load them on any spreadsheet to get the graphs you want.

pgdisplay tries to display a table in an informative way. Still pretty
much experimental.

%prep
%setup -q -n %{sname}-REL%{pgstatsmajver}_%{pgstatsmidver}_%{pgstatsminver}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

# Install README and howto file under PostgreSQL installation directory:
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/bin/pgcsvstat
%{pginstdir}/bin/pgdisplay
%{pginstdir}/bin/pgreport
%{pginstdir}/bin/pgstat
%{pginstdir}/bin/pgwaitevent

%changelog
* Thu Jan 16 2025 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-1PGDG
- Update to 1.4.0
- Add PGDG branding

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Fri Jul 9 2021 Devrim Gündüz <devrim@gunduz.org> - 1.2.0-1
- Update to 1.2.0

* Thu May 20 2021 Devrim Gündüz <devrim@gunduz.org> - 1.1.0-1
- Initial packaging for PostgreSQL RPM Repository
