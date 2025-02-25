%global sname pg_filedump
%global sversion REL_12_0

Summary:	PostgreSQL File Dump Utility
Name:		%{sname}_%{pgmajorversion}
Version:	12.0
Release:	6PGDG%{?dist}
URL:		https://github.com/df7cb/%{sname}
Source0:	https://github.com/df7cb/pg_filedump/archive/%{sversion}.tar.gz
License:	GPLv2+
BuildRequires:	postgresql%{pgmajorversion}-devel
# lz4 dependency
%if 0%{?suse_version} >= 1500
BuildRequires:	liblz4-devel
Requires:	liblz4-1
%endif
%if 0%{?rhel} || 0%{?fedora}
BuildRequires:	lz4-devel
Requires:	lz4-libs
%endif

Obsoletes:	%{sname}%{pgmajorversion} < 12.0-2

%description
Display formatted contents of a PostgreSQL heap/index/control file.

%prep
%setup -q -n %{sname}-%{sversion}

%build
export CFLAGS="$RPM_OPT_FLAGS"

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__mkdir} -p %{buildroot}%{pginstdir}/bin
%{__install} -m 755 pg_filedump %{buildroot}%{pginstdir}/bin

%files
%defattr(-,root,root)
%{pginstdir}/bin/pg_filedump
%doc README.pg_filedump

%changelog
* Tue Feb 25 2025 Devrim Gündüz <devrim@gunduz.org> - 12.0-6PGDG
- Add missing BRs and remove redundant BR

* Fri Feb 23 2024 Devrim Gündüz <devrim@gunduz.org> - 12.0-5PGDG
- Add PGDG branding

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 12.0-4
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

* Mon Jun 7 2021 Devrim Gündüz <devrim@gunduz.org> 12.0-3
- Remove pgxs patch, and export PATH instead.

* Tue Oct 27 2020 Devrim Gündüz <devrim@gunduz.org> 12.0-2
- Use underscore before PostgreSQL version number for consistency, per:
  https://www.postgresql.org/message-id/CAD%2BGXYMfbMnq3c-eYBRULC3nZ-W69uQ1ww8_0RQtJzoZZzp6ug%40mail.gmail.com

* Fri Nov 29 2019 Devrim Gündüz <devrim@gunduz.org> - 12.0-1
- Initial packaging for PostgreSQL RPM Repository
