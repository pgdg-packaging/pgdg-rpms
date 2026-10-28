%pgdg_python3_setup

# Built for the python3.13 alt-stack of Amazon Linux 2023 only, for
# the Google Cloud storage backend of rohmu (pghoard).

%global	modname oauth2client
%global	pymodname oauth2client

Name:		python%{python3_pkgversion}-%{modname}
Version:	4.1.3
Release:	2PGDG%{?dist}
Summary:	OAuth 2.0 client library

License:	Apache-2.0
URL:		https://github.com/googleapis/oauth2client
Source0:	https://files.pythonhosted.org/packages/source/o/oauth2client/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

%description
oauth2client is a client library for OAuth 2.0. It is deprecated
upstream, but rohmu still uses it.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l oauth2client

%files -f %{pyproject_files}
%doc README.md

%changelog
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 4.1.3-2PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 4.1.3-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for
  the Google Cloud storage backend of rohmu (pghoard) on Amazon Linux 2023.
