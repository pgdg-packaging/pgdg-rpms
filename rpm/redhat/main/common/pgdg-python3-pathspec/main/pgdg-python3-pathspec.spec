%pgdg_python3_setup

%global	modname pathspec
%global	pymodname pathspec

Name:		python%{python3_pkgversion}-%{modname}
Version:	0.12.1
Release:	2PGDG%{?dist}
Summary:	Utility library for gitignore style pattern matching of file paths

License:	MPL-2.0
URL:		https://github.com/cpburnz/python-pathspec
Source0:	https://files.pythonhosted.org/packages/source/p/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-flit-core

%description
pathspec is a utility library for pattern matching of file paths, using
gitignore style patterns. It is a dependency of hatchling.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 0.12.1-2PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 0.12.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to build the AI SDKs
  of pg_statviz on RHEL 9 (python3.12). Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
