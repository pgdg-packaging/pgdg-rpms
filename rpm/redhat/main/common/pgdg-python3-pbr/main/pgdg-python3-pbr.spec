# Built for the python3.13 alt-stack of Amazon Linux 2023 only, for
# the OpenStack Swift storage backend of rohmu (pghoard).
# python-swiftclient needs it to build.
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif

%global	modname pbr
%global	pymodname pbr

Name:		python%{python3_pkgversion}-%{modname}
Version:	7.1.3
Release:	1PGDG%{?dist}
Summary:	Python Build Reasonableness

License:	Apache-2.0
URL:		https://docs.openstack.org/pbr/latest/
Source0:	https://files.pythonhosted.org/packages/source/p/pbr/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

%description
PBR is a library that injects some useful and sensible default
behaviors into your setuptools run.

%prep
%autosetup -n %{pymodname}-%{version}

%build
export PBR_VERSION=%{version}
%pyproject_wheel

%install
export PBR_VERSION=%{version}
%pyproject_install
%pyproject_save_files -l pbr
%{__rm} -f %{buildroot}%{_bindir}/pbr

%files -f %{pyproject_files}
%doc README.rst

%changelog
* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 7.1.3-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for
  the OpenStack Swift storage backend of rohmu (pghoard) on Amazon Linux 2023.
