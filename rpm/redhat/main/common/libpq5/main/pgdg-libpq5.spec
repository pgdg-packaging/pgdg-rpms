%global pgmajorversion 17

# Macros that define the configure parameters:
%{!?kerbdir:%global kerbdir "/usr"}

Summary:	PostgreSQL Client Library
Name:		libpq5
Version:	%{pgmajorversion}.6
%if 0%{?suse_version} >= 1500
# SuSE upstream packages have release numbers like 150200.5.19.1
# which overrides our packages. Increase our release number on SuSE.
Release:	420001PGDG%{?dist}
%else
Release:	1PGDG%{?dist}
%endif
License:	PostgreSQL
Url:		https://www.postgresql.org/

Source0:	https://download.postgresql.org/pub/source/v%{version}/postgresql-%{version}.tar.bz2

Patch1:		%{name}-rpm-pgsql.patch
Patch5:		%{name}-var-run-socket.patch

BuildRequires:	gcc glibc-devel bison flex >= 2.5.31
BuildRequires:	readline-devel zlib-devel >= 1.0.4

BuildRequires:	krb5-devel libicu-devel libxml2-devel libxslt-devel
BuildRequires:	pam-devel e2fsprogs-devel systemd systemd-devel
BuildRequires:	systemtap-sdt-devel
%if 0%{?fedora} >= 41 || 0%{?rhel} >= 10
BuildRequires:	systemtap-sdt-dtrace
%endif
BuildRequires:	perl(ExtUtils::MakeMaker)
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 9
BuildRequires:	perl-FindBin
%endif

%if 0%{?suse_version} >= 1500
BuildRequires:	uuid-devel
%else
BuildRequires:	libuuid-devel
%endif

%if 0%{?fedora} || 0%{?rhel}
BuildRequires:	perl-ExtUtils-Embed
%endif

%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
%endif
%if 0%{?fedora} || 0%{?rhel}
BuildRequires:	llvm-devel => 17.0 clang-devel >= 17.0
%endif

Requires:	/sbin/ldconfig libicu

%if 0%{?suse_version} >= 1500
BuildRequires:	libopenssl-devel
%else
BuildRequires:	openssl-devel
%endif

%if 0%{?fedora} >= 41
BuildRequires:	openssl-devel-engine
%endif

# lz4 dependency
%if 0%{?suse_version} >= 1315
BuildRequires:	liblz4-devel
Requires:	liblz4-1
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	lz4-devel
Requires:	lz4-libs
%endif

# zstd dependency
%if 0%{?suse_version} >= 1499
BuildRequires:	libzstd-devel >= 1.4.0
Requires:	libzstd1 >= 1.4.0
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	libzstd-devel >= 1.4.0
Requires:	libzstd >= 1.4.0
%endif

%if 0%{?suse_version}
%if 0%{?suse_version} >= 1315
BuildRequires:	openldap2-devel
%endif
%else
BuildRequires:	openldap-devel
%endif

BuildRequires:	gettext >= 0.10.35

# All supported distros have libselinux-devel package:
BuildRequires:	libselinux-devel >= 2.0.93
# SLES: SLES 15 does not have selinux-policy package. Use
# it only on SLES 12:
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	selinux-policy >= 3.9.13
%endif
# RHEL/Fedora has selinux-policy:
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	selinux-policy >= 3.9.13
%endif

BuildRequires:	openssl-devel

%if 0%{?suse_version} >= 1500
Requires:	libopenssl1_1
%else
Requires:	openssl-libs >= 1.0.2k
%endif

Obsoletes:	libpq <= 99.0
Provides:	postgresql-libs >= 9.2 libpq >= 10.0 libpq.so.5
Provides:	libpq.so.5(RHPG_9.6)(64bit) libpq.so.5(RHPG_10)(64bit)
Provides:	libpq.so.5(RHPG_11)(64bit) libpq.so.5(RHPG_12)(64bit)
Provides:	libpq.so.5(RHPG_13)(64bit) libpq.so.5(RHPG_14)(64bit)
Provides:	libpq.so.5(RHPG_15)(64bit)

%description
The libpq5 package provides the essential shared libraries for any
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package devel
Summary:	Development files for building PostgreSQL client tools
Requires:	%name%{?_isa} = %version-%release
# Historically we had 'postgresqlXX-devel' package which was used for building
# both PG clients and PG server modules; let's have this fake provide to cover
# most of the depending packages and the rest (those which want to build server
# modules) need to be fixed to require postgresql-server-devel package.

%description devel
The libpq5 package provides the essential shared library for any PostgreSQL
client program or interface. You will need to install this package to build any
package or any clients that need to connect to a PostgreSQL server.

