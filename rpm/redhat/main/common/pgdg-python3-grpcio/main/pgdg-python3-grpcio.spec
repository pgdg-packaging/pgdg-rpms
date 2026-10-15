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

%global	modname grpcio
%global	pymodname grpcio

Name:		%{pgdg_pyname}-%{modname}
Version:	1.84.0
Release:	3PGDG%{?dist}
Summary:	HTTP/2-based RPC framework
%if ! 0%{?suse_version}
# This package was called python3.X-<module> before this release, and was
# replaced by EPEL's python3-<module> on RHEL 10:
Obsoletes:	python%{python3_pkgversion}-%{modname} < %{version}-%{release}
%endif

License:	Apache-2.0 AND BSD-3-Clause AND MIT AND MPL-2.0
URL:		https://grpc.io
Source0:	https://files.pythonhosted.org/packages/source/g/%{pymodname}/%{pymodname}-%{version}.tar.gz
Patch0:	grpcio-1.84.0-openssl4.patch

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-wheel
BuildRequires:	gcc gcc-c++ make
%if 0%{?suse_version}
BuildRequires:	libopenssl-3-devel zlib-devel
%else
BuildRequires:	openssl-devel zlib-devel
%endif
# gRPC needs C++17, which the default GCC 7 of SLES 15 does not fully
# support:
%if 0%{?suse_version} == 1500
BuildRequires:	gcc13 gcc13-c++
%endif

Provides:	bundled(abseil-cpp)
Provides:	bundled(c-ares)
Provides:	bundled(re2)
Provides:	bundled(upb)
%if 0%{?suse_version}
Requires:	python%{python3_pkgversion}-typing_extensions
%else
Requires:	python%{pgdg_pyver}dist(typing-extensions)
%endif

%description
gRPC is a modern, open source, high-performance remote procedure call\n(RPC) framework. This package contains the Python bindings.

This package installs the module into the private PGDG Python tree,
%{pgdg_pysitelib}, for bigquery_fdw.

%prep
%autosetup -p1 -n %{pymodname}-%{version}
# PEP 639 license strings need setuptools >= 77, which RHEL 8, Amazon Linux
# 2023 and SLES 15 do not have:
%{__sed} -i 's/^license = "\(.*\)"$/license = { text = "\1" }/' pyproject.toml

%build
# Use the system OpenSSL and zlib; abseil, c-ares, re2 and upb are bundled.
export GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=1
export GRPC_PYTHON_BUILD_SYSTEM_ZLIB=1
# Parallelize the compilation of the extension (it is huge):
export GRPC_PYTHON_BUILD_EXT_COMPILER_JOBS=$(echo "%{?_smp_mflags}" | %{__sed} -n 's/.*-j *\([0-9][0-9]*\).*/\1/p')
export GRPC_PYTHON_BUILD_EXT_COMPILER_JOBS=${GRPC_PYTHON_BUILD_EXT_COMPILER_JOBS:-1}
export CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" LDFLAGS="%{?build_ldflags}"
# Fedora 43 and 44 moved openssl/engine.h, which is deprecated, to
# openssl-devel-engine. Build without the OpenSSL engine support instead, as
# on Fedora 45, whose OpenSSL 4 defines OPENSSL_NO_ENGINE (Patch0 makes the
# include conditional):
%if 0%{?fedora} && 0%{?fedora} <= 44
CFLAGS="$CFLAGS -DOPENSSL_NO_ENGINE" CXXFLAGS="$CXXFLAGS -DOPENSSL_NO_ENGINE"
%endif
%if 0%{?suse_version} == 1500
export CC=gcc-13 CXX=g++-13
%endif
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
* Fri Oct 16 2026 Devrim Gunduz <devrim@gunduz.org> - 1.84.0-3PGDG
- Rename the package to pgdg-python3.X-<module> on all distributions, as
  on SUSE, and obsolete the old python3.X-<module> package. On RHEL 10,
  EPEL's python3-<module> packages obsolete python3.12-<module> < their
  version, so python3-google-api-core 1:2.11.1 replaced ours on updates.
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/367

* Thu Oct 15 2026 Devrim Gunduz <devrim@gunduz.org> - 1.84.0-2PGDG
- Provide pgdg-python3.X-<module> (on SUSE, that is the package name) and
  require the other modules of the private tree by that name. The
  versioned Requires on python3.X-<module> were satisfied by the packages
  of the distribution that have an Epoch (Fedora's and EPEL's
  python3-google-api-core 1:2.27.0), so our google-api-core and proto-plus
  were not installed there. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/367

* Mon Oct 12 2026 Devrim Gunduz <devrim@gunduz.org> - 1.84.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, as part of the
  private Python stack of bigquery_fdw. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/367
- Add a patch from upstream (first in 1.85.0) to build with the OpenSSL 4
  of Fedora 45.
- Build without the deprecated OpenSSL engine support on Fedora 43 and
  44 (OPENSSL_NO_ENGINE), instead of BuildRequiring openssl-devel-engine.
