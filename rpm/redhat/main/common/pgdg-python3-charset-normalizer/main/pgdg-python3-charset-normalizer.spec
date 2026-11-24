%pgdg_python3_setup

%global	modname charset-normalizer
%global	pymodname charset_normalizer

Name:		python%{python3_pkgversion}-%{modname}
Version:	3.5.3
Release:	1PGDG%{?dist}
Summary:	The Real First Universal Charset Detector

License:	MIT
URL:		https://github.com/jawah/charset_normalizer
Source0:	https://files.pythonhosted.org/packages/source/c/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

%if 0%{?suse_version} >= 1500
BuildRequires:	python-rpm-macros
%else
BuildRequires:	pyproject-rpm-macros
%endif
BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel
%if 0%{?rhel} && 0%{?rhel} <= 9
# %%pyproject_install runs with the non-default Python here, and needs its
# packaging module, which pyproject-rpm-macros only pulls in for the OS Python.
BuildRequires:	python%{python3_pkgversion}-packaging
%endif

%description
A library that helps you read text from an unknown charset encoding. This
package is built without the optional Cython extensions.

%prep
%autosetup -n %{pymodname}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
# Remove the command line tool, it conflicts with the
# python3-charset-normalizer package of the OS:
%{__rm} -rf %{buildroot}%{_bindir}

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/%{pymodname}/
%{python3_sitelib}/%{pymodname}-%{version}.dist-info/

%changelog
* Tue Nov 24 2026 Devrim Gündüz <devrim@gunduz.org> - 3.5.3-1PGDG
- Update to 3.5.3 per changes described at:
  https://github.com/jawah/charset_normalizer/blob/master/CHANGELOG.md
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/717
- Remove the unused setuptools_scm BuildRequires.
- BuildRequire pyproject-rpm-macros (python-rpm-macros on SUSE), and
  python3.12-packaging on RHEL 8 and 9: only the builders had them, so
  clean builds failed.

* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 3.4.2-2PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 3.4.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  requests dependency on Amazon Linux 2023. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
