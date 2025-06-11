%global _vpath_builddir .
%global sname pg_top

Summary:	'top' for PostgreSQL process
Name:		%{sname}
Version:	4.1.2
Release:	42PGDG%{?dist}
License:	BSD
URL:		https://gitlab.com/%{sname}/%{sname}
Source0:	https://gitlab.com/%{sname}/%{sname}/-/archive/v%{version}/%{sname}-v%{version}.tar.bz2
BuildRequires:	libpq5-devel ncurses-devel
BuildRequires:	libbsd-devel
%if 0%{?suse_version} >= 1500
BuildRequires:	libelf-devel
%else
BuildRequires:	elfutils-libelf-devel
%endif
Requires:	libpq5 postgresql-server
Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

Obsoletes:	%{sname}_16 < 4.1.0 %{sname}_15 < 4.1.0	%{sname}_14 < 4.1.0
Obsoletes:	%{sname}_13 < 4.1.0 %{sname}_12 < 4.1.0

%description
pg_top is 'top' for PostgreSQL. It is derived from Unix Top. Similar to top,
pg_top allows you to monitor PostgreSQL processes. It also allows you to:
 - View currently running SQL statement of a process.
 - View query plan of a currently running SELECT statement.
 - View locks held by a process.
 - View I/O statistics per process.
 - View replication statistics for downstream nodes.

%prep
%setup -q -n %{sname}-v%{version}

%cmake

%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags}

%install
%if 0%{?suse_version} >= 1500
pushd build
%endif
%{__make} -C "%{_vpath_builddir}" %{?_smp_mflags} install/fast \
	DESTDIR=%{buildroot}

%files
%defattr(-,root,root,-)
%doc README.rst
%license LICENSE
%{_bindir}/%{sname}
%{_mandir}/man1/%{sname}.1.gz

%changelog
* Fri Jun 6 2025 Devrim Gündüz <devrim@gunduz.org> - 4.1.2-42PGDG
- Update to 4.1.2 per changes described at:
  https://gitlab.com/pg_top/pg_top/-/releases#2025-06-04-v412

* Mon Jul 29 2024 Devrim Gündüz <devrim@gunduz.org> - 4.1.1-10PGDG
- Update to 4.1.1

* Mon May 27 2024 Devrim Gündüz <devrim@gunduz.org> - 4.1.0-10PGDG
- Update to 4.1.0
- Move package to common repository.

* Sun Feb 25 2024 Devrim Gündüz <devrim@gunduz.org> - 3.7.0-10PGDG
- Add PGDG branding

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 3.7.0-9
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Thu Sep 29 2022 Devrim Gündüz <devrim@gunduz.org> - 3.7.0-8
- Remove RHEL 6 support, and remove obsoletes

* Thu Feb 4 2021 John Harvey <john.harvey@crunchydata.com> 3.7.0-7
- Fix Obsoletes

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> - 3.7.0-6
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 3.7.0-5.2
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 3.7.0-5.1
- Rebuild against PostgreSQL 11.0

* Fri Aug 26 2016 - Devrim Gündüz <devrim@gunduz.org> 3.7.0-5
- Fix alternatives link, per report from  Dmitriy Sarafannikov.
  Fixes #1604.

* Tue Jan 26 2016 - Devrim Gündüz <devrim@gunduz.org> 3.7.0-4
- Cosmetic updates, and simplify %%doc section.

* Thu Mar 26 2015 - Devrim Gündüz <devrim@gunduz.org> 3.7.0-3
- Fix alternatives path and version.

* Thu Mar 26 2015 - Devrim Gündüz <devrim@gunduz.org> 3.7.0-2
- Update URLs: Project moved to github.
- pg_top now requires autoconf for build.

* Tue Sep 17 2013 - Devrim Gündüz <devrim@gunduz.org> 3.7.0-1
- Update to 3.7.0
- Remove patch2, now in upstream.
- Remove patch1, new GCC's do not like it.

* Mon Jan 17 2011 - Devrim Gündüz <devrim@gunduz.org> 3.6.2-3
- Port a few fixes from EPEL:
 * Fix display of cumulative statistics (BZ#525763)
 * include %%{optflags} during compilation.
 * include DOC files, including license file
 * fix %%defattr

* Thu Nov 11 2010 - Devrim Gündüz <devrim@gunduz.org> 3.6.2-2
- Apply changes for PostgreSQL 9.0 RPM layout

* Thu May 15 2008 - Devrim Gündüz <devrim@gunduz.org> 3.6.2-1
- Update to 3.6.2

* Sat Apr 12 2008 - Devrim Gündüz <devrim@gunduz.org> 3.6.2-0.1.beta3
- Rename to pg_top
- Update to 3.6.2 beta3

* Mon Mar 10 2008 - Devrim Gündüz <devrim@gunduz.org> 3.6.1-1
- Update to 3.6.1

* Sun Jan 20 2008 - Devrim Gündüz <devrim@gunduz.org> 3.6.1-1.beta3
- Update to 3.6.1-beta3

* Thu Dec 13 2007 - Devrim Gündüz <devrim@gunduz.org> 3.6.1-1.beta2
- Initial RPM packaging for Fedora
