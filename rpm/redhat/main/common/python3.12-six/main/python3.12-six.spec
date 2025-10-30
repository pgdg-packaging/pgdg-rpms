%if 0%{?fedora} && 0%{?fedora} == 43
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?fedora} && 0%{?fedora} <= 42
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?suse_version} >= 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif

Name:		python%{python3_pkgversion}-six
Version:	1.17.0
Release:	1PGDG%{?dist}
Summary:	Python 2 and 3 compatibility utilities

License:	MIT
URL:		https://github.com/benjaminp/six
Source0:	https://files.pythonhosted.org/packages/source/s/six/six-%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif

Obsoletes:	python%{python3_pkgversion}-six <= 1.16.0

%description
Six is a Python 2 and 3 compatibility library. It provides utility functions
for smoothing over the differences between the Python versions with the goal
of writing Python code that is compatible on both Python versions.}

%prep
%autosetup -n six-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.rst documentation/index.rst
%{python3_sitelib}/six-*.dist-info/
%pycached %{python3_sitelib}/six.py

%changelog
* Thu Oct 30 2025 Devrim Gunduz <devrim@gunduz.org> - 1.17.0-1PGDG
- Update to 1.17.0. This indirectly fixes a longstanding self-obsolete problem.
  Thanks Lukas Schürmann for the report.
- Switch to pyproject build

* Mon Sep 22 2025 Devrim Gunduz <devrim@gunduz.org> - 1.16.0-1PGDG.1
- Add Fedora 43 support

* Mon May 19 2025 Devrim Gunduz <devrim@gunduz.org> - 1.16.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository to support
  Barman on RHEL 9.
