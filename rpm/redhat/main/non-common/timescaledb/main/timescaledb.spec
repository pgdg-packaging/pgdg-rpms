%global sname	timescaledb

Summary:	A time-series database for high-performance real-time analytics
Name:		%{sname}_%{pgmajorversion}
Version:	2.21.3
Release:	1PGDG%{?dist}
License:	Apache
Source0:	https://github.com/timescale/%{sname}/archive/%{version}.tar.gz
URL:		https://github.com/timescale/%{sname}
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	cmake >= 3.4 openssl-devel

Requires:	postgresql%{pgmajorversion}-server

%description
TimescaleDB is a PostgreSQL extension for high-performance real-time analytics
on time-series and event data.

%prep
%setup -q -n %{sname}-%{version}

# Build only the portions that have Apache Licence, and disable telemetry:
export PATH=%{pginstdir}/bin:$PATH
./bootstrap -DAPACHE_ONLY=1 -DSEND_TELEMETRY_DEFAULT=NO \
	-DPROJECT_INSTALL_METHOD=pgdg -DREGRESS_CHECKS=OFF

%build
export PATH=%{pginstdir}/bin:$PATH
%ifarch ppc64 ppc64le
	CFLAGS="$RPM_OPT_FLAGS -fPIC -pie"
	CXXFLAGS="$RPM_OPT_FLAGS -fPIC -pie"
	export CFLAGS
	export CXXFLAGS
%endif

cd build; %{__make} %{?_smp_mflags}

