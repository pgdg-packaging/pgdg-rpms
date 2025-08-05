%global sname	timescaledb

Summary:	PostgreSQL based time-series database
Name:		%{sname}-tsl_%{pgmajorversion}
Version:	2.21.2
Release:	1PGDG%{?dist}
License:	Timescale
Source0:	https://github.com/timescale/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/timescale/timescaledb
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	openssl-devel
BuildRequires:	cmake >= 3.4
Requires:	postgresql%{pgmajorversion}-server

Conflicts:	%{sname}_%{pgmajorversion}

%description
TimescaleDB is a PostgreSQL extension for high-performance real-time analytics
on time-series and event data.

%package devel
Summary:	Development portions of timescaledb-tsl
Requires:	%{name}%{?_isa} = %{version}-%{release}
BuildRequires:	perl-Test-Harness

%description devel
This packages includes development portions of timescaledb-tsl.

%prep
%setup -q -n %{sname}-%{version}

# Disable telemetry, so that we can distribute it via PGDG repos:
export PATH=%{pginstdir}/bin:$PATH
./bootstrap -DSEND_TELEMETRY_DEFAULT=NO \
	-DREGRESS_CHECKS=OFF

%build
export PATH=%{pginstdir}/bin:$PATH
CFLAGS="$RPM_OPT_FLAGS -fPIC -pie"
CXXFLAGS="$RPM_OPT_FLAGS -fPIC -pie"
export CFLAGS
export CXXFLAGS

cd build; %{__make} %{?_smp_mflags}

%install
export PATH=%{pginstdir}/bin:$PATH
cd build; %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%files
%defattr(-, root, root)
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{sname}*.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%files devel
%{pginstdir}/lib/pgxs/src/test/perl/TimescaleNode.pm

%changelog
* Tue Aug 5 2025 Devrim Gündüz <devrim@gunduz.org> - 2.21.2-1PGDG
- Update to 2.21.2, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.21.2

* Wed Jul 23 2025 Devrim Gündüz <devrim@gunduz.org> - 2.21.1-1PGDG
- Update to 2.21.1, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.21.1

* Thu Jul 10 2025 Devrim Gündüz <devrim@gunduz.org> - 2.21.0-1PGDG
- Update to 2.21.0, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.21.0

* Wed Jun 11 2025 Devrim Gündüz <devrim@gunduz.org> - 2.20.3-1PGDG
- Update to 2.20.3, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.20.3

* Mon Jun 2 2025 Devrim Gündüz <devrim@gunduz.org> - 2.20.2-1PGDG
- Update to 2.20.2, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.20.2

* Wed May 28 2025 Devrim Gündüz <devrim@gunduz.org> - 2.20.1-1PGDG
- Update to 2.20.1, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.20.1

* Sun May 18 2025 Devrim Gündüz <devrim@gunduz.org> - 2.20.0-1PGDG
- Update to 2.20.0, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.20.0

* Wed Apr 16 2025 Devrim Gündüz <devrim@gunduz.org> - 2.19.3-1PGDG
- Update to 2.19.3, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.19.3

* Tue Apr 8 2025 Devrim Gündüz <devrim@gunduz.org> - 2.19.2-1PGDG
- Update to 2.19.2, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.19.2

* Tue Apr 1 2025 Devrim Gündüz <devrim@gunduz.org> - 2.19.1-1PGDG
- Update to 2.19.1, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.19.1

* Wed Mar 19 2025 Devrim Gündüz <devrim@gunduz.org> - 2.19.0-1PGDG
- Update to 2.19.0, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.19.0

* Wed Feb 19 2025 Devrim Gündüz <devrim@gunduz.org> - 2.18.2-1PGDG
- Update to 2.18.2, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.18.2

* Tue Feb 11 2025 Devrim Gündüz <devrim@gunduz.org> - 2.18.1-1PGDG
- Update to 2.18.1, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.18.1

* Fri Feb 7 2025 Devrim Gündüz <devrim@gunduz.org> - 2.18.0-2PGDG
- Remove RHEL 7 support
- Update package description and remove redundant BR

* Fri Feb 7 2025 Devrim Gündüz <devrim@gunduz.org> - 2.18.0-1PGDG
- Update to 2.18.0, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.18.0

* Sat Nov 9 2024 Devrim Gündüz <devrim@gunduz.org> - 2.17.2-1PGDG
- Update to 2.17.2, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.17.2

* Thu Oct 24 2024 Devrim Gündüz <devrim@gunduz.org> - 2.17.1-1PGDG
- Update to 2.17.1, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.17.1

* Tue Oct 8 2024 Devrim Gündüz <devrim@gunduz.org> - 2.17.0-1PGDG
- Update to 2.17.0, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.17.0

* Thu Aug 8 2024 Devrim Gündüz <devrim@gunduz.org> - 2.16.1-1PGDG
- Update to 2.16.1, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.16.1

* Fri Aug 2 2024 Devrim Gündüz <devrim@gunduz.org> - 2.16.0-1PGDG
- Update to 2.16.0, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.16.0

