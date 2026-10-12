%if 0%{?fedora} && 0%{?fedora} == 45
%global __ospython %{_bindir}/python3.15
%global python3_pkgversion 3.15
%endif
%if 0%{?fedora} && 0%{?fedora} <= 44
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?suse_version} == 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
# Build the python311 flavor with the SUSE pyproject macros, instead of
# the default python3 (3.6):
%global	pythons python311
%endif
%if 0%{?suse_version} == 1600
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

%{expand: %%global pyver %(echo `%{__ospython} -c "import sys; sys.stdout.write(sys.version[:4])"`)}
%global python3_sitelib %(%{__ospython} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

Summary:	MySQL to PostgreSQL replica system
Name:		pg_chameleon
Version:	2.0.21
Release:	14PGDG%{?dist}
License:	BSD
Source0:	https://github.com/the4thdoctor/%{name}/archive/v%{version}.tar.gz
URL:		https://github.com/the4thdoctor/%{name}
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel
# python%%{python3_pkgversion}-devel is what pulls python3-rpm-generators
# into the buildroot on RHEL/Fedora; pyproject builds alone do not.
# Without it, neither python(abi) nor python%%{python3_pkgversion}dist(...)
# get generated. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/228
%if !0%{?suse_version}
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	pyproject-rpm-macros
%endif


# On RHEL/Fedora/AL2023 the runtime Requires are generated from the
# dist-info metadata as python%%{python3_pkgversion}dist(...).
%if 0%{?suse_version} >= 1500
Requires:	python3-PyYAML python%{python3_pkgversion}-parsy
Requires:	python%{python3_pkgversion}-daemonize python%{python3_pkgversion}-tabulate
Requires:	python%{python3_pkgversion}-psycopg2 python%{python3_pkgversion}-rollbar
Requires:	python%{python3_pkgversion}-PyMySQL python%{python3_pkgversion}-mysql-replication >= 0.31

%endif

%description
pg_chameleon is a MySQL to PostgreSQL replica system written in Python 3.
The system use the library mysql-replication to pull the row images from
MySQL which are stored into PostgreSQL as JSONB. A pl/pgsql function decodes
the jsonb values and replays the changes against the PostgreSQL database.

%prep
%setup -q -n %{name}-%{version}
# No RPM provides psycopg2-binary; the packaged psycopg2 is the same module.
# Sphinx is only needed to build the docs, not at runtime:
%{__sed} -i -e "s/'psycopg2-binary>=/'psycopg2>=/" \
	-e "/'Sphinx>=/d" setup.py
# pkg_resources is deprecated and only available with setuptools; use
# importlib.metadata from the standard library instead:
%{__sed} -i -e 's/^from pkg_resources import get_distribution$/from importlib.metadata import version/' \
	-e "s/^__version__ = get_distribution('pg_chameleon')$/__version__ = 'pg_chameleon ' + version('pg_chameleon')/" \
	scripts/chameleon.py
%{__sed} -i -e 's/^from pkg_resources import get_distribution$/from importlib.metadata import version/' \
	-e "s/str(get_distribution('PyYAML')).split(' ')\[1\]/version('PyYAML')/" \
	pg_chameleon/lib/global_lib.py
# distutils was removed in Python 3.12; get_python_lib is imported but
# never used:
%{__sed} -i '/^from distutils.sysconfig import get_python_lib$/d' \
	pg_chameleon/lib/global_lib.py pg_chameleon/lib/pg_lib.py

%build
%pyproject_wheel

%install
%pyproject_install

%files
%defattr(-,root,root,755)
%doc docs/ README.rst
%license LICENSE.txt
%{_bindir}/chameleon
%{_bindir}/chameleon.py
%{python3_sitelib}/%{name}-%{version}.dist-info/
%{python3_sitelib}/%{name}/*.py
%{python3_sitelib}/%{name}/__pycache__/*.pyc
%{python3_sitelib}/%{name}/configuration/config-example.yml
%{python3_sitelib}/%{name}/lib/*.py
%{python3_sitelib}/%{name}/lib/__pycache__/*.pyc
%{python3_sitelib}/%{name}/sql/*.sql
%{python3_sitelib}/%{name}/sql/upgrade/*.sql

%changelog
* Mon Oct 12 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0.21-14PGDG
- Remove the hand-written python3-* Requires on RHEL and Fedora. On RHEL 9
  they pointed to the system python3 (3.9) packages, and they could not
  be satisfied by the renamed python3.12-* packages. The generated
  python3.12dist() Requires already cover all dependencies.
- Add missing pyproject-rpm-macros BuildRequires.
- Use importlib.metadata instead of pkg_resources, which is only
  available with setuptools, so chameleon failed to start.
- Remove the unused distutils import, which made chameleon fail to start
  on Python >= 3.12.

* Mon Oct 12 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0.21-13PGDG
- Replace psycopg2-binary with psycopg2 and remove Sphinx in setup.py's
  install_requires, so that the generated python3dist() Requires can be
  satisfied.

* Sun Oct 11 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0.21-12PGDG
- Build the python311 flavor on SLES 15. The SUSE pyproject macros built
  for the default python3 (3.6), so the build failed there. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226
- Fix the Fedora 44 interpreter pin: the Fedora 45 change made it cover
  only Fedora <= 43, so the spec did not parse on Fedora 44.
- Migrate %%python3_sitelib off the removed distutils.sysconfig module to
  sysconfig.get_path().

* Sun Sep 20 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0.21-11PGDG
- Add Fedora 45 support

* Fri Sep 11 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0.21-10PGDG
- Remove Fedora <= 42 support

* Thu Sep 10 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0.21-9PGDG
- Add missing BR

* Fri Aug 28 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0.21-8PGDG
- Package the .dist-info directory itself instead of globbing only its
  contents (dist-info/*), so RHEL/Fedora's pythondist.attr generator
  (which is anchored on the .dist-info directory entry) actually fires
  and emits the correct runtime Requires. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226
- Add back python%{python3_pkgversion}-devel as a BuildRequires on the
  non-SLES branch, needed to pull python3-rpm-generators into the
  buildroot for this pyproject build. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/228

* Tue Aug 25 2026 Devrim Gunduz <devrim@gunduz.org> - 2.0.21-7PGDG
- Also set __python3 (not just __ospython) for Amazon Linux 2023, so
  %pyproject_wheel/%pyproject_install actually build against python3.13
  instead of silently falling back to the system default python3.
  This one already had its own local sitelib override, so the
  mismatch was active (not just cosmetic): pip would install via 3.9
  while %files looked for files under python3.13's site-packages.

* Tue Aug 25 2026 Devrim Gündüz <devrim@gunduz.org> - 2.0.21-6PGDG
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Thu May 7 2026 Devrim Gündüz <devrim@gunduz.org> - 2.0.21-5PGDG
- Add missing BRs

* Tue Apr 28 2026 Devrim Gündüz <devrim@gunduz.org> - 2.0.21-4PGDG
- Switch to pyproject build.
- Use Python 3.14 on Fedora 44.

* Sat Mar 28 2026 Devrim Gündüz <devrim@gunduz.org> - 2.0.21-3PGDG
- Fix SLES dependencies

* Mon Mar 23 2026 Devrim Gündüz <devrim@gunduz.org> - 2.0.21-2PGDG
- Add SLES 16 and Fedora 44 support

* Wed Jan 22 2025 Devrim Gündüz <devrim@gunduz.org> - 2.0.21-1PGDG
- Update to 2.0.21 per changes described at
  https://github.com/the4thdoctor/pg_chameleon/releases/tag/v2.0.21

* Wed Jan 1 2025 Devrim Gündüz <devrim@gunduz.org> - 2.0.20-1PGDG
- Update to 2.0.20 per changes described at
  https://github.com/the4thdoctor/pg_chameleon/releases/tag/v2.0.20

* Mon Feb 19 2024  Devrim Gündüz <devrim@gunduz.org> - 2.0.19-2PGDG
- Add PGDG branding

* Thu Mar 30 2023  Devrim Gündüz <devrim@gunduz.org> - 2.0.19-1
- Update to 2.0.19

* Wed Apr 20 2022  Devrim Gündüz <devrim@gunduz.org> - 2.0.18-1
- Update to 2.0.18

* Mon Feb 7 2022 Devrim Gündüz <devrim@gunduz.org> - 2.0.17-1
- Update to 2.0.17
- Add Python 3.10 support to the spec file.

* Mon Jan 3 2022 Devrim Gündüz <devrim@gunduz.org> - 2.0.16-4
- Fix SLES dependency, per https://redmine.postgresql.org/issues/7094

* Mon Nov 1 2021 Devrim Gündüz <devrim@gunduz.org> - 2.0.16-3
- Looks like we don't need python3-sphinx dependency.

* Thu Dec 10 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.16-2
- Fix RHEL 7 dependency

* Wed Dec 9 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.16-1
- Update to 2.0.16

* Wed Sep 23 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.15-1
- Update to 2.0.15

* Tue Aug 18 2020 Devrim Gündüz <devrim@gunduz.org> - 2.0.14-1
- Initial RPM packaging for PostgreSQL RPM Repository
