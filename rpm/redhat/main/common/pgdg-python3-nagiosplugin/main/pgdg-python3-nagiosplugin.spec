%pgdg_python3_setup

%global modname nagiosplugin

%global python3_sitelib %(%{__python3} -Esc "import sysconfig; print(sysconfig.get_path('purelib', vars={'platbase': '/usr', 'base': '%{_prefix}'}))")

Name:		python%{python3_pkgversion}-%{modname}
Version:	1.4.0
Release:	43PGDG%{?dist}
Summary:	Class library for writing Nagios (Icinga) plugins

License:	ZPL-2.1
URL:		https://github.com/mpounsett/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/n/%{modname}/%{modname}-%{version}.tar.gz
BuildArch:	noarch

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
# SUSE's Python dependency generators. python3-devel pulls this in, but
# python%%{python3_pkgversion}-devel does not.
BuildRequires:	python-rpm-packaging
%else
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-%{modname} < %{version}-%{release}
%endif

%description
nagiosplugin is a Python class library which helps writing Nagios (or
Icinga) compatible plugins easily in Python. It cares for much of the
boilerplate code and default logic commonly found in Nagios checks.

%prep
%setup -q -n %{modname}-%{version}
# distutils is not in Python 3.12 and later anymore. convert_path() only
# converts "/" to the path separator of the OS, which is "/" here, too:
sed -i 's/^from distutils.util import convert_path$/convert_path = str/' setup.py
grep -q '^convert_path = str$' setup.py

%build
%pyproject_wheel

%install
%pyproject_install

%files
%doc README.txt HISTORY.txt
%license LICENSE.txt
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}-%{version}.dist-info/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 1.4.0-43PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Mon Oct 26 2026 Devrim Gunduz <devrim@gunduz.org> - 1.4.0-42PGDG
- Initial packaging for the PostgreSQL RPM repository, for
  nagios-plugins-patroni (check_patroni), on RHEL 8, 9 and 10, Amazon
  Linux 2023 and SLES 16, where no package provides it for the Python
  version that we build check_patroni with. On RHEL 10, obsolete the EPEL
  python3-nagiosplugin package. Start the release from 42, so that our
  package wins over EPEL's. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/427