%ifarch ppc64 ppc64le
AutoReq:	0
%endif

%prep
%setup -q -n postgresql-%{version}
%patch -P 1 -p0
%patch -P 5 -p0

%build
CFLAGS="${CFLAGS:-%optflags}"
# Strip out -ffast-math from CFLAGS....
CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`
%if 0%{?rhel}
	LDFLAGS="-Wl,--as-needed"; export LDFLAGS
%endif

export CFLAGS

export PYTHON=/usr/bin/python3

CFLAGS="${CFLAGS:-%optflags}"
# Strip out -ffast-math from CFLAGS....
CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`
%if 0%{?rhel}
LDFLAGS="-Wl,--as-needed"; export LDFLAGS
%endif
export CFLAGS

# These configure options must match main build
%configure \
	--enable-rpath \
	--enable-dtrace \
	--enable-nls \
	--with-gssapi \
	--with-icu \
	--with-includes=%{kerbdir}/include \
	--with-libraries=%{kerbdir}/%{_lib} \
	--with-ldap \
	--with-libxslt \
	--with-libxml \
	--with-llvm \
	--with-lz4 \
	--with-openssl \
	--with-pam \
	--with-selinux \
	--with-systemd \
	--with-system-tzdata=%{_datadir}/zoneinfo \
	--with-uuid=e2fs \
	--with-zstd

%global build_subdirs \\\
	src/include \\\
	src/common \\\
	src/port \\\
	src/interfaces/libpq \\\
	src/bin/pg_config

for subdir in %build_subdirs; do
MAKELEVEL=0 %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} -C "$subdir"
done

%install
%{__rm} -rf %{buildroot}

for subdir in %build_subdirs; do
MAKELEVEL=0 %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install -C "$subdir"
done

# remove files not to be packaged
find %{buildroot} -name '*.a' -delete
%{__rm} -r %{buildroot}%_datadir/pgsql/postgres.bki
%{__rm} -r %{buildroot}%_datadir/pgsql/system_constraints.sql

%{__cp} /dev/null libs.lst

find_lang_bins ()
{
    lstfile=$1 ; shift
    cp /dev/null "$lstfile"
    for binary; do
	%find_lang "$binary"-%pgmajorversion
	cat "$binary"-%pgmajorversion.lang >>"$lstfile"
    done
}

find_lang_bins %name.lst	libpq5
find_lang_bins %name-devel.lst	pg_config

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

# FILES section.

%files -f %name.lst
%defattr(-,root,root)
%{_libdir}/libpq.so*
%doc %_datadir/pgsql/pg_service.conf.sample

