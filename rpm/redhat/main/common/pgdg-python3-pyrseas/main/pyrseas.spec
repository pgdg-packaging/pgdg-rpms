%pgdg_python3_setup

%{expand: %%global py3ver %(echo `%{__python3} -c "import sys; sys.stdout.write(sys.version[:3])"`)}
%global python3_sitelib %(%{__python3} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

%global sname pyrseas
%global cname Pyrseas

Summary:	Compare and synchronize PostgreSQL database schemas
Name:		python%{python3_pkgversion}-%{sname}
Version:	0.10.0
Release:	7PGDG%{?dist}
License:	BSD
Source0:	https://github.com/perseas/%{cname}/archive/refs/tags/v%{version}.tar.gz
URL:		https://github.com/perseas/%{cname}/
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel python%{python3_pkgversion}-setuptools

%if 0%{?suse_version}
# SUSE does not generate runtime Requires from the Python metadata by
# default; Fedora and RHEL do:
Requires:	python%{python3_pkgversion}-PyYAML >= 5.3
%if 0%{?suse_version} >= 1600
# There is no psycopg 3 for python311 on SLES 15:
Requires:	python3-psycopg3 >= 3.1
%endif
%endif
%if 0%{?rhel} == 8
# The python3.12 packages of RHEL 8 get no automatic python3.12dist()
# Requires either:
Requires:	python%{python3_pkgversion}dist(psycopg) >= 3.1
Requires:	python%{python3_pkgversion}-PyYAML >= 5.3
%endif
# %%pgdg_python3_setup renamed python3-pyrseas to python%%{python3_pkgversion}-pyrseas:
Provides:	python3-%{sname} = %{version}-%{release}
Obsoletes:	python3-%{sname} < %{version}-%{release}
Obsoletes:	python2-%{sname} <= 0.9.0

%description
Pyrseas provides a framework and utilities to upgrade and maintain a relational
database. Its purpose is to enhance and follow through on the concepts of the
Andromeda Project. This is Python 3 version.

%prep
%setup -q -n %{cname}-%{version}

%build
%{__python3} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python3} setup.py install --root %{buildroot}

%files
%defattr(-,root,root,755)
%doc docs/ README.rst
%{_bindir}/dbaugment
%{_bindir}/dbtoyaml
%{_bindir}/yamltodb
%{python3_sitelib}/%{cname}-%{version}-py%{py3ver}*.egg-info/
%{python3_sitelib}/%{sname}

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 0.10.0-7PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0, and build with its
  Python everywhere, not only on Amazon Linux 2023. The package is now
  python%%{python3_pkgversion}-pyrseas, which provides and obsoletes
  python3-pyrseas. On RHEL 8, require psycopg 3 and PyYAML explicitly,
  and on SLES 15, PyYAML.
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Mon Oct 26 2026 Devrim Gunduz <devrim@gunduz.org> - 0.10.0-6PGDG
- Amazon Linux 2023: Build with python3.13: psycopg 3 and PyYAML are only
  available for it there, so the package could not be installed.
- Get python3_sitelib from sysconfig instead of the removed
  distutils.sysconfig module. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/427

* Mon Oct 26 2026 Devrim Gunduz <devrim@gunduz.org> - 0.10.0-5PGDG
- Remove the dependency on pgdbconn, which Pyrseas does not use since
  0.10.0 (it uses psycopg 3 directly), and which is not in the repo
  anymore, so the package could not be installed. SLES 16: Require psycopg
  3 and PyYAML. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/427

* Thu Sep 10 2026 - Devrim Gündüz <devrim@gunduz.org> 0.10.0-4PGDG
- Add missing BR

* Fri Aug 28 2026 - Devrim Gündüz <devrim@gunduz.org> 0.10.0-3PGDG
- Package the .egg-info directory itself instead of globbing only its
  contents (egg-info/*), so RHEL/Fedora's pythondist.attr generator
  (which is anchored on the .egg-info directory entry) actually fires
  and emits the correct runtime Requires. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226

* Wed Feb 21 2024 - Devrim Gündüz <devrim@gunduz.org> 0.10.0-2-PGDG
- Add PGDG branding

* Tue Nov 8 2022 - Devrim Gündüz <devrim@gunduz.org> 0.10.0-1
- Update to 0.10.0

* Thu Apr 16 2020 - Devrim Gündüz <devrim@gunduz.org> 0.9.1-1
- Update to 0.9.1
- Remove Python2 stuff

* Fri Jul 26 2019 - Devrim Gündüz <devrim@gunduz.org> 0.9.0-1
- Update to 0.9.0
- Add dbpgconn dependency

* Mon Oct 15 2018 Devrim Gündüz <devrim@gunduz.org> - 0.8.0-1.1
- Rebuild against PostgreSQL 11.0

* Thu Aug 23 2018 - Devrim Gündüz <devrim@gunduz.org> 0.8.0-1
- Update to 0.8.0

* Tue Nov 29 2016 - Devrim Gündüz <devrim@gunduz.org> 0.7.3-1
- Initial RPM packaging for PostgreSQL RPM Repository
