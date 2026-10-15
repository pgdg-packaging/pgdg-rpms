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

%global	modname googleapis-common-protos
%global	pymodname googleapis_common_protos

Name:		%{pgdg_pyname}-%{modname}
Version:	1.75.5
Release:	3PGDG%{?dist}
Summary:	Common protobufs used in Google APIs
%if ! 0%{?suse_version}
# This package was called python3.X-<module> before this release, and was
# replaced by EPEL's python3-<module> on RHEL 10:
Obsoletes:	python%{python3_pkgversion}-%{modname} < %{version}-%{release}
%endif

License:	Apache-2.0
URL:		https://github.com/googleapis/google-cloud-python/tree/main/packages/googleapis-common-protos
Source0:	https://files.pythonhosted.org/packages/source/g/%{pymodname}/%{pymodname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel

Requires:	pgdg-python%{python3_pkgversion}-protobuf >= 7.36.2

%description
Classes generated from the common protos in the googleapis repository.

This package installs the module into the private PGDG Python tree,
%{pgdg_pysitelib}, for bigquery_fdw.

%prep
%autosetup -n %{pymodname}-%{version}
# PEP 639 license strings need setuptools >= 77, which RHEL 8, Amazon Linux
# 2023 and SLES 15 do not have:
%{__sed} -i 's/^license = "\(.*\)"$/license = { text = "\1" }/' pyproject.toml

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
* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 1.75.5-3PGDG
- Rename the package to pgdg-python3.X-<module> on all distributions, as
  on SUSE, and obsolete the old python3.X-<module> package. On RHEL 10,
  EPEL's python3-<module> packages obsolete python3.12-<module> < their
  version, so python3-google-api-core 1:2.11.1 replaced ours on updates.
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/367

* Thu Oct 15 2026 Devrim Gunduz <devrim@gunduz.org> - 1.75.5-2PGDG
- Provide pgdg-python3.X-<module> (on SUSE, that is the package name) and
  require the other modules of the private tree by that name. The
  versioned Requires on python3.X-<module> were satisfied by the packages
  of the distribution that have an Epoch (Fedora's and EPEL's
  python3-google-api-core 1:2.27.0), so our google-api-core and proto-plus
  were not installed there. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/367

* Mon Oct 12 2026 Devrim Gunduz <devrim@gunduz.org> - 1.75.5-1PGDG
- Initial packaging for the PostgreSQL RPM repository, as part of the
  private Python stack of bigquery_fdw. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/367
