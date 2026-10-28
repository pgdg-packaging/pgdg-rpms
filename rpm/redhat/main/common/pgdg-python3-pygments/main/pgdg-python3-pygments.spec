%pgdg_python3_setup

%global	modname pygments
%global	pymodname pygments

Name:		python%{python3_pkgversion}-%{modname}
Version:	2.21.0
Release:	3PGDG%{?dist}
Summary:	Syntax highlighting engine written in Python

License:	BSD-2-Clause
URL:		https://pygments.org/
Source0:	https://files.pythonhosted.org/packages/source/p/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-hatchling

%description
Pygments is a generic syntax highlighter suitable for use in code hosting,
forums, wikis or other applications that need to prettify source code.

%prep
%autosetup -n %{pymodname}-%{version}
# The PEP 639 license-files list needs hatchling 1.27; RHEL 8 has our
# 1.25 (see python3.12-hatchling). Its default license file patterns pick
# up the same files:
%{__sed} -i -e '/^license-files = /d' -e 's/"hatchling>=1.27"/"hatchling"/' pyproject.toml
if grep -q '^license-files\|hatchling>=1.27' pyproject.toml; then exit 1; fi

%build
%pyproject_wheel

%install
%pyproject_install
%if 0%{?rhel} == 8 || 0%{?rhel} == 9
# The OS python3-pygments ships pygmentize; only the module is needed:
%{__rm} -f %{buildroot}%{_bindir}/pygmentize
%endif

%files
%license LICENSE AUTHORS
%doc README.rst
%if 0%{?rhel} != 8 && 0%{?rhel} != 9
%{_bindir}/pygmentize
%endif
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 2.21.0-3PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 2.21.0-2PGDG
- Add RHEL 9 support, for pgcli.
- RHEL 8 and 9: Do not ship pygmentize, which conflicts with the one
  in the OS python3-pygments package. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Fri Oct 23 2026 Devrim Gunduz <devrim@gunduz.org> - 2.21.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for pgcli on
  RHEL 8 (python3.12), without EPEL. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422
