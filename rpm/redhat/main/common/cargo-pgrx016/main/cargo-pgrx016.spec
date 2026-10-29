# cargo-pgrx is the build tool of the pgrx framework, which PostgreSQL extensions
# written in Rust are built with. It has to be exactly the same version as the
# pgrx crate that the extension uses, so there is one package per pgrx release
# series (cargo-pgrx016 for 0.16.x). This is why the binary is versioned.
%global crate		cargo-pgrx
%global pgrx_series	0.16
%global errnover	0.3.14

Name:		cargo-pgrx016
Version:	0.16.1
Release:	2PGDG%{?dist}
Summary:	Cargo subcommand to build PostgreSQL extensions written in Rust (pgrx 0.16)
# The licenses of the crates that are compiled into the binary, checked with
# "cargo metadata --filter-platform x86_64-unknown-linux-gnu" (291 crates):
License:	MIT AND Apache-2.0 AND Unicode-3.0 AND ISC AND Zlib AND BSD-3-Clause AND 0BSD AND Unlicense AND CC0-1.0 AND MIT-0 AND CDLA-Permissive-2.0 AND bzip2-1.0.6 AND BSL-1.0
URL:		https://github.com/pgcentralfoundation/pgrx
Source0:	https://static.crates.io/crates/%{crate}/%{crate}-%{version}.crate
# The crate has no license file:
Source1:	https://raw.githubusercontent.com/pgcentralfoundation/pgrx/v%{version}/LICENSE#/%{crate}-%{version}-LICENSE
# The dependencies of the crate, for building without network access. Made with
# "./cargo-pgrx016-vendor.sh %%{version}", which also vendors openssl 0.10.80 and
# openssl-sys 0.9.116 (see %%prep), and runs cargo-vendor-filterer for the Linux
# architectures that we build on.
# It has to be made again for every new version.
Source2:	https://download.postgresql.org/pub/repos/yum/rust-sources/%{crate}/%{crate}-%{version}-vendor.tar.xz
# cargo-vendor-filterer replaced the errno crate with an empty stub, as it
# does not know that rustix uses its libc backend (which needs errno) on
# ppc64le. See %%prep:
Source3:	https://static.crates.io/crates/errno/errno-%{errnover}.crate

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

# rustix uses its libc backend on ppc64le, as inline assembly is not stable on
# powerpc64 yet, and the libc backend needs errno. The vendor tarball only has
# an empty stub of it, so replace that with the real crate. The checksum is
# the one in Cargo.lock:
rm -rf vendor/errno
mkdir vendor/errno
tar -xzf %{SOURCE3} -C vendor/errno --strip-components=1
echo '{"files":{},"package":"39cab71617ae0d63f51a36d69f866391735b51691dbda63cf6f96d042b63efeb"}' > vendor/errno/.cargo-checksum.json

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
* Thu Oct 29 2026 Devrim Gündüz <devrim@gunduz.org> - 0.16.1-2PGDG
- Replace the empty errno stub in the vendored crates with the real crate.
  rustix uses its libc backend on ppc64le, which needs errno, and the build
  failed there.

* Fri Sep 25 2026 Devrim Gündüz <devrim@gunduz.org> - 0.16.1-1PGDG
- Initial packaging for the PostgreSQL RPM repository, to build pgvectorscale,
  which is written in Rust with pgrx 0.16.1.
