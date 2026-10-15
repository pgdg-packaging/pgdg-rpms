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

%global	modname proto-plus
%global	pymodname proto_plus

Name:		%{pgdg_pyname}-%{modname}
Version:	1.29.0
Release:	4PGDG%{?dist}
Summary:	Beautiful, Pythonic protocol buffers
%if ! 0%{?suse_version}
# This package was called python3.X-<module> before this release, and was
# replaced by EPEL's python3-<module> on RHEL 10:
Obsoletes:	python%{python3_pkgversion}-%{modname} < %{version}-%{release}
%endif

License:	Apache-2.0
URL:		https://github.com/googleapis/google-cloud-python/tree/main/packages/proto-plus
Source0:	https://files.pythonhosted.org/packages/source/p/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

Requires:	pgdg-python%{python3_pkgversion}-protobuf >= 7.36.2

%description
Beautiful, idiomatic protocol buffers in Python.

This package installs the module into the private PGDG Python tree,
%{pgdg_pysitelib}, for bigquery_fdw.

%prep
%autosetup -n %{pymodname}-%{version}
# The trove-classifiers module of SLES 16 does not know Python 3.15 yet, and
# setuptools rejects pyproject.toml when it is installed:
%{__sed} -i '/"Programming Language :: Python :: 3\.15",/d' pyproject.toml

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
* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 1.29.0-4PGDG
- Rename the package to pgdg-python3.X-<module> on all distributions, as
  on SUSE, and obsolete the old python3.X-<module> package. On RHEL 10,
  EPEL's python3-<module> packages obsolete python3.12-<module> < their
  version, so python3-google-api-core 1:2.11.1 replaced ours on updates.
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/367

* Thu Oct 15 2026 Devrim Gunduz <devrim@gunduz.org> - 1.29.0-3PGDG
- Provide pgdg-python3.X-<module> (on SUSE, that is the package name) and
  require the other modules of the private tree by that name. The
  versioned Requires on python3.X-<module> were satisfied by the packages
  of the distribution that have an Epoch (Fedora's and EPEL's
  python3-google-api-core 1:2.27.0), so our google-api-core and proto-plus
  were not installed there. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/367

* Wed Oct 14 2026 Devrim Gunduz <devrim@gunduz.org> - 1.29.0-2PGDG
- Remove the Python 3.15 classifier from pyproject.toml: setuptools rejects
  it when an older trove-classifiers module is installed, as on SLES 16.
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/367

* Mon Oct 12 2026 Devrim Gunduz <devrim@gunduz.org> - 1.29.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, as part of the
  private Python stack of bigquery_fdw. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/367
