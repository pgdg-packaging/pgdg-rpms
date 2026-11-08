%pgdg_python3_setup

%global modname daemonize

Name:		python%{python3_pkgversion}-%{modname}
Version:	2.5.0
Release:	45PGDG%{?dist}
Summary:	Library for writing system daemons in Python

License:	MIT
URL:		https://github.com/thesharp/%{modname}
Source0:	%{url}/archive/v%{version}/%{modname}-%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif

%description
daemonize is a library for writing system daemons in Python.

%prep
%autosetup -n %{modname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{modname}-%{version}.dist-info/
%{python3_sitelib}/%{modname}.py
%{python3_sitelib}/__pycache__/%{modname}.*

%changelog
* Sun Nov 8 2026 Devrim Gunduz <devrim@gunduz.org> - 2.5.0-45PGDG
- Switch to pyproject builds, and use the python3_sitelib of
  %%pgdg_python3_setup: the distutils module that the spec used is not
  available in Python 3.12, so python3.12-daemonize could not be built on
  RHEL 8, for pg_chameleon. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/513

* Wed Oct 28 2026 Devrim Gündüz <devrim@gunduz.org> - 2.5.0-44PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Tue Aug 25 2026 Devrim Gündüz <devrim@gunduz.org> - 2.5.0-43
- Build against the python3.13 alt-stack on Amazon Linux 2023, to keep
  the Python stack consistent across all packages in the repo.

* Sat Mar 28 2026 Devrim Gündüz <devrim@gunduz.org> - 2.5.0-42
- Add to SLES

* Thu Dec 10 2020 Devrim Gündüz <devrim@gunduz.org> - 2.5.0-8
- Initial packaging to satisfy pg_chameleon dependency on
  RHEL 7 and 8.