%files devel -f %name-devel.lst
%_bindir/pg_config
%_includedir/*
%_libdir/libpq.so
%_libdir/pkgconfig/libpq.pc

%changelog
* Fri Aug 29 2025 Devrim Gündüz <devrim@gunduz.org> - 17.6-42-1PGDG
- Update to 17.6

* Fri May 9 2025 Devrim Gündüz <devrim@gunduz.org> - 17.5-42-1PGDG
- Update to 17.5

* Tue Apr 8 2025 Devrim Gündüz <devrim@gunduz.org> - 17.4-3PGDG
- systemtap-sdt-dtrace is RHEL 10+ and Fedora 41+ package.
- perl-FindBin Fedora 40+ and RHEL 9+ package

* Mon Apr 7 2025 Devrim Gündüz <devrim@gunduz.org> - 17.4-2PGDG
- Sync build parameters with main package.
- Install more files with -devel subpackage. Need it for some of the
  packages in common repository.

* Tue Feb 18 2025 Devrim Gündüz <devrim@gunduz.org> - 17.4-42-1PGDG
- Update to 17.4

* Sun Feb 16 2025 Devrim Gündüz <devrim@gunduz.org> - 17.3-42-1PGDG
- Update to 17.3

* Sun Dec 29 2024 Devrim Gündüz <devrim@gunduz.org> - 17.2-42-2PGDG
- SuSE upstream packages have release numbers like 150200.5.19.1
  which overrides our packages. Increase our release number on SuSE.

* Mon Dec 9 2024 Devrim Gündüz <devrim@gunduz.org> - 17.2-42-1PGDG
- Update to 17.2

* Thu Oct 17 2024 Devrim Gündüz <devrim@gunduz.org> - 17.0-43-1PGDG
- Remove .bki and .sql files to avoid conflict with Fedora packages.

* Tue Sep 24 2024 Devrim Gündüz <devrim@gunduz.org> - 17.0-42-1PGDG
- Update to 17.0

* Thu Sep 19 2024 Devrim Gündüz <devrim@gunduz.org> - 16.4-43-1PGDG
- Add missing BRs

* Wed Aug 7 2024 Devrim Gündüz <devrim@gunduz.org> - 16.4-42-1PGDG
- Update to 16.4

* Mon May 27 2024 Devrim Gündüz <devrim@gunduz.org> - 16.3-42-1PGDG
- Update to 16.3

* Fri Feb 9 2024 Devrim Gündüz <devrim@gunduz.org> - 16.2-43-1PGDG
- Enable debug package

* Thu Feb 8 2024 Devrim Gündüz <devrim@gunduz.org> - 16.2-42-1PGDG
- Update to 16.2

* Tue Nov 7 2023 Devrim Gündüz <devrim@gunduz.org> - 16.1-42-1PGDG
- Update to 16.1

* Thu Sep 14 2023 Devrim Gündüz <devrim@gunduz.org> - 16.0-42-1PGDG
- Update to 16.0

* Wed Aug 9 2023 Devrim Gündüz <devrim@gunduz.org> - 15.4-42.1-1PGDG
- Remove RHEL 6 bits

* Wed Aug 9 2023 Devrim Gündüz <devrim@gunduz.org> - 15.4-42-1PGDG
- Update to 15.4

* Thu May 11 2023 Devrim Gündüz <devrim@gunduz.org> - 15.3-42-1PGDG
- Update to 15.3

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 15.2-42.1PGDG.1
- Modernise %%patch usage, which has been deprecated in Fedora 38

* Thu Feb 9 2023 Devrim Gündüz <devrim@gunduz.org> - 15.2-42-1PGDG
- Update to 15.2

* Tue Dec 6 2022 Devrim Gündüz <devrim@gunduz.org> - 15.1-42.1-1
- Remove Advance Toolchain support from RHEL 7 - ppc64le.

* Sat Nov 12 2022 Devrim Gündüz <devrim@gunduz.org> - 15.1-42-1PGDG
- Update to 15.1

* Fri Oct 21 2022 Devrim Gündüz <devrim@gunduz.org> - 15.0-42.2PGDG
- It's 9.6, not 96 :(

* Fri Oct 21 2022 Devrim Gündüz <devrim@gunduz.org> - 15.0-42.1PGDG
- Keep providing libpq.so.5(RHPG_96)(64bit). Distros still need it.

* Fri Oct 14 2022 Devrim Gündüz <devrim@gunduz.org> - 15.0-42PGDG
- Update to 15.0

* Thu Aug 11 2022 Devrim Gündüz <devrim@gunduz.org> - 14.5-42PGDG
- Update to 14.5

* Fri Jun 24 2022 Devrim Gündüz <devrim@gunduz.org> - 14.4-42PGDG
- Update to 14.4

* Thu Jun 2 2022 Devrim Gündüz <devrim@gunduz.org> - 14.3-42PGDG
- Update to 14.3

* Tue Feb 8 2022 Devrim Gündüz <devrim@gunduz.org> - 14.2-42PGDG
- Update to 14.2

* Wed Jan 5 2022 Devrim Gündüz <devrim@gunduz.org> - 14.1-42PGDG
- Update to 14.1

* Wed Oct 6 2021 Devrim Gündüz <devrim@gunduz.org> - 14.0-42PGDG
- Update to 14.0

* Thu Aug 12 2021 Devrim Gündüz <devrim@gunduz.org> - 13.4-42PGDG
- Update to 13.4

* Thu May 13 2021 Devrim Gündüz <devrim@gunduz.org> - 13.3-10PGDG
- Update to 13.3

* Tue Mar 23 2021 Devrim Gündüz <devrim@gunduz.org> - 13.2-11PGDG
- Add a few dependencies for ppc64le.

* Thu Feb 11 2021 Devrim Gündüz <devrim@gunduz.org> - 13.2-10PGDG
- Update to 13.2

* Mon Nov 16 2020 Devrim Gündüz <devrim@gunduz.org> - 13.1-10PGDG
- Update to 13.1

* Tue Sep 22 2020 Devrim Gündüz <devrim@gunduz.org> - 13.0-10PGDG
- Update to 13.0

* Thu Aug 20 2020 Devrim Gündüz <devrim@gunduz.org> - 12.4-10PGDG
- Update to 12.4

* Tue Jun 2 2020 Devrim Gündüz <devrim@gunduz.org> - 12.3-10PGDG
- Rework on the spec file, using Fedora's spec file.
- Update to 12.3
- Also provide libpq, to override OS package.

* Fri Apr 17 2020 Devrim Gündüz <devrim@gunduz.org> - 12.2-1PGDG
- Initial packaging for PostgreSQL RPM repository
