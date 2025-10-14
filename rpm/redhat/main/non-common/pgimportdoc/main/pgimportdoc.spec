%global sname	pgimportdoc

Summary:	command line tool for import XML, TEXT and BYTEA documents to PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	0.1.4
Release:	4PGDG%{?dist}
License:	BSD
Source0:	https://github.com/okbob/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/okbob/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel postgresql%{pgmajorversion}
# All supported distros have libselinux-devel package:
BuildRequires:	libselinux-devel >= 2.0.93
# SLES: SLES 15 does not have selinux-policy packageç
# RHEL/Fedora has selinux-policy:
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	selinux-policy >= 3.9.13
%endif
# lz4 dependency
%if 0%{?suse_version} >= 1500
BuildRequires:	liblz4-devel
Requires:	liblz4-1
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	lz4-devel
Requires:	lz4-libs
%endif
# zstd dependency
%if 0%{?suse_version} >= 1500
BuildRequires:	libzstd-devel >= 1.4.0
Requires:	libzstd1 >= 1.4.0
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	libzstd-devel >= 1.4.0
Requires:	libzstd >= 1.4.0
%endif

%if 0%{?suse_version} == 1500
Requires:	libopenssl1_1
BuildRequires:	libopenssl-1_1-devel
%endif
%if 0%{?suse_version} == 1600
Requires:	libopenssl3
BuildRequires:	libopenssl-3-devel
%endif
%if 0%{?fedora} >= 41 || 0%{?rhel} >= 8
Requires:	openssl-libs >= 1.1.1k
BuildRequires:	openssl-devel
%endif


BuildRequires:	libxml2-devel libxslt-devel pam-devel
BuildRequires:	krb5-devel readline-devel zlib-devel
Requires:	postgresql%{pgmajorversion}

Obsoletes:	%{sname}%{pgmajorversion} < 0.1.3-2

%description
pgimportdoc is command line tool for user friendly import XML, TEXT, and
BYTEA documents to PostgreSQL.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{_bindir}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{pginstdir}/bin/%{sname}

%changelog
* Tue Oct 7 2025 Devrim Gündüz <devrim@gunduz.org> - 0.1.4-4PGDG
- Add SLES 16 support

* Tue Feb 25 2025 - Devrim Gündüz <devrim@gunduz.org> 0.1.4-3PGDG
- Add missing BRs

* Fri Feb 23 2024 - Devrim Gündüz <devrim@gunduz.org> 0.1.4-2PGDG
- Add PGDG branding

* Mon Apr 24 2023 - Devrim Gündüz <devrim@gunduz.org> 0.1.4-1
- Update to 0.1.4

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 0.1.3-4
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Fri Jun 4 2021 Devrim Gündüz <devrim@gunduz.org> 0.1.3-3
- Remove pgxs patches, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 0.1.3-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Thu Sep 26 2019 Devrim Gündüz <devrim@gunduz.org> - 0.1.3-1.2
- Rebuild for PostgreSQL 12

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.1.3-1.1
- Rebuild against PostgreSQL 11.0

* Thu Aug 23 2018 - Devrim Gündüz <devrim@gunduz.org> 0.1.3-1
- Update to 0.1.3

* Tue Feb 21 2017 - Devrim Gündüz <devrim@gunduz.org> 0.1.2-1
- Update to 0.1.2

* Tue Feb 21 2017 - Pavel Stehule <pavel.stehule@gmail.com> 0.1.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
