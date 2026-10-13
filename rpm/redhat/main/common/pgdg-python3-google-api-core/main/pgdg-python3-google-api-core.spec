# This module is installed into the private PGDG Python tree
# (%%{pgdg_pysitelib}), not into the system site-packages. bigquery_fdw
# adds that directory to sys.path, so the newer versions it needs do not
# conflict with the (older) copies shipped by the distribution. The
# interpreter is the one multicorn2 embeds. See
# https://github.com/pgdg-packaging/pgdg-rpms/issues/367
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

# SUSE ships its own (older) copies of these modules with exactly the
# same package names, which ours would replace, so use distinct names
# there:
%if 0%{?suse_version}
%global	pgdg_pyname pgdg-python%{python3_pkgversion}
%else
%global	pgdg_pyname python%{python3_pkgversion}
%endif
%global	pgdg_pyprefix %{_prefix}/lib/pgdg-python
%global	pgdg_pysitelib %{pgdg_pyprefix}/python%{pgdg_pyver}/site-packages

# The files are not in the system site-packages, so the brp script would
# byte-compile them with the default python3, which may be a different
# version. Byte-compile them in %%install instead:
%global	_python_bytecompile_extra 0
%global	__brp_python_bytecompile %{nil}

%global	modname google-api-core
%global	pymodname google_api_core

Name:		%{pgdg_pyname}-%{modname}
Version:	2.30.2
Release:	1PGDG%{?dist}
Summary:	Core library for Google client libraries

License:	Apache-2.0
URL:		https://github.com/googleapis/google-cloud-python/tree/main/packages/google-api-core
Source0:	https://files.pythonhosted.org/packages/source/g/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

Requires:	%{pgdg_pyname}-googleapis-common-protos >= 1.75.5
Requires:	%{pgdg_pyname}-protobuf >= 7.36.2
Requires:	%{pgdg_pyname}-proto-plus >= 1.29.0
Requires:	python%{python3_pkgversion}-google-auth
Requires:	python%{python3_pkgversion}-requests

%description
This library is not meant to stand-alone. Instead it defines common
helpers used by all Google API clients.

This package installs the module into the private PGDG Python tree,
%{pgdg_pysitelib}, for bigquery_fdw.

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
* Mon Oct 12 2026 Devrim Gunduz <devrim@gunduz.org> - 2.30.2-1PGDG
- Initial packaging for the PostgreSQL RPM repository, as part of the
  private Python stack of bigquery_fdw. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/367
