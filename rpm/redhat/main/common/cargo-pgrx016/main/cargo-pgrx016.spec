# cargo-pgrx is the build tool of the pgrx framework, which PostgreSQL extensions
# written in Rust are built with. It has to be exactly the same version as the
# pgrx crate that the extension uses, so there is one package per pgrx release
# series (cargo-pgrx016 for 0.16.x). This is why the binary is versioned.
%global crate		cargo-pgrx
%global pgrx_series	0.16

Name:		cargo-pgrx016
Version:	0.16.1
Release:	1PGDG%{?dist}
Summary:	Cargo subcommand to build PostgreSQL extensions written in Rust (pgrx 0.16)
# The licenses of the crates that are compiled into the binary, checked with
# "cargo metadata --filter-platform x86_64-unknown-linux-gnu" (291 crates):
License:	MIT AND Apache-2.0 AND Unicode-3.0 AND ISC AND Zlib AND BSD-3-Clause AND 0BSD AND Unlicense AND CC0-1.0 AND MIT-0 AND CDLA-Permissive-2.0 AND bzip2-1.0.6 AND BSL-1.0
URL:		https://github.com/pgcentralfoundation/pgrx
Source0:	https://static.crates.io/crates/%{crate}/%{crate}-%{version}.crate
# The crate has no license file:
Source1:	https://raw.githubusercontent.com/pgcentralfoundation/pgrx/v%{version}/LICENSE#/%{crate}-%{version}-LICENSE
# The dependencies of the crate, for building without network access. Made with:
#   tar xf cargo-pgrx-%%{version}.crate && cd cargo-pgrx-%%{version}
#   cargo vendor --locked -s ../openssl-new/Cargo.toml vendor
# where ../openssl-new is an empty crate (with a Cargo.lock) that depends on
# openssl = "=0.10.80" and openssl-sys = "=0.9.116", see %%prep.
#   tar --sort=name --mtime=@0 --owner=0 --group=0 --numeric-owner -cf - vendor | xz -T0 -6 > ../cargo-pgrx-%%{version}-vendor.tar.xz
# It has to be made again for every new version.
Source2:	https://download.postgresql.org/pub/repos/yum/rust-sources/%{crate}-%{version}-vendor.tar.xz

# The newest crates in Cargo.lock of this release need Rust 1.85:
BuildRequires:	rust >= 1.85
BuildRequires:	cargo >= 1.85
# Native code of the crates (ring, zstd-sys, bzip2-sys) and openssl-sys:
BuildRequires:	gcc make pkgconfig(openssl)

%description
cargo-pgrx is the cargo subcommand of pgrx, a framework for developing
PostgreSQL extensions in Rust. It creates, builds, tests and packages the
extensions.

This package is the 0.16 series, for building extensions that use pgrx 0.16.x.
It is installed as cargo-pgrx-%{pgrx_series}, and is run as:

  cargo-pgrx-%{pgrx_series} pgrx <command> ...

It is only needed to build such extensions, not to run them.

%prep
%setup -q -n %{crate}-%{version} -a 2
cp -p %{SOURCE1} LICENSE

# Use the vendored crates, and nothing from the network:
mkdir -p .cargo
cat > .cargo/config.toml <<'CARGOEOF'
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
CARGOEOF

# openssl-sys 0.9.109 in Cargo.lock of this release does not build with OpenSSL
# 4 (Fedora 45). Use the versions that cargo-pgrx 0.19.1 uses, which are in the
# vendor tarball too:
CARGO_HOME="$PWD/.cargo-home" cargo update --offline -p openssl --precise 0.10.80

%build
export CARGO_HOME="$PWD/.cargo-home"
# Keep the debug information for the debuginfo package:
export CARGO_PROFILE_RELEASE_DEBUG=2
export CARGO_PROFILE_RELEASE_STRIP=none
%{?build_rustflags:export RUSTFLAGS="%{build_rustflags}"}
cargo build --release --frozen

%install
install -Dpm 0755 target/release/%{crate} %{buildroot}%{_bindir}/%{crate}-%{pgrx_series}

%check
# cargo-pgrx is run by cargo as "cargo-pgrx pgrx ...", so it expects "pgrx" first:
./target/release/%{crate} pgrx --version

%files
%license LICENSE
%doc README.md
%{_bindir}/%{crate}-%{pgrx_series}

%changelog
* Fri Sep 25 2026 Devrim Gündüz <devrim@gunduz.org> - 0.16.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to build pgvectorscale,
  which is written in Rust with pgrx 0.16.1.
