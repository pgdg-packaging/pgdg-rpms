%global sname pgpool-II

Summary:	PostgreSQL extensions for pgpool-II
Name:		%{sname}-pg%{pgmajorversion}-extensions
Version:	4.6.0
Release:	1PGDG%{?dist}
License:	BSD
URL:		https://pgpool.net
Source0:	https://www.pgpool.net/mediawiki/images/%{sname}-%{version}.tar.gz
Requires:	postgresql%{pgmajorversion}-server %{sname}-pcp

BuildRequires:	postgresql%{pgmajorversion}-devel pam-devel
BuildRequires:	libmemcached-devel openssl-devel
%if 0%{?suse_version} >= 1500
BuildRequires:	openldap2-devel
Requires(post):	systemd-sysvinit
%else
BuildRequires:	openldap-devel
Requires(post):	systemd-sysv
Requires(post):	systemd
Requires(preun):	systemd
Requires(postun):	systemd
%endif

Requires:	libmemcached
Requires:	%{sname}

%description
PostgreSQL extensions, libraries and sql files for pgpool-II.

%prep
%setup -q -n %{sname}-%{version}

%build
# We need this flag on SLES so that pgpool can find libmemched.
# Otherwise, we get "libmemcached.so: undefined reference to `pthread_once'" error.
%if 0%{?suse_version}
	export LDFLAGS='-lpthread'
%endif
%ifarch ppc64 ppc64le
%configure --build=ppc64le \
%else
./configure \
%endif
	--prefix /usr \
	--libdir %{_libdir} \
	--disable-static \
	--sysconfdir=%{_sysconfdir}/%{name}/ \
	--with-ldap \
	--with-memcached=%{_includedir}/libmemcached \
	--with-openssl \
	--with-pam \
	--with-pgsql=%{pginstdir}

# https://fedoraproject.org/wiki/Packaging:Guidelines#Removing_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

export PATH=%{pginstdir}/bin/:$PATH
USE_PGXS=1 %{__make} %{?_smp_mflags}
USE_PGXS=1 %{__make} %{?_smp_mflags} -C src/sql/pgpool_adm
USE_PGXS=1 %{__make} %{?_smp_mflags} -C src/sql/pgpool-recovery
USE_PGXS=1 %{__make} %{?_smp_mflags} -C src/sql/pgpool-regclass

%install
export PATH=%{pginstdir}/bin/:$PATH
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install -C src/sql/pgpool_adm
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install -C src/sql/pgpool-recovery
%{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install -C src/sql/pgpool-regclass

# nuke libtool archive and static lib
%{__rm} -f %{buildroot}%{_libdir}/libpcp.{a,la}
# Remove bitcode files
%{__rm} -rf %{buildroot}%{pginstdir}/lib/bitcode/

%files
%doc README AUTHORS
%license COPYING
%{pginstdir}/lib/pgpool_adm.so
%{pginstdir}/lib/pgpool-recovery.so
%{pginstdir}/lib/pgpool-regclass.so
%{pginstdir}/share/extension/pgpool_adm*.sql
%{pginstdir}/share/extension/pgpool_adm.control
%{pginstdir}/share/extension/pgpool-regclass.sql
%{pginstdir}/share/extension/pgpool_regclass--1.0.sql
%{pginstdir}/share/extension/pgpool_regclass.control
%{pginstdir}/share/extension/pgpool-recovery.sql
%{pginstdir}/share/extension/pgpool_recovery*.sql
%{pginstdir}/share/extension/pgpool_recovery.control

%changelog
* Mon Mar 3 2025 Devrim Gündüz <devrim@gunduz.org> - 4.6.0-1PGDG
- Update to 4.6.0 per changes described at:
  https://www.pgpool.net/docs/latest/en/html/release-4-6-0.html

* Tue Feb 25 2025 Devrim Gündüz <devrim@gunduz.org> - 4.5.5-2PGDG
- Add missing BR

* Mon Dec 16 2024 Devrim Gündüz <devrim@gunduz.org> - 4.5.5-1PGDG
- Update to 4.5.5 per changes described at:
  https://www.pgpool.net/docs/latest/en/html/release-4-5-5.html

* Mon Sep 9 2024 Devrim Gündüz <devrim@gunduz.org> - 4.5.4-1PGDG
- Update to 4.5.4 per changes described at:
  https://www.pgpool.net/docs/latest/en/html/release-4-5-4.html
  Fixes CVE-2024-45624.

* Fri Aug 16 2024 Devrim Gündüz <devrim@gunduz.org> - 4.5.3-1PGDG
- Update to 4.5.3 per changes described at:
  https://www.pgpool.net/docs/latest/en/html/release-4-5-3.html

* Wed May 29 2024 Devrim Gündüz <devrim@gunduz.org> - 4.5.2-1PGDG
- Update to 4.5.2 per changes described at:
  https://www.pgpool.net/docs/latest/en/html/release-4-5-2.html

* Thu Feb 29 2024 Devrim Gündüz <devrim@gunduz.org> - 4.5.1-1PGDG
- Update to 4.5.1

* Fri Feb 23 2024 Devrim Gündüz <devrim@gunduz.org> - 4.5.0-2PGDG
- Enable -debug* subpackages

* Mon Jan 23 2023 Devrim Gündüz <devrim@gunduz.org> - 4.5.0-1PGDG
- Update to 4.5.0
- Add PGDG branding

* Mon Jan 23 2023 Devrim Gündüz <devrim@gunduz.org> - 4.4.2-1
- Update to 4.4.2

* Sun Dec 25 2022 Devrim Gündüz <devrim@gunduz.org> - 4.4.1-1
- Update to 4.4.1

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 4.3.3-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Fri Aug 19 2022 Devrim Gündüz <devrim@gunduz.org> - 4.3.3-1
- Update to 4.3.3
- Build with --with-ldap, per #7687 .

* Thu May 19 2022 Devrim Gündüz <devrim@gunduz.org> - 4.3.2-1
- Update to 4.3.2

* Mon Feb 21 2022 Devrim Gündüz <devrim@gunduz.org> - 4.3.1-1
- Update to 4.3.1

* Tue Dec 28 2021 Devrim Gündüz <devrim@gunduz.org> - 4.3.0-1
- Initial packaging for 4.3 series.
