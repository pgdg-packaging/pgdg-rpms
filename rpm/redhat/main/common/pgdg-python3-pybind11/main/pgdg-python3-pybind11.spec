%pgdg_python3_setup

%global	modname pybind11

Name:		python%{python3_pkgversion}-%{modname}
Version:	2.13.6
Release:	2PGDG%{?dist}
Summary:	Seamless operability between C++11 and Python

License:	BSD-3-Clause
URL:		https://github.com/pybind/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/p/%{modname}/%{modname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

%description
pybind11 is a lightweight header-only library that exposes C++ types in
Python and vice versa, mainly to create Python bindings of existing C++
code.

This package installs pybind11 for Python %{python3_pkgversion}. The
pkg-config file is in the directory printed by
"python%{python3_pkgversion} -m pybind11 --pkgconfigdir".

%prep
%autosetup -n %{modname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
# Remove pybind11-config, it conflicts with the python3-pybind11 package
# of the OS. Use "python%{python3_pkgversion} -m pybind11" instead.
%{__rm} -f %{buildroot}%{_bindir}/%{modname}-config

%files
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/%{modname}-%{version}.dist-info/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 2.13.6-2PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Tue Oct 06 2026 Devrim Gunduz <devrim@gunduz.org> - 2.13.6-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  pg_statviz dependency on Amazon Linux 2023.