%install
export PATH=%{pginstdir}/bin:$PATH
cd build; %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install
%{__rm} -f %{buildroot}/%{pginstdir}/lib/pgxs/src/test/perl/*pm

%files
%defattr(-, root, root)
%doc README.md
%license LICENSE-APACHE
%{pginstdir}/lib/%{sname}*.so
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Tue Aug 12 2025 Devrim Gündüz <devrim@gunduz.org> - 2.21.3-1PGDG
- Update to 2.21.3, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.21.3

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

* Tue Jan 28 2025 Devrim Gündüz <devrim@gunduz.org> - 2.18.0-2PGDG
- Remove redundant BR
- Build in parallel

* Thu Jan 23 2025 Devrim Gündüz <devrim@gunduz.org> - 2.18.0-1PGDG
- Update to 2.18.0, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.18.0
- Remove RHEL 7 support

* Wed Nov 6 2024 Devrim Gündüz <devrim@gunduz.org> - 2.17.2-1PGDG
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
- Remove RHEL 6 bits

* Thu Jul 6 2023 Devrim Gündüz <devrim@gunduz.org> - 2.11.1-1PGDG
- Update to 2.11.1, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.11.1
- Add PGDG branding

* Tue May 30 2023 Devrim Gündüz <devrim@gunduz.org> - 2.11.0-1
- Update to 2.11.0, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.11.0

* Mon May 8 2023 Devrim Gündüz <devrim@gunduz.org> - 2.10.3-1
- Update to 2.10.3, per changes described at:
  https://github.com/timescale/timescaledb/releases/tag/2.10.3

* Mon Apr 24 2023 Devrim Gunduz <devrim@gunduz.org> - 2.10.2-1.1
- Modernise %%patch usage, which has been deprecated in Fedora 38

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

* Mon Dec 05 2022 Devrim Gündüz <devrim@gunduz.org> - 2.8.1-2
- Get rid of AT and switch to GCC on RHEL 7 - ppc64le

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

* Mon Apr 18 2022 Devrim Gündüz <devrim@gunduz.org> - 2.6.1-1
- Update to 2.6.1

* Fri Feb 25 2022 Devrim Gündüz <devrim@gunduz.org> - 2.6.0-1
- Update to 2.6.0

* Mon Feb 14 2022 Devrim Gündüz <devrim@gunduz.org> - 2.5.2-1
- Update to 2.5.2

* Mon Nov 1 2021 Devrim Gündüz <devrim@gunduz.org> - 2.5.1-1
- Update to 2.5.1

* Mon Nov 1 2021 Devrim Gündüz <devrim@gunduz.org> - 2.5.0-1
- Update to 2.5.0
- Remove patch0, and export PATH instead.

* Wed Sep 22 2021 Devrim Gündüz <devrim@gunduz.org> - 2.4.2-1
- Update to 2.4.2

* Thu Aug 26 2021 Devrim Gündüz <devrim@gunduz.org> - 2.4.1-1
- Update to 2.4.1

* Wed May 26 2021 Devrim Gündüz <devrim@gunduz.org> - 2.3.0-1
- Update to 2.3.0

* Thu Apr 15 2021 Devrim Gündüz <devrim@gunduz.org> - 2.2.0-1
- Update to 2.2.0

* Wed Apr 7 2021 Devrim Gündüz <devrim@gunduz.org> - 2.1.1-2
- Add missing BR

* Thu Apr 1 2021 Devrim Gündüz <devrim@gunduz.org> - 2.1.1-1
- Update to 2.1.1

* Mon Mar 1 2021 John Harvey <john.harvey@crunchydata.com> - 2.1.0-1
- Update to 2.1.0

* Mon Feb 15 2021 Devrim Gündüz <devrim@gunduz.org> - 2.0.1-1
- Update to 2.0.1
- Use patch1 only on RHEL 7, otherwise it breaks SLES-15 builds.

* Tue Dec 22 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.0-1
- Update to 2.0.0

* Wed Sep 23 2020 Devrim Gündüz <devrim@gunduz.org> - 1.7.4-1
- Update to 1.7.4

* Wed Jul 29 2020 Devrim Gündüz <devrim@gunduz.org> - 1.7.2-1
- Update to 1.7.2

* Mon Apr 27 2020 Devrim Gündüz <devrim@gunduz.org> - 1.7.0-1
- Update to 1.7.0

* Thu Apr 2 2020 Devrim Gündüz <devrim@gunduz.org> - 1.6.1-1
- Update to 1.6.1

* Sat Jan 18 2020 Devrim Gündüz <devrim@gunduz.org> - 1.6.0-1
- Update to 1.6.0

* Sun Nov 24 2019 Devrim Gündüz <devrim@gunduz.org> - 1.5.1-1
- Update to 1.5.1

* Thu Jul 25 2019 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-1
- Update to 1.4.0

* Thu Jun 27 2019 Devrim Gündüz <devrim@gunduz.org> - 1.3.2-1
- Update to 1.3.2
- Add -DPROJECT_INSTALL_METHOD=pgdg to help upstream get better
  data when users enable telemetry.

* Tue Jun 11 2019 Devrim Gündüz <devrim@gunduz.org> - 1.3.1-1
- Update to 1.3.1
- Disable telemetry by default.
- Remove my patch that disabled telemetry.

* Tue Jun 4 2019 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-2
- Add a patch to disable telemetry by default.

* Mon May 6 2019 Devrim Gündüz <devrim@gunduz.org> - 1.3.0-1
- Update to 1.3.0
- Build only the portions that have Apache Licence.

* Tue Feb 5 2019 Devrim Gündüz <devrim@gunduz.org> - 1.1.1-2
- Add dependency to PostgreSQL server package.

* Fri Dec 21 2018 Devrim Gündüz <devrim@gunduz.org> - 1.1.1-1
- Update to 1.1.1

* Thu Dec 6 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0.1-1
- Update to 1.0.1

* Mon Nov 5 2018 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1
- Update to 1.0.0

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.12.1-1.1
- Rebuild against PostgreSQL 11.0

* Thu Sep 20 2018 Devrim Gündüz <devrim@gunduz.org> 0.12.1-1
- Update to 0.12.1, per #3662

* Wed Aug 15 2018 Devrim Gündüz <devrim@gunduz.org> 0.11.0-1
- Update to 0.11.0, per #3555.

* Sat Aug 11 2018 Devrim Gündüz <devrim@gunduz.org> 0.10.1-2
- Ignore .bc files on PPC arch.

* Fri Jul 13 2018 Devrim Gündüz <devrim@gunduz.org> 0.10.1-1
- Update to 0.10.1, per #3497.

* Mon May 14 2018 Devrim Gündüz <devrim@gunduz.org> 0.9.2-1
- Update to 0.9.2, per #3345

* Tue Mar 27 2018 Devrim Gündüz <devrim@gunduz.org> 0.9.1-1
- Update to 0.9.1, per #3231

* Wed Mar 7 2018 Devrim Gündüz <devrim@gunduz.org> 0.9.0-1
- Update to 0.9.0, per #3178

* Mon Feb 12 2018 Devrim Gündüz <devrim@gunduz.org> 0.8.0-2
- Rebuild against PostgreSQL 10.2, per
  https://github.com/timescale/timescaledb/issues/422

* Tue Feb 6 2018 Devrim Gündüz <devrim@gunduz.org> 0.8.0-1
- Initial packaging for PostgreSQL RPM Repository
