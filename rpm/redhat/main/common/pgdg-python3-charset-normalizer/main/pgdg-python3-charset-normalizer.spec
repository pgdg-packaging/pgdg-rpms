%pgdg_python3_setup

%global	modname charset-normalizer
%global	pymodname charset_normalizer

Name:		python%{python3_pkgversion}-%{modname}
Version:	3.4.2
Release:	2PGDG%{?dist}
Summary:	The Real First Universal Charset Detector

License:	MIT
URL:		https://github.com/jawah/charset_normalizer
Source0:	https://files.pythonhosted.org/packages/source/c/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel
BuildRequires:	python%{python3_pkgversion}-setuptools_scm

%description
A library that helps you read text from an unknown charset encoding. This
package is built without the optional mypyc compiled module.

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
* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 3.4.2-2PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 3.4.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to satisfy
  requests dependency on Amazon Linux 2023. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
