# This module is installed into the private PGDG Python tree
# (%%{pgdg_pysitelib}), not into the system site-packages, as it
# needs the google-api-core of that tree. It is only built on Amazon Linux
# 2023, for the Google Cloud storage backend of rohmu (pghoard), which adds
# that directory to sys.path.
%if 0%{?fedora} && 0%{?fedora} == 45
%global	__python3 %{_bindir}/python3.15
%global	python3_pkgversion 3.15
%global	pgdg_pyver 3.15
%endif
%if 0%{?fedora} && 0%{?fedora} <= 44
%global	__python3 %{_bindir}/python3.14
%global	python3_pkgversion 3.14
%global	pgdg_pyver 3.14
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__python3 %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%global	pgdg_pyver 3.12
%endif
%if 0%{?amzn} == 2023
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%global	pgdg_pyver 3.13
%endif
%if 0%{?suse_version} == 1500
%global	__python3 %{_bindir}/python3.11
%global	python3_pkgversion 311
%global	pgdg_pyver 3.11
%endif
%if 0%{?suse_version} == 1600
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 313
%global	pgdg_pyver 3.13
%endif

# Use names that the distributions do not use: SUSE ships its own (older)
# copies of these modules as python3XX-<module>, and on RHEL 10, where
# Python 3.12 is the default, EPEL's python3-<module> packages obsolete
# python3.12-<module> < their version (python3-google-api-core with an
# Epoch), which replaced ours on updates:
%global	pgdg_pyname pgdg-python%{python3_pkgversion}
%global	pgdg_pyprefix %{_prefix}/lib/pgdg-python
%global	pgdg_pysitelib %{pgdg_pyprefix}/python%{pgdg_pyver}/site-packages

# The files are not in the system site-packages, so the brp script would
# byte-compile them with the default python3, which may be a different
# version. Byte-compile them in %%install instead:
%global	_python_bytecompile_extra 0
%global	__brp_python_bytecompile %{nil}

%global	modname google-api-python-client
%global	pymodname google_api_python_client

Name:		%{pgdg_pyname}-%{modname}
Version:	2.201.0
Release:	1PGDG%{?dist}
Summary:	Google API Client Library for Python

License:	Apache-2.0
URL:		https://github.com/googleapis/google-api-python-client
Source0:	https://files.pythonhosted.org/packages/source/g/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

Requires:	pgdg-python%{python3_pkgversion}-google-api-core >= 2.30.2
Requires:	python%{python3_pkgversion}-google-auth
Requires:	python%{pgdg_pyver}dist(google-auth-httplib2)
Requires:	python%{pgdg_pyver}dist(httplib2)
Requires:	python%{pgdg_pyver}dist(uritemplate)

%description
The Google API Client Library for Python, for Google's discovery based
APIs.

This package installs the module into the private PGDG Python tree,
%{pgdg_pysitelib}, for the Google Cloud storage backend of rohmu (pghoard).

%prep
%autosetup -n %{pymodname}-%{version}

%build
%{__python3} -m pip wheel --no-deps --no-build-isolation --no-index \
	--disable-pip-version-check -w pgdg-dist .

%install
%{__python3} -m pip install --no-deps --no-index --no-compile \
	--disable-pip-version-check --ignore-installed \
	--target %{buildroot}%{pgdg_pysitelib} pgdg-dist/*.whl
%{__rm} -rf %{buildroot}%{pgdg_pysitelib}/bin
%{__python3} -m compileall -q -f -j0 -s %{buildroot} -p / \
	%{buildroot}%{pgdg_pysitelib}

%files
%license LICENSE
%dir %{pgdg_pyprefix}
%dir %{pgdg_pyprefix}/python%{pgdg_pyver}
%{pgdg_pysitelib}/

%changelog
* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 2.201.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, for the Google Cloud
  storage backend of rohmu (pghoard) on Amazon Linux 2023. It is installed
  into the private PGDG Python tree, which has the google-api-core it
  needs.
