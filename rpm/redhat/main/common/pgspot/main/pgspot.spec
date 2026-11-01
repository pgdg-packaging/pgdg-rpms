%pgdg_python3_setup

%global sname pgspot
%{!?runselftest:%global runselftest 0}

Name:		pgspot
Version:	0.9.4
Release:	3PGDG%{?dist}
Summary:	Spot vulnerabilities in PostgreSQL extension scripts
License:	PostgreSQL
Url:		https://github.com/timescale/%{sname}
Source0:	https://github.com/timescale/%{sname}/archive/refs/tags/%{version}.tar.gz
BuildArch:	noarch
# Not every distribution generates the requirements from the Python metadata,
# and pgspot needs a PostgreSQL 17 parser, which is pglast 7.x:
Requires:	pglast >= 7.21
Requires:	pglast < 8
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel
%if %runselftest
BuildRequires:	pglast >= 7.21 python%{python3_pkgversion}-pytest
%endif

%description
pgspot checks extension scripts for PostgreSQL security best practices.
In addition to checking extension scripts it can also be used to check
security definer functions or any other PostgreSQL SQL code.

pgspot checks for the following vulnerabilities:
- search_path-based attacks
- unsafe object creation

%prep
%setup -q -n %{sname}-%{version}
# Upstream pins pglast==7.21, which would block the pglast 7.x bug fix
# releases. Those keep the same parser:
sed -i 's/pglast==7.21/pglast>=7.21,<8/' requirements.txt setup.cfg

%build
%pyproject_wheel

%install
%pyproject_install

%check
%if %runselftest
# The tests run the pgspot script, so use the one from the build root
export PATH=%{buildroot}%{_bindir}:$PATH PYTHONPATH=%{buildroot}%{python3_sitelib}
# tests/snapshot_test.py needs pytest-snapshot, which is not packaged; it
# compares the output for each testdata/*.sql with testdata/expected, so do
# that here instead.
for f in testdata/*.sql; do
	pgspot $f | diff -u testdata/expected/$(basename $f .sql).out -
done
%{__python3} -m pytest tests --ignore=tests/snapshot_test.py -p no:cacheprovider
%endif

%files
%defattr(-,root,root,0755)
%doc README.md CHANGELOG.md REFERENCE.md
%license LICENSE
%{_bindir}/%{sname}
%{python3_sitelib}/%{sname}/*.py
%{python3_sitelib}/%{sname}/__pycache__/*.pyc
%{python3_sitelib}/%{sname}/pg_catalog/*.py
%{python3_sitelib}/%{sname}/pg_catalog/__pycache__/*.pyc
%{python3_sitelib}/%{sname}-%{version}.dist-info/

%changelog
* Sat Oct 31 2026 Devrim Gündüz <devrim@gunduz.org> - 0.9.4-3PGDG
- Accept any pglast 7.x >= 7.21 instead of exactly 7.21, in the package
  and in the Python metadata, to be able to use pglast 7.22, which keeps
  the same PostgreSQL 17 parser. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/505

* Wed Oct 28 2026 Devrim Gündüz <devrim@gunduz.org> - 0.9.4-2PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Mon Oct 19 2026 Devrim Gündüz <devrim@gunduz.org> - 0.9.4-1PGDG
- Update to 0.9.4 per changes described at:
  https://github.com/timescale/pgspot/releases/tag/0.9.4
- This version requires pglast 7.21. Require it explicitly, as RHEL and
  SUSE do not generate the requirements from the Python metadata.

* Sun Oct 11 2026 Devrim Gunduz <devrim@gunduz.org> - 0.9.2-3PGDG
- Build the python311 flavor on SLES 15. The SUSE pyproject macros built
  for the default python3 (3.6), so the build failed there. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226
- Set python3_sitelib to the python3.11 one on SLES 15, too: the SUSE macro
  points to the default python3 (3.6).

* Sat Oct 3 2026 Devrim Gündüz <devrim@gunduz.org> - 0.9.2-2PGDG
- Add %%check, running the upstream tests. It is disabled by default;
  enable it with --define 'runselftest 1'.

* Wed Sep 16 2026 Devrim Gunduz <devrim@gunduz.org> - 0.9.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository
