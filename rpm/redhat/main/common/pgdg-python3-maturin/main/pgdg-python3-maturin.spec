%if 0%{?fedora} && 0%{?fedora} == 45
%global __ospython %{_bindir}/python3.15
%global python3_pkgversion 3.15
%endif
%if 0%{?fedora} && 0%{?fedora} <= 44
%global __ospython %{_bindir}/python3.14
%global python3_pkgversion 3.14
%endif
%if 0%{?rhel} && 0%{?rhel} <= 10
%global	__ospython %{_bindir}/python3.12
%global	python3_pkgversion 3.12
%endif
%if 0%{?rhel} == 9
%global	__python3 %{_bindir}/python3.12
%endif
%if 0%{?amzn} == 2023
%global	__ospython %{_bindir}/python3.13
%global	__python3 %{_bindir}/python3.13
%global	python3_pkgversion 3.13
%endif
%if 0%{?suse_version} == 1500
%global	__ospython %{_bindir}/python3.11
%global	python3_pkgversion 311
%endif
%if 0%{?suse_version} == 1600
%global	__ospython %{_bindir}/python3.13
%global	python3_pkgversion 313
%endif

%global	modname maturin

Name:		python%{python3_pkgversion}-%{modname}
Version:	1.15.0
Release:	1PGDG%{?dist}
Summary:	Build and publish crates with pyo3, cffi and uniffi bindings as Python packages
# maturin is MIT OR Apache-2.0. The licenses of the crates that are compiled
# into the binary (without the default features, as setup.py builds it),
# checked with "cargo tree -e normal --no-default-features" (201 crates):
License:	(MIT OR Apache-2.0) AND MIT AND Apache-2.0 AND Apache-2.0 WITH LLVM-exception AND 0BSD AND BSD-3-Clause AND bzip2-1.0.6 AND MPL-2.0 AND Unicode-3.0 AND Zlib
URL:		https://github.com/PyO3/%{modname}
Source0:	https://files.pythonhosted.org/packages/source/m/%{modname}/%{modname}-%{version}.tar.gz
# The crates that maturin depends on, for building without network access.
# Made with "./pgdg-python3-maturin-vendor.sh %%{version}", which runs
# cargo-vendor-filterer for the Linux architectures that we build on.
# It has to be made again for every new version.
# The CDN cached a 404 for the plain URL. The query string makes it fetch
# the file again; #/ keeps the local file name unchanged.
Source1:	https://download.postgresql.org/pub/repos/yum/rust-sources/%{modname}/%{modname}-%{version}-vendor.tar.xz?v=2#/%{modname}-%{version}-vendor.tar.xz

BuildRequires:	python%{python3_pkgversion}-devel
BuildRequires:	python%{python3_pkgversion}-pip
BuildRequires:	python%{python3_pkgversion}-setuptools
BuildRequires:	python%{python3_pkgversion}-setuptools-rust
BuildRequires:	python%{python3_pkgversion}-wheel
BuildRequires:	pyproject-rpm-macros
# rust-version in Cargo.toml of this release:
BuildRequires:	rust >= 1.89
BuildRequires:	cargo >= 1.89
BuildRequires:	gcc

%description
maturin builds and publishes crates with pyo3, cffi and uniffi bindings as
well as Rust binaries as Python packages. It is also a PEP 517 build backend.

This package is built without the default features (no upload, no cross
compilation), as needed for building Python extensions written in Rust,
such as pydantic-core and jiter.

%prep
%setup -q -n %{modname}-%{version} -a 1

# Use the vendored crates, and nothing from the network:
mkdir -p .cargo
cat > .cargo/config.toml <<'CARGOEOF'
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
CARGOEOF

# The license metadata uses PEP 639, which needs setuptools >= 77. Use the
# older format, as Amazon Linux 2023 has setuptools 69:
sed -i -e 's|^license = "MIT OR Apache-2.0"$|license = { text = "MIT OR Apache-2.0" }|' \
	-e '/^license-files = \[$/,/^\]$/d' pyproject.toml
grep -q '^license = { text = "MIT OR Apache-2.0" }$' pyproject.toml
if grep -q '^license-files' pyproject.toml; then exit 1; fi

# Older trove-classifiers releases, like the one of Amazon Linux 2023, do not
# know the GraalPy classifier, and setuptools fails the build. Classifiers are
# only PyPI metadata, so remove them all:
sed -i '/^classifiers = \[$/,/^\]$/d' pyproject.toml
if grep -q '^classifiers' pyproject.toml; then exit 1; fi

# setuptools-rust 1.7 of Amazon Linux 2023 has no env argument in RustBin. It
# is only used to install Rust when cargo is not found, which is never the
# case here:
sed -i 's|, cargo_manifest_args=\["--locked"\], env=env)|, cargo_manifest_args=["--locked"])|' setup.py
grep -q 'cargo_manifest_args=\["--locked"\])\]' setup.py

%build
export CARGO_HOME="$PWD/.cargo-home"
# Keep the debug information for the debuginfo package:
export CARGO_PROFILE_RELEASE_DEBUG=2
export CARGO_PROFILE_RELEASE_STRIP=none
%{?build_rustflags:export RUSTFLAGS="%{build_rustflags}"}
export CARGO_NET_OFFLINE=true
%pyproject_wheel

%install
%pyproject_install

%files
%license license-mit license-apache
%doc README.md Changelog.md
%{_bindir}/%{modname}
%{python3_sitearch}/%{modname}/
%{python3_sitearch}/%{modname}-%{version}.dist-info/

%changelog
* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 1.15.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to build pydantic-core
  and jiter (for pg_statviz) on Amazon Linux 2023. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Add RHEL 9 support (python3.12), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Remove the classifiers from pyproject.toml, as the trove-classifiers
  release of Amazon Linux 2023 does not know the GraalPy classifier.
