%pgdg_python3_setup

%global	modname maturin
%global	errnover 0.3.14

Name:		python%{python3_pkgversion}-%{modname}
Version:	1.16.0
Release:	42PGDG%{?dist}
Summary:	Build and publish crates with pyo3, cffi and uniffi bindings as Python packages
# maturin is MIT OR Apache-2.0. The licenses of the crates that are compiled
# into the binary (without the default features, as setup.py builds it),
# checked with "cargo tree -e normal --no-default-features" (195 crates):
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
# cargo-vendor-filterer replaced the errno crate with an empty stub, as it
# does not know that rustix uses its libc backend (which needs errno) on
# ppc64le. See %%prep:
Source2:	https://static.crates.io/crates/errno/errno-%{errnover}.crate

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

%if 0%{?rhel} == 10
# Replace the EPEL package of the same module, which has the same files:
Obsoletes:	maturin < %{version}-%{release}
%endif

%description
maturin builds and publishes crates with pyo3, cffi and uniffi bindings as
well as Rust binaries as Python packages. It is also a PEP 517 build backend.

This package is built without the default features (no upload, no cross
compilation), as needed for building Python extensions written in Rust,
such as pydantic-core and jiter.

%if 0%{?rhel} == 10
%package -n %{name}+patchelf
Summary:	Metapackage for %{name}: patchelf extras
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	/usr/bin/patchelf
# Replace the EPEL metapackage, which requires EPEL's own maturin version, so
# it made dnf upgrade fail:
Provides:	maturin+patchelf = %{version}-%{release}
Obsoletes:	maturin+patchelf < %{version}-%{release}

%description -n %{name}+patchelf
This is a metapackage bringing in patchelf, which maturin uses to set the
rpath of the libraries it builds.

%files -n %{name}+patchelf
%endif

%prep
%setup -q -n %{modname}-%{version} -a 1

# rustix uses its libc backend on ppc64le, as inline assembly is not stable on
# powerpc64 yet, and the libc backend needs errno. The vendor tarball only has
# an empty stub of it, so replace that with the real crate. The checksum is
# the one in Cargo.lock:
rm -rf vendor/errno
mkdir vendor/errno
tar -xzf %{SOURCE2} -C vendor/errno --strip-components=1
echo '{"files":{},"package":"39cab71617ae0d63f51a36d69f866391735b51691dbda63cf6f96d042b63efeb"}' > vendor/errno/.cargo-checksum.json

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
* Fri Oct 30 2026 Devrim Gunduz <devrim@gunduz.org> - 1.16.0-42PGDG
- Update to 1.16.0, per changes described at:
  https://github.com/PyO3/maturin/releases/tag/v1.16.0
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/486
- Update the vendored crates tarball for the new version.

* Wed Oct 28 2026 Devrim Gunduz <devrim@gunduz.org> - 1.15.0-45PGDG
- Use %%pgdg_python3_setup from pgdg-srpm-macros 2.5.0 instead of the
  per-distro Python block and the __ospython macro. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/462

* Mon Oct 26 2026 Devrim Gunduz <devrim@gunduz.org> - 1.15.0-44PGDG
- RHEL 10: Add the +patchelf metapackage, which replaces EPEL's
  maturin+patchelf. That requires EPEL's own maturin version, so it made
  dnf upgrade fail. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Mon Oct 26 2026 Devrim Gunduz <devrim@gunduz.org> - 1.15.0-43PGDG
- Replace the empty errno stub in the vendored crates with the real crate.
  rustix uses its libc backend on ppc64le, which needs errno, and the build
  failed there.

* Sat Oct 24 2026 Devrim Gunduz <devrim@gunduz.org> - 1.15.0-42PGDG
- Add RHEL 10 support, without EPEL, and obsolete the EPEL maturin package
  there. Start the release from 42, so that our packages win over EPEL's.
  Per https://github.com/pgdg-packaging/pgdg-rpms/issues/422

* Wed Oct 07 2026 Devrim Gunduz <devrim@gunduz.org> - 1.15.0-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to build pydantic-core
  and jiter (for pg_statviz) on Amazon Linux 2023. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Add RHEL 9 support (python3.12), for pg_statviz. Per
  https://github.com/pgdg-packaging/pgdg-rpms/issues/249
- Remove the classifiers from pyproject.toml, as the trove-classifiers
  release of Amazon Linux 2023 does not know the GraalPy classifier.