* Fri Jul 5 2024 Devrim Gündüz <devrim@gunduz.org> - 2.15.3-1PGDG
- Update to 2.15.3, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.15.3

* Wed Jun 12 2024 Devrim Gündüz <devrim@gunduz.org> - 2.15.2-1PGDG
- Update to 2.15.2, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.15.2
  https://github.com/timescale/timescaledb/releases/tag/2.15.1

* Wed May 8 2024 Devrim Gündüz <devrim@gunduz.org> - 2.15.0-1PGDG
- Update to 2.15.0, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.15.0

* Wed Feb 21 2024 Devrim Gündüz <devrim@gunduz.org> - 2.14.2-1PGDG
- Update to 2.14.2, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.14.2

* Mon Feb 12 2024 Devrim Gündüz <devrim@gunduz.org> - 2.14.0-1PGDG
- Update to 2.14.0, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.14.0

* Wed Jan 10 2024 Devrim Gündüz <devrim@gunduz.org> - 2.13.1-1PGDG
- Update to 2.13.1, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.13.1

* Tue Jan 2 2024 Devrim Gündüz <devrim@gunduz.org> - 2.13.0-2PGDG
- Add missing BR for -devel subpackage.

* Wed Nov 29 2023 Devrim Gündüz <devrim@gunduz.org> - 2.13.0-1PGDG
- Update to 2.13.0, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.13.0

* Fri Oct 20 2023 Devrim Gündüz <devrim@gunduz.org> - 2.12.2-1PGDG
- Update to 2.12.2, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.12.2

* Wed Oct 4 2023 Devrim Gündüz <devrim@gunduz.org> - 2.12.0-1PGDG
- Update to 2.12.0, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.12.0

* Mon Aug 21 2023 Devrim Gündüz <devrim@gunduz.org> - 2.11.2-1PGDG
- Update to 2.11.2, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.11.2

* Thu Jul 6 2023 Devrim Gündüz <devrim@gunduz.org> - 2.11.1-1PGDG
- Update to 2.11.1, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.11.1
- Add PGDG branding

* Tue May 30 2023 Devrim Gündüz <devrim@gunduz.org> - 2.11.0-1
- Update to 2.11.0, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.11.0
- Remove RHEL 7 AT specific portions.

* Mon May 8 2023 Devrim Gündüz <devrim@gunduz.org> - 2.10.3-1
- Update to 2.10.3, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.10.3

* Fri Apr 21 2023 Devrim Gündüz <devrim@gunduz.org> - 2.10.2-1
- Update to 2.10.2, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.10.2

* Mon Feb 27 2023 Devrim Gündüz <devrim@gunduz.org> - 2.10.0-1
- Update to 2.10.0, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.10.0

* Wed Feb 15 2023 Devrim Gündüz <devrim@gunduz.org> - 2.9.3-1
- Update to 2.9.3, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.9.3

* Mon Jan 30 2023 Devrim Gündüz <devrim@gunduz.org> - 2.9.2-1
- Update to 2.9.2, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.9.2

* Wed Jan 4 2023 Devrim Gündüz <devrim@gunduz.org> - 2.9.1-1
- Update to 2.9.1, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.9.1

* Mon Oct 10 2022 Devrim Gündüz <devrim@gunduz.org> - 2.8.1-1
- Update to 2.8.1, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.8.1

* Thu Sep 8 2022 Devrim Gündüz <devrim@gunduz.org> - 2.8.0-1
- Update to 2.8.0, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.8.0

* Wed Jul 27 2022 Devrim Gündüz <devrim@gunduz.org> - 2.7.2-1
- Update to 2.7.2, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.7.2

* Mon May 30 2022 Devrim Gündüz <devrim@gunduz.org> - 2.7.0-1
- Update to 2.7.0
- Add -devel subpackage

* Mon Apr 18 2022 Devrim Gündüz <devrim@gunduz.org> - 2.6.1-1
- Update to 2.6.1

* Fri Feb 25 2022 Devrim Gündüz <devrim@gunduz.org> - 2.6.0-1
- Update to 2.6.0

* Mon Feb 14 2022 Devrim Gündüz <devrim@gunduz.org> - 2.5.2-1
- Update to 2.5.2

* Thu Dec 16 2021 Devrim Gündüz <devrim@gunduz.org> - 2.5.1-1
- Update to 2.5.1

* Mon Nov 1 2021 Devrim Gündüz <devrim@gunduz.org> - 2.5.0-1
- Update to 2.5.0
- Remove patch0, and export PATH instead.

* Wed Sep 22 2021 Devrim Gündüz <devrim@gunduz.org> - 2.4.2-1
- Update to 2.4.2

* Thu Aug 26 2021 Devrim Gündüz <devrim@gunduz.org> - 2.4.1-1
- Update to 2.4.1

* Wed May 26 2021 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-1
- Initial packaging of TimescaleDB with Timescale license.
