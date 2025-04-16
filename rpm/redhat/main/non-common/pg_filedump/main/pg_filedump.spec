%global sname pg_filedump

%global pg_fdmajorver 17
%global pg_fdminorver 3

%global sversion REL_%{pg_fdmajorver}_%{pg_fdminorver}

Summary:	PostgreSQL File Dump Utility
Name:		%{sname}_%{pgmajorversion}
Version:	%{pg_fdmajorver}.%{pg_fdminorver}
Release:	1PGDG%{?dist}
URL:		https://github.com/df7cb/%{sname}
Source0:	https://github.com/df7cb/%{sname}/archive/%{sversion}.tar.gz
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

Obsoletes:	%{sname}17 <= 17.1 %{sname}16 <= 17.1 %{sname}15 <= 17.1
Obsoletes:	%{sname}14 <= 17.1 %{sname}13 <= 17.1

%description
Display formatted contents of a PostgreSQL heap/index/control file.

%prep
%setup -q -n %{sname}-%{sversion}

%build
export CFLAGS="$RPM_OPT_FLAGS"

USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__mkdir} -p %{buildroot}%{pginstdir}/bin
%{__install} -m 755 pg_filedump %{buildroot}%{pginstdir}/bin

%files
%defattr(-,root,root)
%{pginstdir}/bin/pg_filedump
%doc README.pg_filedump.md

%changelog
* Wed Apr 16 2025 Devrim Gündüz <devrim@gunduz.org> - 17.3-1PGDG
- Update to 17.3 per changes described at:
  https://github.com/df7cb/pg_filedump/releases/tag/REL_17_3

* Tue Apr 15 2025 Devrim Gündüz <devrim@gunduz.org> - 17.2-1PGDG
- Update to 17.2 per changes described at:
  https://github.com/df7cb/pg_filedump/releases/tag/REL_17_2

* Tue Feb 25 2025 Devrim Gündüz <devrim@gunduz.org> - 17.1-2PGDG
- Add missing BRs and remove redundant BR

* Sat Nov 9 2024 Devrim Gündüz <devrim@gunduz.org> - 17.1-1PGDG
- Update to 17.1 per changes described at:
  https://github.com/df7cb/pg_filedump/releases/tag/REL_17_1

* Sat Sep 21 2024 Devrim Gündüz <devrim@gunduz.org> - 17.0-1PGDG
- Initial packaging for the PostgreSQL RPM Repository
