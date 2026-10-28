%pgdg_python3_setup

%global	modname cppy

Name:		python%{python3_pkgversion}-%{modname}
Version:	1.3.1
Release:	43PGDG%{?dist}
Summary:	C++ headers for C extension development

License:	BSD-3-Clause
URL:		https://github.com/nucleic/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/c/%{modname}/%{modname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
%if ! 0%{?suse_version}
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-setuptools_scm
BuildRequires:	python%{python3_pkgversion}-wheel

Requires:	python%{python3_pkgversion}-setuptools

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	python3-cppy < %{version}-%{release}
%endif

%description
A small C++ header library which makes it easier to write Python extension
modules. The primary feature is a PyObject smart pointer which automatically
handles reference counting and provides convenience methods for performing
common object operations.

%prep
%autosetup -n %{modname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}-%{version}.dist-info/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 1.3.1-43PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 1.3.1-42PGDG
- Add RHEL 10 support, without EPEL, and obsolete the EPEL python3-cppy
  package there. Start the release from 42, so that our packages win over
  EPEL's. Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Tue Oct 06 2026 Devrim Gunduz <devrim@gunduz.org> - 1.3.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  pg_statviz dependency on Amazon Linux 2023.
- Add RHEL 9 support (python3.12), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
