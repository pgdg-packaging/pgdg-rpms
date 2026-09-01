%global sname PyMySQL
%global pname pymysql

%if 0%{?suse_version} == 1500
%global	__python3 %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

%global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")

Name:		python%{python3_pkgversion}-%{sname}
Version:	1.2.0
Release:	1PGDG%{?dist}
Summary:	Pure-Python MySQL client library

License:	MIT
URL:		https://github.com/%{sname}/%{sname}
Source0:	https://github.com/%{sname}/%{sname}/archive/refs/tags/v%{version}.tar.gz
Patch0:		%{sname}-pyproject-license.patch

Provides:	python3-%{sname}

BuildArch:	noarch
# python%%{python3_pkgversion}-devel is what pulls python3-rpm-generators
# into the buildroot on RHEL/Fedora; pyproject builds alone do not.
# Without it, neither python(abi) nor python%%{python3_pkgversion}dist(...)
# get generated. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/228
%if !0%{?suse_version}
BuildRequires:	python%{python3_pkgversion}-devel
%endif

%description
This package contains a pure-Python MySQL client library. The goal of PyMySQL is
to be a drop-in replacement for MySQLdb and work on CPython, PyPy, IronPython
and Jython.

%prep
%autosetup -n %{sname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%doc README.md
%license LICENSE
%{python3_sitelib}/%{sname}-%{version}.dist-info/
%{python3_sitelib}/%{pname}/*.py
%{python3_sitelib}/%{pname}/constants/*.py
%{python3_sitelib}/%{pname}/__pycache__/*pyc
%{python3_sitelib}/%{pname}/constants/__pycache__/*.py*

%changelog
* Mon Aug 31 2026 Devrim Gunduz <devrim@gunduz.org> - 1.2.0-1PGDG
- Update to 1.2.0 per changes described at:
  https://github.com/PyMySQL/PyMySQL/releases/tag/v1.2.0

* Fri Aug 28 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1.2-43PGDG
- Package the .dist-info directory itself instead of globbing only its
  contents (dist-info/*), so RHEL/Fedora's pythondist.attr generator
  (which is anchored on the .dist-info directory entry) actually fires
  and emits the correct runtime Requires. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/226
- Add back python%{python3_pkgversion}-devel as a BuildRequires on the
  non-SLES branch, needed to pull python3-rpm-generators into the
  buildroot for this pyproject build. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/228

* Sat Mar 28 2026 Devrim Gunduz <devrim@gunduz.org> - 1.1.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support
  pg_chameleon on SLES-15
